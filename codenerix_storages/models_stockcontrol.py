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

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from codenerix.models import CodenerixModel
from codenerix_products.models import ProductFinal, ProductUnique, PRODUCT_UNIQUE_VALUE_LENGTH
from codenerix_invoicing.models_purchases import Provider, PurchasesOrder, PurchasesLineAlbaran
from codenerix_invoicing.models_sales import SalesAlbaran

from .models import Storage, StorageBox, StorageOperator, StorageZone


# Generic classes for Inventory and Inventory Line
class GenInventory(CodenerixModel):  # META: Abstract class
    end = models.DateTimeField(_("Ends"), blank=True, null=True, editable=False)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    processed = models.BooleanField(_("Processed"), blank=False, null=False, default=False, editable=False)

    def lock_update(self):
        if self.processed:
            return _("This Inventory has been already processed, can not be updated")
        else:
            return None

    def lock_delete(self):
        if self.processed:
            return _("This Inventory has been already processed, can not be deleted")
        else:
            return None

    class Meta(CodenerixModel.Meta):
        abstract = True


class GenInventoryLine(CodenerixModel):  # META: Abstract class
    box = models.ForeignKey(StorageBox, on_delete=models.CASCADE, related_name='storage_%(class)s', verbose_name=_("Box"), null=False, blank=False)
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='storage_%(class)s', null=False, blank=False, verbose_name=_("Product Final"))
    product_unique = models.ForeignKey(ProductUnique, on_delete=models.CASCADE, related_name='storage_%(class)s', null=True, blank=True, verbose_name=_("Product Unique"))
    product_unique_value = models.CharField(_("Product Unique Value"), max_length=PRODUCT_UNIQUE_VALUE_LENGTH, blank=True, null=True, default=None, editable=False)
    operator = models.ForeignKey(StorageOperator, on_delete=models.CASCADE, related_name='storage_%(class)s', verbose_name=_("Storage Operator"), null=False, blank=False)
    quantity = models.FloatField(_("Quantity"), null=False, blank=False, default=1.0)
    notes = models.TextField(_("Notes"), blank=True, null=True)

    def __str__(self):
        return "{}::{}-{}-{}-{}".format(self.box, self.product_final, self.product_unique, self.product_unique_value, self.quantity)

    def lock_update(self):
        inventory = getattr(self, 'inventory', None)
        if inventory and inventory.processed:
            return _("This Inventory has been already processed, can not be updated")
        else:
            return None

    def lock_delete(self):
        inventory = getattr(self, 'inventory', None)
        if inventory and inventory.processed:
            return _("This Inventory has been already processed, can not be deleted")
        else:
            return None

    class Meta(CodenerixModel.Meta):
        abstract = True


# Inventory
class Inventory(GenInventory):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='inventorys', verbose_name=_("Storage"), null=False, blank=False)
    zone = models.ForeignKey(StorageZone, on_delete=models.CASCADE, related_name='inventorys', verbose_name=_("Zone"), null=True, blank=True)

    def __fields__(self, info):
        fields = []
        fields.append(('storage', _('Storage')))
        fields.append(('zone', _('Zone')))
        fields.append(('created', _('Starts')))
        fields.append(('end', _('Ends')))
        fields.append(('notes', _('Notes')))
        fields.append(('processed', None))
        fields.append((None, _('Actions')))
        return fields

    def __str__(self):
        if self.zone:
            return u"{} - {}:{}".format(self.created, self.storage, self.zone)
        else:
            return u"{} - {}".format(self.created, self.storage)


class InventoryLine(GenInventoryLine):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='storage_inventorys', verbose_name=_("Inventory"), null=False, blank=False)
    caducity = models.DateField(_("Caducity"), blank=True, null=True, default=None)

    def __fields__(self, info):
        fields = []
        fields.append(('box', _("Box")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        fields.append(('product_unique_value', _("Unique Value")))
        fields.append(('operator', _("Operator")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('caducity', _("Caducity")))
        fields.append(('notes', _("Notes")))
        return fields

    def __limitQ__(self, info):
        limit = {}
        ipk = info.kwargs.get('ipk', None)
        limit['file_link'] = Q(inventory__pk=ipk)
        return limit


# Distribution
class Distribution(CodenerixModel):
    purchasesorder = models.ForeignKey(PurchasesOrder, on_delete=models.CASCADE, related_name='distributions', verbose_name=_("Order"), null=True, blank=True)


class DistributionLine(CodenerixModel):
    distribution = models.ForeignKey(Distribution, on_delete=models.PROTECT, related_name='distribution_lines', verbose_name='Distribution List', blank=False, null=False)
    storage = models.ForeignKey(Storage, related_name='distribution_lines', verbose_name=_("Storage"), null=False, blank=False, on_delete=models.PROTECT)
    quantity = models.FloatField(_("Quantity"), null=False, blank=False, default=1.0)
    expected_date = models.DateTimeField(_("Desired Date"), blank=True, null=True)


# InventoryIn
class InventoryIn(GenInventory):
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name='inventorys', verbose_name=_('Provider'), blank=False, null=False)

    def __fields__(self, info):
        fields = []
        fields.append(('provider', _('Provider')))
        fields.append(('created', _('Starts')))
        fields.append(('end', _('Ends')))
        fields.append(('notes', _('Notes')))
        fields.append((None, _('Actions')))
        return fields

    def __str__(self):
        return u"{}::{}".format(self.provider, self.created)


class InventoryInLine(GenInventoryLine):
    purchasesorder = models.ForeignKey(PurchasesOrder, on_delete=models.CASCADE, related_name='inventory_lines', verbose_name=_("Order"), null=True, blank=True)
    purchaseslinealbaran = models.ManyToManyField(PurchasesLineAlbaran, related_name='inventory_lines', verbose_name=_("Line Albaran"))
    inventory = models.ForeignKey(InventoryIn, on_delete=models.CASCADE, related_name='inventory_lines', verbose_name=_("Inventory"), null=False, blank=False)
    caducity = models.DateField(_("Caducity"), blank=True, null=True, default=None)

    def __fields__(self, info):
        fields = []
        fields.append(('purchasesorder', _("Purchases Order")))
        fields.append(('purchaseslinealbaran', _("Purchases Line Albaran")))
        fields.append(('box', _("Box")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        fields.append(('product_unique_value', _("Unique Value")))
        fields.append(('operator', _("Operator")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('caducity', _("Caducity")))
        fields.append(('notes', _("Notes")))
        return fields

    def __limitQ__(self, info):
        limit = {}
        ipk = info.kwargs.get('ipk', None)
        limit['file_link'] = Q(inventory__pk=ipk)
        return limit


# InventoryOut
class InventoryOut(GenInventory):
    albaran = models.ForeignKey(SalesAlbaran, on_delete=models.PROTECT, related_name='inventorys', verbose_name=_('Albaran'), blank=False, null=False)

    def __fields__(self, info):
        fields = []
        fields.append(('albaran', _('Albaran')))
        fields.append(('created', _('Starts')))
        fields.append(('end', _('Ends')))
        fields.append(('notes', _('Notes')))
        fields.append((None, _('Actions')))
        return fields

    def __str__(self):
        return u"{}::{}".format(self.albaran, self.created)


class InventoryOutLine(GenInventoryLine):
    inventory = models.ForeignKey(InventoryOut, on_delete=models.CASCADE, related_name='inventory_lines', verbose_name=_("Inventory line"), null=False, blank=False)

    def __fields__(self, info):
        fields = []
        fields.append(('box', _("Box")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        fields.append(('product_unique_value', _("Unique Value")))
        fields.append(('operator', _("Operator")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('notes', _("Notes")))
        return fields

    def __limitQ__(self, info):
        limit = {}
        ipk = info.kwargs.get('ipk', None)
        limit['file_link'] = Q(inventory__pk=ipk)
        return limit


# Solicitud de stock entre de almacenes
class RequestStock(CodenerixModel):
    storage_source = models.ForeignKey(Storage, related_name='request_stocks_src', verbose_name=_("Storage source"), null=False, blank=False, on_delete=models.PROTECT)
    storage_destination = models.ForeignKey(Storage, related_name='request_stocks_dst', verbose_name=_("Storage destionation"), null=False, blank=False, on_delete=models.PROTECT)
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='request_stocks')
    request_date = models.DateTimeField(_("Request Date"), blank=False, null=False)
    desired_date = models.DateTimeField(_("Desired Date"), blank=False, null=False)

    def __fields__(self, info):
        fields = []
        fields.append(('batch_source', _('Batch source'), 100))
        fields.append(('batch_destination', _('Batch destination'), 100))
        fields.append(('stock_movement_products', _('Products'), 100))
        fields.append(('storage_source', _("Storage source")))
        fields.append(('storage_destination', _("Storage destionation")))
        fields.append(('request_user', _('Request user')))
        fields.append(('request_date', _("Request Date")))
        fields.append(('desired_date', _("Desired Date")))
        return fields

    def __str__(self):
        return u"{} -> {}".format(self.storage_source, self.storage_destination)

    def lock_delete(self):
        if self.line_request_stock.exists():
            return _("Cannot delete request stock model, relationship between request stock model and lines")
        if self.outgoing_albarans.exists():
            return _("Cannot delete request stock model, relationship between request stock model and outgoing albaran")
        else:
            return super(RequestStock, self).lock_delete()

    def save(self, *args, **kwargs):
        self.code_format = getattr(settings, 'CDNX_STORAGE_CODE_REQUEST_STOCK', 'RS{year}{day}{month}-{hour}{minute}--{number}')
        return super(RequestStock, self).save(*args, **kwargs)


class LineRequestStock(CodenerixModel):
    request_stock = models.ForeignKey(RequestStock, on_delete=models.CASCADE, related_name='line_request_stock', verbose_name=_("Request stock"), null=False, blank=False)
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_request_stock', verbose_name=_("Product"), null=False, blank=False)
    quantity = models.FloatField(_("Quantity"), null=False, blank=False)

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _('Product'), 100))
        fields.append(('quantity', _('Quantity'), 100))
        return fields

    def __str__(self):
        return u"{} ({})".format(self.product_final, self.quantity)


class OutgoingAlbaran(CodenerixModel):
    inventory = models.ForeignKey(InventoryOut, on_delete=models.PROTECT, related_name='outgoing_albarans', verbose_name=_('Inventory'), blank=True, null=True)
    request_stock = models.ForeignKey(RequestStock, on_delete=models.CASCADE, related_name='outgoing_albarans', verbose_name=_("Request stock"), null=True, blank=True)
    prepare_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='outgoing_albarans')
    prepare_date = models.DateTimeField(_("Prepare Date"), blank=False, null=False)
    outgoing_date = models.DateTimeField(_("Outgoing Date"), blank=True, null=True)
    estimated_date = models.DateTimeField(_("Estimated Date"), blank=True, null=True)

    def __fields__(self, info):
        fields = []
        fields.append(('request_stock', _("Request stock")))
        fields.append(('prepare_user', _('Prepare user')))
        fields.append(('prepare_date', _("Prepare Date")))
        fields.append(('outgoing_date', _("Outgoing Date")))
        fields.append(('estimated_date', _("Estimated Date")))
        return fields

    def __str__(self):
        return u"{} ({})".format(self.outgoing_date, self.request_stock)

    def lock_delete(self):
        if self.line_outgoing_albarans.exists():
            return _("Cannot delete outgoing albaran model, relationship between outgoing albaran model and lines")
        if self.incoming_albarans.exists():
            return _("Cannot delete outgoing albaran model, relationship between outgoing albaran model and incoming albaran")
        else:
            return super(OutgoingAlbaran, self).lock_delete()

    def save(self, *args, **kwargs):
        self.code_format = getattr(settings, 'CDNX_STORAGE_CODE_OUTGOING_ALBARAN', 'OA{year}{day}{month}-{hour}{minute}--{number}')
        return super(OutgoingAlbaran, self).save(*args, **kwargs)


class LineOutgoingAlbaran(CodenerixModel):
    outgoing_albaran = models.ForeignKey(OutgoingAlbaran, related_name='line_outgoing_albarans', verbose_name=_("Outgoing Albaran"), null=False, blank=False, on_delete=models.CASCADE)
    product_unique = models.ForeignKey(ProductUnique, related_name='line_outgoing_albarans', verbose_name=_("Outgoing Albaran"), null=False, blank=False, on_delete=models.CASCADE)
    # prepare_user = models.ForeignKey(User, related_name='line_outgoing_albarans_prepare', verbose_name=_("Prepare user"), blank=False, null=False, on_delete=models.CASCADE)
    validator_user = models.ForeignKey(User, related_name='line_outgoing_albarans_validator', verbose_name=_("Validator user"), blank=False, null=False, on_delete=models.CASCADE)
    # box = 1

    def __fields__(self, info):
        fields = []
        fields.append(('outgoing_albaran', _("Outgoing Albaran")))
        fields.append(('product_unique', _("Outgoing Albaran")))
        fields.append(('prepare_user', _("Prepare user")))
        fields.append(('validator_user', _("Validator user")))
        # box = 1
        return fields

    def __str__(self):
        return u"{} ({})".format(self.outgoing_albaran, self.product_unique)


class IncomingAlbaran(CodenerixModel):
    outgoing_albaran = models.ForeignKey(OutgoingAlbaran, related_name='incoming_albarans', verbose_name=_("Outgoing Albaran"), null=False, blank=False, on_delete=models.CASCADE)
    reception_user = models.ForeignKey(User, related_name='incoming_albarans', verbose_name=_("Reception user"), blank=False, null=False, on_delete=models.CASCADE)
    reception_date = models.DateTimeField(_("Reception Date"), blank=True, null=True)

    def __fields__(self, info):
        fields = []
        fields.append(('outgoing_albaran', _("Outgoing Albaran")))
        fields.append(('reception_user', _("Reception user")))
        fields.append(('reception_date', _("Reception Date")))
        return fields

    def __str__(self):
        return u"{} ({})".format(self.outgoing_albaran, self.reception_user)

    def lock_delete(self):
        if self.line_incoming_albarans.exists():
            return _("Cannot delete incoming albaran model, relationship between incoming albaran model and lines")
        else:
            return super(IncomingAlbaran, self).lock_delete()

    def save(self, *args, **kwargs):
        self.code_format = getattr(settings, 'CDNX_STORAGE_CODE_INGOING_ALBARAN', 'OI{year}{day}{month}-{hour}{minute}--{number}')
        return super(IncomingAlbaran, self).save(*args, **kwargs)


class LineIncomingAlbaran(CodenerixModel):
    incoming_albaran = models.ForeignKey(IncomingAlbaran, related_name='line_incoming_albarans', verbose_name=_("Incoming Albaran"), null=False, blank=False, on_delete=models.CASCADE)
    box = models.ForeignKey(StorageBox, related_name='line_ingoming_albarans', verbose_name=_("Box"), null=False, blank=False, on_delete=models.CASCADE)
    product_unique = models.ForeignKey(OutgoingAlbaran, related_name='line_incoming_albarans', verbose_name=_("Product"), null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.FloatField(_("Quantity"), null=False, blank=False)
    validator_user = models.ForeignKey(User, related_name='line_incoming_albarans', verbose_name=_("Validator user"), blank=False, null=False, on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = []
        fields.append(('incoming_albaran', _("Incoming Albaran")))
        fields.append(('box', _("Box")))
        fields.append(('product_unique', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('validator_user', _("Validator user")))
        return fields

    def __str__(self):
        return u"{} ({})".format(self.product_unique, self.quantity)
