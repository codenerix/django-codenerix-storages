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

from django.db.models import Q, F, Sum, Count
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
from codenerix_invoicing.models_purchases import PurchasesOrder, PurchasesLineOrder
from codenerix_storages.models import StorageOperator
from codenerix_storages.models_stockcontrol import Inventory, InventoryLine, InventoryIn, InventoryInLine, InventoryOut, InventoryOutLine
from codenerix_storages.forms_stockcontrol import InventoryForm, InventoryLineForm, InventoryInForm, InventoryInLineForm, InventoryOutForm, InventoryOutLineForm


# Inventory
class GenInventoryUrl(object):
    ws_entry_point = '{}/inventory'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryList(GenInventoryUrl, GenList):
    model = Inventory
    extra_context = {
        'menu': ['storage', 'inventory'],
        'bread': [_('Storage'), _('Inventory')],
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
        self.ws_entry_point = reverse('CDNX_storages_inventoryline_list', kwargs={"ipk": kwargs.get('ipk')})[1:]
        return super(InventoryLineList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit


class InventoryLineWork(GenInventoryLineUrl, GenList):
    model = InventoryLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryLine'), _('InventoryLine')]}
    defaultordering = "-created"
    static_partial_header = 'codenerix_storages/inventory_work_header.html'
    static_partial_row = 'codenerix_storages/inventory_work_row'
    static_app_row = 'codenerix_storages/inventory_work_app.js'
    static_controllers_row = 'codenerix_storages/inventory_work_controllers.js'
    linkedit = False
    linkadd = False
    default_ordering = '-created'
    gentrans = {
        'new': _('Unique product is new!'),
        'notfound': _('Product not found!'),
        'removerecord': _('Are you sure you want to remove "<name>"?'),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('box', _("Box")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        fields.append(('caducity', _("Caducity")))
        fields.append(('product_unique_value', None))
        return fields

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryline_work', kwargs={"ipk": self.ipk})[1:]
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]
        self.ws_submit = reverse('CDNX_storages_inventoryline_addws', kwargs={"ipk": self.ipk})[1:]

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
            'errors': {
                'zone': None,
                'quantity': None,
                'product': None,
                'unique': None,
                'caducity': None,
            },
            'ws': {
                'ean13_fullinfo': self.ws_ean13_fullinfo,
                'unique_fullinfo': self.ws_unique_fullinfo,
                'submit': self.ws_submit,
            },
            'form_zone': form.fields['box'].widget.render('box', None, {
                'ng-class': '{"bg-danger": data.meta.context.errors.zone}',
            }),
            'form_quantity': form.fields['quantity'].widget.render('quantity', None, {
                'ng-init': 'quantity=1.0',
                'ng-class': '{"bg-danger": data.meta.context.errors.quantity}',
            }),
            'form_product': form.fields['product_final'].widget.render('product_final', None, {
                'codenerix-on-enter': 'product_changed(this)',
                'ng-disabled': '!(box>0 && quantity>0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-info": unique_new, "bg-danger": data.meta.context.errors.unique}',
            }),
            'form_caducity': form.fields['caducity'].widget.render('caducity', None, {
                'codenerix-on-enter': 'submit_scenario()',
                'codenerix-focus': 'data.meta.context.caducity_focus',
                'ng-disabled': 'data.meta.context.caducity_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.caducity}',
                'placeholder': 'dd/mm/aaaa',
            }),
        }
        return super(InventoryLineWork, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit


class InventoryLineCreate(GenInventoryLineUrl, GenCreate):
    model = InventoryLine
    form_class = InventoryLineForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__ipk = kwargs.get('ipk', None)
        return super(InventoryLineCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__ipk:
            inventory = Inventory.objects.get(pk=self.__ipk)
            operator = StorageOperator.objects.get(external__user=self.request.user)
            self.request.inventory = inventory
            form.instance.inventory = inventory
            self.request.operator = operator
            form.instance.operator = operator
        return super(InventoryLineCreate, self).form_valid(form)


class InventoryLineCreateModal(GenCreateModal, InventoryLineCreate):
    pass


class InventoryLineCreateWS(InventoryLineCreate):
    json = True

    def form_valid(self, form):
        form.instance.product_unique_value = self.request.POST.get('product_unique_value', None)
        return super(InventoryLineCreateWS, self).form_valid(form)


class InventoryLineUpdate(GenInventoryLineUrl, GenUpdate):
    model = InventoryLine
    form_class = InventoryLineForm

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(InventoryLineUpdate, self).dispatch(*args, **kwargs)


class InventoryLineUpdateModal(GenUpdateModal, InventoryLineUpdate):
    pass


class InventoryLineDelete(GenInventoryLineUrl, GenDelete):
    model = InventoryLine


class InventoryLineDetail(GenInventoryLineUrl, GenDetail):
    model = InventoryLine
    groups = InventoryLineForm.__groups_details__()

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(InventoryLineDetail, self).dispatch(*args, **kwargs)


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


# Inventory Incoming Stock
class GenInventoryInUrl(object):
    ws_entry_point = '{}/inventoryin'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryInList(GenInventoryInUrl, GenList):
    model = InventoryIn
    extra_context = {
        'menu': ['storage', 'inventoryin'],
        'bread': [_('Storage'), _('Incoming Stock')],
    }
    gentrans = {
        'getreport': _("Get report"),
        'doinventory': _("Do inventory"),
    }

    def dispatch(self, *args, **kwargs):
        self.client_context = {
            'url_doinventory': reverse('CDNX_storages_inventoryinline_work', kwargs={"ipk": "__IPK__"}),
            'url_getreport': reverse('CDNX_storages_inventoryinline_list', kwargs={"ipk": "__IPK__"}),
        }
        return super(InventoryInList, self).dispatch(*args, **kwargs)


class InventoryInCreate(GenInventoryInUrl, GenCreate):
    model = InventoryIn
    form_class = InventoryInForm


class InventoryInCreateModal(GenCreateModal, InventoryInCreate):
    pass


class InventoryInUpdate(GenInventoryInUrl, GenUpdate):
    model = InventoryIn
    form_class = InventoryInForm


class InventoryInUpdateModal(GenUpdateModal, InventoryInUpdate):
    pass


class InventoryInDelete(GenInventoryInUrl, GenDelete):
    model = InventoryIn


class InventoryInDetail(GenInventoryInUrl, GenDetail):
    model = InventoryIn
    groups = InventoryInForm.__groups_details__()


# Inventory Incoming Stock Line
class GenInventoryInLineUrl(object):
    ws_entry_point = '{}/inventorylinein'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryInLineList(GenInventoryInLineUrl, GenList):
    model = InventoryInLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryInLine'), _('InventoryInLine')]}
    defaultordering = "-created"

    def dispatch(self, *args, **kwargs):
        self.ws_entry_point = reverse('CDNX_storages_inventoryinline_list', kwargs={"ipk": kwargs.get('ipk')})[1:]
        return super(InventoryInLineList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit


class InventoryInLineWork(GenInventoryInLineUrl, GenList):
    model = InventoryInLine
    extra_context = {
        'menu': ['storage', 'inventoryin'],
        'bread': [_('Storage'), _('Incoming Stock')],
    }
    defaultordering = "-created"
    static_partial_header = 'codenerix_storages/inventoryin_work_header.html'
    static_partial_row = 'codenerix_storages/inventoryin_work_row'
    static_app_row = 'codenerix_storages/inventoryin_work_app.js'
    static_controllers_row = 'codenerix_storages/inventoryin_work_controllers.js'
    linkedit = False
    linkadd = False
    default_ordering = '-created'
    gentrans = {
        'new': _('Unique product is new!'),
        'notfound': _('Product not found!'),
        'removerecord': _('Are you sure you want to remove "<name>"?'),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('purchasesorder', _("Order")))
        fields.append(('box', _("Box")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_final__pk', None))
        fields.append(('product_unique', _("Unique")))
        fields.append(('caducity', _("Caducity")))
        fields.append(('product_unique_value', None))
        return fields

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryinline_work', kwargs={"ipk": self.ipk})[1:]
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryinline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryinline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]
        self.ws_submit = reverse('CDNX_storages_inventoryinline_addws', kwargs={"ipk": self.ipk})[1:]
        self.ws_inventoryinline_purchasesorder = reverse('CDNX_storages_inventoryinline_purchase_order', kwargs={"inventoryinline_pk": 1, "purchasesorder_pk": 1})[1:]

        # Prepare form
        fields = []
        fields.append((DynamicSelect, 'purchasesorder', 3, 'CDNX_invoicing_orderpurchasess_foreign', ['provider:{}'.format(self.ipk)], {
            'ng-change': 'order_change($externalScope.row.pk, $externalScope.purchasesorder)',
            'placeholder': '{{{{row.purchasesorder|default:"{}"}}}}'.format(_("Press * or start typing")),
            'ng-placeholder': '(row.purchasesorder || \'{}\')'.format(_("Press * or start typing")),
        }))
        fields.append((DynamicSelect, 'box', 3, 'CDNX_storages_storageboxs_foreign', [], {}))
        fields.append((DynamicInput, 'product_final', 3, 'CDNX_products_productfinalsean13_foreign', [], {}))
        fields.append((DynamicInput, 'product_unique', 3,  'CDNX_products_productuniquescode_foreign', ['product_final'], {}))
        form = InventoryInLineForm()
        for (widget, key, minchars, url, autofill, newattrs) in fields:
            wattrs = form.fields[key].widget.attrs
            wattrs.update(newattrs)
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
            'errors': {
                'zone': None,
                'quantity': None,
                'product': None,
                'unique': None,
                'caducity': None,
            },
            'ws': {
                'ean13_fullinfo': self.ws_ean13_fullinfo,
                'unique_fullinfo': self.ws_unique_fullinfo,
                'submit': self.ws_submit,
                'inventoryinline_purchasesorder': self.ws_inventoryinline_purchasesorder,
            },
            'form_order': form.fields['purchasesorder'].widget.render('purchasesorder', None, {
                'ng-class': '{"bg-danger": data.meta.context.errors.order}',
            }),
            'form_order_row': form.fields['purchasesorder'].widget.render('purchasesorder', None, {
                'ng-class': '{"bg-danger": data.meta.context.errors.order_row}',
            }),
            'form_zone': form.fields['box'].widget.render('box', None, {
                'ng-class': '{"bg-danger": data.meta.context.errors.zone}',
            }),
            'form_quantity': form.fields['quantity'].widget.render('quantity', None, {
                'ng-init': 'quantity=1.0',
                'ng-class': '{"bg-danger": data.meta.context.errors.quantity}',
            }),
            'form_product': form.fields['product_final'].widget.render('product_final', None, {
                'codenerix-on-enter': 'product_changed(this)',
                'ng-disabled': '!(box>0 && quantity>0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.unique || unique_error}',
            })+" <span class='fa fa-exclamation-triangle text-danger' ng-show='unique_error' alt='{{unique_error}}' title='{{unique_error}}'></span>",
            'form_caducity': form.fields['caducity'].widget.render('caducity', None, {
                'codenerix-on-enter': 'submit_scenario()',
                'codenerix-focus': 'data.meta.context.caducity_focus',
                'ng-disabled': 'data.meta.context.caducity_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.caducity}',
                'placeholder': 'dd/mm/aaaa',
            }),
        }
        return super(InventoryInLineWork, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit

    def json_builder(self, answer, context):

        # Get the list of purhasesorders for this inventory
        qs = self.get_queryset(raw_query=True)
        temp = list(set(qs.values_list('purchasesorder')))
        purchasesorders = []
        for ele in temp:
            if ele[0] is not None:
                purchasesorders.append(ele[0])

        # List of registered products and quantity
        # registered = self.model.objects.filter(inventory__pk=self.ipk).values("product_final").annotate(total=Count("quantity"))
        registered = self.bodybuilder(context['object_list'], self.autorules())

        # Get purchases (requested products)
        requested = PurchasesLineOrder.objects.filter(order__pk__in=purchasesorders).values("order", "product",  "product__code", "product__ean13").annotate(total=Sum("quantity"))
        # raise IOError(requested)

        # Process registered products
        body_registered = []
        for g in registered:
            g['missing'] = float(g['quantity'])

            if g['purchasesorder']:
                for r in requested:
                    if r['order']:
                        if r['product'] == int(g['product_final__pk']):
                            if r['total'] > g['missing']:
                                r['total'] -= g['missing']
                                g['missing'] = 0.0
                            else:
                                g['missing'] -= r['total']
                                r['total'] = 0.0

            # Add a new token
            body_registered.append(g)

        # Process unregistered products
        body_requested = []
        for r in requested:
            # If still left
            if r['total'] > 0:
                token = {
                    'caducity': None,
                    'purchasesorder': None,
                    'product_unique_value': None,
                    'product_final': '{} ({})'.format(r['product__code'], r['product__ean13']),
                    'product_final__pk': None,
                    'product_unique': None,
                    'pk': None,
                    'quantity': r['total'],
                    'box': None,
                    'total': None,
                }

            # Add a new token
            body_requested.append(token)

        # Return answer
        answer['table']['body'] = body_requested + body_registered
        return answer


class InventoryInLineCreate(GenInventoryInLineUrl, GenCreate):
    model = InventoryInLine
    form_class = InventoryInLineForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__ipk = kwargs.get('ipk', None)
        return super(InventoryInLineCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__ipk:
            inventory = InventoryIn.objects.get(pk=self.__ipk)
            operator = StorageOperator.objects.get(external__user=self.request.user)
            self.request.inventory = inventory
            form.instance.inventory = inventory
            self.request.operator = operator
            form.instance.operator = operator
        return super(InventoryInLineCreate, self).form_valid(form)


class InventoryInLineCreateModal(GenCreateModal, InventoryInLineCreate):
    pass


class InventoryInLineCreateWS(InventoryInLineCreate):
    json = True

    def form_valid(self, form):
        form.instance.product_unique_value = self.request.POST.get('product_unique_value', None)
        return super(InventoryInLineCreateWS, self).form_valid(form)


class InventoryInLineUpdate(GenInventoryInLineUrl, GenUpdate):
    model = InventoryInLine
    form_class = InventoryInLineForm

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(InventoryInLineUpdate, self).dispatch(*args, **kwargs)


class InventoryInLineUpdateModal(GenUpdateModal, InventoryInLineUpdate):
    pass


class InventoryInLineDelete(GenInventoryInLineUrl, GenDelete):
    model = InventoryInLine


class InventoryInLineDetail(GenInventoryInLineUrl, GenDetail):
    model = InventoryInLine
    groups = InventoryInLineForm.__groups_details__()

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(InventoryInLineDetail, self).dispatch(*args, **kwargs)


class InventoryInLineEAN13Fullinfo(View):

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


class InventoryInLineUniqueFullinfo(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        # Get incoming info
        unique = kwargs.get("unique", None)

        # Prepare answer
        answer = {}

        # If we got a unique code
        if unique:
            pu = ProductUnique.objects.filter(value=unique).first()
            pl = InventoryInLine.objects.filter(product_unique_value=unique).first()
            # Prepare answer
            if pu:
                answer['pk'] = pu.pk
                answer['error'] = True
                answer['errortxt'] = _("Unique product already exists in our database!") + " [PK:{}]".format(pu.pk)
            if pl:
                answer['pl'] = pl.pk
                answer['error'] = True
                answer['errortxt'] = _("Unique product already registered here!") + " [PK:{}]".format(pl.pk)

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')


class InventoryInLinePurhcaseOrder(View):

    def dispatch(self, *args, **kwargs):
        # Get args
        ipk = kwargs.get('inventoryinline_pk', None)
        ppk = kwargs.get('purchasesorder_pk', None)

        # Prepare answer
        answer = {}

        # Find line
        inventoryinline = InventoryInLine.objects.filter(pk=ipk).first()
        if inventoryinline:
            if ppk == 'null':
                inventoryinline.purchasesorder = None
                inventoryinline.save()
                answer['result'] = 'OK'
                answer['error'] = False
            else:
                purchasesorder = PurchasesOrder.objects.filter(pk=ppk).first()
                if purchasesorder:
                    inventoryinline.purchasesorder = purchasesorder
                    inventoryinline.save()
                    answer['result'] = 'OK'
                    answer['error'] = False
                else:
                    answer['error'] = True
                    answer['errortxt'] = _("Purchase order not found!")+" [PK:{}]".format(ppk)
        else:
            answer['error'] = True
            answer['errortxt'] = _("Inventory IN Line not found!")+" [PK:{}]".format(ipk)

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')


# Inventory Outgoing Stock
class GenInventoryOutUrl(object):
    ws_entry_point = '{}/inventoryout'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryOutList(GenInventoryOutUrl, GenList):
    model = InventoryOut
    extra_context = {
        'menu': ['storage', 'inventoryout'],
        'bread': [_('Storage'), _('Outgoing stock (Orders)')],
    }
    gentrans = {
        'getreport': _("Get report"),
        'doinventory': _("Do inventory"),
    }

    def dispatch(self, *args, **kwargs):
        self.client_context = {
            'url_doinventory': reverse('CDNX_storages_inventoryoutline_work', kwargs={"ipk": "__IPK__"}),
            'url_getreport': reverse('CDNX_storages_inventoryoutline_list', kwargs={"ipk": "__IPK__"}),
        }
        return super(InventoryOutList, self).dispatch(*args, **kwargs)


class InventoryOutCreate(GenInventoryOutUrl, GenCreate):
    model = InventoryOut
    form_class = InventoryOutForm


class InventoryOutCreateModal(GenCreateModal, InventoryOutCreate):
    pass


class InventoryOutUpdate(GenInventoryOutUrl, GenUpdate):
    model = InventoryOut
    form_class = InventoryOutForm


class InventoryOutUpdateModal(GenUpdateModal, InventoryOutUpdate):
    pass


class InventoryOutDelete(GenInventoryOutUrl, GenDelete):
    model = InventoryOut


class InventoryOutDetail(GenInventoryOutUrl, GenDetail):
    model = InventoryOut
    groups = InventoryOutForm.__groups_details__()


# Inventory Outoging Stock Line
class GenInventoryOutLineUrl(object):
    ws_entry_point = '{}/inventoryoutline'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryOutLineList(GenInventoryOutLineUrl, GenList):
    model = InventoryOutLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryOutLine'), _('InventoryOutLine')]}
    defaultordering = "-created"

    def dispatch(self, *args, **kwargs):
        self.ws_entry_point = reverse('CDNX_storages_inventoryoutline_list', kwargs={"ipk": kwargs.get('ipk')})[1:]
        return super(InventoryOutLineList, self).dispatch(*args, **kwargs)


class InventoryOutLineWork(GenInventoryOutLineUrl, GenList):
    model = InventoryOutLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryOutLine'), _('InventoryOutLine')]}
    defaultordering = "-created"
    static_partial_header = 'codenerix_storages/inventoryout_work_header.html'
    static_partial_row = 'codenerix_storages/inventoryout_work_row'
    static_app_row = 'codenerix_storages/inventoryout_work_app.js'
    static_controllers_row = 'codenerix_storages/inventoryout_work_controllers.js'
    linkedit = False
    linkadd = False
    default_ordering = '-created'
    gentrans = {
        'new': _('Unique product is new!'),
        'notfound': _('Product not found!'),
        'removerecord': _('Are you sure you want to remove "<name>"?'),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('box', _("Box")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        fields.append(('caducity', _("Caducity")))
        fields.append(('product_unique_value', None))
        return fields

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryoutline_work', kwargs={"ipk": self.ipk})[1:]
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryoutline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryoutline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]
        self.ws_submit = reverse('CDNX_storages_inventoryoutline_addws', kwargs={"ipk": self.ipk})[1:]

        # Prepare form
        fields = []
        fields.append((DynamicSelect, 'box', 3, 'CDNX_storages_storageboxs_foreign', []))
        fields.append((DynamicInput, 'product_final', 3, 'CDNX_products_productfinalsean13_foreign', []))
        fields.append((DynamicInput, 'product_unique', 3,  'CDNX_products_productuniquescode_foreign', ['product_final']))
        form = InventoryOutLineForm()
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
            'errors': {
                'zone': None,
                'quantity': None,
                'product': None,
                'unique': None,
                'caducity': None,
            },
            'ws': {
                'ean13_fullinfo': self.ws_ean13_fullinfo,
                'unique_fullinfo': self.ws_unique_fullinfo,
                'submit': self.ws_submit,
            },
            'form_zone': form.fields['box'].widget.render('box', None, {
                'ng-class': '{"bg-danger": data.meta.context.errors.zone}',
            }),
            'form_quantity': form.fields['quantity'].widget.render('quantity', None, {
                'ng-init': 'quantity=1.0',
                'ng-class': '{"bg-danger": data.meta.context.errors.quantity}',
            }),
            'form_product': form.fields['product_final'].widget.render('product_final', None, {
                'codenerix-on-enter': 'product_changed(this)',
                'ng-disabled': '!(box>0 && quantity>0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-info": unique_new, "bg-danger": data.meta.context.errors.unique}',
            }),
            'form_caducity': form.fields['caducity'].widget.render('caducity', None, {
                'codenerix-on-enter': 'submit_scenario()',
                'codenerix-focus': 'data.meta.context.caducity_focus',
                'ng-disabled': 'data.meta.context.caducity_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.caducity}',
                'placeholder': 'dd/mm/aaaa',
            }),
        }
        return super(InventoryOutLineWork, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit


class InventoryOutLineCreate(GenInventoryOutLineUrl, GenCreate):
    model = InventoryOutLine
    form_class = InventoryOutLineForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__ipk = kwargs.get('ipk', None)
        return super(InventoryOutLineCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__ipk:
            inventory = InventoryOut.objects.get(pk=self.__ipk)
            operator = StorageOperator.objects.get(external__user=self.request.user)
            self.request.inventory = inventory
            form.instance.inventory = inventory
            self.request.operator = operator
            form.instance.operator = operator
        return super(InventoryOutLineCreate, self).form_valid(form)


class InventoryOutLineCreateModal(GenCreateModal, InventoryOutLineCreate):
    pass


class InventoryOutLineCreateWS(InventoryOutLineCreate):
    json = True

    def form_valid(self, form):
        form.instance.product_unique_value = self.request.POST.get('product_unique_value', None)
        return super(InventoryOutLineCreateWS, self).form_valid(form)


class InventoryOutLineUpdate(GenInventoryOutLineUrl, GenUpdate):
    model = InventoryOutLine
    form_class = InventoryOutLineForm

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(InventoryOutLineUpdate, self).dispatch(*args, **kwargs)


class InventoryOutLineUpdateModal(GenUpdateModal, InventoryOutLineUpdate):
    pass


class InventoryOutLineDelete(GenInventoryOutLineUrl, GenDelete):
    model = InventoryOutLine


class InventoryOutLineDetail(GenInventoryOutLineUrl, GenDetail):
    model = InventoryOutLine
    groups = InventoryOutLineForm.__groups_details__()

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(InventoryOutLineDetail, self).dispatch(*args, **kwargs)


class InventoryOutLineEAN13Fullinfo(View):

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


class InventoryOutLineUniqueFullinfo(View):

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
