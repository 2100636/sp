# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from project.cart.cart import add_to_cart, get_cart_items, remove_from_cart, update_cart
from project.cart.admin import CartItemResource, CartItem
from project.cart.forms import ExportForm
from project.cart.purchases import get_purchases_dict
from project.core.views import check_profile
from project.accounts.models import getProfile
from project.core.models import Catalog
from import_export import resources
from excel_response import ExcelResponse
import datetime

@check_profile
def cartView(request, template_name):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata.has_key('remove'):
            remove_from_cart(request)
        if postdata.has_key('update'):
            update_cart(request)
    cart_items = get_cart_items(request)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@check_profile
def purchasesCartView(request, template_name):  # TODO: настроить экспорт по закупкам
    purchases_dict = get_purchases_dict(request)  # получаем словарь словарей ... описание в purchases.py
    form = ExportForm(request.POST or None)
    data = []
    if form.is_valid():
        postdata = request.POST.copy()
        if 'export' in postdata:
            # получаем каталог из словаря purchases_dict
            for dict_tmp in purchases_dict.values():
                for catalog, cart_items in dict_tmp.items():
                    if catalog.id == int(postdata['catalog']):
                        data = [[u'Название товара', u'Свойство товара', u'Колличество', u'Фамилия', u'Имя',
                                 u'Телефон', u'e-mail', u'Адрес', u'Дата бронирования']]
                        for item in cart_items:
                            profile = getProfile(item.user)
                            date = str(item.date_added)
                            data.append([item.product.product_name, item.properties, item.quantity, profile.lastName,
                                         profile.firstName, profile.phone, profile.email, profile.address,
                                         date])
            return ExcelResponse(data, 'catalog')
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))