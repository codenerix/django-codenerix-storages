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
from django.conf import settings
from django.utils.translation import ugettext as _

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from codenerix_storages.models_stockcontrol import Inventory, InventoryAlbaran, InventoryAlbaranLine
from codenerix_storages.forms_stockcontrol import InventoryForm, InventoryAlbaranForm, InventoryAlbaranLineForm


# Inventory
class GenInventoryUrl(object):
    ws_entry_point = '{}/inventory'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryList(GenInventoryUrl, GenList):
    model = Inventory
    show_details = True
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('Inventory'), _('Inventory')]}
    gentrans = {
        'open': _("Open"),
        'close': _("Close"),
        'start': _("Start"),
        'end': _("End"),
    }


class InventoryCreate(GenInventoryUrl, GenCreate):
    model = Inventory
    form_class = InventoryForm


class InventoryCreateModal(GenCreateModal, InventoryCreate):
    pass


class InventoryUpdate(GenInventoryUrl, GenUpdate):
    model = Inventory
    show_details = True
    form_class = InventoryForm


class InventoryUpdateModal(GenUpdateModal, InventoryUpdate):
    pass


class InventoryDelete(GenInventoryUrl, GenDelete):
    model = Inventory


class InventoryDetail(GenInventoryUrl, GenDetail):
    model = Inventory
    groups = InventoryForm.__groups_details__()


# InventoryAlbaran
class GenInventoryAlbaranUrl(object):
    ws_entry_point = '{}/inventoryalbaran'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryAlbaranList(GenInventoryAlbaranUrl, GenList):
    model = InventoryAlbaran
    show_details = True
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryAlbaran'), _('InventoryAlbaran')]}


class InventoryAlbaranCreate(GenInventoryAlbaranUrl, GenCreate):
    model = InventoryAlbaran
    form_class = InventoryAlbaranForm


class InventoryAlbaranCreateModal(GenCreateModal, InventoryAlbaranCreate):
    pass


class InventoryAlbaranUpdate(GenInventoryAlbaranUrl, GenUpdate):
    model = InventoryAlbaran
    show_details = True
    form_class = InventoryAlbaranForm


class InventoryAlbaranUpdateModal(GenUpdateModal, InventoryAlbaranUpdate):
    pass


class InventoryAlbaranDelete(GenInventoryAlbaranUrl, GenDelete):
    model = InventoryAlbaran


class InventoryAlbaranDetail(GenInventoryAlbaranUrl, GenDetail):
    model = InventoryAlbaran
    groups = InventoryAlbaranForm.__groups_details__()
    tabs = [
        {'id': 'Products', 'name': _('Products'), 'ws': 'CDNX_storages_inventoryalbaranline_sublist', 'rows': 'base'},
    ]


# InventoryAlbaranLine
class GenInventoryAlbaranLineUrl(object):
    ws_entry_point = '{}/inventoryalbaranline'.format(settings.CDNX_STORAGES_URL_STOCKCONTROL)


class InventoryAlbaranLineList(GenInventoryAlbaranLineUrl, GenList):
    model = InventoryAlbaranLine
    show_details = True
    extra_context = {'menu': ['storage', 'storage'], 'bread': [_('InventoryAlbaranLine'), _('InventoryAlbaranLine')]}


class InventoryAlbaranLineCreate(GenInventoryAlbaranLineUrl, GenCreate):
    model = InventoryAlbaranLine
    form_class = InventoryAlbaranLineForm


class InventoryAlbaranLineCreateModal(GenCreateModal, InventoryAlbaranLineCreate):
    pass


class InventoryAlbaranLineUpdate(GenInventoryAlbaranLineUrl, GenUpdate):
    model = InventoryAlbaranLine
    show_details = True
    form_class = InventoryAlbaranLineForm


class InventoryAlbaranLineUpdateModal(GenUpdateModal, InventoryAlbaranLineUpdate):
    pass


class InventoryAlbaranLineDelete(GenInventoryAlbaranLineUrl, GenDelete):
    model = InventoryAlbaranLine


class InventoryAlbaranLineDetail(GenInventoryAlbaranLineUrl, GenDetail):
    model = InventoryAlbaranLine
    groups = InventoryAlbaranLineForm.__groups_details__()


class InventoryAlbaranLineDetailModal(GenDetailModal, InventoryAlbaranLineDetail):
    pass


class InventoryAlbaranLineSubList(GenInventoryAlbaranLineUrl, GenList):
    model = InventoryAlbaranLine
    linkadd = False
    extra_context = {'menu': ['Storage', 'storage'], 'bread': [_('Storage'), _('Storage')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(inventory_albaran__pk=pk)
        return limit
