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
from codenerix.widgets import MultiStaticSelect
from codenerix_extensions.helpers import get_external_model
from codenerix_storages.models import Storage, StorageZone
from codenerix_storages.models import StorageBox, StorageBoxStructure, StorageBoxKind, StorageOperator


class StorageForm(GenModelForm):

    class Meta:
        model = Storage
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['name', 6],
            ),
            (
                _('Address'), 12,
                ['country', 3],
                ['region', 3],
                ['province', 3],
                ['city', 3],
                ['town', 9],
                ['zipcode', 3],
                ['address', 9],
                ['phone', 3],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['name', 6],
            ),
            (
                _('Address'), 12,
                ['country', 3],
                ['region', 3],
                ['province', 3],
                ['city', 3],
                ['town', 9],
                ['zipcode', 3],
                ['address', 9],
                ['phone', 3],
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
        exclude = ['weight', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['box_structure', 6],
                ['box_kind', 6],
                ['name', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['box_structure', 6],
                ['box_kind', 6],
                ['name', 6],
                ['weight', 6],
            )
        ]
        return g


class StorageBoxFormUpdate(GenModelForm):
    class Meta:
        model = StorageBox
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['box_structure', 6],
                ['box_kind', 6],
                ['name', 6],
                ['weight', 6, {'extra': ['ng-disabled=true']}],
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
                _('Details'), 12,
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
                _('Details'), 12,
                ['length', 6],
                ['width', 6],
                ['heigth', 6],
                ['weight', 6],
                ['max_weight', 6],
                ['name', 6],
            )
        ]


class StorageOperatorForm(GenModelForm):
    codenerix_external_field = forms.ModelChoiceField(
        label=StorageOperator.foreignkey_external()['label'],
        queryset=get_external_model(StorageOperator).objects.all()
    )
    zone = forms.ModelMultipleChoiceField(
        queryset=StorageZone.objects.all().order_by('name'),
        label=_('Zones'),
        required=False,
        widget=MultiStaticSelect(
            attrs={'manytomany': True, }
        )
    )

    password1 = forms.CharField(label=_("Pin for storage software"), min_length=4, widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label=_("Confirm pin"), min_length=4, widget=forms.PasswordInput, required=False)

    class Meta:
        model = StorageOperator
        exclude = []
        autofill = {
            'codenerix_external_field': ['select', 3, StorageOperator.foreignkey_external()['related']],
        }

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['codenerix_external_field', 6],
                ['zone', 4],
                ['enable', 2],
                ['password1', 6],
                ['password2', 6],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['codenerix_external_field', 6],
                ['zone', 4],
                ['enable', 2],
            )
        ]

    def clean(self):
        cleaned_data = super(StorageOperatorForm, self).clean()

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            del cleaned_data['password1']
            del cleaned_data['password2']
            raise forms.ValidationError(_("Passwords do not match"))
