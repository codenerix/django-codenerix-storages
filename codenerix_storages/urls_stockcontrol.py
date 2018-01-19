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
from codenerix_storages.views_stockcontrol import InventoryList, InventoryCreate, InventoryCreateModal, InventoryUpdate, InventoryUpdateModal, InventoryDelete, InventoryDetail
from codenerix_storages.views_stockcontrol import InventoryLineList, InventoryLineWork, InventoryLineCreate, InventoryLineCreateModal, InventoryLineUpdate, InventoryLineUpdateModal, InventoryLineDelete, InventoryLineDetail

urlpatterns = [
    url(r'^inventory$', InventoryList.as_view(), name='CDNX_storages_inventory_list'),
    url(r'^inventory/add$', InventoryCreate.as_view(), name='CDNX_storages_inventory_add'),
    url(r'^inventory/addmodal$', InventoryCreateModal.as_view(), name='CDNX_storages_inventory_addmodal'),
    url(r'^inventory/(?P<pk>\w+)$', InventoryDetail.as_view(), name='CDNX_storages_inventory_details'),
    url(r'^inventory/(?P<pk>\w+)/edit$', InventoryUpdate.as_view(), name='CDNX_storages_inventory_edit'),
    url(r'^inventory/(?P<pk>\w+)/editmodal$', InventoryUpdateModal.as_view(), name='CDNX_storages_inventory_editmodal'),
    url(r'^inventory/(?P<pk>\w+)/delete$', InventoryDelete.as_view(), name='CDNX_storages_inventory_delete'),

    url(r'^inventoryline/(?P<ipk>\w+)$', InventoryLineList.as_view(), name='CDNX_storages_inventoryline_list'),
    url(r'^inventoryline/(?P<ipk>\w+)/work$', InventoryLineWork.as_view(), name='CDNX_storages_inventoryline_work'),
    url(r'^inventoryline/(?P<ipk>\w+)/add$', InventoryLineCreate.as_view(), name='CDNX_storages_inventoryline_add'),
    url(r'^inventoryline/(?P<ipk>\w+)/addmodal$', InventoryLineCreateModal.as_view(), name='CDNX_storages_inventoryline_addmodal'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)$', InventoryLineDetail.as_view(), name='CDNX_storages_inventoryline_details'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)/edit$', InventoryLineUpdate.as_view(), name='CDNX_storages_inventoryline_edit'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)/editmodal$', InventoryLineUpdateModal.as_view(), name='CDNX_storages_inventoryline_editmodal'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)/delete$', InventoryLineDelete.as_view(), name='CDNX_storages_inventoryline_delete'),
]
