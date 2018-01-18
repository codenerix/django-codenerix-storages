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
from codenerix_storages.views_stockcontrol import InventoryAlbaranList, InventoryAlbaranCreate, InventoryAlbaranCreateModal, InventoryAlbaranUpdate, InventoryAlbaranUpdateModal, InventoryAlbaranDelete, InventoryAlbaranDetail
from codenerix_storages.views_stockcontrol import InventoryAlbaranLineList, InventoryAlbaranLineCreate, InventoryAlbaranLineCreateModal, InventoryAlbaranLineUpdate, InventoryAlbaranLineUpdateModal, InventoryAlbaranLineDelete, InventoryAlbaranLineDetail, InventoryAlbaranLineSubList, InventoryAlbaranLineDetailModal

urlpatterns = [
    url(r'^inventory$', InventoryList.as_view(), name='CDNX_storages_inventory_list'),
    url(r'^inventory/add$', InventoryCreate.as_view(), name='CDNX_storages_inventory_add'),
    url(r'^inventory/addmodal$', InventoryCreateModal.as_view(), name='CDNX_storages_inventory_addmodal'),
    url(r'^inventory/(?P<pk>\w+)$', InventoryDetail.as_view(), name='CDNX_storages_inventory_details'),
    url(r'^inventory/(?P<pk>\w+)/edit$', InventoryUpdate.as_view(), name='CDNX_storages_inventory_edit'),
    url(r'^inventory/(?P<pk>\w+)/editmodal$', InventoryUpdateModal.as_view(), name='CDNX_storages_inventory_editmodal'),
    url(r'^inventory/(?P<pk>\w+)/delete$', InventoryDelete.as_view(), name='CDNX_storages_inventory_delete'),

    url(r'^inventoryalbaran$', InventoryAlbaranList.as_view(), name='CDNX_storages_inventoryalbaran_list'),
    url(r'^inventoryalbaran/add$', InventoryAlbaranCreate.as_view(), name='CDNX_storages_inventoryalbaran_add'),
    url(r'^inventoryalbaran/addmodal$', InventoryAlbaranCreateModal.as_view(), name='CDNX_storages_inventoryalbaran_addmodal'),
    url(r'^inventoryalbaran/(?P<pk>\w+)$', InventoryAlbaranDetail.as_view(), name='CDNX_storages_inventoryalbaran_details'),
    url(r'^inventoryalbaran/(?P<pk>\w+)/edit$', InventoryAlbaranUpdate.as_view(), name='CDNX_storages_inventoryalbaran_edit'),
    url(r'^inventoryalbaran/(?P<pk>\w+)/editmodal$', InventoryAlbaranUpdateModal.as_view(), name='CDNX_storages_inventoryalbaran_editmodal'),
    url(r'^inventoryalbaran/(?P<pk>\w+)/delete$', InventoryAlbaranDelete.as_view(), name='CDNX_storages_inventoryalbaran_delete'),

    url(r'^inventoryalbaranline$', InventoryAlbaranLineList.as_view(), name='CDNX_storages_inventoryalbaranline_list'),
    url(r'^inventoryalbaranline/add$', InventoryAlbaranLineCreate.as_view(), name='CDNX_storages_inventoryalbaranline_add'),
    url(r'^inventoryalbaranline/addmodal$', InventoryAlbaranLineCreateModal.as_view(), name='CDNX_storages_inventoryalbaranline_addmodal'),
    url(r'^inventoryalbaranline/(?P<pk>\w+)$', InventoryAlbaranLineDetail.as_view(), name='CDNX_storages_inventoryalbaranline_details'),
    url(r'^inventoryalbaranline/(?P<pk>\w+)/edit$', InventoryAlbaranLineUpdate.as_view(), name='CDNX_storages_inventoryalbaranline_edit'),
    url(r'^inventoryalbaranline/(?P<pk>\w+)/editmodal$', InventoryAlbaranLineUpdateModal.as_view(), name='CDNX_storages_inventoryalbaranline_editmodal'),
    url(r'^inventoryalbaranline/(?P<pk>\w+)/delete$', InventoryAlbaranLineDelete.as_view(), name='CDNX_storages_inventoryalbaranline_delete'),
    url(r'^inventoryalbaranline/(?P<pk>\w+)/sublist$', InventoryAlbaranLineSubList.as_view(), name='CDNX_storages_inventoryalbaranline_sublist'),
    url(r'^inventoryalbaranline/(?P<pk>\w+)/sublist/add$', InventoryAlbaranLineCreateModal.as_view(), name='CDNX_storages_inventoryalbaranline_sublist_add'),
    url(r'^inventoryalbaranline/(?P<pk>\w+)/sublist/addmodal$', InventoryAlbaranLineCreateModal.as_view(), name='CDNX_storages_inventoryalbaranline_sublist_addmodal'),
    url(r'^inventoryalbaranline/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', InventoryAlbaranLineDetailModal.as_view(), name='CDNX_storages_inventoryalbaranline_sublist_details'),
    url(r'^inventoryalbaranline/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', InventoryAlbaranLineUpdateModal.as_view(), name='CDNX_storages_inventoryalbaranline_sublist_edit'),
    url(r'^inventoryalbaranline/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', InventoryAlbaranLineUpdateModal.as_view(), name='CDNX_storages_inventoryalbaranline_sublist_editmodal'),
    url(r'^inventoryalbaranline/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', InventoryAlbaranLineDelete.as_view(), name='CDNX_storages_inventoryalbaranline_sublist_delete'),
]
