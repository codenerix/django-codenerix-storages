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

from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext as _
from django.urls import reverse

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail
from codenerix.widgets import DynamicInput, DynamicSelect

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
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        return fields

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryline_work', kwargs={"ipk": self.ipk})[1:]

        # Prepare form
        fields = []
        fields.append((DynamicSelect, 'box', 3, 'CDNX_storages_storageboxs_foreign'))
        fields.append((DynamicInput, 'product_final', 333, 'CDNX_products_productfinals_foreign_sales'))
        fields.append((DynamicInput, 'product_unique', 333,  'CDNX_products_productuniques_foreign'))
        form = InventoryLineForm()
        for (widget, key, minchars, url) in fields:
            wattrs = form.fields[key].widget.attrs
            form.fields[key].widget = widget(wattrs)
            form.fields[key].widget.form_name = form.form_name
            form.fields[key].widget.field_name = key
            form.fields[key].widget.autofill_deepness = minchars
            form.fields[key].widget.autofill_url = url
            form.fields[key].widget.autofill = []

        # Prepare context
        self.client_context = {
            'ipk': self.ipk,
            'final_focus': 'true',
            'unique_focus': 'false',
            'unique_disabled': 'true',
            'form_zone': form.fields['box'].widget.render('box', None, {}),
            'form_product': form.fields['product_final'].widget.render('product_final', None, {
                'codenerix-on-enter':'product_final=product_changed(product_final)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter':'Array(product_final, product_unique)==unique_changed(product_final, product_unique); product_final=""; product_unique=""',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
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
