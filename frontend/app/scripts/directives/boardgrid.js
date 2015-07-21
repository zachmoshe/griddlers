'use strict';

/**
 * @ngdoc directive
 * @name griddlersApp.directive:boardGrid
 * @description
 * # boardGrid
 */
angular.module('griddlersApp')
	.directive('boardGrid', function () {
		return {
			templateUrl: 'views/partials/boardgrid.html',
			restrict: 'E',
			scope: {
				board: '=board'
			}
		};
	});
