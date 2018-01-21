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
from codenerix_storages.views import StorageBoxList, StorageBoxCreate, StorageBoxCreateModal, StorageBoxDetail, StorageBoxUpdate, StorageBoxUpdateModal, StorageBoxDelete, StorageBoxSubList, StorageBoxDetailModal, StorageBoxForeign
from codenerix_storages.views import StorageBoxStructureList, StorageBoxStructureCreate, StorageBoxStructureCreateModal, StorageBoxStructureUpdate, StorageBoxStructureUpdateModal, StorageBoxStructureDelete, StorageBoxStructureSubList, StorageBoxStructureDetails, StorageBoxStructureDetailModal
from codenerix_storages.views import StorageBoxKindList, StorageBoxKindCreate, StorageBoxKindCreateModal, StorageBoxKindUpdate, StorageBoxKindUpdateModal, StorageBoxKindDelete, StorageBoxKindSubList, StorageBoxKindDetails, StorageBoxKindDetailModal
from codenerix_storages.views import StorageOperatorList, StorageOperatorCreate, StorageOperatorCreateModal, StorageOperatorUpdate, StorageOperatorUpdateModal, StorageOperatorDelete, StorageOperatorSubList, StorageOperatorDetails, StorageOperatorDetailModal

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
    url(r'^storageboxs/foreign/(?P<search>[\w\W]+|\*)$', StorageBoxForeign.as_view(), name='CDNX_storages_storageboxs_foreign'),
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

    # StorageBoxStructure
    url(r'^storageboxstructures$', StorageBoxStructureList.as_view(), name='CDNX_storages_storageboxstructures_list'),
    url(r'^storageboxstructures/add$', StorageBoxStructureCreate.as_view(), name='CDNX_storages_storageboxstructures_add'),
    url(r'^storageboxstructures/addmodal$', StorageBoxStructureCreateModal.as_view(), name='CDNX_storages_storageboxstructures_addmodal'),
    url(r'^storageboxstructures/(?P<pk>\w+)$', StorageBoxStructureDetails.as_view(), name='CDNX_storages_storageboxstructures_details'),
    url(r'^storageboxstructures/(?P<pk>\w+)/edit$', StorageBoxStructureUpdate.as_view(), name='CDNX_storages_storageboxstructures_edit'),
    url(r'^storageboxstructures/(?P<pk>\w+)/editmodal$', StorageBoxStructureUpdateModal.as_view(), name='CDNX_storages_storageboxstructures_editmodal'),
    url(r'^storageboxstructures/(?P<pk>\w+)/delete$', StorageBoxStructureDelete.as_view(), name='CDNX_storages_storageboxstructures_delete'),
    url(r'^storageboxstructures/(?P<pk>\w+)/sublist$', StorageBoxStructureSubList.as_view(), name='CDNX_storages_storageboxstructures_sublist'),
    url(r'^storageboxstructures/(?P<pk>\w+)/sublist/add$', StorageBoxStructureCreateModal.as_view(), name='CDNX_storages_storageboxstructures_sublist_add'),
    url(r'^storageboxstructures/(?P<pk>\w+)/sublist/addmodal$', StorageBoxStructureCreateModal.as_view(), name='CDNX_storages_storageboxstructures_sublist_addmodal'),
    url(r'^storageboxstructures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageBoxStructureDetailModal.as_view(), name='CDNX_storages_storageboxstructures_sublist_details'),
    url(r'^storageboxstructures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageBoxStructureUpdateModal.as_view(), name='CDNX_storages_storageboxstructures_sublist_edit'),
    url(r'^storageboxstructures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageBoxStructureUpdateModal.as_view(), name='CDNX_storages_storageboxstructures_sublist_editmodal'),
    url(r'^storageboxstructures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageBoxStructureDelete.as_view(), name='CDNX_storages_storageboxstructures_sublist_delete'),

    # StorageBoxKind
    url(r'^storageboxkinds$', StorageBoxKindList.as_view(), name='CDNX_storages_storageboxkinds_list'),
    url(r'^storageboxkinds/add$', StorageBoxKindCreate.as_view(), name='CDNX_storages_storageboxkinds_add'),
    url(r'^storageboxkinds/addmodal$', StorageBoxKindCreateModal.as_view(), name='CDNX_storages_storageboxkinds_addmodal'),
    url(r'^storageboxkinds/(?P<pk>\w+)$', StorageBoxKindDetails.as_view(), name='CDNX_storages_storageboxkinds_details'),
    url(r'^storageboxkinds/(?P<pk>\w+)/edit$', StorageBoxKindUpdate.as_view(), name='CDNX_storages_storageboxkinds_edit'),
    url(r'^storageboxkinds/(?P<pk>\w+)/editmodal$', StorageBoxKindUpdateModal.as_view(), name='CDNX_storages_storageboxkinds_editmodal'),
    url(r'^storageboxkinds/(?P<pk>\w+)/delete$', StorageBoxKindDelete.as_view(), name='CDNX_storages_storageboxkinds_delete'),
    url(r'^storageboxkinds/(?P<pk>\w+)/sublist$', StorageBoxKindSubList.as_view(), name='CDNX_storages_storageboxkinds_sublist'),
    url(r'^storageboxkinds/(?P<pk>\w+)/sublist/add$', StorageBoxKindCreateModal.as_view(), name='CDNX_storages_storageboxkinds_sublist_add'),
    url(r'^storageboxkinds/(?P<pk>\w+)/sublist/addmodal$', StorageBoxKindCreateModal.as_view(), name='CDNX_storages_storageboxkinds_sublist_addmodal'),
    url(r'^storageboxkinds/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageBoxKindDetailModal.as_view(), name='CDNX_storages_storageboxkinds_sublist_details'),
    url(r'^storageboxkinds/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageBoxKindUpdateModal.as_view(), name='CDNX_storages_storageboxkinds_sublist_edit'),
    url(r'^storageboxkinds/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageBoxKindUpdateModal.as_view(), name='CDNX_storages_storageboxkinds_sublist_editmodal'),
    url(r'^storageboxkinds/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageBoxKindDelete.as_view(), name='CDNX_storages_storageboxkinds_sublist_delete'),

    url(r'^storageoperators$', StorageOperatorList.as_view(), name='CDNX_storages_storageoperators_list'),
    url(r'^storageoperators/add$', StorageOperatorCreate.as_view(), name='CDNX_storages_storageoperators_add'),
    url(r'^storageoperators/addmodal$', StorageOperatorCreateModal.as_view(), name='CDNX_storages_storageoperators_addmodal'),
    url(r'^storageoperators/(?P<pk>\w+)$', StorageOperatorDetails.as_view(), name='CDNX_storages_storageoperators_details'),
    url(r'^storageoperators/(?P<pk>\w+)/edit$', StorageOperatorUpdate.as_view(), name='CDNX_storages_storageoperators_edit'),
    url(r'^storageoperators/(?P<pk>\w+)/editmodal$', StorageOperatorUpdateModal.as_view(), name='CDNX_storages_storageoperators_editmodal'),
    url(r'^storageoperators/(?P<pk>\w+)/delete$', StorageOperatorDelete.as_view(), name='CDNX_storages_storageoperators_delete'),
    url(r'^storageoperators/(?P<pk>\w+)/sublist$', StorageOperatorSubList.as_view(), name='CDNX_storages_storageoperators_sublist'),
    url(r'^storageoperators/(?P<pk>\w+)/sublist/add$', StorageOperatorCreateModal.as_view(), name='CDNX_storages_storageoperators_sublist_add'),
    url(r'^storageoperators/(?P<pk>\w+)/sublist/addmodal$', StorageOperatorCreateModal.as_view(), name='CDNX_storages_storageoperators_sublist_addmodal'),
    url(r'^storageoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StorageOperatorDetailModal.as_view(), name='CDNX_storages_storageoperators_sublist_details'),
    url(r'^storageoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', StorageOperatorUpdateModal.as_view(), name='CDNX_storages_storageoperators_sublist_edit'),
    url(r'^storageoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StorageOperatorUpdateModal.as_view(), name='CDNX_storages_storageoperators_sublist_editmodal'),
    url(r'^storageoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StorageOperatorDelete.as_view(), name='CDNX_storages_storageoperators_sublist_delete'),


]
