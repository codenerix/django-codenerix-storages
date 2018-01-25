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

        $scope.product_final = null;
        $scope.product_unique = null;
        $scope.final_error = false;

        $scope.product_changed = function (product_final_text, element, url) {

            // Filter product final
            $scope.product_final = product_final_text.split(" ")[0];
            $scope.final_error = false;
            element.product_final = $scope.product_final;

            // Prepare URL
            var eanurl = "/" + url.replace("/PRODUCT_FINAL_EAN13/", "/"+$scope.product_final+"/");

            // Query the product
            $http.get( eanurl, {}, {} )
            .success(function(answer, stat) {
                if (stat==200 || stat ==202) {
                    // Decide next step
                    if (Object.keys(answer).length) {
                        // Set caducity status
                        $scope.data.meta.context.caducity_disabled = !answer.caducable;
                        $scope.data.meta.context.unique_disabled = !answer.unique;

                        // Check for unique
                        if (answer.unique) {
                            $scope.data.meta.context.unique_focus = true;
                        } else {
                            if (answer.caducable) {
                                $scope.data.meta.context.caducity_focus = true;
                            } else {
                                // We are done here
                                element.product_final = ""
                                $scope.data.meta.context.final_focus = true;
                                $scope.data.meta.context.unique_disabled = true;
                                $scope.data.meta.context.caducity_disabled = true;
                                $scope.refresh();
                            }
                        }
                    } else {
                        // No answer, invalid product
                        $scope.data.meta.context.final_focus = true;
                        $scope.data.meta.context.unique_disabled = true;
                        $scope.data.meta.context.caducity_disabled = true;
                        $scope.final_error = true;
                    }
                } else {
                     // Error happened, show an alert$
                     console.log("ERROR "+stat+": "+answer);
                     console.log(answer);
                     alert("ERROR "+stat+": "+answer);
                }
            })
            .error(function(data, status, headers, config) {
                if (cnf_debug){
                    alert(data);
                } else {
                    alert(cnf_debug_txt)
                }
            });
        };
        $scope.unique_changed = function (product_unique_text, element, url) {

            // Filter product final
            $scope.product_unique = product_unique_text.split(" ")[0];
            element.product_unique = $scope.product_unique;

            // Prepare URL
            var uniqueurl = "/" + url.replace("/PRODUCT_FINAL_UNIQUE/", "/"+$scope.product_unique+"/");

            // Query the product
            $http.get( uniqueurl, {}, {} )
            .success(function(answer, stat) {
                if (stat==200 || stat ==202) {
                    if (Object.keys(answer).length) {
                        // Decide next step
                        if (!$scope.data.meta.context.caducity_disabled) {
                            $scope.data.meta.context.caducity_focus = true;
                        } else {
                            // We are done here
                            element.product_final = ""
                            $scope.data.meta.context.final_focus = true;
                            $scope.data.meta.context.unique_disabled = true;
                            $scope.data.meta.context.caducity_disabled = true;
                            $scope.refresh();
                        }
                    } else {
                    }
                } else {
                     // Error happened, show an alert$
                     console.log("ERROR "+stat+": "+answer);
                     console.log(answer);
                     alert("ERROR "+stat+": "+answer);
                }
            })
            .error(function(data, status, headers, config) {
                if (cnf_debug){
                    alert(data);
                } else {
                    alert(cnf_debug_txt)
                }
            });



            console.log(element);
            console.log("UNIQUE CHANGED: "+$scope.product_final+":"+product_unique);
            $scope.product_unique = product_unique;
            $scope.data.meta.context.unique_disabled = true;
            $scope.data.meta.context.unique_focus = false;
            $scope.data.meta.context.final_focus = true;
            $scope.refresh();
            return Array("", "");
        }
    }
]);
