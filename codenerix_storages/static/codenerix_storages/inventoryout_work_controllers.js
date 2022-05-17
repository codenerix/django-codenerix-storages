/*
 *
 * django-codenerix-storages
 *
 * Codenerix GNU
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
        $scope.product_final_pk = null;
        $scope.product_unique = null;
        $scope.product_unique_pk = null;
        $scope.final_error = false;
        $scope.unique_new = false;
        $scope.inscope = null;

        $scope.clean_up = function () {
            // We are done here
            $scope.final_error = false;
            $scope.unique_new = false;
            $scope.inscope.product_final = "";
            $scope.inscope.product_unique = "";
            $scope.product_final = null;
            $scope.product_final_pk = null;
            $scope.product_unique = null;
            $scope.product_unique_pk = null;
            $scope.data.meta.context.final_focus = true;
            $scope.data.meta.context.unique_disabled = true;
            $scope.data.meta.context.errors = {
                'zone': null,
                'quantity': null,
                'product': null,
                'unique': null,
            };
            $scope.refresh();
        };

        $scope.product_changed = function (inscope) {
            // Save inscope
            $scope.inscope = inscope;

            // Filter product final
            $scope.product_final = $scope.inscope.product_final.split(" ")[0];
            $scope.final_error = false;
            $scope.inscope.product_final = $scope.product_final;

            // Prepare URL
            var url = $scope.data.meta.context.ws.ean13_fullinfo;
            var eanurl = "/" + url.replace("/PRODUCT_FINAL_EAN13/", "/"+$scope.product_final+"/");

            // Query the product
            $http.get( eanurl, {}, {} )
            .success(function(answer, stat) {
                if (stat==200 || stat ==202) {
                    // Decide next step
                    if (Object.keys(answer).length) {
                        // Set unique status
                        $scope.data.meta.context.unique_disabled = !answer.unique;
                        $scope.product_final_pk = answer.pk

                        // Check for unique
                        if (answer.unique) {
                            $scope.data.meta.context.unique_focus = true;
                        } else {
                            // We are done here
                            $scope.submit_scenario();
                        }
                    } else {
                        // No answer, invalid product
                        $scope.product_final = null;
                        $scope.product_final_pk = null;
                        $scope.data.meta.context.unique_disabled = true;
                        $scope.data.meta.context.final_focus = true;
                        $scope.final_error = true;
                    }
                } else {
                    // Error happened, show an alert$
                    console.log("ERROR "+stat+": "+answer);
                    console.log(answer);
                    $scope.data.meta.context.unique_disabled = true;
                    $scope.data.meta.context.final_focus = true;
                    $scope.final_error = true;
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

        $scope.unique_changed = function () {

            // Filter product final
            var url = $scope.data.meta.context.ws.unique_fullinfo;
            $scope.product_unique = $scope.inscope.product_unique.split(" ")[0];
            $scope.inscope.product_unique = $scope.product_unique;

            // Prepare URL
            var uniqueurl = "/" + url.replace("/PRODUCT_FINAL_UNIQUE/", "/"+$scope.product_unique+"/");

            // Query the product
            $http.get( uniqueurl, {}, {} )
            .success(function(answer, stat) {
                if (stat==200 || stat ==202) {
                    if (Object.keys(answer).length) {
                        $scope.product_unique_pk = answer.pk;
                        $scope.unique_new = false;
                    } else {
                        $scope.product_unique_pk = null;
                        $scope.unique_new = true;
                    }
                    // We are done here
                    $scope.submit_scenario();
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
        }

        $scope.submit_scenario = function () {
            // Prepare URL
            var url = '/'+$scope.data.meta.context.ws.submit;

            // Prepare DATA
            var data = {
                'product_final': $scope.product_final_pk,
                'product_unique': $scope.product_unique_pk,
                'product_unique_value': $scope.product_unique,
                'box': $scope.inscope.box,
                'quantity': $scope.inscope.quantity,
            }

            $http.post( url, data, {} )
            .success(function(answer, stat) {
                angular.forEach($scope.data.meta.context.errors, function (value, key) {
                    $scope.data.meta.context.errors[key] = "";
                });
                if (stat==200 || stat ==202) {
                    if ((typeof(answer['head'])!='undefined') && (typeof(answer['head']['errors'])!='undefined')) {
                        angular.forEach(answer['head']['errors'], function (value, key) {
                            angular.forEach(value, function(error) {
                                $scope.data.meta.context.errors[key] += value+".";
                            });
                        });
                    } else {
                        // We are done here
                        $scope.clean_up();
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

        $scope.setnotes = function() {
            var url = "/" + $scope.data.meta.context.ws.inventoryout_notesmodal;
            $scope.ws= url;

            var functions = function(scope) {};
            var callback = function(scope, answer) {
                $scope.refresh();
            };

            $scope.cb_window = openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);

        };


        $scope.setlinenotes = function(row_pk) {
            if (row_pk) {
                var url = $scope.data.meta.context.ws.inventoryoutline_notesmodal;
                url = "/" + url.replace("/INVENTORYLINE_PK/", "/"+row_pk+"/");
                $scope.ws=url;

                var functions = function(scope) {};
                var callback = function(scope, answer) {
                    $scope.refresh();
                };

                $scope.cb_window = openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
            }

        };

        $scope.albaranar = function(tempurl) {

            // Prepare URL
            var url = tempurl+'/../albaranar';
            url = url.replace("inventoryoutline", "inventoryout")

            var functions = function(scope) {};
            var callback = function(scope, answer) {
                $window.location.href = "/"+$scope.data.meta.context.ws.url_inventoryin;
            };
            var callback_cancel = function(scope, answer) {
                $scope.refresh();
            };

            function action(quickmodal_ok, quickmodal_error) {
                $http.get( url, {}, {} )
                .success(function(answer, stat) {
                    if (answer.return != 'OK'){
                        quickmodal_error(answer.return);
                    } else {
                        quickmodal_ok(answer);
                    }
                })
                .error(function(data, status, headers, config) {
                    if (cnf_debug){
                        if (data) {
                            quickmodal_error(data);
                        } else {
                            quickmodal_error(cnf_debug_txt);
                        }
                    } else {
                        quickmodal_error(cnf_debug_txt);
                    }
                });
            }

            quickmodal($scope, $timeout, $uibModal, 'sm', action, functions, callback, callback_cancel);
        };

    }
]);
