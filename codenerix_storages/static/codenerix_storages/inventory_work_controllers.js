/*
 *
 * django-codenerix-storages
 *
 * Copyright 2017 Centrologic Computational Logistic Center S.L.
 *
 * Project URL : http://www.codenerix.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

// Angular codenerix Controllers
angular.module('codenerixSTORAGESControllers', [])

.controller('CDNXSTORAGESInventoryWorkCtrl', ['$scope', '$rootScope', '$timeout', '$location', '$uibModal', '$templateCache', '$http', '$state', 'Register', 'ListMemory',
    function($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        multilist($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, 0, "/"+ws_entry_point);

        $scope.product_changed = function (product_final) {
            console.log("PRODUCT CHANGED: "+product_final);
            if (product_final == 'hola') {
                $scope.data.meta.context.unique_disabled = true;
                $scope.data.meta.context.unique_focus = false;
                $scope.data.meta.context.final_focus = true;
                $scope.refresh();
                return '';
            } else {
                $scope.data.meta.context.unique_disabled = false;
                $scope.data.meta.context.unique_focus = true;
                $scope.data.meta.context.final_focus = false;
                return product_final;
            }
        };
        $scope.unique_changed = function (product_final, product_unique) {
            console.log("UNIQUE CHANGED: "+product_final+":"+product_unique);
            $scope.data.meta.context.unique_disabled = true;
            $scope.data.meta.context.unique_focus = false;
            $scope.data.meta.context.final_focus = true;
            $scope.refresh();
            return Array("", "");
        }
    }
]);
