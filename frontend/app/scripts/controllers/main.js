'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('griddlersApp')
	.controller('MainCtrl', function ($scope, BoardService) {
		$scope.numBoards = 6;
		$scope.randomBoards = [];

		BoardService.getRandomBoards(6)
		.then(function(randomBoards) { 
			$scope.$evalAsync(function() { 
				$scope.randomBoards = randomBoards;
			});
		});

		Promise.delay(5000)
		.then(function() {
			var boards = [];
			for (var i=0 ; i<$scope.numBoards; i++) { 
				var b = $scope.randomBoards[i];
				if (b) { 
					boards.push(b);
				} else { 
					boards.push({ board: 'NO_BOARD' });
				}
			}
			$scope.$evalAsync(function() { 
				$scope.randomBoards = boards;
			});
		});

	});
