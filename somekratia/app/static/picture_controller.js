/**
 * Created by emmilinkola on 30/12/15.
 */


app.controller('pictureController', ['$scope', '$http', 'UserData', 'Upload', '$timeout', function($scope, $http, UserData, Upload, $timeout){

    $scope.changePicture = function(file) {
        file.upload = Upload.upload({
            url: '/user/picture',
            data: {picture: file},
        });

        file.upload.then(function (response) {
          $timeout(function () {
            file.result = response.data;
          });
            UserData.reloadProfilePictures();
        }, function (response) {
          if (response.status > 0)
            $scope.errorMsg = response.status + ': ' + response.data;
        }, function (evt) {
          // Math.min is to fix IE which reports 200% sometimes
          file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
           });
    }

}]);