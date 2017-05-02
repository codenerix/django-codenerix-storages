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

from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.conf import settings

from codenerix_extensions.views import GenCreateBridge, GenUpdateBridge
from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from codenerix_storages.models import Storage, StorageZone, StorageBatch, StorageContact
from codenerix_storages.forms import StorageForm, StorageContactForm, \
    StorageZoneForm, StorageZoneOwnForm, \
    StorageBatchForm, StorageBatchOwnForm


# ###########################################
class GenStorageUrl(object):
    ws_entry_point = '{}/storages'.format(settings.CDNX_STORAGES)


# Storage
class StorageList(GenStorageUrl, GenList):
    model = Storage
    show_details = True
    extra_context = {'menu': ['Storage', 'people'], 'bread': [_('Storage'), _('People')]}


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
    template_model = "storages/storage_details.html"
    tabs = [
        {'id': 'Zone', 'name': _('Zones'), 'ws': 'CDNX_storages_storagezones_sublist', 'rows': 'base'},
        {'id': 'Batch', 'name': _('Batches'), 'ws': 'CDNX_storages_storagebatchs_sublist', 'rows': 'base'},
        {'id': 'Contacts', 'name': _('Contacts'), 'ws': 'CDNX_storages_storagecontacts_sublist', 'rows': 'base'},
    ]


class StorageSubList(GenStorageUrl, GenList):
    model = Storage
    show_details = False
    json = False
    template_model = "storages/storage_sublist.html"
    extra_context = {'menu': ['Storage', 'people'], 'bread': [_('Storage'), _('People')]}

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
    extra_context = {'menu': ['StorageZone', 'people'], 'bread': [_('StorageZone'), _('People')]}


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
    # field_check = True
    field_delete = True

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(storage__pk=pk)
        return limit


class StorageZoneDetail(GenStorageZoneUrl, GenDetail):
    model = StorageZone
    groups = StorageZoneForm.__groups_details__()
    template_model = "storages/storagezone_details.html"
    tabs = [
        {'id': 'Batch', 'name': _('Bacthes'), 'ws': 'CDNX_storages_own_storagebatchs_sublist', 'rows': 'base'},
    ]
    exclude_fields = []


class StorageZoneDetailModal(GenDetailModal, StorageZoneDetail):
    pass


# ###########################################
class GenStorageBatchUrl(object):
    ws_entry_point = '{}/storagebatchs'.format(settings.CDNX_STORAGES)


# StorageBatch
class StorageBatchList(GenStorageBatchUrl, GenList):
    model = StorageBatch
    show_details = True
    extra_context = {'menu': ['StorageBatch', 'people'], 'bread': [_('StorageBatch'), _('People')]}


class StorageBatchCreate(GenStorageBatchUrl, GenCreate):
    model = StorageBatch
    form_class = StorageBatchForm


class StorageBatchCreateModal(GenCreateModal, StorageBatchCreate):
    pass


class StorageBatchOwnCreateModal(GenCreateModal, StorageBatchCreate):
    form_class = StorageBatchOwnForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__storage_zone_pk = kwargs.get('pk', None)
        return super(StorageBatchOwnCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__storage_zone_pk:
            zone = StorageZone.objects.get(pk=self.__storage_zone_pk)
            self.request.zone = zone
            form.instance.zone = zone

        return super(StorageBatchOwnCreateModal, self).form_valid(form)


class StorageBatchUpdate(GenStorageBatchUrl, GenUpdate):
    model = StorageBatch
    show_details = True
    form_class = StorageBatchForm


class StorageBatchUpdateModal(GenUpdateModal, StorageBatchUpdate):
    pass


class StorageBatchOwnUpdateModal(GenUpdateModal, StorageBatchUpdate):
    form_class = StorageBatchOwnForm


class StorageBatchDelete(GenStorageBatchUrl, GenDelete):
    model = StorageBatch


class StorageBatchSubList(GenStorageBatchUrl, GenList):
    model = StorageBatch
    field_delete = True

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(zone__storage__pk=pk)
        return limit

    def __searchF__(self, info):
        tf = {}
        tf['ref'] = (_('ref'), lambda x: Q(ref__icontains=x), 'input')
        return tf

    def __searchQ__(self, info, text):
        tf = {}
        tf['ref'] = Q(ref__icontains=text)
        return tf


class StorageBatchOwnSubList(GenStorageBatchUrl, GenList):
    model = StorageBatch
    field_delete = True

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(zone__pk=pk)
        return limit


class StorageBatchDetail(GenStorageBatchUrl, GenDetail):
    model = StorageBatch
    groups = StorageBatchForm.__groups_details__()
    exclude_fields = []


class StorageBatchDetailModal(GenStorageBatchUrl, GenDetailModal):
    model = StorageBatch
    groups = StorageBatchForm.__groups_details__()
    exclude_fields = []


# ###########################################
class GenStorageContactUrl(object):
    ws_entry_point = '{}/storagecontacts'.format(settings.CDNX_STORAGES)


# StorageContact
class StorageContactCreateModal(GenStorageContactUrl, GenCreateModal):
    model = StorageContact
    form_class = StorageContactForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__storage_pk = kwargs.get('pk', None)
        return super(StorageContactCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__storage_pk:
            external = form.cleaned_data['codenerix_external_field']
            storage = Storage.objects.get(pk=self.__storage_pk)
            storage_contact = StorageContact.objects.filter(external_contact=external).first()

            with transaction.atomic():
                if not storage_contact:
                    storage_contact = StorageContact()
                    storage_contact.save()
                storage_contact.storage.add(storage)
                external.storage_contacts = storage_contact
                external.save()
            self.object = storage_contact
            return HttpResponseRedirect(self.get_success_url())
        else:
            errors = form._errors.setdefault("codenerix_external_field", ErrorList())
            errors.append(_("Storage not seleted!"))
            return super(StorageContactCreateModal, self).form_invalid(form)


class StorageContactUpdateModal(GenStorageContactUrl, GenUpdateModal, GenUpdate):
    model = StorageContact
    show_details = True
    form_class = StorageContactForm


class StorageContactDelete(GenStorageContactUrl, GenDelete):
    model = StorageContact


class StorageContactSubList(GenStorageContactUrl, GenList):
    model = StorageContact
    field_delete = True

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(storage__pk=pk)
        return limit


class StorageContactDetailModal(GenStorageContactUrl, GenDetailModal):
    model = StorageContact
    groups = StorageContactForm.__groups_details__()
    template_model = "storages/storagecontact_details.html"
    exclude_fields = ['storage', ]
