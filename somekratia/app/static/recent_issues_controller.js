/**
 * Created by tiitulahti on 23/12/15.
 */

angular.module('myApp').controller('recentIssuesController', ['$scope', '$http','UiState', function($scope, $http, UiState){
    $scope.uiState = UiState;

    $scope.openRecent = function() {

        for (var key in $scope.uiState) {
            if ($scope.uiState.hasOwnProperty(key)) {
                $scope.uiState[key] = false;
            }
        }

        $scope.uiState.showRecent = true;
    }

}
]);