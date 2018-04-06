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
from django.utils.translation import ugettext_lazy as _

from codenerix.models import GenInterface, CodenerixModel
from codenerix.models_people import GenRole

from codenerix_extensions.helpers import get_external_method
from codenerix_geodata.models import GeoAddress
from codenerix_storages.settings import CDNX_STORAGE_PERMISSIONS


class Storage(GeoAddress, CodenerixModel):
    name = models.CharField(_("Storage"), max_length=80, null=False, blank=False)

    def __fields__(self, info):
        fields = super(Storage, self).__fields__(info)
        fields.insert(0, ('name', _('Storage')))
        return fields

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return self.__str__()


# zonas del almacen
class StorageZone(CodenerixModel):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='storage_zones', verbose_name=_("Storage"), null=False, blank=False)
    name = models.CharField(_("Zone"), max_length=80, null=False, blank=False)
    salable = models.BooleanField(_('Salable'), default=True)

    def __fields__(self, info):
        fields = []
        fields.append(('name', _('Zone'), 100))
        fields.append(('storage', _('Storage'), 100))
        fields.append(('salable', _('Salable'), 100))
        return fields

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return self.__str__()

    def lock_delete(self):
        if self.storage_operators.exists():
            return _("Cannot delete storage zone model, relationship between storage zone model and storage operator")
        elif self.storage_boxes_structure.exists():
            return _("Cannot delete storage zone model, relationship between storage zone model and storage box structure")
        else:
            return super(StorageZone, self).lock_delete()


class StorageBoxStructure(CodenerixModel):
    zone = models.ForeignKey(StorageZone, on_delete=models.CASCADE, related_name='storage_boxes_structure', verbose_name=_("Zone"), null=True, blank=True)
    box_structure = models.ForeignKey('StorageBoxStructure', on_delete=models.CASCADE, related_name='storage_boxes_structure', verbose_name=_("Structure box"), null=True, blank=True)
    length = models.FloatField(_('Length'), blank=True, null=True)
    width = models.FloatField(_('Width'), blank=True, null=True)
    heigth = models.FloatField(_('Heigth'), blank=True, null=True)
    # peso de las cajas y estructuras de cajas contenidas
    weight = models.FloatField(_('Weight'), blank=True, null=True)
    max_weight = models.FloatField(_('Max weight'), blank=True, null=True)
    name = models.CharField(_("Name"), max_length=80, null=False, blank=False)

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _('Zone'), 100))
        fields.append(('box_structure', _('Box structure'), 100))
        fields.append(('name', _('Name'), 100))
        fields.append(('width', _('Width')))
        fields.append(('heigth', _('Heigth')))
        fields.append(('weight', _('Weight')))
        fields.append(('max_weight', _('Max weight')))
        return fields

    def lock_delete(self):
        if self.storage_boxes_structure.exists():
            return _("Cannot delete storage zone model, related to himself")
        elif self.storage_boxes.exists():
            return _("Cannot delete storage zone model, relationship between storage structure model and storage box")
        else:
            return super(StorageBoxStructure, self).lock_delete()


class StorageBoxKind(CodenerixModel):
    length = models.FloatField(_('Length'), blank=True, null=True)
    width = models.FloatField(_('Width'), blank=True, null=True)
    heigth = models.FloatField(_('Heigth'), blank=True, null=True)
    # caja vacía
    weight = models.FloatField(_('Weight'), blank=True, null=True)
    max_weight = models.FloatField(_('Max weight'), blank=True, null=True)
    name = models.CharField(_("Name"), max_length=80, null=False, blank=False)

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('length', _('Length')))
        fields.append(('width', _('Width')))
        fields.append(('heigth', _('Heigth')))
        fields.append(('weight', _('Weight')))
        return fields

    def lock_delete(self):
        if self.storage_boxes.exists():
            return _("Cannot delete storage zone model, relationship between storage box kind model and storage box")
        else:
            return super(StorageBoxKind, self).lock_delete()


class StorageBox(CodenerixModel):
    box_structure = models.ForeignKey(StorageBoxStructure, on_delete=models.CASCADE, related_name='storage_boxes', verbose_name=_("Box Structure"), null=False, blank=False)
    box_kind = models.ForeignKey(StorageBoxKind, on_delete=models.CASCADE, related_name='storage_boxes', verbose_name=_("Box Kind"), null=False, blank=False)
    name = models.CharField(_("Name"), max_length=80, null=False, blank=False)
    # peso de los productos contenidos
    weight = models.FloatField(_('Weight'), blank=False, null=False, default=0)

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _('Name'), 100))
        fields.append(('box_structure', _('Box Structure'), 100))
        fields.append(('box_kind', _('Box Kind'), 100))
        fields.append(('weight', _('Weight'), 100))
        return fields


# ############################
class ABSTRACT_GenStorageOperator(models.Model):  # META: Abstract class

    class Meta(object):
        abstract = True


class StorageOperator(GenRole, CodenerixModel):
    class CodenerixMeta:
        abstract = ABSTRACT_GenStorageOperator
        rol_groups = {
            'StorageOperator': CDNX_STORAGE_PERMISSIONS['operator'],
        }
        rol_permissions = []
        force_methods = {
            'foreignkey_storage_operator': ('CDNX_get_fk_info_storage_operator', _('---')),
        }

    zone = models.ManyToManyField(StorageZone, related_name='storage_operators', verbose_name=_('Zones'))
    enable = models.BooleanField(_("Enable"), blank=False, null=False, default=True)

    @staticmethod
    def foreignkey_external():
        return get_external_method(StorageOperator, StorageOperator.CodenerixMeta.force_methods['foreignkey_storage_operator'][0])

    def __str__(self):
        return u"{}".format(self.pk)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _("Zones")))
        fields.append(('enable', _("Enable")))
        fields = get_external_method(StorageOperator, '__fields_storage__', info, fields)
        return fields


# puente entre los datos del almacen y 'person'
class GenStorageOperator(GenInterface, ABSTRACT_GenStorageOperator):  # META: Abstract class
    storage_operator = models.OneToOneField(StorageOperator, related_name='external', verbose_name=_("Storage operator"), null=True, on_delete=models.SET_NULL, blank=True)

    class Meta(GenInterface.Meta, ABSTRACT_GenStorageOperator.Meta):
        abstract = True

    class CodenerixMeta:
        force_methods = {
            'foreignkey_storage_operator': ('CDNX_get_fk_info_storage_operator', _('---')),
        }
