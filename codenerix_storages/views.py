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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.conf import settings

from codenerix_extensions.views import GenCreateBridge, GenUpdateBridge
from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from codenerix_storages.models import Storage, StorageZone
from codenerix_storages.models import StorageBox
from codenerix_storages.models import StorageBoxStructure, StorageBoxKind

from codenerix_storages.forms import StorageForm
from codenerix_storages.forms import StorageZoneForm, StorageZoneOwnForm
from codenerix_storages.forms import StorageBoxForm
from codenerix_storages.forms import StorageBoxStructureForm, StorageBoxKindForm


# ###########################################
class GenStorageUrl(object):
    ws_entry_point = '{}/storages'.format(settings.CDNX_STORAGES)


# Storage
class StorageList(GenStorageUrl, GenList):
    model = Storage
    show_details = True
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('Storage'), _('Storage')]}


class StorageCreate(GenStorageUrl, GenCreate, GenCreateBridge):
    model = Storage
    form_class = StorageForm

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = Storage
        related_field = 'storage'
        error_message = [
            _("The selected entry is already a storage, select another entry!"),
            _("The selected entry is not available anymore, please, try again!")
        ]
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class StorageCreateModal(GenCreateModal, StorageCreate):
    pass


class StorageUpdate(GenStorageUrl, GenUpdate, GenUpdateBridge):
    model = Storage
    show_details = True
    form_class = StorageForm

    def get_form(self, form_class=None):
        form = super(StorageUpdate, self).get_form(form_class)
        # initial external field
        form.fields['codenerix_external_field'].initial = form.instance.external
        return form

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = Storage
        related_field = 'storage'
        error_message = [
            _("The selected entry is not available anymore, please, try again!")
        ]
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class StorageUpdateModal(GenUpdateModal, StorageUpdate):
    pass


class StorageDelete(GenStorageUrl, GenDelete):
    model = Storage


class StorageDetails(GenStorageUrl, GenDetail):
    model = Storage
    groups = StorageForm.__groups_details__()
    tabs = [
        {'id': 'Zone', 'name': _('Zones'), 'ws': 'CDNX_storages_storagezones_sublist', 'rows': 'base'},
    ]


class StorageSubList(GenStorageUrl, GenList):
    model = Storage
    show_details = False
    json = False
    extra_context = {'menu': ['Storage', 'storage'], 'bread': [_('Storage'), _('Storage')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(storage_zones__pk=pk)
        return limit


# ###########################################
class GenStorageZoneUrl(object):
    ws_entry_point = '{}/storagezones'.format(settings.CDNX_STORAGES)


# StorageZone
class StorageZoneList(GenStorageZoneUrl, GenList):
    model = StorageZone
    show_details = True
    extra_context = {'menu': ['StorageZone', 'storage'], 'bread': [_('StorageZone'), _('Storage')]}


class StorageZoneCreate(GenStorageZoneUrl, GenCreate):
    model = StorageZone
    form_class = StorageZoneForm


class StorageZoneCreateModal(GenCreateModal, StorageZoneCreate):
    pass


class OwnStorageZoneCreateModal(GenCreateModal, StorageZoneCreate):
    form_class = StorageZoneOwnForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__storage_pk = kwargs.get('pk', None)
        return super(StorageZoneCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__storage_pk:
            storage = Storage.objects.get(pk=self.__storage_pk)
            self.request.storage = storage
            form.instance.storage = storage

        return super(StorageZoneCreate, self).form_valid(form)


class StorageZoneUpdate(GenStorageZoneUrl, GenUpdate):
    model = StorageZone
    show_details = True
    form_class = StorageZoneForm


class StorageZoneUpdateModal(GenUpdateModal, StorageZoneUpdate):
    pass


class OwnStorageZoneUpdateModal(GenUpdateModal, StorageZoneUpdate):
    form_class = StorageZoneOwnForm


class StorageZoneDelete(GenStorageZoneUrl, GenDelete):
    model = StorageZone


class StorageZoneSubList(GenStorageZoneUrl, GenList):
    model = StorageZone
    field_delete = True

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(storage__pk=pk)
        return limit


class StorageZoneDetail(GenStorageZoneUrl, GenDetail):
    model = StorageZone
    groups = StorageZoneForm.__groups_details__()
    tabs = []
    exclude_fields = []


class StorageZoneDetailModal(GenDetailModal, StorageZoneDetail):
    pass


# ###########################################
class GenStorageBoxUrl(object):
    ws_entry_point = '{}/storagezones'.format(settings.CDNX_STORAGES)


# StorageBox
class StorageBoxList(GenStorageBoxUrl, GenList):
    model = StorageBox
    show_details = True
    extra_context = {'menu': ['StorageBox', 'storage'], 'bread': [_('StorageBox'), _('Storage')]}


class StorageBoxCreate(GenStorageBoxUrl, GenCreate):
    model = StorageBox
    form_class = StorageBoxForm


class StorageBoxCreateModal(GenCreateModal, StorageBoxCreate):
    pass


class StorageBoxUpdate(GenStorageBoxUrl, GenUpdate):
    model = StorageBox
    show_details = True
    form_class = StorageBoxForm


class StorageBoxUpdateModal(GenUpdateModal, StorageBoxUpdate):
    pass


class StorageBoxDelete(GenStorageBoxUrl, GenDelete):
    model = StorageBox


class StorageBoxSubList(GenStorageBoxUrl, GenList):
    model = StorageBox
    field_delete = True

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(storage__pk=pk)
        return limit


class StorageBoxDetail(GenStorageBoxUrl, GenDetail):
    model = StorageBox
    groups = StorageBoxForm.__groups_details__()
    tabs = []
    exclude_fields = []


class StorageBoxDetailModal(GenDetailModal, StorageBoxDetail):
    pass


# ###########################################
# StorageBoxStructure
class StorageBoxStructureList(GenList):
    model = StorageBoxStructure
    extra_context = {'menu': ['StorageBoxStructure', 'storage'], 'bread': [_('StorageBoxStructure'), _('Storage')]}


class StorageBoxStructureCreate(GenCreate):
    model = StorageBoxStructure
    form_class = StorageBoxStructureForm


class StorageBoxStructureCreateModal(GenCreateModal, StorageBoxStructureCreate):
    pass


class StorageBoxStructureUpdate(GenUpdate):
    model = StorageBoxStructure
    form_class = StorageBoxStructureForm


class StorageBoxStructureUpdateModal(GenUpdateModal, StorageBoxStructureUpdate):
    pass


class StorageBoxStructureDelete(GenDelete):
    model = StorageBoxStructure


class StorageBoxStructureSubList(GenList):
    model = StorageBoxStructure
    show_details = False
    extra_context = {'menu': ['StorageBoxStructure', 'storage'], 'bread': [_('StorageBoxStructure'), _('Storage')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(xxxxxxx__pk=pk)
        return limit


class StorageBoxStructureDetails(GenDetail):
    model = StorageBoxStructure
    groups = StorageBoxStructureForm.__groups_details__()


class StorageBoxStructureDetailModal(GenDetailModal, StorageBoxStructureDetails):
    pass


# ###########################################
# StorageBoxKind
class StorageBoxKindList(GenList):
    model = StorageBoxKind
    extra_context = {'menu': ['StorageBoxKind', 'storage'], 'bread': [_('StorageBoxKind'), _('Storage')]}


class StorageBoxKindCreate(GenCreate):
    model = StorageBoxKind
    form_class = StorageBoxKindForm


class StorageBoxKindCreateModal(GenCreateModal, StorageBoxKindCreate):
    pass


class StorageBoxKindUpdate(GenUpdate):
    model = StorageBoxKind
    form_class = StorageBoxKindForm


class StorageBoxKindUpdateModal(GenUpdateModal, StorageBoxKindUpdate):
    pass


class StorageBoxKindDelete(GenDelete):
    model = StorageBoxKind


class StorageBoxKindSubList(GenList):
    model = StorageBoxKind
    show_details = False
    extra_context = {'menu': ['StorageBoxKind', 'people'], 'bread': [_('StorageBoxKind'), _('People')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(xxxxxxx__pk=pk)
        return limit


class StorageBoxKindDetails(GenDetail):
    model = StorageBoxKind
    groups = StorageBoxKindForm.__groups_details__()


class StorageBoxKindDetailModal(GenDetailModal, StorageBoxKindDetails):
    pass
