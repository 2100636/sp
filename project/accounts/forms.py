# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.translation import ugettext, ugettext_lazy as _
from captcha.fields import CaptchaField
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.core.models import Purchase, Catalog, CatalogProductProperties, Product
from django.forms import ModelForm, Form
from project.core.functions import *


class OrganizerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizerProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs = {'placeholder':'Ваше Имя', 'class':'form-control'}
        self.fields['lastName'].widget.attrs = {'placeholder':'Ваша Фамилия', 'class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder':'Ваш e-mail', 'class':'form-control'}
        self.fields['phone'].widget.attrs = {'placeholder':'Ваш телефон', 'class':'form-control'}
        self.fields['address'].widget.attrs = {'placeholder':'Ваш адрес', 'class':'form-control'}
        self.fields['city'].widget.attrs = {'placeholder':'Ваш город', 'class':'form-control'}
        self.fields['zipCode'].widget.attrs = {'placeholder':'Почтовый индекс', 'class':'form-control'}
        self.fields['icon'].widget.attrs = {'class':'btn btn-block btn-default btn-sm'}

    class Meta:
        model = OrganizerProfile
        # widgets = {'user': forms.HiddenInput()}
        exclude = ('user',)

    def save(self, user):
        obj = super(OrganizerProfileForm, self).save(commit=False)
        obj.user = user
        return obj.save()

class UserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=100,
        regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': "Это значение может состоять из латинских букв, цифр и знаков @/./+/-/_."},
        widget=forms.TextInput(attrs={'placeholder': 'Ваше Имя', 'class': 'form-control'}),
    )
    email = forms.EmailField(
        label=_("Email"),
        error_messages = {'invalid': "Введите корректный e-mail адрес"},
        widget=forms.TextInput(attrs={'placeholder': 'Ваш e-mail', 'class': 'form-control'}),
    )
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.ModelForm):
    error_messages = {
        'wrong': ("Имя пользователя или пароль введены неверно"),
    }
    username = forms.RegexField(label=_("Username"), max_length=100,
        regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': "Это значение может состоять из латинских букв, цифр и знаков @/./+/-/_."},
        widget=forms.TextInput(attrs={'placeholder': 'Ваше Имя', 'class': 'form-control'}),
    )
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ("username",)

    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return username
    #     raise forms.ValidationError(self.error_messages['duplicate_username'])

    # def auth_user(self):
    #     username = self.cleaned_data["username"]
    #     password = self.cleaned_data["password"]
    #     try:
    #         User.objects.get(username=username)
    #         user = auth.authenticate(username=username, password=password)
    #         return user
    #     except User.DoesNotExist:
    #         return forms.ValidationError(self.error_messages['wrong'])


class purchaseForm(ModelForm):
    class Meta:
        model = Purchase
        exclude = ('organizerProfile',)

    def save(self, user):
        obj = super(purchaseForm, self).save(commit=False)
        obj.organizerProfile = getOrganizerProfile(user)
        obj.save()
        # assert isinstance(obj, object) #pycharm сам влепил
        return obj


class catalogForm(ModelForm):
    class Meta:
        model = Catalog
        exclude = ('catalog_purchase',)
    def save(self, purchase_id):
        # TODO: сделать валидацию на существование закупки (purchase_id)
        obj = super(catalogForm, self).save(commit=False)
        obj.catalog_purchase = Purchase.objects.get(id=purchase_id)
        obj.save()
        return obj


class catalogProductPropertiesForm(ModelForm):
    class Meta:
        model = CatalogProductProperties
        fields = ["cpp_name", "cpp_values"]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('catalog',)
    def save(self, catalog_id):
        # TODO: сделать валидацию на существование каталога (catalog_id)
        obj = super(ProductForm, self).save(commit=False)
        obj.catalog = Catalog.objects.get(id=catalog_id)
        obj.save()
        return obj



def propertyForm(catalog_id):

    cpp_obj = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
    list = []
    for cpp_object in cpp_obj:
        values = cpp_object.cpp_values.split(";")
        local_dict = {}
        for value in values:
            local_dict.update({value: cpp_object.cpp_name})
        list.append(local_dict)

    #return list
    class DynamicPropertyForm(forms.Form):

        def __init__(self, *args, **kwargs):
            super(DynamicPropertyForm, self).__init__(*args, **kwargs)

            for dict_item in list:
                list_choices = []
                for key, value in dict_item.items():
                    list_choices.append([key, key])
                    name = value
                slug = translit(name).lower()
                self.fields['%s' % slug] = forms.ChoiceField(widget=forms.RadioSelect, label=name, choices=list_choices)

    return DynamicPropertyForm()




# class testFrom(forms.Form):
    # flieds, sdfdf, sdfd  = [forms.CharField(),forms.CharField(),forms.CharField()]
    #
    # flied = forms.CharField()
    # sdfdf = forms.CharField()
    # sdfd = forms.CharField()
    #
    # choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)













