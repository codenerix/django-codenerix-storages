# -*- coding: utf-8 -*-
#
# django-codenerix-storages
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail
from codenerix.widgets import DynamicInput, DynamicSelect

from codenerix_products.models import ProductFinal, ProductUnique
from codenerix_storages.models_stockcontrol import Inventory, InventoryLine
from codenerix_storages.forms_stockcontrol import InventoryForm, InventoryLineForm


# Inventory
class GenInventoryUrl(object):
    ws_entry_point = '{}/inventory'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryList(GenInventoryUrl, GenList):
    model = Inventory
    extra_context = {
        'menu': ['storage', 'storage'],
        'bread': [_('Inventory'), _('Inventory')],
    }
    gentrans = {
        'getreport': _("Get report"),
        'doinventory': _("Do inventory"),
    }

    def dispatch(self, *args, **kwargs):
        self.client_context = {
            'url_doinventory': reverse('CDNX_storages_inventoryline_work', kwargs={"ipk": "__IPK__"}),
            'url_getreport': reverse('CDNX_storages_inventoryline_list', kwargs={"ipk": "__IPK__"}),
        }
        return super(InventoryList, self).dispatch(*args, **kwargs)


class InventoryCreate(GenInventoryUrl, GenCreate):
    model = Inventory
    form_class = InventoryForm


class InventoryCreateModal(GenCreateModal, InventoryCreate):
    pass


class InventoryUpdate(GenInventoryUrl, GenUpdate):
    model = Inventory
    form_class = InventoryForm


class InventoryUpdateModal(GenUpdateModal, InventoryUpdate):
    pass


class InventoryDelete(GenInventoryUrl, GenDelete):
    model = Inventory


class InventoryDetail(GenInventoryUrl, GenDetail):
    model = Inventory
    groups = InventoryForm.__groups_details__()


# InventoryLine
class GenInventoryLineUrl(object):
    ws_entry_point = '{}/inventoryline'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryLineList(GenInventoryLineUrl, GenList):
    model = InventoryLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryLine'), _('InventoryLine')]}
    defaultordering = "-created"

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryline_list', kwargs={"ipk": self.ipk})[1:]
        return super(InventoryLineList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=self.ipk)
        return limit


class InventoryLineWork(GenInventoryLineUrl, GenList):
    model = InventoryLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryLine'), _('InventoryLine')]}
    defaultordering = "-created"
    static_partial_header = 'codenerix_storages/inventory_work_header.html'
    static_app_row = 'codenerix_storages/inventory_work_app.js'
    static_controllers_row = 'codenerix_storages/inventory_work_controllers.js'

    def __fields__(self, info):
        fields = []
        fields.append(('box', _("Box")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        fields.append(('caducity', _("Caducity")))
        return fields

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryline_work', kwargs={"ipk": self.ipk})[1:]
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]

        # Prepare form
        fields = []
        fields.append((DynamicSelect, 'box', 3, 'CDNX_storages_storageboxs_foreign', []))
        fields.append((DynamicInput, 'product_final', 3, 'CDNX_products_productfinalsean13_foreign', []))
        fields.append((DynamicInput, 'product_unique', 3,  'CDNX_products_productuniquescode_foreign', ['product_final']))
        form = InventoryLineForm()
        for (widget, key, minchars, url, autofill) in fields:
            wattrs = form.fields[key].widget.attrs
            form.fields[key].widget = widget(wattrs)
            form.fields[key].widget.form_name = form.form_name
            form.fields[key].widget.field_name = key
            form.fields[key].widget.autofill_deepness = minchars
            form.fields[key].widget.autofill_url = url
            form.fields[key].widget.autofill = autofill

        # Prepare context
        self.client_context = {
            'ipk': self.ipk,
            'final_focus': True,
            'unique_focus': False,
            'unique_disabled': True,
            'caducity_focus': True,
            'caducity_disabled': True,
            'form_zone': form.fields['box'].widget.render('box', None, {}),
            'form_quantity': form.fields['quantity'].widget.render('quantity', None, {'ng-init': 'quantity=1.0'}),
            'form_product': form.fields['product_final'].widget.render('product_final', None, {
                'codenerix-on-enter': 'product_changed(product_final, this, "{}")'.format(self.ws_ean13_fullinfo),
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error}',
                'autofocus': '',
            })+" <span class='fa fa-warning text-danger' ng-show='final_error' title='{}'></span>".format(_("Product not found!")),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed(product_unique, this, "{}")'.format(self.ws_unique_fullinfo),
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
            }),
            'form_caducity': form.fields['caducity'].widget.render('caducity', None, {
                'codenerix-focus': 'data.meta.context.caducity_focus',
                'ng-disabled': 'data.meta.context.caducity_disabled',
            }),
        }
        return super(InventoryLineWork, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=self.ipk)
        return limit


class InventoryLineCreate(GenInventoryLineUrl, GenCreate):
    model = InventoryLine
    form_class = InventoryLineForm


class InventoryLineCreateModal(GenCreateModal, InventoryLineCreate):
    pass


class InventoryLineUpdate(GenInventoryLineUrl, GenUpdate):
    model = InventoryLine
    form_class = InventoryLineForm


class InventoryLineUpdateModal(GenUpdateModal, InventoryLineUpdate):
    pass


class InventoryLineDelete(GenInventoryLineUrl, GenDelete):
    model = InventoryLine


class InventoryLineDetail(GenInventoryLineUrl, GenDetail):
    model = InventoryLine
    groups = InventoryLineForm.__groups_details__()


class InventoryLineEAN13Fullinfo(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        # Get incoming info
        ean13 = kwargs.get("ean13", None)

        # Prepare answer
        answer = {}

        # If we got a ean13 code
        if ean13:
            pf = ProductFinal.objects.filter(ean13=ean13).first()
            if pf:
                fe = answer['unique'] = pf.product.feature_special
                if fe:
                    unique = bool(fe.unique)
                else:
                    unique = False

                # Prepare answer
                answer['pk'] = pf.pk
                answer['caducable'] = pf.product.caducable
                answer['unique'] = unique

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')


class InventoryLineUniqueFullinfo(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        # Get incoming info
        unique = kwargs.get("unique", None)

        # Prepare answer
        answer = {}

        # If we got a ean13 code
        if unique:
            pu = ProductUnique.objects.filter(value=unique).first()
            # Prepare answer
            if pu:
                answer['pk'] = pu.pk

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')
