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

from django.conf.urls import url
from codenerix_storages.views import \
    StorageList, StorageCreate, StorageCreateModal, StorageUpdate, StorageUpdateModal, StorageDelete, StorageDetails, \
    StorageZoneList, StorageZoneCreate, StorageZoneCreateModal, StorageZoneUpdate, StorageZoneUpdateModal, StorageZoneDelete, StorageZoneSubList, StorageZoneDetail, StorageZoneDetailModal, OwnStorageZoneCreateModal, OwnStorageZoneUpdateModal, \
    StorageBatchList, StorageBatchCreate, StorageBatchCreateModal, StorageBatchOwnCreateModal, StorageBatchUpdate, StorageBatchUpdateModal, StorageBatchOwnUpdateModal, StorageBatchDelete, StorageBatchDetail, StorageBatchSubList, StorageBatchDetailModal, \
    StorageContactCreateModal, StorageContactDelete, StorageContactSubList, StorageContactDetailModal, StorageBatchOwnSubList, \
    StorageContactUpdateModal

urlpatterns = [
    url(r'^storages$', StorageList.as_view(), name='CDNX_storages_storages_list'),
    url(r'^storages/add$', StorageCreate.as_view(), name='CDNX_storages_storages_add'),
    url(r'^storages/addmodal$', StorageCreateModal.as_view(), name='CDNX_storages_storages_addmodal'),
    url(r'^storages/(?P<pk>\w+)$', StorageDetails.as_view(), name='CDNX_storages_storages_details'),
    url(r'^storages/(?P<pk>\w+)/edit$', StorageUpdate.as_view(), name='CDNX_storages_storages_edit'),
    url(r'^storages/(?P<pk>\w+)/editmodal$', StorageUpdateModal.as_view(), name='CDNX_storages_storages_editmodal'),
    url(r'^storages/(?P<pk>\w+)/delete$', StorageDelete.as_view(), name='CDNX_storages_storages_delete'),

    # StorageZone
    url(r'^storagezones$', StorageZoneList.as_view(), name='CDNX_storages_storagezones_list'),
    url(r'^storagezones/add$', StorageZoneCreate.as_view(), name='CDNX_storages_storagezones_add'),
    url(r'^storagezones/addmodal$', StorageZoneCreateModal.as_view(), name='CDNX_storages_storagezones_addmodal'),
    url(r'^storagezones/(?P<pk>\w+)$', StorageZoneDetail.as_view(), name='CDNX_storages_storagezones_detail'),
    url(r'^storagezones/(?P<pk>\w+)/edit$', StorageZoneUpdate.as_view(), name='CDNX_storages_storagezones_edit'),
    url(r'^storagezones/(?P<pk>\w+)/editmodal$', StorageZoneUpdateModal.as_view(), name='CDNX_storages_storagezones_editmodal'),
    url(r'^storagezones/(?P<pk>\w+)/delete$', StorageZoneDelete.as_view(), name='CDNX_storages_storagezones_delete'),
    url(r'^storagezones/(?P<pk>\w+)/sublist$', StorageZoneSubList.as_view(), name='CDNX_storages_storagezones_sublist'),
    url(r'^storagezones/(?P<pk>\w+)/sublist/add$', StorageZoneCreateModal.as_view(), name='CDNX_storages_storagezones_sublist_add'),
    url(r'^storagezones/(?P<pk>\w+)/sublist/addmodal$', OwnStorageZoneCreateModal.as_view(), name='CDNX_storages_storagezones_sublist_addmodal'),
    url(r'^storagezones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageZoneDetailModal.as_view(), name='CDNX_storages_storagezones_sublist_details'),
    url(r'^storagezones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageZoneUpdateModal.as_view(), name='CDNX_storages_storagezones_sublist_edit'),
    url(r'^storagezones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', OwnStorageZoneUpdateModal.as_view(), name='CDNX_storages_storagezones_sublist_editmodal'),
    url(r'^storagezones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageZoneDelete.as_view(), name='CDNX_storages_storagezones_sublist_delete'),

    # StorageBatch
    url(r'^storagebatchs$', StorageBatchList.as_view(), name='CDNX_storages_storagebatchs_list'),
    url(r'^storagebatchs/add$', StorageBatchCreate.as_view(), name='CDNX_storages_storagebatchs_add'),
    url(r'^storagebatchs/addmodal$', StorageBatchCreateModal.as_view(), name='CDNX_storages_storagebatchs_addmodal'),
    url(r'^storagebatchs/(?P<pk>\w+)$', StorageBatchDetail.as_view(), name='CDNX_storages_storagezones_detail'),
    url(r'^storagebatchs/(?P<pk>\w+)/edit$', StorageBatchUpdate.as_view(), name='CDNX_storages_storagebatchs_edit'),
    url(r'^storagebatchs/(?P<pk>\w+)/editmodal$', StorageBatchUpdateModal.as_view(), name='CDNX_storages_storagebatchs_editmodal'),
    url(r'^storagebatchs/(?P<pk>\w+)/delete$', StorageBatchDelete.as_view(), name='CDNX_storages_storagebatchs_delete'),

    url(r'^storagebatchs/(?P<pk>\w+)/sublist$', StorageBatchSubList.as_view(), name='CDNX_storages_storagebatchs_sublist'),
    url(r'^storagebatchs/(?P<pk>\w+)/sublist/add$', StorageBatchCreateModal.as_view(), name='CDNX_storages_storagebatchs_sublist_add'),
    url(r'^storagebatchs/(?P<pk>\w+)/sublist/addmodal$', StorageBatchCreateModal.as_view(), name='CDNX_storages_storagebatchs_sublist_addmodal'),
    url(r'^storagebatchs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageBatchDetailModal.as_view(), name='CDNX_storages_storagebatchs_sublist_details'),
    url(r'^storagebatchs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageBatchUpdateModal.as_view(), name='CDNX_storages_storagebatchs_sublist_edit'),
    url(r'^storagebatchs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageBatchUpdateModal.as_view(), name='CDNX_storages_storagebatchs_sublist_editmodal'),
    url(r'^storagebatchs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageBatchDelete.as_view(), name='CDNX_storages_storagebatchs_sublist_delete'),

    url(r'^storagebatchs/(?P<pk>\w+)/own/sublist$', StorageBatchOwnSubList.as_view(), name='CDNX_storages_own_storagebatchs_sublist'),
    url(r'^storagebatchs/(?P<pk>\w+)/own/sublist/add$', StorageBatchOwnCreateModal.as_view(), name='CDNX_storages_own_storagebatchs_sublist_add'),
    url(r'^storagebatchs/(?P<pk>\w+)/own/sublist/addmodal$', StorageBatchOwnCreateModal.as_view(), name='CDNX_storages_own_storagebatchs_sublist_addmodal'),
    url(r'^storagebatchs/(?P<cpk>\w+)/own/sublist/(?P<pk>\w+)/editmodal$', StorageBatchOwnUpdateModal.as_view(), name='CDNX_storages_own_storagebatchs_sublist_editmodal'),
    url(r'^storagebatchs/(?P<cpk>\w+)/own/sublist/(?P<pk>\w+)/delete$', StorageBatchDelete.as_view(), name='CDNX_storages_own_storagebatchs_sublist_delete'),

    # StorageContact
    url(r'^storagecontacts/(?P<pk>\w+)/sublist$', StorageContactSubList.as_view(), name='CDNX_storages_storagecontacts_sublist'),
    url(r'^storagecontacts/(?P<pk>\w+)/sublist/add$', StorageContactCreateModal.as_view(), name='CDNX_storages_storagecontacts_sublist_add'),
    url(r'^storagecontacts/(?P<pk>\w+)/sublist/addmodal$', StorageContactCreateModal.as_view(), name='CDNX_storages_storagecontacts_sublist_addmodal'),
    url(r'^storagecontacts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageContactDetailModal.as_view(), name='CDNX_storages_storagecontacts_sublist_details'),
    url(r'^storagecontacts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageContactUpdateModal.as_view(), name='CDNX_storages_storagecontacts_sublist_editmodal'),
    url(r'^storagecontacts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageContactDelete.as_view(), name='CDNX_storages_storagecontacts_sublist_delete'),
]
