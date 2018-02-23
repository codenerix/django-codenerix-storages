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

from django.contrib import admin
from codenerix_storages.models import Storage, StorageZone, StorageBoxStructure, StorageBoxKind, StorageBox, StorageOperator
from codenerix_storages.models_stockcontrol import RequestStock, LineRequestStock, OutgoingAlbaran, LineOutgoingAlbaran, IncomingAlbaran, LineIncomingAlbaran
from codenerix_storages.models_stockcontrol import Inventory, InventoryLine, InventoryIn, InventoryInLine, InventoryOut, InventoryOutLine

admin.site.register(Storage)
admin.site.register(StorageZone)
admin.site.register(StorageBoxStructure)
admin.site.register(StorageBoxKind)
admin.site.register(StorageBox)
admin.site.register(StorageOperator)

admin.site.register(RequestStock)
admin.site.register(LineRequestStock)
admin.site.register(OutgoingAlbaran)
admin.site.register(LineOutgoingAlbaran)
admin.site.register(IncomingAlbaran)
admin.site.register(LineIncomingAlbaran)
admin.site.register(Inventory)
admin.site.register(InventoryLine)
admin.site.register(InventoryIn)
admin.site.register(InventoryInLine)
admin.site.register(InventoryOut)
admin.site.register(InventoryOutLine)
