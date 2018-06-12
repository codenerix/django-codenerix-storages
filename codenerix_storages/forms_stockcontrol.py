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

# from django.utils.translation import ugettext_lazy as _

from django import forms
from django.utils.translation import ugettext as _

from codenerix.forms import GenModelForm
from codenerix_storages.models_stockcontrol import Inventory, InventoryLine, InventoryIn, InventoryInLine, InventoryOut, InventoryOutLine, Distribution, DistributionLine, OutgoingAlbaran, LineOutgoingAlbaran


class InventoryForm(GenModelForm):

    class Meta:
        model = Inventory
        exclude = ['end', 'notes']

    def __groups__(self):
        g = []
        # (
        #     _('Details'), 12,
        #     ['name', 6],
        # ),
        return g

    @staticmethod
    def __groups_details__():
        g = []
        # (
        #    _('Details'), 12,
        #    ['name', 6],
        # ),
        return g


class InventoryNotesForm(GenModelForm):

    class Meta:
        model = Inventory
        fields = ['notes']

    def __groups__(self):
        g = [(
            _('Notes'), 12,
            ['notes', 12],
         ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class InventoryLineForm(GenModelForm):

    class Meta:
        model = InventoryLine
        exclude = ['inventory', 'operator']

    def __groups__(self):
        g = []
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class InventoryLineNotesForm(GenModelForm):

    class Meta:
        model = InventoryLine
        fields = ['notes']

    def __groups__(self):
        g = [(
            _('Notes'), 12,
            ['notes', 12],
         ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class DistributionForm(GenModelForm):

    class Meta:
        model = Distribution
        exclude = ['end']

    def __groups__(self):
        g = []
        # (
        #     _('Details'), 12,
        #     ['name', 6],
        # ),
        return g

    @staticmethod
    def __groups_details__():
        g = []
        # (
        #    _('Details'), 12,
        #    ['name', 6],
        # ),
        return g


class DistributionLineForm(GenModelForm):

    class Meta:
        model = DistributionLine
        exclude = ['distribution']

    def __groups__(self):
        g = []
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class InventoryInForm(GenModelForm):

    class Meta:
        model = InventoryIn
        exclude = ['end']

    def __groups__(self):
        g = []
        # (
        #     _('Details'), 12,
        #     ['name', 6],
        # ),
        return g

    @staticmethod
    def __groups_details__():
        g = []
        # (
        #    _('Details'), 12,
        #    ['name', 6],
        # ),
        return g


class InventoryInNotesForm(GenModelForm):

    class Meta:
        model = InventoryIn
        fields = ['notes']

    def __groups__(self):
        g = [(
            _('Notes'), 12,
            ['notes', 12],
         ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class InventoryInLineForm(GenModelForm):

    class Meta:
        model = InventoryInLine
        exclude = ['inventory', 'operator', 'purchaseslinealbaran']

    def __groups__(self):
        g = []
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity', None)
        if not quantity or quantity <= 0:
            raise forms.ValidationError("You didn't specify any quantity!")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        pf = cleaned_data.get("product_final", None)
        if pf:
            fe = pf.product.feature_special
            if fe:
                must_be_unique = bool(fe.unique)
                quantity = cleaned_data.get("quantity", None)
                if must_be_unique and quantity and quantity > 1:
                    self.add_error('quantity', _("This product must be unique, you can not add several products with the same unique code"))


class InventoryInLineNotesForm(GenModelForm):

    class Meta:
        model = InventoryInLine
        fields = ['notes']

    def __groups__(self):
        g = [(
            _('Notes'), 12,
            ['notes', 12],
         ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class InventoryOutForm(GenModelForm):

    class Meta:
        model = InventoryOut
        exclude = ['end']
        autofill = {
            'albaran': ['select', 3, 'CDNX_storages_inventoryout_albaran_foreign'],
        }

    def __groups__(self):
        g = [
         (
             _('InventoryOut'), 12,
             ['albaran', 12],
             ['notes', 12],
         ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = []
        # (
        #    _('Details'), 12,
        #    ['name', 6],
        # ),
        return g


class InventoryOutNotesForm(GenModelForm):

    class Meta:
        model = InventoryOut
        fields = ['notes']

    def __groups__(self):
        g = [(
            _('Notes'), 12,
            ['notes', 12],
         ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class InventoryOutLineForm(GenModelForm):

    class Meta:
        model = InventoryOutLine
        exclude = ['inventory', 'operator']

    def __groups__(self):
        g = []
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class InventoryOutLineNotesForm(GenModelForm):

    class Meta:
        model = InventoryOutLine
        fields = ['notes']

    def __groups__(self):
        g = [(
            _('Notes'), 12,
            ['notes', 12],
         ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = []
        return g


class OutgoingAlbaranForm(GenModelForm):

    class Meta:
        model = OutgoingAlbaran
        exclude = []

    def __groups__(self):
        g = [(
            _('Details'), 12,
            ['inventory', 2],
            ['request_stock', 2],
            ['prepare_user' , 2],
            ['prepare_date', 2],
            ['outgoing_date', 2],
            ['estimated_date', 2],
        ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [(
            _('Details'), 12,
            ['inventory', 2],
            ['request_stock', 2],
            ['prepare_user' , 2],
            ['prepare_date', 2],
            ['outgoing_date', 2],
            ['estimated_date', 2],
        ),
        ]
        return g


class LineOutgoingAlbaranForm(GenModelForm):

    class Meta:
        model = LineOutgoingAlbaran
        exclude = []

    def __groups__(self):
        g = [(
            _('Details'), 12,
            ['outgoing_albaran', 4],
            ['product_unique' , 4],
            ['validator_user', 4],
        ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [(
            _('Details'), 12,
            ['outgoing_albaran', 4],
            ['product_unique' , 4],
            ['validator_user', 4],
        ),
        ]
        return g
