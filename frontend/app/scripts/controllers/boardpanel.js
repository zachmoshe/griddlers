'use strict';

/*globals Chart */

Chart.defaults.global.scaleBeginAtZero = true;


/**
 * @ngdoc function
 * @name griddlersApp.controller:BoardPanelCtrl
 * @description
 * # BoardPanelCtrl
 * Controller of the griddlersApp
 */

angular.module('griddlersApp')
	.controller('BoardPanelCtrl', function ($scope, $routeParams, BoardService) {
		$scope.workLoadingStatus = {};
		$scope.chart = {
			dataSeries: [ [], [] ],
			labels: [],
			series: [ '% Certain', 'Avg Change' ],
			options: {
				bezierCurveTension: 0.1,
			},
			colors: [ '#FF4444', '#44FF44', '#4444FF' ]
		};

		var iterations = null;
		var currentIter = 0;


		setWorkId($routeParams.id);



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


		function setIterations(iters) {
			iterations = iters;
			currentIter = 0;
			$scope.iter = iterations[currentIter];

			$scope.chart.dataSeries = [ 
				iters.map(function(iter) { return iter.stats.pct_certain.toFixed(2); }),
				iters.map(function(iter) { return iter.stats.avg_change.toFixed(2); }),
			];
			$scope.chart.labels = iters.map(function(iter) { return 'Iter #' + iter.iteration_number; });
		};

		function setWorkId(workId) { 
			iterations = null;
			$scope.workLoadingStatus = { status: 'LOADING', message: 'Loading your board processing request' };

			BoardService.waitForWork(workId, function(statusUpdate) { 
				$scope.$evalAsync(function() { 
					if (statusUpdate === 'WAITING') { 
						$scope.workLoadingStatus = { status: 'WAITING', message: 'Waiting for an available worker to solve your board' };
					}
				});
			})
			.then(function(data) { 
				$scope.$evalAsync(function() { 
					$scope.workLoadingStatus = { status: 'DONE' };
					setIterations(data);
				});
			})
			.catch(function(err) { 
				$scope.$evalAsync(function() { 
					$scope.workLoadingStatus = { status: 'ERROR', message: err };
				});
			});
		};

			
	});
