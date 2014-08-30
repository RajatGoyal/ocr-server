photodice.controller('userController', function($scope, $resource, userFactory) {
    $scope.userName = '';
    $scope.userPw = '';
    $scope.Signup = function() {
        var userC = $resource("http://localhost:8000/api/v1/register/");
        var newUser = new userC();
        newUser.username = $scope.userName;
        newUser.password = $scope.userPw;
        newUser.$save(function(user, headers) { // Success
            userFactory.setUser(user.username, user.id);
            console.log("$save (signUp) success " + JSON.stringify(user));
            $scope.userName = ''; //cleanup
            $scope.userPw = ''; //cleanup
        }, function(error) { // failure - TODO: add message
            console.log("$save (signUp) failed " + JSON.stringify(error.data.error_message))
        });
    }
    $scope.Signin = function() {
        var userResource = $resource('http://localhost:8000/api/v1/user/login/');
        user = new userResource();
        user.username = $scope.userName;
        user.password = $scope.userPw;
        user.$save(function() { // Success
            userFactory.setUser($scope.userName);
            console.log("$save (signIn) success " + JSON.stringify(user));
            $scope.userName = ''; //cleanup
            $scope.userPw = ''; //cleanup
        }, function(error) { // failure - TODO: add message
            console.log("$save (signIn) failed " + JSON.stringify(error.data.error_message));
        });
    }
    $scope.Signout = function() {
        console.log("called signout");
        var userResource = $resource('http://xx.xxx.xxx.xx:xxxx/api/v1/user/logout/:user', {
            user: '@user'
        });
        var user = userResource({
            user: userFactory.getUser()
        }, function() {
            user.$save(function(user, headers) { // Success
                userFactory.setUser('');
                console.log("$save (signIn) success " + JSON.stringify(user));
            }, function(error) { // failure - TODO: add message
                console.log("$save (signIn) failed " + JSON.stringify(error.data.error_message));
            });
        });
    }
});