'use strict';

/**
 * @ngdoc directive
 * @name griddlersApp.directive:boardSvg
 * @description
 * # boardSvg
 */
 angular.module('griddlersApp')
 .directive('boardSvg', function () {
	return {
		templateUrl: 'views/partials/board-svg.html',
		templateNamespace: 'svg',
		restrict: 'E',
		scope: {
			board: '@',
			workid: '@'
		},
		controller: function($scope) { 

			$scope.$watch('board', function(val) { 
				if (!val || val === "") { return; }

				var board = JSON.parse(val);

				var num_rows = board.matrix.length;
				var num_cols = board.matrix[0].length;
				var cell_width = 100/num_cols;
				var cell_height = 100/num_rows;

				// horizontal lines
				var hlines = [];
				for (var i=0 ; i<=num_rows; i++) { 
					hlines.push({ x1: "0%", y1: (100*i/num_rows)+"%", x2: "100%", y2: (100*i/num_rows)+"%"});
				}
				hlines.push({ x1: "0%", y1: "100%", x2: "100%", y2: "100%" });
				$scope.horizontalLines = hlines;
				
				// vertical lines
				var vlines = [];
				for (i=0 ; i<=num_cols; i++) { 
					vlines.push({ x1: (100*i/num_rows)+"%", y1: "0%", x2: (100*i/num_rows)+"%", y2: "100%" });
				}
				vlines.push({ x1: "100%", y1: "0%", x2: "100%", y2: "100%" });
				$scope.verticalLines = vlines;

				// cells
				var cells = [];
				for (var row=0 ; row < num_rows ; row++) { 
					for (var col=0 ; col < num_cols ; col++) { 

						if (board.matrix[row][col] > 0) {
							var grayLevel = 255 * (1-board.matrix[row][col]);
							var gray = "rgb("+grayLevel+","+grayLevel+","+grayLevel+")";	
							cells.push({ x: (col * cell_width) + "%", y: (row * cell_height) + "%", width: cell_width + "%", height: cell_height + "%", fill: gray });
						}
					}
				}
				$scope.cells = cells;

			});

		},
	};
 });
