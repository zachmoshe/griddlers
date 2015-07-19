'use strict';

/**
 * @ngdoc function
 * @name griddlersApp.controller:BoardCtrl
 * @description
 * # BoardCtrl
 * Controller of the griddlersApp
 */
Chart.defaults.global.scaleBeginAtZero = true;

angular.module('griddlersApp')
	.controller('BoardCtrl', [ '$scope', 'BoardService', function ($scope, boardSvc) {
		var iterations = [];
		var currentIter = 0;

		var setIterations = function(iters) {
			iterations = iters;
			currentIter = 0;
			$scope.iter = iterations[currentIter];

			$scope.chartDataSeries = [ 
				iters.map(function(iter) { return iter.stats.pct_certain.toFixed(2); }),
				//iters.map(function(iter) { return iter.stats.time_elapsed.toFixed(2); }),
				iters.map(function(iter) { return iter.stats.avg_change.toFixed(2); }),
			];
			$scope.chartLabels = iters.map(function(iter) { return 'Iter #' + iter.iteration_number; });
			$scope.chartSeries = [ 
				'% Certain', 
				//'Time', 
				'Avg Change'
			];
			$scope.chartOptions = { 
				bezierCurveTension: 0.1,
			};
			$scope.chartColors = [ '#FF4444', '#44FF44', '#4444FF' ];
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
			return (100 * (currentIter + 1) / iterations.length).toFixed(0);
		}

		$scope.setWorkId = function(workId, callback) { 
			boardSvc.loadWorkResults(workId, function(err, data) { 
				if (err) { 
					if (err.code == 'NoSuchKey') { 
						console.error("No such key " + workId);
					} else { 
						console.error("Other S3 error - ", err.message)
					}
				}
				else { 
					$scope.$evalAsync(function() { 
						setIterations(data);
					});
				}
			});
		}


	}]);
