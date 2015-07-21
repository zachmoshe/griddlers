'use strict';

/*globals Chart */

Chart.defaults.global.scaleBeginAtZero = true;


/**
 * @ngdoc function
 * @name griddlersApp.controller:BoardCtrl
 * @description
 * # BoardCtrl
 * Controller of the griddlersApp
 */

angular.module('griddlersApp')
	.controller('BoardCtrl', [ '$scope', 'BoardService', function ($scope, boardSvc) {
		var iterations = null;
		var currentIter = 0;
		$scope.chart = {
			dataSeries: [ [], [] ],
			labels: [],
			series: [ '% Certain', 'Avg Change' ],
			options: {
				bezierCurveTension: 0.1,
			},
			colors: [ '#FF4444', '#44FF44', '#4444FF' ]
		};
		$scope.isBoardLoading = false;

		var setIterations = function(iters) {
			iterations = iters;
			currentIter = 0;
			$scope.iter = iterations[currentIter];

			$scope.chart.dataSeries = [ 
				iters.map(function(iter) { return iter.stats.pct_certain.toFixed(2); }),
				iters.map(function(iter) { return iter.stats.avg_change.toFixed(2); }),
			];
			$scope.chart.labels = iters.map(function(iter) { return 'Iter #' + iter.iteration_number; });
		};

		$scope.nextIter = function() { 
			currentIter = Math.min(iterations.length - 1, currentIter + 1);
			$scope.iter = iterations[currentIter];
		};
		$scope.prevIter = function() { 
			currentIter = Math.max(0, currentIter - 1);
			$scope.iter = iterations[currentIter];
		};

		$scope.iterPct = function() { 
			if (!iterations) { return 0; }
			return (100 * (currentIter + 1) / iterations.length).toFixed(0);
		};

		$scope.iterationsReady = function() { 
			return (iterations !== null && iterations.length > 0);
		};


		$scope.setWorkId = function(workId) { 
			iterations = null;
			$scope.isBoardLoading = true;
			boardSvc.loadWorkResults(workId, function(err, data) { 
				if (err) { 
					$scope.isBoardLoading = false;
					console.error("Error while loading workId " + workId + " : " + err); 
				} else { 
					$scope.$evalAsync(function() { 
						$scope.isBoardLoading = false;
						setIterations(data);
					});
				}
			});
		};


	}]);
