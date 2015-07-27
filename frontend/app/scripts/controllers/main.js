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
		$scope.randomBoards = [];

		BoardService.getRandomBoards(6)
		.then(function(randomBoards) { 
			$scope.$evalAsync(function() { 
				$scope.randomBoards = randomBoards;
			});
		});

	});
