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
		.then(function(randomWorkIds) { 
			randomWorkIds.map(function(workId, idx) { 
				BoardService.waitForWork(workId, function(){})
				.then(function(iterations) { 
					$scope.$evalAsync(function() { 
						$scope.randomBoards[idx] = { board: iterations.slice(-1)[0].board, workId: workId };
					});
				});
			});
		});

	});
