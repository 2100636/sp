# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns('project.core.views',

    url(r'^viewproduct/$', 'viewProduct',
		{'template_name':'core/viewproduct.html'},
		name='viewproduct'),



    # Главная страница
    url(r'^$', 'index_view',
		{'template_name':'core/index.html'},
		name='catalog_home'),
    url(r'^purchase-(\d+)/$', 'corePurchase',
		{'template_name': 'core/core_purchase.html'},
		name='corePurchase'),
    url(r'^purchase-(?P<purchase_id>\d+)/catalog-(?P<catalog_id>\d+)/$', 'coreCatalog',
		{'template_name': 'core/core_catalog.html'},
		name='coreCatalog'),



    # Страницы сайта
    # url(r'^(?P<slug>[-\w]+)/$', 'page_view',
    #     {'template_name':'main/page.html'},
    #     name='page_view'),
)
