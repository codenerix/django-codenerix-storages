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
from codenerix_extensions.helpers import get_external_method


# puente entre los datos del almacen y 'person'
class GenStorage(GenInterface):
    storage = models.OneToOneField("codenerix_storages.Storage", related_name='external', verbose_name=_("Storage"), null=True, on_delete=models.SET_NULL, blank=True)

    class Meta:
        abstract = True

    class CodenerixMeta:
        force_methods = {
            'foreignkey_storage': ('CDNX_get_fk_info_storage', _('---')),
        }


# puente entre los contactos del almacen y 'person'
class GenStorageContact(GenInterface):
    storage_contacts = models.OneToOneField("codenerix_storages.StorageContact", related_name='external_contact', verbose_name=_("Contact persons of storage"), null=True, on_delete=models.SET_NULL, blank=True)

    class Meta:
        abstract = True

    class CodenerixMeta:
        force_methods = {
            'foreignkey_storage': ('CDNX_get_fk_info_storage_contacts', _('---')),
        }


# almacen
class Storage(CodenerixModel):
    class CodenerixMeta:
        abstract = GenStorage

    alias = models.CharField(_("Alias"), max_length=80, null=False, blank=False)

    def __fields__(self, info):
        fields = []
        fields.append(('alias', _('Alias'), 100))
        fields = get_external_method(Storage, '__fields_storage__', info, fields)
        return fields

    @staticmethod
    def foreignkey_external():
        return get_external_method(Storage, GenStorage.CodenerixMeta.force_methods['foreignkey_storage'][0])

    def __unicode__(self):
        return u"{}".format(self.alias)

    def __str__(self):
        return self.__unicode__()

    def lock_delete(self):
        if self.storage_contacts.exists():
            return _("Cannot delete storage model, relationship between storage model and contacts")
        elif self.storage_zones.exists():
            return _("Cannot delete storage model, relationship between storage model and zones")
        else:
            return super(Storage, self).lock_delete()


# contactos del almacen
class StorageContact(CodenerixModel):
    class CodenerixMeta:
        abstract = GenStorageContact

    storage = models.ManyToManyField(Storage, related_name='storage_contacts', verbose_name=_("Storage"), null=False, blank=False)

    def __unicode__(self):
        return u"{}".format("self.storage")

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def foreignkey_external():
        return get_external_method(StorageContact, GenStorageContact.CodenerixMeta.force_methods['foreignkey_storage'][0])

    def __fields__(self, info):
        fields = []
        fields.append(('storage', _('Storages'), 100))
        fields = get_external_method(Storage, '__fields_storage_contacts__', info, fields)
        return fields


# zonas del almacen
class StorageZone(CodenerixModel):
    storage = models.ForeignKey(Storage, related_name='storage_zones', verbose_name=_("Storage"), null=False, blank=False)
    name = models.CharField(_("Zone"), max_length=80, null=False, blank=False)

    def __fields__(self, info):
        fields = []
        fields.append(('name', _('Zone'), 100))
        fields.append(('storage', _('Storage'), 100))
        return fields

    def __unicode__(self):
        return u"{}".format(self.name)

    def __str__(self):
        return self.__unicode__()

    def lock_delete(self):
        if self.storage_zones.exists():
            return _("Cannot delete storage zone model, relationship between storage zone model and bacth")
        else:
            return super(StorageZone, self).lock_delete()


# Lotes
class StorageBatch(CodenerixModel):
    zone = models.ForeignKey(StorageZone, related_name='storage_zones', verbose_name=_("Zone"), null=False, blank=False)
    ref = models.CharField(_("Reference"), max_length=80, null=False, blank=False)

    class Meta:
        verbose_name = _("Storage's Batch")
        verbose_name_plural = _("Storage's Batchs")

    def __fields__(self, info):
        fields = []
        fields.append(('ref', _('Reference'), 100))
        fields.append(('zone', _('Zone'), 100))
        fields.append(('zone__storage', _('Storage'), 100))
        return fields

    def __unicode__(self):
        return u"{}".format(self.ref)

    def __str__(self):
        return self.__unicode__()

    def delete(self, *args, **kwargs):
        try:
            return super(StorageBatch, self).delete(*args, **kwargs)
        except models.ProtectedError as e:
            raise Exception(e[0])
