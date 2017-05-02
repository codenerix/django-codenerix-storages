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

from django import forms
from django.utils.translation import ugettext_lazy as _
from codenerix.forms import GenModelForm
from codenerix_extensions.helpers import get_external_model
from codenerix_storages.models import Storage, StorageZone, StorageBatch, StorageContact


class StorageForm(GenModelForm):
    codenerix_external_field = forms.ModelChoiceField(
        label=Storage.foreignkey_external()['label'],
        queryset=get_external_model(Storage).objects.all()
    )

    class Meta:
        model = Storage
        exclude = []
        autofill = {
            'codenerix_external_field': ['select', 3, Storage.foreignkey_external()['related']],
        }

    def __groups__(self):
        g = [
           (_('Details'), 12,
                ['codenerix_external_field', 6],
                ['alias', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
           (_('Details'), 12,
                ['company', 6],
                ['alias', 6],
            )
        ]
        return g


class StorageContactForm(GenModelForm):
    codenerix_external_field = forms.ModelChoiceField(
        label=StorageContact.foreignkey_external()['label'],
        queryset=get_external_model(StorageContact).objects.all()
    )

    class Meta:
        model = StorageContact
        exclude = ['storage']
        autofill = {
            'codenerix_external_field': ['select', 3, StorageContact.foreignkey_external()['related']],
        }

    def __groups__(self):
        g = [
           (_('Details'), 12,
                ['codenerix_external_field', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
           (_('Details'), 12,
                ['external_contact', 6],
            )
        ]
        return g


class StorageZoneForm(GenModelForm):
    class Meta:
        model = StorageZone
        exclude = []

    def __groups__(self):
        g = [
           (_('Details'), 12,
                ['storage', 6],
                ['name', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
           (_('Details'), 12,
                ['storage', 6],
                ['name', 6],
            )
        ]
        return g


class StorageZoneOwnForm(GenModelForm):
    class Meta:
        model = StorageZone
        exclude = ['storage', ]

    def __groups__(self):
        g = [
           (_('Details'), 12,
                ['name', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
           (_('Details'), 12,
                ['storage', 6],
                ['name', 6],
            )
        ]
        return g


class StorageBatchForm(GenModelForm):
    class Meta:
        model = StorageBatch
        exclude = []

    def __groups__(self):
        g = [
           (_('Details'), 12,
                ['zone', 6],
                ['ref', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
           (_('Details'), 12,
                ['zone', 6],
                ['ref', 6],
            )
        ]
        return g


class StorageBatchOwnForm(GenModelForm):
    class Meta:
        model = StorageBatch
        exclude = ['zone']

    def __groups__(self):
        g = [
           (_('Details'), 12,
                ['ref', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
           (_('Details'), 12,
                ['zone', 6],
                ['ref', 6],
            )
        ]
        return g
