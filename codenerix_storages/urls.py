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
from codenerix_storages.views import StorageList, StorageCreate, StorageCreateModal, StorageUpdate, StorageUpdateModal, StorageDelete, StorageDetails
from codenerix_storages.views import StorageZoneList, StorageZoneCreate, StorageZoneCreateModal, StorageZoneUpdate, StorageZoneUpdateModal, StorageZoneDelete, StorageZoneSubList, StorageZoneDetail, StorageZoneDetailModal, OwnStorageZoneCreateModal, OwnStorageZoneUpdateModal
# from codenerix_storages.views import StorageContactCreateModal, StorageContactDelete, StorageContactSubList, StorageContactDetailModal
# from codenerix_storages.views import StorageContactUpdateModal
# StorageBatchList, StorageBatchCreate, StorageBatchCreateModal, StorageBatchOwnCreateModal, StorageBatchUpdate, StorageBatchUpdateModal, StorageBatchOwnUpdateModal, StorageBatchDelete, StorageBatchDetail, StorageBatchSubList, StorageBatchDetailModal, StorageBatchOwnSubList
# from codenerix_storages.views import StorageHallList, StorageHallCreate, StorageHallCreateModal, StorageHallDetail, StorageHallUpdate, StorageHallUpdateModal, StorageHallDelete, StorageHallSubList, StorageHallDetailModal
# from codenerix_storages.views import StorageRackList, StorageRackCreate, StorageRackCreateModal, StorageRackDetail, StorageRackUpdate, StorageRackUpdateModal, StorageRackDelete, StorageRackSubList, StorageRackDetailModal
# from codenerix_storages.views import StorageShelfList, StorageShelfCreate, StorageShelfCreateModal, StorageShelfDetail, StorageShelfUpdate, StorageShelfUpdateModal, StorageShelfDelete, StorageShelfSubList, StorageShelfDetailModal
from codenerix_storages.views import StorageBoxList, StorageBoxCreate, StorageBoxCreateModal, StorageBoxDetail, StorageBoxUpdate, StorageBoxUpdateModal, StorageBoxDelete, StorageBoxSubList, StorageBoxDetailModal

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

    # StorageBox
    url(r'^storageboxs$', StorageBoxList.as_view(), name='CDNX_storages_storageboxs_list'),
    url(r'^storageboxs/add$', StorageBoxCreate.as_view(), name='CDNX_storages_storageboxs_add'),
    url(r'^storageboxs/addmodal$', StorageBoxCreateModal.as_view(), name='CDNX_storages_storageboxs_addmodal'),
    url(r'^storageboxs/(?P<pk>\w+)$', StorageBoxDetail.as_view(), name='CDNX_storages_storagezones_detail'),
    url(r'^storageboxs/(?P<pk>\w+)/edit$', StorageBoxUpdate.as_view(), name='CDNX_storages_storageboxs_edit'),
    url(r'^storageboxs/(?P<pk>\w+)/editmodal$', StorageBoxUpdateModal.as_view(), name='CDNX_storages_storageboxs_editmodal'),
    url(r'^storageboxs/(?P<pk>\w+)/delete$', StorageBoxDelete.as_view(), name='CDNX_storages_storageboxs_delete'),

    url(r'^storageboxs/(?P<pk>\w+)/sublist$', StorageBoxSubList.as_view(), name='CDNX_storages_storageboxs_sublist'),
    url(r'^storageboxs/(?P<pk>\w+)/sublist/add$', StorageBoxCreateModal.as_view(), name='CDNX_storages_storageboxs_sublist_add'),
    url(r'^storageboxs/(?P<pk>\w+)/sublist/addmodal$', StorageBoxCreateModal.as_view(), name='CDNX_storages_storageboxs_sublist_addmodal'),
    url(r'^storageboxs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageBoxDetailModal.as_view(), name='CDNX_storages_storageboxs_sublist_details'),
    url(r'^storageboxs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageBoxUpdateModal.as_view(), name='CDNX_storages_storageboxs_sublist_edit'),
    url(r'^storageboxs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageBoxUpdateModal.as_view(), name='CDNX_storages_storageboxs_sublist_editmodal'),
    url(r'^storageboxs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageBoxDelete.as_view(), name='CDNX_storages_storageboxs_sublist_delete'),
]
"""
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

    # StorageHall
    url(r'^storagehalls$', StorageHallList.as_view(), name='CDNX_storages_storagehalls_list'),
    url(r'^storagehalls/add$', StorageHallCreate.as_view(), name='CDNX_storages_storagehalls_add'),
    url(r'^storagehalls/addmodal$', StorageHallCreateModal.as_view(), name='CDNX_storages_storagehalls_addmodal'),
    url(r'^storagehalls/(?P<pk>\w+)$', StorageHallDetail.as_view(), name='CDNX_storages_storagezones_detail'),
    url(r'^storagehalls/(?P<pk>\w+)/edit$', StorageHallUpdate.as_view(), name='CDNX_storages_storagehalls_edit'),
    url(r'^storagehalls/(?P<pk>\w+)/editmodal$', StorageHallUpdateModal.as_view(), name='CDNX_storages_storagehalls_editmodal'),
    url(r'^storagehalls/(?P<pk>\w+)/delete$', StorageHallDelete.as_view(), name='CDNX_storages_storagehalls_delete'),

    url(r'^storagehalls/(?P<pk>\w+)/sublist$', StorageHallSubList.as_view(), name='CDNX_storages_storagehalls_sublist'),
    url(r'^storagehalls/(?P<pk>\w+)/sublist/add$', StorageHallCreateModal.as_view(), name='CDNX_storages_storagehalls_sublist_add'),
    url(r'^storagehalls/(?P<pk>\w+)/sublist/addmodal$', StorageHallCreateModal.as_view(), name='CDNX_storages_storagehalls_sublist_addmodal'),
    url(r'^storagehalls/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageHallDetailModal.as_view(), name='CDNX_storages_storagehalls_sublist_details'),
    url(r'^storagehalls/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageHallUpdateModal.as_view(), name='CDNX_storages_storagehalls_sublist_edit'),
    url(r'^storagehalls/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageHallUpdateModal.as_view(), name='CDNX_storages_storagehalls_sublist_editmodal'),
    url(r'^storagehalls/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageHallDelete.as_view(), name='CDNX_storages_storagehalls_sublist_delete'),

    # StorageRack
    url(r'^storageracks$', StorageRackList.as_view(), name='CDNX_storages_storageracks_list'),
    url(r'^storageracks/add$', StorageRackCreate.as_view(), name='CDNX_storages_storageracks_add'),
    url(r'^storageracks/addmodal$', StorageRackCreateModal.as_view(), name='CDNX_storages_storageracks_addmodal'),
    url(r'^storageracks/(?P<pk>\w+)$', StorageRackDetail.as_view(), name='CDNX_storages_storagezones_detail'),
    url(r'^storageracks/(?P<pk>\w+)/edit$', StorageRackUpdate.as_view(), name='CDNX_storages_storageracks_edit'),
    url(r'^storageracks/(?P<pk>\w+)/editmodal$', StorageRackUpdateModal.as_view(), name='CDNX_storages_storageracks_editmodal'),
    url(r'^storageracks/(?P<pk>\w+)/delete$', StorageRackDelete.as_view(), name='CDNX_storages_storageracks_delete'),

    url(r'^storageracks/(?P<pk>\w+)/sublist$', StorageRackSubList.as_view(), name='CDNX_storages_storageracks_sublist'),
    url(r'^storageracks/(?P<pk>\w+)/sublist/add$', StorageRackCreateModal.as_view(), name='CDNX_storages_storageracks_sublist_add'),
    url(r'^storageracks/(?P<pk>\w+)/sublist/addmodal$', StorageRackCreateModal.as_view(), name='CDNX_storages_storageracks_sublist_addmodal'),
    url(r'^storageracks/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageRackDetailModal.as_view(), name='CDNX_storages_storageracks_sublist_details'),
    url(r'^storageracks/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageRackUpdateModal.as_view(), name='CDNX_storages_storageracks_sublist_edit'),
    url(r'^storageracks/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageRackUpdateModal.as_view(), name='CDNX_storages_storageracks_sublist_editmodal'),
    url(r'^storageracks/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageRackDelete.as_view(), name='CDNX_storages_storageracks_sublist_delete'),

    # StorageShelf
    url(r'^storageshelfs$', StorageShelfList.as_view(), name='CDNX_storages_storageshelfs_list'),
    url(r'^storageshelfs/add$', StorageShelfCreate.as_view(), name='CDNX_storages_storageshelfs_add'),
    url(r'^storageshelfs/addmodal$', StorageShelfCreateModal.as_view(), name='CDNX_storages_storageshelfs_addmodal'),
    url(r'^storageshelfs/(?P<pk>\w+)$', StorageShelfDetail.as_view(), name='CDNX_storages_storagezones_detail'),
    url(r'^storageshelfs/(?P<pk>\w+)/edit$', StorageShelfUpdate.as_view(), name='CDNX_storages_storageshelfs_edit'),
    url(r'^storageshelfs/(?P<pk>\w+)/editmodal$', StorageShelfUpdateModal.as_view(), name='CDNX_storages_storageshelfs_editmodal'),
    url(r'^storageshelfs/(?P<pk>\w+)/delete$', StorageShelfDelete.as_view(), name='CDNX_storages_storageshelfs_delete'),

    url(r'^storageshelfs/(?P<pk>\w+)/sublist$', StorageShelfSubList.as_view(), name='CDNX_storages_storageshelfs_sublist'),
    url(r'^storageshelfs/(?P<pk>\w+)/sublist/add$', StorageShelfCreateModal.as_view(), name='CDNX_storages_storageshelfs_sublist_add'),
    url(r'^storageshelfs/(?P<pk>\w+)/sublist/addmodal$', StorageShelfCreateModal.as_view(), name='CDNX_storages_storageshelfs_sublist_addmodal'),
    url(r'^storageshelfs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageShelfDetailModal.as_view(), name='CDNX_storages_storageshelfs_sublist_details'),
    url(r'^storageshelfs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageShelfUpdateModal.as_view(), name='CDNX_storages_storageshelfs_sublist_edit'),
    url(r'^storageshelfs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageShelfUpdateModal.as_view(), name='CDNX_storages_storageshelfs_sublist_editmodal'),
    url(r'^storageshelfs/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageShelfDelete.as_view(), name='CDNX_storages_storageshelfs_sublist_delete'),
    
"""
