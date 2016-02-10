/**
 * Created by tiitulahti on 18/12/15.
 */


app.controller('loginWindowController', ['$scope', '$http', 'UserData', 'UiState', 'MapHolder', function($scope, $http, UserData, UiState, MapHolder){
    $scope.userData = UserData;
    $scope.uiState = UiState;

    $scope.textfieldClick = function(){
        $scope.uiState.inputClick = true;
    }

    $scope.toggleShow = function() {
        if($scope.uiState.inputClick) {
            $scope.uiState.inputClick = false;
            console.log("if");
            return;
        }
        else {
            $scope.uiState.showLoginWindow = !$scope.uiState.showLoginWindow;
             $scope.uiState.showLogin = !$scope.uiState.showLogin;
            console.log("else");
        }
    }

    $scope.toggleLoginRegister = function() {
        $scope.uiState.showRegister = !$scope.uiState.showRegister;
        $scope.uiState.showLogin = !$scope.uiState.showLogin;


    }

    $scope.add = function(){
      var f = document.getElementById('file').files[0],
          r = new FileReader();
      r.onloadend = function(e){
        var data = e.target.result;
        //send you binary data via $http or $resource or do anything else with it
      }
      r. readAsArrayBuffer(f);
    }

/*var config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
            method: 'POST',
            data: {
                username: username,
                password: password,
                email: email,
                file: $scope.file,
            },
            transformRequest: function (data, headersGetter) {
                var formData = new FormData();
                angular.forEach(data, function (value, key) {
                    formData.append(key, value);
                });

                var headers = headersGetter();
                delete headers['Content-Type'];

                return formData;
            },
            url: '/register/'
        };*/

    $scope.register = function(username, email, password, file) {

        $http({
            method: 'POST',
            url: '/register/',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data: {
                username: username,
                password: password,
                email: email,
                //file: $scope.file,
            },

        }).success(function(response){
            alert("Rekisteröityminen onnistui!");
            $scope.userData.username = response.name;
            $scope.userData.userId = response.id;
            $scope.uiState.showLoginWindow = false;
        }).error(function(){
            alert("Rekisteröitymisessä tapahtui virhe, yritäthän uudelleen!");
        });
    }


    $scope.login = function(username, password){
        var config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
            method: 'POST',
            data: {
                username: username,
                password: password
            },
            url: "/login"
        };
        $http(config).success(function(response){
            alert("Tervetuloa "+ username);
            $scope.userData.username = response.name;
            $scope.userData.userId = response.id;
            $scope.userData.subscriptions = response.subscriptions;
            $scope.uiState.showLoginWindow = false;
            console.log($scope.userData.username);
        }).error(function(){
            alert("Kirjautumisessa tapahtui virhe, yritäthän uudelleen!");
        })
    };

}
]);

angular.module('myApp').controller('logoutController', ['$scope', '$http', 'UserData', function($scope, $http, UserData){
    $scope.userData = UserData;

    $scope.logout = function(){
        var config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
            method: 'POST',
        };
        $http.post("/logout", config).success(function(response){
            //alert("Uloskirjautuminen onnistui.");
            $scope.userData.username = undefined;
            $scope.userData.userId = 0;
            $scope.userData.subscriptions = {};
        }).error(function(){
            alert("Uloskirjautumisessa tapahtui virhe, yritäthän uudelleen!");
        })
    };
}
]);

/*app.controller('loginController', function($scope, UserData){
    $scope.userData = UserData;
    var loginbutton = document.querySelector('[ng-controller="loginShowController"]');
    var loginscope = angular.element(loginbutton).scope();


    $scope.toggleShow = function() {
        loginscope.toggleShow();
    }

});

app.controller('loginShowController', function($scope, $rootScope, UserData){
    $scope.userData = UserData;
    $scope.inputClick = false;

    $scope.toggleShow = function() {
        if($scope.inputClick) {
            $scope.inputClick = false;
            return;
        }
        else {
            $rootScope.showLogin = !$rootScope.showLogin;
        }
    }
});     */