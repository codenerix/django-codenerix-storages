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

from codenerix_storages.views_stockcontrol import InventoryList, InventoryCreate, InventoryCreateModal, InventoryUpdate, InventoryUpdateModal, InventoryDelete, InventoryDetail, InventorySetStock, InventoryNotesModal
from codenerix_storages.views_stockcontrol import InventoryLineList, InventoryLineWork, InventoryLineCreate, InventoryLineCreateWS, InventoryLineCreateModal, InventoryLineUpdate, InventoryLineUpdateModal, InventoryLineDelete, InventoryLineDetail, InventoryLineEAN13Fullinfo, InventoryLineUniqueFullinfo, InventoryLineNotesModal

from codenerix_storages.views_stockcontrol import DistributionList, DistributionCreate, DistributionCreateModal, DistributionDelete
from codenerix_storages.views_stockcontrol import DistributionLineList, DistributionLineWork, DistributionLineCreate, DistributionLineCreateWS, DistributionLineCreateModal, DistributionLineUpdate, DistributionLineUpdateModal, DistributionLineDelete, DistributionLineDetail

from codenerix_storages.views_stockcontrol import InventoryInList, InventoryInCreate, InventoryInCreateModal, InventoryInDelete, InventoryInAlbaranar, InventoryInNotesModal
from codenerix_storages.views_stockcontrol import InventoryInLineList, InventoryInLineWork, InventoryInLineCreate, InventoryInLineCreateWS, InventoryInLineCreateModal, InventoryInLineUpdate, InventoryInLineUpdateModal, InventoryInLineDelete, InventoryInLineDetail, InventoryInLineEAN13Fullinfo, InventoryInLineUniqueFullinfo, InventoryInLinePurhcaseOrder, InventoryInLineNotesModal

from codenerix_storages.views_stockcontrol import InventoryOutList, InventoryOutCreate, InventoryOutCreateModal, InventoryOutDelete, InventoryOutAlbaranForeign, InventoryOutAlbaranar, InventoryOutNotesModal
from codenerix_storages.views_stockcontrol import InventoryOutLineList, InventoryOutLineWork, InventoryOutLineCreate, InventoryOutLineCreateWS, InventoryOutLineCreateModal, InventoryOutLineUpdate, InventoryOutLineUpdateModal, InventoryOutLineDelete, InventoryOutLineDetail, InventoryOutLineEAN13Fullinfo, InventoryOutLineUniqueFullinfo, InventoryOutLineNotesModal

urlpatterns = [
    url(r'^inventory$', InventoryList.as_view(), name='CDNX_storages_inventory_list'),
    url(r'^inventory/add$', InventoryCreate.as_view(), name='CDNX_storages_inventory_add'),
    url(r'^inventory/addmodal$', InventoryCreateModal.as_view(), name='CDNX_storages_inventory_addmodal'),
    url(r'^inventory/(?P<pk>\w+)$', InventoryDetail.as_view(), name='CDNX_storages_inventory_details'),
    url(r'^inventory/(?P<pk>\w+)/edit$', InventoryUpdate.as_view(), name='CDNX_storages_inventory_edit'),
    url(r'^inventory/(?P<pk>\w+)/editmodal$', InventoryUpdateModal.as_view(), name='CDNX_storages_inventory_editmodal'),
    url(r'^inventory/(?P<pk>\w+)/delete$', InventoryDelete.as_view(), name='CDNX_storages_inventory_delete'),
    url(r'^inventory/(?P<pk>\w+)/setstock$', InventorySetStock.as_view(), name='CDNX_storages_inventory_setstock'),
    url(r'^inventory/(?P<pk>\w+)/notesmodal$', InventoryNotesModal.as_view(), name='CDNX_storages_inventory_notesmodal'),

    url(r'^inventoryline/(?P<ipk>\w+)$', InventoryLineList.as_view(), name='CDNX_storages_inventoryline_list'),
    url(r'^inventoryline/(?P<ipk>\w+)/work$', InventoryLineWork.as_view(), name='CDNX_storages_inventoryline_work'),
    url(r'^inventoryline/(?P<ipk>\w+)/work/(?P<pk>\w+)/delete$', InventoryLineDelete.as_view(), name='CDNX_storages_inventoryline_work_delete'),
    url(r'^inventoryline/(?P<ipk>\w+)/add$', InventoryLineCreate.as_view(), name='CDNX_storages_inventoryline_add'),
    url(r'^inventoryline/(?P<ipk>\w+)/addws$', InventoryLineCreateWS.as_view(), name='CDNX_storages_inventoryline_addws'),
    url(r'^inventoryline/(?P<ipk>\w+)/addmodal$', InventoryLineCreateModal.as_view(), name='CDNX_storages_inventoryline_addmodal'),
    url(r'^inventoryline/(?P<pk>\w+)/notesmodal$', InventoryLineNotesModal.as_view(), name='CDNX_storages_inventoryline_notesmodal'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)$', InventoryLineDetail.as_view(), name='CDNX_storages_inventoryline_details'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)/edit$', InventoryLineUpdate.as_view(), name='CDNX_storages_inventoryline_edit'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)/editmodal$', InventoryLineUpdateModal.as_view(), name='CDNX_storages_inventoryline_editmodal'),
    url(r'^inventoryline/(?P<ipk>\w+)/(?P<pk>\w+)/delete$', InventoryLineDelete.as_view(), name='CDNX_storages_inventoryline_delete'),
    url(r'^inventorylineean13/(?P<ean13>[a-zA-Z0-9+-_/]+)/fullinfo$', InventoryLineEAN13Fullinfo.as_view(), name='CDNX_storages_inventoryline_ean13_fullinfo'),
    url(r'^inventorylineunique/(?P<unique>[a-zA-Z0-9+-_/]+)/fullinfo$', InventoryLineUniqueFullinfo.as_view(), name='CDNX_storages_inventoryline_unique_fullinfo'),

    url(r'^distribution$', DistributionList.as_view(), name='CDNX_storages_distribution_list'),
    url(r'^distribution/add$', DistributionCreate.as_view(), name='CDNX_storages_distribution_add'),
    url(r'^distribution/addmodal$', DistributionCreateModal.as_view(), name='CDNX_storages_distribution_addmodal'),
    # url(r'^distribution/(?P<pk>\w+)$', DistributionDetail.as_view(), name='CDNX_storages_distribution_details'),
    # url(r'^distribution/(?P<pk>\w+)/edit$', DistributionUpdate.as_view(), name='CDNX_storages_distribution_edit'),
    # url(r'^distribution/(?P<pk>\w+)/editmodal$', DistributionUpdateModal.as_view(), name='CDNX_storages_distribution_editmodal'),
    url(r'^distribution/(?P<pk>\w+)/delete$', DistributionDelete.as_view(), name='CDNX_storages_distribution_delete'),

    url(r'^distributionline/(?P<ipk>\w+)$', DistributionLineList.as_view(), name='CDNX_storages_distributionline_list'),
    url(r'^distributionline/(?P<ipk>\w+)/work$', DistributionLineWork.as_view(), name='CDNX_storages_distributionline_work'),
    url(r'^distributionline/(?P<ipk>\w+)/work/(?P<pk>\w+)/delete$', DistributionLineDelete.as_view(), name='CDNX_storages_distributionline_work_delete'),
    url(r'^distributionline/(?P<ipk>\w+)/add$', DistributionLineCreate.as_view(), name='CDNX_storages_distributionline_add'),
    url(r'^distributionline/(?P<ipk>\w+)/addws$', DistributionLineCreateWS.as_view(), name='CDNX_storages_distributionline_addws'),
    url(r'^distributionline/(?P<ipk>\w+)/addmodal$', DistributionLineCreateModal.as_view(), name='CDNX_storages_distributionline_addmodal'),
    url(r'^distributionline/(?P<ipk>\w+)/(?P<pk>\w+)$', DistributionLineDetail.as_view(), name='CDNX_storages_distributionline_details'),
    url(r'^distributionline/(?P<ipk>\w+)/(?P<pk>\w+)/edit$', DistributionLineUpdate.as_view(), name='CDNX_storages_distributionline_edit'),
    url(r'^distributionline/(?P<ipk>\w+)/(?P<pk>\w+)/editmodal$', DistributionLineUpdateModal.as_view(), name='CDNX_storages_distributionline_editmodal'),
    url(r'^distributionline/(?P<ipk>\w+)/(?P<pk>\w+)/delete$', DistributionLineDelete.as_view(), name='CDNX_storages_distributionline_delete'),


    url(r'^inventoryin$', InventoryInList.as_view(), name='CDNX_storages_inventoryin_list'),
    url(r'^inventoryin/add$', InventoryInCreate.as_view(), name='CDNX_storages_inventoryin_add'),
    url(r'^inventoryin/addmodal$', InventoryInCreateModal.as_view(), name='CDNX_storages_inventoryin_addmodal'),
    url(r'^inventoryin/(?P<pk>\w+)/delete$', InventoryInDelete.as_view(), name='CDNX_storages_inventoryin_delete'),
    url(r'^inventoryin/(?P<pk>\w+)/albaranar$', InventoryInAlbaranar.as_view(), name='CDNX_storages_inventoryin_albaranar'),
    url(r'^inventoryin/(?P<pk>\w+)/notesmodal$', InventoryInNotesModal.as_view(), name='CDNX_storages_inventoryin_notesmodal'),
    # url(r'^inventoryin/(?P<pk>\w+)$', InventoryInDetail.as_view(), name='CDNX_storages_inventoryin_details'),
    # url(r'^inventoryin/(?P<pk>\w+)/edit$', InventoryInUpdate.as_view(), name='CDNX_storages_inventoryin_edit'),
    # url(r'^inventoryin/(?P<pk>\w+)/editmodal$', InventoryInUpdateModal.as_view(), name='CDNX_storages_inventoryin_editmodal'),

    url(r'^inventoryinline/(?P<ipk>\w+)$', InventoryInLineList.as_view(), name='CDNX_storages_inventoryinline_list'),
    url(r'^inventoryinline/(?P<ipk>\w+)/work$', InventoryInLineWork.as_view(), name='CDNX_storages_inventoryinline_work'),
    url(r'^inventoryinline/(?P<ipk>\w+)/work/(?P<pk>\w+)/delete$', InventoryInLineDelete.as_view(), name='CDNX_storages_inventoryinline_work_delete'),
    url(r'^inventoryinline/(?P<ipk>\w+)/add$', InventoryInLineCreate.as_view(), name='CDNX_storages_inventoryinline_add'),
    url(r'^inventoryinline/(?P<ipk>\w+)/addws$', InventoryInLineCreateWS.as_view(), name='CDNX_storages_inventoryinline_addws'),
    url(r'^inventoryinline/(?P<ipk>\w+)/addmodal$', InventoryInLineCreateModal.as_view(), name='CDNX_storages_inventoryinline_addmodal'),
    url(r'^inventoryinline/(?P<pk>\w+)/notesmodal$', InventoryInLineNotesModal.as_view(), name='CDNX_storages_inventoryinline_notesmodal'),
    url(r'^inventoryinline/(?P<ipk>\w+)/(?P<pk>\w+)$', InventoryInLineDetail.as_view(), name='CDNX_storages_inventoryinline_details'),
    url(r'^inventoryinline/(?P<ipk>\w+)/(?P<pk>\w+)/edit$', InventoryInLineUpdate.as_view(), name='CDNX_storages_inventoryinline_edit'),
    url(r'^inventoryinline/(?P<ipk>\w+)/(?P<pk>\w+)/editmodal$', InventoryInLineUpdateModal.as_view(), name='CDNX_storages_inventoryinline_editmodal'),
    url(r'^inventoryinline/(?P<ipk>\w+)/(?P<pk>\w+)/delete$', InventoryInLineDelete.as_view(), name='CDNX_storages_inventoryinline_delete'),
    url(r'^inventoryinlineean13/(?P<ean13>[a-zA-Z0-9+-_/]+)/fullinfo$', InventoryInLineEAN13Fullinfo.as_view(), name='CDNX_storages_inventoryinline_ean13_fullinfo'),
    url(r'^inventoryinlineunique/(?P<unique>[a-zA-Z0-9+-_/]+)/fullinfo$', InventoryInLineUniqueFullinfo.as_view(), name='CDNX_storages_inventoryinline_unique_fullinfo'),
    url(r'^inventoryinlinepurchaseorder/(?P<inventoryinline_pk>\w+)/(?P<purchasesorder_pk>\w+)$', InventoryInLinePurhcaseOrder.as_view(), name='CDNX_storages_inventoryinline_purchase_order'),

    url(r'^inventoryout$', InventoryOutList.as_view(), name='CDNX_storages_inventoryout_list'),
    url(r'^inventoryout/add$', InventoryOutCreate.as_view(), name='CDNX_storages_inventoryout_add'),
    url(r'^inventoryout/addmodal$', InventoryOutCreateModal.as_view(), name='CDNX_storages_inventoryout_addmodal'),
    url(r'^inventoryout/albaran/(?P<search>[\w\W]+|\*)$', InventoryOutAlbaranForeign.as_view(), name='CDNX_storages_inventoryout_albaran_foreign'),
    url(r'^inventoryout/(?P<pk>\w+)/delete$', InventoryOutDelete.as_view(), name='CDNX_storages_inventoryout_delete'),
    url(r'^inventoryout/(?P<pk>\w+)/albaranar', InventoryOutAlbaranar.as_view(), name='CDNX_storages_inventoryout_albaranar'),
    url(r'^inventoryout/(?P<pk>\w+)/notesmodal$', InventoryOutNotesModal.as_view(), name='CDNX_storages_inventoryout_notesmodal'),
    # url(r'^inventoryout/(?P<pk>\w+)$', InventoryOutDetail.as_view(), name='CDNX_storages_inventoryout_details'),
    # url(r'^inventoryout/(?P<pk>\w+)/edit$', InventoryOutUpdate.as_view(), name='CDNX_storages_inventoryout_edit'),
    # url(r'^inventoryout/(?P<pk>\w+)/editmodal$', InventoryOutUpdateModal.as_view(), name='CDNX_storages_inventoryout_editmodal'),

    url(r'^inventoryoutline/(?P<ipk>\w+)$', InventoryOutLineList.as_view(), name='CDNX_storages_inventoryoutline_list'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/work$', InventoryOutLineWork.as_view(), name='CDNX_storages_inventoryoutline_work'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/work/(?P<pk>\w+)/delete$', InventoryOutLineDelete.as_view(), name='CDNX_storages_inventoryoutline_work_delete'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/add$', InventoryOutLineCreate.as_view(), name='CDNX_storages_inventoryoutline_add'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/addws$', InventoryOutLineCreateWS.as_view(), name='CDNX_storages_inventoryoutline_addws'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/addmodal$', InventoryOutLineCreateModal.as_view(), name='CDNX_storages_inventoryoutline_addmodal'),
    url(r'^inventoryoutline/(?P<pk>\w+)/notesmodal$', InventoryOutLineNotesModal.as_view(), name='CDNX_storages_inventoryoutline_notesmodal'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/(?P<pk>\w+)$', InventoryOutLineDetail.as_view(), name='CDNX_storages_inventoryoutline_details'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/(?P<pk>\w+)/edit$', InventoryOutLineUpdate.as_view(), name='CDNX_storages_inventoryoutline_edit'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/(?P<pk>\w+)/editmodal$', InventoryOutLineUpdateModal.as_view(), name='CDNX_storages_inventoryoutline_editmodal'),
    url(r'^inventoryoutline/(?P<ipk>\w+)/(?P<pk>\w+)/delete$', InventoryOutLineDelete.as_view(), name='CDNX_storages_inventoryoutline_delete'),
    url(r'^inventoryoutlineean13/(?P<ean13>[a-zA-Z0-9+-_/]+)/fullinfo$', InventoryOutLineEAN13Fullinfo.as_view(), name='CDNX_storages_inventoryoutline_ean13_fullinfo'),
    url(r'^inventoryoutlineunique/(?P<unique>[a-zA-Z0-9+-_/]+)/fullinfo$', InventoryOutLineUniqueFullinfo.as_view(), name='CDNX_storages_inventoryoutline_unique_fullinfo'),
]
