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

from django.utils.translation import ugettext_lazy as _
from codenerix.forms import GenModelForm
from codenerix_storages.models import Storage, StorageZone
from codenerix_storages.models import StorageBox, StorageBoxStructure, StorageBoxKind


class StorageForm(GenModelForm):

    class Meta:
        model = Storage
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['name', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['name', 6],
            )
        ]
        return g


class StorageZoneForm(GenModelForm):
    class Meta:
        model = StorageZone
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['storage', 6],
                ['name', 6],
                ['salable', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['storage', 6],
                ['name', 6],
                ['salable', 6],
            )
        ]
        return g


class StorageZoneOwnForm(GenModelForm):
    class Meta:
        model = StorageZone
        exclude = ['storage', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['name', 6],
                ['salable', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['storage', 6],
                ['name', 6],
                ['salable', 6],
            )
        ]
        return g


class StorageBoxForm(GenModelForm):
    class Meta:
        model = StorageBox
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['shelf', 6],
                ['length', 6],
                ['width', 6],
                ['heigth', 6],
                ['weight', 6],
                ['alias', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['shelf', 6],
                ['length', 6],
                ['width', 6],
                ['heigth', 6],
                ['weight', 6],
                ['alias', 6],
            )
        ]
        return g


class StorageBoxStructureForm(GenModelForm):
    class Meta:
        model = StorageBoxStructure
        exclude = []
    
    def __groups__(self):
        return [
            (
                _('Details', 12),
                ['zone', 6],
                ['box_structure', 6],
                ['length', 6],
                ['width', 6],
                ['heigth', 6],
                ['weight', 6],
                ['max_weight', 6],
                ['name', 6],
            )
        ]

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['zone', 6],
                ['box_structure', 6],
                ['length', 6],
                ['width', 6],
                ['heigth', 6],
                ['weight', 6],
                ['max_weight', 6],
                ['name', 6],
            )
        ]
        return g


class StorageBoxKindForm(GenModelForm):
    class Meta:
        model = StorageBoxKind
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details', 12),
                ['length', 6],
                ['width', 6],
                ['heigth', 6],
                ['weight', 6],
                ['max_weight', 6],
                ['name', 6],
            )
        ]
        
    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details', 12),
                ['length', 6],
                ['width', 6],
                ['heigth', 6],
                ['weight', 6],
                ['max_weight', 6],
                ['name', 6],
            )
        ]
