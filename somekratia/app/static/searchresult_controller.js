3/**
 * Created by vihtori on 26/11/15.
 */
angular.module('myApp').controller('searchResultController', ['$scope', '$http', 'UiState', function($scope, $http, UiState) {
    $scope.uiState = UiState;
    $scope.searchText = {value: ""};
    $scope.$watch('searchResults', function(newval, oldval){
        if (typeof newval != "undefined"){
            for (var key in $scope.uiState) {
                if ($scope.uiState.hasOwnProperty(key)) {
                    $scope.uiState[key] = false;
                }
            }
            $scope.uiState.showSearchResults = true;
        }
    });
}
]);