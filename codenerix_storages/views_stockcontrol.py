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

from django.db import transaction
from django.db.models import Q, F, Sum, Value
from django.db.models.functions import Substr, Length, Concat
from django.conf import settings
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from django.utils import timezone
from django.template.loader import get_template

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenForeignKey
from codenerix.widgets import DynamicInput, DynamicSelect

from codenerix_products.models import ProductFinal, ProductUnique
from codenerix_invoicing.models_purchases import PurchasesOrder, PurchasesLineOrder, PurchasesAlbaran, PurchasesLineAlbaran
from codenerix_invoicing.models_sales import SalesLines, SalesAlbaran
from codenerix_storages.models import StorageOperator, StorageBox
from codenerix_storages.models_stockcontrol import Inventory, InventoryLine, InventoryIn, InventoryInLine, InventoryOut, InventoryOutLine, Distribution, DistributionLine, OutgoingAlbaran, LineOutgoingAlbaran
from codenerix_storages.forms_stockcontrol import InventoryForm, InventoryNotesForm, InventoryLineForm, InventoryLineNotesForm, InventoryInForm, InventoryInNotesForm, InventoryInLineForm, InventoryInLineNotesForm, InventoryOutForm, InventoryOutNotesForm, InventoryOutLineForm, InventoryOutLineNotesForm, DistributionForm, DistributionLineForm
from codenerix_extensions.helpers import get_language_database


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


class InventoryNotes(GenInventoryUrl, GenUpdate):
    model = Inventory
    form_class = InventoryNotesForm
    linkdelete = False


class InventoryNotesModal(GenUpdateModal, InventoryNotes):
    pass


class InventoryDelete(GenInventoryUrl, GenDelete):
    model = Inventory


class InventoryDetail(GenInventoryUrl, GenDetail):
    model = Inventory
    groups = InventoryForm.__groups_details__()


class InventorySetStock(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        # Get Inventory PK
        self.ipk = kwargs.get('pk', None)
        inventory = Inventory.objects.filter(pk=self.ipk).first()

        # Prepare answer
        answer = {}

        # Check answer
        if inventory:

            # Get language
            lang = get_language_database()

            # Every block is transactional
            with transaction.atomic():

                # Prepare a compact queryset
                compact = ProductUnique.objects
                if inventory.zone:
                    compact = compact.filter(box__box_structure__zone=inventory.zone)
                else:
                    compact = compact.filter(box__box_structure__zone__storage=inventory.storage)
                compact = compact.values(
                    "box__id",
                    "product_final__id",
                    "value",
                    "caducity"
                ).annotate(
                    box=F('box__id'),
                    product_final=F('product_final__id'),
                    product_unique=F('value'),
                    total=Sum('stock_real'),
                )
                # Add filter for location

                # Simulate Inventory
                for line in compact:
                    # Box
                    box_id = line.get('box')
                    box = StorageBox.objects.get(pk=box_id)

                    # Product final
                    product_final_id = line.get('product_final')
                    product_final = ProductFinal.objects.get(pk=product_final_id)

                    # Product unique
                    product_unique_value = line.get('product_unique', None)
                    if product_unique_value is None:
                        product_unique = None
                    else:
                        product_unique = product_unique_value

                    # Caducity
                    caducity_value = line.get('caducity', None)
                    if caducity_value is None:
                        caducity = None
                    else:
                        caducity = caducity_value

                    # Total
                    total_storage = line['total']

                    # Calculate the total products in this storage/zone
                    inv = InventoryLine.objects.filter(inventory__pk=self.ipk, product_final=product_final)
                    if product_unique is None:
                        inv = inv.filter(product_unique__isnull=True)
                    else:
                        inv = inv.filter(product_unique__value=product_unique)
                    if caducity is None:
                        inv = inv.filter(caducity__isnull=True)
                    else:
                        inv = inv.filter(caducity=caducity)

                    # Unify result
                    total_inv = inv.values(
                        "box__id",
                        "product_final__id",
                        "product_unique__id",
                        "caducity"
                    ).annotate(
                        box=F('box__id'),
                        product_final=F('product_final__id'),
                        product_unique=F('product_unique__id'),
                    ).aggregate(
                        total=Sum('quantity')
                    ).get('total')

                    if total_inv is None:
                        total_inv = 0.0

                    # Find if there are more or less than it should be
                    dif = total_inv - total_storage
                    if dif > 0:
                        # Add new products
                        pu = ProductUnique()
                        pu.box = box
                        pu.product_final = product_final
                        pu.value = product_unique
                        pu.caducity = caducity
                        pu.stock_original = dif
                        pu.save()
                    elif dif < 0:
                        # Find extra producs
                        pus = ProductUnique.objects.filter(
                            box=box,
                            product_final=product_final,
                            value=product_unique,
                            caducity=caducity,
                        )
                        # Remove extra products until quantity is normalized
                        dif = abs(dif)
                        for pu in pus:
                            # Calculate free products
                            free = pu.stock_real-pu.stock_locked
                            if free:
                                # There are free products here
                                if free <= dif:
                                    dif -= free
                                    if pu.stock_locked == 0:
                                        # No more products here, delete please!
                                        pu.delete()
                                    else:
                                        # We will remove the free ones
                                        pu.stock_original -= free
                                        pu.save()
                                else:
                                    # We have enought products here to make free
                                    pu.stock_real -= dif
                                    pu.save()
                                    dif = 0

                        # If we should delete some products but can not anymore
                        if dif:
                            raise IOError("Not enought produts to be deleted!")

                # Add the rest of extra products
                inv = InventoryLine.objects.filter(
                    inventory__pk=self.ipk,
                    product_final__products_unique__isnull=True
                ).values(
                    "box__name",
                    "product_final__{}__name".format(lang),
                    "product_unique__value",
                    "caducity"
                ).annotate(
                    total=Sum('quantity'),
                    box_id=F('box__id'),
                    box=F('box__name'),
                    product_final_id=F('product_final__id'),
                    product_final=Concat(
                        F('product_final__{}__name'.format(lang)),
                        Value(" ("),
                        F('product_final__ean13'),
                        Value(")")
                    ),
                    product_unique_id=F('product_unique__id'),
                    product_unique=F('product_unique__value'),
                )
                for line in inv:
                    # Get details
                    box = StorageBox.objects.get(pk=line['box_id'])
                    product_final = ProductFinal.objects.get(pk=line['product_final_id'])
                    product_unique = line['product_unique']
                    caducity = line['caducity']
                    total = line['total']

                    # Add new products
                    pu = ProductUnique()
                    pu.box = box
                    pu.product_final = product_final
                    pu.value = product_unique
                    pu.caducity = caducity
                    pu.stock_original = total
                    pu.save()

                # End inventory
                inventory.processed = True
                inventory.end = timezone.now()
                inventory.save()

            # Return answer
            answer['return'] = "OK"
        else:
            answer['error'] = True
            answer['errortxt'] = _("Inventory not found!")

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')


# InventoryLine
class GenInventoryLineUrl(object):
    ws_entry_point = '{}/inventoryline'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryLineList(GenInventoryLineUrl, GenList):
    model = InventoryLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryLine'), _('InventoryLine')]}
    defaultordering = "-created"
    linkadd = False
    linkedit = False

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
    default_ordering = "product_final"  # Must be PRODUCT_FINAL so the Sum() will work properly
    static_partial_header = 'codenerix_storages/inventory_work_header.html'
    static_partial_row = 'codenerix_storages/inventory_work_row'
    static_app_row = 'codenerix_storages/inventory_work_app.js'
    static_controllers_row = 'codenerix_storages/inventory_work_controllers.js'
    linkedit = False
    linkadd = False
    gentrans = {
        'new': _('Unique product is new!'),
        'notfound': _('Product not found!'),
        'removerecord': _('Are you sure you want to remove "<name>"?'),
        'inventariar': _("Inventariar"),
        'compact': _("Compact"),
        'extended': _("Extended"),
    }

    def __fields__(self, info):
        fields = []
        if not info.jsonquery.get("extended", False):
            fields.append(('box__name', _("Box")))
            fields.append(('total', _("Quantity")))
            fields.append(('product_final__code', _("Product")))
            fields.append(('product_unique__value', _("Unique")))
        else:
            fields.append(('box', _("Box")))
            fields.append(('quantity', _("Quantity")))
            fields.append(('product_final', _("Product")))
            fields.append(('product_unique', _("Unique")))
        fields.append(('product_unique_value', None))
        fields.append(('caducity', _("Caducity")))
        fields.append(('notes', _("Notes")))
        return fields

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryline_work', kwargs={"ipk": self.ipk})[1:]
        return super(InventoryLineWork, self).dispatch(*args, **kwargs)

    def set_context_json(self, jsonquery):
        # Get constants
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]
        self.ws_submit = reverse('CDNX_storages_inventoryline_addws', kwargs={"ipk": self.ipk})[1:]
        self.ws_inventory_notesmodal = reverse('CDNX_storages_inventory_notesmodal', kwargs={"pk": self.ipk})[1:]
        self.ws_inventoryline_notesmodal = reverse('CDNX_storages_inventoryline_notesmodal', kwargs={"pk": 'INVENTORYLINE_PK'})[1:]
        self.url_inventory = reverse('CDNX_storages_inventory_list')[1:]

        # Find provider_pk
        inv = Inventory.objects.filter(pk=self.ipk).first()

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
            'processed': inv.processed,
            'notes': inv.notes,
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
                'inventory_notesmodal': self.ws_inventory_notesmodal,
                'inventoryline_notesmodal': self.ws_inventoryline_notesmodal,
                'url_inventory': self.url_inventory,
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
                'codenerix-on-tab': 'product_changed(this)',
                'ng-disabled': '!(box>0 && quantity>0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-on-tab': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-info": unique_new, "bg-danger": data.meta.context.errors.unique}',
            }),
            'form_caducity': form.fields['caducity'].widget.render('caducity', None, {
                'codenerix-on-enter': 'submit_scenario()',
                'codenerix-on-tab': 'submit_scenario()',
                'codenerix-focus': 'data.meta.context.caducity_focus',
                'ng-disabled': 'data.meta.context.caducity_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.caducity}',
                'placeholder': 'dd/mm/aaaa',
            }),
        }
        return super(InventoryLineWork, self).set_context_json(jsonquery)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit

    def custom_queryset(self, queryset, info):
        lang = get_language_database()
        inventory = Inventory.objects.filter(pk=self.ipk).first()

        # Return extended or compact result
        if not info.jsonquery.get("extended", False):
            queryset = queryset.all().values(
                "box__name",
                "product_final__{}__name".format(lang),
                "product_unique__value",
                "caducity"
            ).annotate(
                total=Sum('quantity'),
                box_id=F('box__id'),
                box=F('box__name'),
                product_final_id=F('product_final__id'),
                product_final=Concat(
                    F('product_final__{}__name'.format(lang)),
                    Value(" ("),
                    F('product_final__ean13'),
                    Value(")")
                ),
                product_unique_id=F('product_unique__id'),
                product_unique=F('product_unique__value'),
            ).annotate(
                quantity=F('total'),
                total_notes=Sum(Length(Substr('notes', 1, 1))),
            )

        # Prepare options
        new = []
        new.append((_("Box"), _("Product final"), _("Product unique"), _("Caducity"), _("Quantity"), _("Locked")))
        lost = []
        lost.append((_("Box"), _("Product final"), _("Product unique"), _("Caducity"), _("Quantity"), _("Locked")))

        # Prepare a compact queryset
        compact = ProductUnique.objects
        if inventory.zone:
            compact = compact.filter(box__box_structure__zone=inventory.zone)
        else:
            compact = compact.filter(box__box_structure__zone__storage=inventory.storage)
        compact = compact.values(
            "box__id",
            "product_final__id",
            "value",
            "caducity"
        ).annotate(
            box=F('box__id'),
            product_final=F('product_final__id'),
            product_unique=F('value'),
            total_real=Sum('stock_real'),
            total_locked=Sum('stock_locked')
        )

        # Simulate Inventory
        total_new = 0.0
        total_lost = 0.0
        locked_inventory = 0
        for line in compact:
            # Box
            box_id = line.get('box')
            box = StorageBox.objects.get(pk=box_id)

            # Product final
            product_final_id = line.get('product_final')
            product_final = ProductFinal.objects.get(pk=product_final_id)

            # Product unique
            product_unique_value = line.get('product_unique', None)
            if product_unique_value is None:
                product_unique = None
            else:
                product_unique = product_unique_value

            # Caducity
            caducity_value = line.get('caducity', None)
            if caducity_value is None:
                caducity = None
            else:
                caducity = caducity_value

            # Total
            total_storage = line['total_real']
            total_locked = line['total_locked']

            # Calculate the total products in this storage/zone
            inv = InventoryLine.objects.filter(inventory__pk=self.ipk, product_final=product_final)
            if product_unique is None:
                inv = inv.filter(product_unique__isnull=True)
            else:
                inv = inv.filter(product_unique__value=product_unique)
            if caducity is None:
                inv = inv.filter(caducity__isnull=True)
            else:
                inv = inv.filter(caducity=caducity)

            # Unify result
            total_inv = inv.values(
                "box__id",
                "product_final__id",
                "product_unique__id",
                "caducity"
            ).annotate(
                box=F('box__id'),
                product_final=F('product_final__id'),
                product_unique=F('product_unique__id'),
            ).aggregate(
                total=Sum('quantity')
            ).get('total')

            if total_inv is None:
                total_inv = 0.0

            # Find if there are more or less than it should be
            dif = total_inv - total_storage
            locked = total_inv - total_locked
            if locked < 0:
                locked = abs(locked)
                locked_inventory += locked
            else:
                locked = None
            if dif > 0:
                # We have more products than we should
                new.append((
                    str(box),
                    str(product_final),
                    product_unique and str(product_unique) or None,
                    caducity and str(caducity) or None,
                    dif,
                    locked
                ))
                total_new += dif
            elif dif < 0:
                # We have less products than we should
                lost.append((
                    str(box),
                    str(product_final),
                    product_unique and str(product_unique) or None,
                    caducity and str(caducity) or None,
                    abs(dif),
                    locked
                ))
                total_lost += abs(dif)

        inv = InventoryLine.objects.filter(
            inventory__pk=self.ipk,
            product_final__products_unique__isnull=True
        ).values(
            "box__name",
            "product_final__{}__name".format(lang),
            "product_unique__value",
            "caducity"
        ).annotate(
            total=Sum('quantity'),
            box_id=F('box__id'),
            box=F('box__name'),
            product_final_id=F('product_final__id'),
            product_final=Concat(
                F('product_final__{}__name'.format(lang)),
                Value(" ("),
                F('product_final__ean13'),
                Value(")")
            ),
            product_unique_id=F('product_unique__id'),
            product_unique=F('product_unique__value'),
        )
        for line in inv:
            # Get details
            box = line['box']
            product_final = line['product_final']
            product_unique = line['product_unique']
            caducity = line['caducity']
            total = line['total']

            # Find if there are more or less than it should be
            new.append((
                str(box),
                str(product_final),
                product_unique and str(product_unique) or None,
                caducity and str(caducity) or None,
                total,
                None
            ))
            total_new += total

        # Make body
        body = []
        if total_lost:
            body.append({'title': _('Lost'), 'total': total_lost, 'style': 'danger', 'data': lost})
        if total_new:
            body.append({'title': _('New'), 'total': total_new, 'style': 'success', 'data': new})

        # Render simulation
        context = {}
        context['body'] = body
        context['locked_inventory'] = locked_inventory
        context['processed'] = inventory.processed
        template = get_template('codenerix_storages/inventory.html')
        simulation = template.render(context)

        # Add locked to header
        header = []
        if total_lost:
            header.append({'title': _('Lost'), 'total': total_lost, 'style': 'danger'})
        if locked_inventory:
            header.append({'title': _('Locked'), 'total': locked_inventory, 'style': 'warning'})
        if total_new:
            header.append({'title': _('New'), 'total': total_new, 'style': 'success'})

        # Set new context
        self.client_context['simulation_header'] = header
        self.client_context['simulation'] = simulation
        self.client_context['locked_inventory'] = locked_inventory

        # Return final queryset
        return queryset


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


class InventoryLineNotes(GenInventoryLineUrl, GenUpdate):
    model = InventoryLine
    form_class = InventoryLineNotesForm
    linkdelete = False


class InventoryLineNotesModal(GenUpdateModal, InventoryLineNotes):
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


# Distribution List
class DistributionList(GenList):
    model = Distribution
    linkedit = False
    field_delete = True
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
        return super(DistributionList, self).dispatch(*args, **kwargs)


class DistributionCreate(GenCreate):
    model = Distribution
    form_class = DistributionForm


class DistributionCreateModal(GenCreateModal, DistributionCreate):
    pass


class DistributionUpdate(GenUpdate):
    model = Distribution
    form_class = DistributionForm


class DistributionUpdateModal(GenUpdateModal, DistributionUpdate):
    pass


class DistributionDelete(GenDelete):
    model = Distribution


class DistributionDetail(GenDetail):
    model = Distribution
    groups = DistributionForm.__groups_details__()


# Distribution List Line
class DistributionLineList(GenList):
    model = DistributionLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('DistributionLine'), _('DistributionLine')]}
    defaultordering = "-created"

    def dispatch(self, *args, **kwargs):
        self.ws_entry_point = reverse('CDNX_storages_inventoryinline_list', kwargs={"ipk": kwargs.get('ipk')})[1:]
        return super(DistributionLineList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit


class DistributionLineWork(GenList):
    model = DistributionLine
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
        'albaranar': _("Albaranar"),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('purchasesorder', _("Purchase Order")))
        fields.append(('purchasesorder__pk', None))
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

        # Find provider_pk
        inv = Distribution.objects.filter(pk=self.ipk).first()
        if inv:
            provider_pk = inv.provider.pk
        else:
            provider_pk = None

        # Prepare form
        fields = []
        fields.append((DynamicSelect, 'purchasesorder', 3, 'CDNX_invoicing_orderpurchasess_foreign', ['provider:{}'.format(provider_pk)], {
            'ng-change': 'order_change($externalScope.row.pk, $externalScope.purchasesorder)',
            'placeholder': '{{{{row.purchasesorder|default:"{}"}}}}'.format(_("Press * or start typing")),
            'ng-placeholder': '(row.purchasesorder || \'{}\')'.format(_("Press * or start typing")),
        }))
        fields.append((DynamicSelect, 'box', 3, 'CDNX_storages_storageboxs_foreign', [], {}))
        fields.append((DynamicInput, 'product_final', 3, 'CDNX_products_productfinalsean13_foreign', [], {}))
        fields.append((DynamicInput, 'product_unique', 3,  'CDNX_products_productuniquescode_foreign', ['product_final'], {}))
        form = DistributionLineForm()
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
                'codenerix-on-tab': 'product_changed(this)',
                'ng-disabled': '!(box>0 && quantity>0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-on-tab': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.unique || unique_error}',
            })+" <span class='fa fa-exclamation-triangle text-danger' ng-show='unique_error' alt='{{unique_error}}' title='{{unique_error}}'></span>",
            'form_caducity': form.fields['caducity'].widget.render('caducity', None, {
                'codenerix-on-enter': 'submit_scenario()',
                'codenerix-on-tab': 'submit_scenario()',
                'codenerix-focus': 'data.meta.context.caducity_focus',
                'ng-disabled': 'data.meta.context.caducity_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.caducity}',
                'placeholder': 'dd/mm/aaaa',
            }),
        }
        return super(DistributionLineWork, self).dispatch(*args, **kwargs)

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
        registered = self.bodybuilder(context['object_list'], self.autorules())
        # raise IOError(registered)

        # Get purchases (requested products)
        requested = PurchasesLineOrder.objects.filter(order__pk__in=purchasesorders).values("order", "product",  "product__code", "product__ean13").annotate(total=Sum("quantity"))
        # raise IOError(requested)

        # Get already purchased products
        alreadyin = ProductUnique.objects.filter(line_albaran_purchases__line_order__order__pk__in=purchasesorders).values('product_final').annotate(total=Sum('stock_original'))

        # Recalculate quantity of requested products
        for r in requested:
            for i in alreadyin:
                if i['product_final'] == r['product']:
                    r['total'] -= i['total']
                    break

        # Process registered products
        body_registered = []
        for g in registered:
            # It is not a virtual line
            g['virtual'] = False
            # Copy quantity
            g['missing'] = float(g['quantity'])
            if g['purchasesorder__pk']:

                for r in requested:
                    if r['order'] and (r['product'] == int(g['product_final__pk'])) and (r['order'] == int(g['purchasesorder__pk'])):
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
        alldone = True
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
                    'virtual': True,
                }
                alldone = False

                # Add a new token
                body_requested.append(token)

        # Return answer
        answer['meta']['alldone'] = alldone
        answer['table']['body'] = body_requested + body_registered
        return answer


class DistributionLineCreate(GenCreate):
    model = DistributionLine
    form_class = DistributionLineForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__ipk = kwargs.get('ipk', None)
        return super(DistributionLineCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__ipk:
            inventory = Distribution.objects.get(pk=self.__ipk)
            operator = StorageOperator.objects.get(external__user=self.request.user)
            self.request.inventory = inventory
            form.instance.inventory = inventory
            self.request.operator = operator
            form.instance.operator = operator
        return super(DistributionLineCreate, self).form_valid(form)


class DistributionLineCreateModal(GenCreateModal, DistributionLineCreate):
    pass


class DistributionLineCreateWS(DistributionLineCreate):
    json = True

    def form_valid(self, form):
        form.instance.product_unique_value = self.request.POST.get('product_unique_value', None)
        return super(DistributionLineCreateWS, self).form_valid(form)


class DistributionLineUpdate(GenUpdate):
    model = DistributionLine
    form_class = DistributionLineForm

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(DistributionLineUpdate, self).dispatch(*args, **kwargs)


class DistributionLineUpdateModal(GenUpdateModal, DistributionLineUpdate):
    pass


class DistributionLineDelete(GenDelete):
    model = DistributionLine


class DistributionLineDetail(GenDetail):
    model = DistributionLine
    groups = DistributionLineForm.__groups_details__()

    def dispatch(self, *args, **kwargs):
        self.ipk = kwargs.get('ipk')
        return super(DistributionLineDetail, self).dispatch(*args, **kwargs)


# Inventory Incoming Stock
class GenInventoryInUrl(object):
    ws_entry_point = '{}/inventoryin'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryInList(GenInventoryInUrl, GenList):
    model = InventoryIn
    linkedit = False
    field_delete = True
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


class InventoryInNotes(GenInventoryInUrl, GenUpdate):
    model = InventoryIn
    form_class = InventoryInNotesForm
    linkdelete = False


class InventoryInNotesModal(GenUpdateModal, InventoryInNotes):
    pass


class InventoryInDelete(GenInventoryInUrl, GenDelete):
    model = InventoryIn


class InventoryInDetail(GenInventoryInUrl, GenDetail):
    model = InventoryIn
    groups = InventoryInForm.__groups_details__()


class InventoryInAlbaranar(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        # Get Inventory PK
        pk = kwargs.get('pk', None)
        inventory = InventoryIn.objects.filter(pk=pk).first()

        # Prepare answer
        answer = {}

        # Check answer
        if inventory:
            # Create Albaran
            pa = PurchasesAlbaran()
            pa.code = 'AUTO'
            pa.date = timezone.now()
            pa.provider = inventory.provider
            pa.save()
            # For each line in inventory
            for line in inventory.inventory_lines.all():
                # Find total matched products
                if line.purchaseslinealbaran.exists():
                    total_products_matched = line.purchaseslinealbaran.aggregate(total=Sum("quantity"))['total']
                else:
                    total_products_matched = 0

                # While there are elements in inventory that we must match somewhere
                while line.quantity > total_products_matched:

                    # Every block is transactional
                    with transaction.atomic():

                        # Total products left to match
                        total_products_to_match = line.quantity - total_products_matched

                        # Locate a line order to link to
                        lo = PurchasesLineOrder.objects.filter(
                            order=line.purchasesorder,
                            product=line.product_final
                        ).annotate(
                            total_albaran=Sum("line_albaran_purchases__quantity")
                        ).filter(
                            quantity__gt=F("total_albaran")
                        ).first()

                        if lo:
                            # We got a lineorder which hasn't be totally linked
                            price = lo.price
                            tax = lo.tax
                            description = lo.description
                            quantity = min(lo.quantity-lo.total_albaran, total_products_to_match)
                        else:
                            lo = PurchasesLineOrder.objects.filter(
                                order=line.purchasesorder,
                                product=line.product_final,
                                line_albaran_purchases__isnull=True
                            ).first()
                            # No lineorder found, this is an extra product
                            price = line.product_final.calculate_price()['price_base']
                            tax = line.product_final.product.tax.tax
                            description = str(line.product_final)
                            quantity = total_products_to_match

                        # Locate or create product unique
                        if line.product_unique:
                            pu = line.product_unique
                        else:
                            pu = ProductUnique()
                            pu.product_final = line.product_final
                            pu.box = line.box
                            pu.value = line.product_unique_value
                            pu.stock_original = quantity
                            pu.caducity = line.caducity
                            pu.save()

                        # Create Unique Product
                        pal = PurchasesLineAlbaran()
                        pal.albaran = pa
                        pal.line_order = lo
                        pal.validator_user = self.request.user
                        pal.quantity = quantity
                        pal.price = price
                        pal.tax = tax
                        pal.description = description
                        pal.save()
                        pal.product_unique.add(pu)
                        pal.save()
                        # Save inventory line
                        line.purchaseslinealbaran.add(pal)
                        line.save()

                    # Find total matched products
                    total_products_matched = line.purchaseslinealbaran.aggregate(total=Sum("quantity"))['total']

            # End inventory
            inventory.processed = True
            inventory.end = timezone.now()
            inventory.save()

            # Return answer
            answer['return'] = "OK"
        else:
            answer['error'] = True
            answer['errortxt'] = _("Incoming Inventory not found!")

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')


# Inventory Incoming Stock Line
class GenInventoryInLineUrl(object):
    ws_entry_point = '{}/inventorylinein'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryInLineList(GenInventoryInLineUrl, GenList):
    model = InventoryInLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryInLine'), _('InventoryInLine')]}
    defaultordering = "-created"
    linkadd = False
    linkedit = False

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
        'albaranar': _("Albaranar"),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('purchasesorder', _("Purchase Order")))
        fields.append(('purchasesorder__pk', None))
        fields.append(('box', _("Box")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_final__pk', None))
        fields.append(('product_unique', _("Unique")))
        fields.append(('product_unique_value', None))
        fields.append(('caducity', _("Caducity")))
        fields.append(('notes', _("Notes")))
        return fields

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryinline_work', kwargs={"ipk": self.ipk})[1:]
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryinline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryinline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]
        self.ws_submit = reverse('CDNX_storages_inventoryinline_addws', kwargs={"ipk": self.ipk})[1:]
        self.ws_inventoryinline_purchasesorder = reverse('CDNX_storages_inventoryinline_purchase_order', kwargs={"inventoryinline_pk": 1, "purchasesorder_pk": 1})[1:]
        self.ws_inventoryin_notesmodal = reverse('CDNX_storages_inventoryin_notesmodal', kwargs={"pk": self.ipk})[1:]
        self.ws_inventoryinline_notesmodal = reverse('CDNX_storages_inventoryinline_notesmodal', kwargs={"pk": 'INVENTORYLINE_PK'})[1:]
        self.url_inventoryin = reverse('CDNX_storages_inventoryin_list')[1:]

        # Find provider_pk
        inv = InventoryIn.objects.filter(pk=self.ipk).first()
        if inv:
            provider_pk = inv.provider.pk
        else:
            provider_pk = None

        # Prepare form
        fields = []
        fields.append((DynamicSelect, 'purchasesorder', 3, 'CDNX_invoicing_orderpurchasess_foreign', ['provider:{}'.format(provider_pk)], {
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
            'notes': inv.notes,
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
                'inventoryin_notesmodal': self.ws_inventoryin_notesmodal,
                'inventoryinline_notesmodal': self.ws_inventoryinline_notesmodal,
                'url_inventoryin': self.url_inventoryin,
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
                'codenerix-on-tab': 'product_changed(this)',
                'ng-disabled': '!(box>0 && quantity>0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-on-tab': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.unique || unique_error}',
            })+" <span class='fa fa-exclamation-triangle text-danger' ng-show='unique_error' alt='{{unique_error}}' title='{{unique_error}}'></span>",
            'form_caducity': form.fields['caducity'].widget.render('caducity', None, {
                'codenerix-on-enter': 'submit_scenario()',
                'codenerix-on-tab': 'submit_scenario()',
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
        registered = self.bodybuilder(context['object_list'], self.autorules())
        # raise IOError(registered)

        # Get purchases (requested products)
        requested = PurchasesLineOrder.objects.filter(order__pk__in=purchasesorders).values("order", "product",  "product__code", "product__ean13").annotate(total=Sum("quantity"))
        # raise IOError(requested)

        # Get already purchased products
        alreadyin = ProductUnique.objects.filter(line_albaran_purchases__line_order__order__pk__in=purchasesorders).values('product_final').annotate(total=Sum('stock_original'))

        # Recalculate quantity of requested products
        for r in requested:
            for i in alreadyin:
                if i['product_final'] == r['product']:
                    r['total'] -= i['total']
                    break

        # Process registered products
        body_registered = []
        for g in registered:
            # It is not a virtual line
            g['virtual'] = False
            # Copy quantity
            g['missing'] = float(g['quantity'])
            if g['purchasesorder__pk']:

                for r in requested:
                    if r['order'] and (r['product'] == int(g['product_final__pk'])) and (r['order'] == int(g['purchasesorder__pk'])):
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
        alldone = True
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
                    'virtual': True,
                }
                alldone = False

                # Add a new token
                body_requested.append(token)

        # Return answer
        answer['meta']['alldone'] = alldone
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


class InventoryInLineNotes(GenInventoryInLineUrl, GenUpdate):
    model = InventoryInLine
    form_class = InventoryInLineNotesForm
    linkdelete = False


class InventoryInLineNotesModal(GenUpdateModal, InventoryInLineNotes):
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
    linkedit = False
    field_delete = True
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


class InventoryOutNotes(GenInventoryInUrl, GenUpdate):
    model = InventoryOut
    form_class = InventoryOutNotesForm
    linkdelete = False


class InventoryOutNotesModal(GenUpdateModal, InventoryOutNotes):
    pass


class InventoryOutDelete(GenInventoryOutUrl, GenDelete):
    model = InventoryOut


class InventoryOutDetail(GenInventoryOutUrl, GenDetail):
    model = InventoryOut
    groups = InventoryOutForm.__groups_details__()


class InventoryOutAlbaranForeign(GenForeignKey):
    model = SalesAlbaran
    label = "{code}"

    def get_foreign(self, queryset, search, filter):
        return queryset.filter(send=True, inventorys__isnull=True).all()


class InventoryOutAlbaranar(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        # Get Inventory PK
        pk = kwargs.get('pk', None)
        inventory = InventoryOut.objects.filter(pk=pk).first()

        # Prepare answer
        answer = {}

        # Check answer
        if inventory:

            # Every block is transactional
            with transaction.atomic():

                # Create Albaran
                oa = OutgoingAlbaran()
                oa.inventory = inventory
                oa.prepare_user = self.request.user
                oa.prepare_date = timezone.now()
                oa.save()

                # For each line in inventory
                for line in inventory.inventory_lines.all():
                    # New line
                    loa = LineOutgoingAlbaran()
                    loa.outgoing_albaran = oa
                    # Locate the product unique (from product final or with product unique if defined)
                    if line.product_unique:
                        # Check if it is the same unique from the Albaran
                        pu = line.product_unique
                        # If it is not the same (exchange them)
                        # ProductUnique.objects.filter(product_final=line.product_final)
                        raise IOError(pu)
                        # Count down from Product Uniques
                        # ...
                        # Link it
                        loa.product_unique = pu
                        # Save the line
                        loa.save()
                    else:
                        # Locate a product_unique from product final
                        pus = ProductUnique.objects.filter(
                            product_final=line.product_final,
                            stock_locked__gt=0
                        )
                        # For each one found
                        left = line.quantity
                        for pu in pus:

                            # Find out our ProductUnique
                            if pu.stock_locked == left:
                                # We have exact match
                                fpu = pu
                                # We took everything we need, we are done
                                left = 0
                            elif pu.stock_locked > left:
                                # Split
                                fpu = pu.duplicate(left, locked=True)
                                # We took everything we need, we are done
                                left = 0
                            elif pu.stock_locked < left:
                                # Check if we have to split
                                if pu.stock_real > pu.stock_locked:
                                    # There are free products, we have to split
                                    fpu = pu.duplicate(pu.stock_locked, locked=True)
                                else:
                                    # We are taking everything from here
                                    fpu = pu
                                # We didn't get everything we need, keep going
                                left -= fpu.stock_locked

                            # Remove all stock from them
                            fpu.stock_real = 0
                            fpu.stock_locked = 0

                            # Link it
                            loa.product_unique = fpu

                            # Save the line
                            loa.save()

                            # If we do not have left products to link
                            if not left:
                                # We have finished
                                break

                # If we have left products to link
                if left:
                    # We couldn't do the job, there are not enought products
                    raise IOError("Not enought locked products in the storage!")

                # End inventory
                inventory.processed = True
                inventory.end = timezone.now()
                inventory.save()

            # Return answer
            answer['return'] = "OK"
        else:
            answer['error'] = True
            answer['errortxt'] = _("Outgoing Inventory not found!")

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')


# Inventory Outoging Stock Line
class GenInventoryOutLineUrl(object):
    ws_entry_point = '{}/inventoryoutline'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryOutLineList(GenInventoryOutLineUrl, GenList):
    model = InventoryOutLine
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryOutLine'), _('InventoryOutLine')]}
    defaultordering = "-created"
    linkadd = False
    linkedit = False

    def dispatch(self, *args, **kwargs):
        self.ws_entry_point = reverse('CDNX_storages_inventoryoutline_list', kwargs={"ipk": kwargs.get('ipk')})[1:]
        return super(InventoryOutLineList, self).dispatch(*args, **kwargs)


class InventoryOutLineWork(GenInventoryOutLineUrl, GenList):
    model = InventoryOutLine
    extra_context = {
        'menu': ['storage', 'inventoryout'],
        'bread': [_('Storage'), _('Outgoing Stock')],
    }
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
        'albaranar': _("Albaranar"),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('box', _("Box")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_final__pk', None))
        fields.append(('product_unique', _("Unique")))
        fields.append(('product_unique_value', None))
        fields.append(('notes', _("Notes")))
        return fields

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')
        self.ws_entry_point = reverse('CDNX_storages_inventoryoutline_work', kwargs={"ipk": self.ipk})[1:]
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryoutline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryoutline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]
        self.ws_submit = reverse('CDNX_storages_inventoryoutline_addws', kwargs={"ipk": self.ipk})[1:]
        self.ws_inventoryout_notesmodal = reverse('CDNX_storages_inventoryout_notesmodal', kwargs={"pk": self.ipk})[1:]
        self.ws_inventoryoutline_notesmodal = reverse('CDNX_storages_inventoryoutline_notesmodal', kwargs={"pk": 'INVENTORYLINE_PK'})[1:]
        self.url_inventoryout = reverse('CDNX_storages_inventoryout_list')[1:]

        # Find provider_pk
        inv = InventoryOut.objects.filter(pk=self.ipk).first()

        # Prepare form
        fields = []
        fields.append((DynamicSelect, 'box', 3, 'CDNX_storages_storageboxs_foreign', [], {}))
        fields.append((DynamicInput, 'product_final', 3, 'CDNX_products_productfinalsean13_foreign', [], {}))
        fields.append((DynamicInput, 'product_unique', 3,  'CDNX_products_productuniquescode_foreign', ['product_final'], {}))
        form = InventoryOutLineForm()
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
            'notes': inv.notes,
            'final_focus': True,
            'unique_focus': False,
            'unique_disabled': True,
            'errors': {
                'zone': None,
                'quantity': None,
                'product': None,
                'unique': None,
            },
            'ws': {
                'ean13_fullinfo': self.ws_ean13_fullinfo,
                'unique_fullinfo': self.ws_unique_fullinfo,
                'submit': self.ws_submit,
                'inventoryout_notesmodal': self.ws_inventoryout_notesmodal,
                'inventoryoutline_notesmodal': self.ws_inventoryoutline_notesmodal,
                'url_inventoryout': self.url_inventoryout,
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
                'codenerix-on-tab': 'product_changed(this)',
                'ng-disabled': '!(box>0 && quantity>0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-on-tab': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.unique || unique_error}',
            })+" <span class='fa fa-exclamation-triangle text-danger' ng-show='unique_error' alt='{{unique_error}}' title='{{unique_error}}'></span>",
        }
        return super(InventoryOutLineWork, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(inventory__pk=info.kwargs.get('ipk'))
        return limit

    def json_builder(self, answer, context):

        # List of registered products and quantity
        registered = self.bodybuilder(context['object_list'], self.autorules())
        # raise IOError(registered)
        # G: [{'pk': '1', 'caducity': None, 'product_final': 'asdf (1234)',
        #    'product_unique_value': 'asadfasdf', 'product_final__pk': '1', 'box': 'BOX1234', 'product_unique': None, 'quantity': '1.0'}]

        # Get albaran
        inventory = InventoryOut.objects.filter(pk=self.ipk).first()
        if inventory:
            albaran_pk = inventory.albaran.pk
        else:
            albaran_pk = None

        # Get purchasedproducts (requested products)
        requested = SalesLines.objects.filter(albaran__pk=albaran_pk).values("product_final",  "product_final__code", "product_final__ean13").annotate(total=Sum("quantity"))
        # raise IOError(requested)
        # R: <QuerySet [{'total': 20.0, 'product_final__code': 'aaa', 'product_final': 1, 'product_final__ean13': '1234'}]>

        # Process registered products
        body_registered = []
        for g in registered:
            # It is not a virtual line
            g['virtual'] = False
            # Copy quantity
            g['missing'] = float(g['quantity'])

            for r in requested:
                if r['product_final'] == int(g['product_final__pk']):
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
                    'product_unique_value': None,
                    'product_final': '{} ({})'.format(r['product_final__code'], r['product_final__ean13']),
                    'product_final__pk': None,
                    'product_unique': None,
                    'pk': None,
                    'quantity': r['total'],
                    'box': None,
                    'total': None,
                    'virtual': True,
                }

                # Add a new token
                body_requested.append(token)

        # Return answer
        answer['table']['body'] = body_requested + body_registered
        return answer


class InventoryOutLineCreate(GenInventoryOutLineUrl, GenCreate):
    model = InventoryOutLine
    form_class = InventoryOutLineForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__ipk = kwargs.get('ipk', None)
        return super(InventoryOutLineCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__ipk:
            # If products must be unique, make sure we get only the unique selected
            filters = {'product_final': form.instance.product_final}
            if form.instance.product_final.product.feature_special and form.instance.product_final.product.feature_special.unique:
                filters['value'] = form.instance.product_unique_value
            unique_products = ProductUnique.objects.filter(**filters)

            # If no uniques found
            if unique_products.exists() is False:
                # product unique not exixsts
                errors = form._errors.setdefault("unique", ErrorList())
                errors.append(_('Product uniques not found'))
                return super(InventoryOutLineCreate, self).form_invalid(form)
            else:
                unique_product = unique_products.filter(stock_locked__lt=form.instance.quantity).first()
                if unique_product is None:
                    # quantity error
                    errors = form._errors.setdefault("quantity", ErrorList())
                    errors.append(_('Quantity invalid'))
                    return super(InventoryOutLineCreate, self).form_invalid(form)
                else:
                    inventory = InventoryOut.objects.get(pk=self.__ipk)
                    operator = StorageOperator.objects.get(external__user=self.request.user)
                    self.request.inventory = inventory
                    form.instance.inventory = inventory
                    self.request.operator = operator
                    form.instance.operator = operator

        # Return as usually
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


class InventoryOutLineNotes(GenInventoryOutLineUrl, GenUpdate):
    model = InventoryOutLine
    form_class = InventoryOutLineNotesForm
    linkdelete = False


class InventoryOutLineNotesModal(GenUpdateModal, InventoryOutLineNotes):
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
