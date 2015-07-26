'use strict';

/*globals Chart */

Chart.defaults.global.scaleBeginAtZero = true;
Chart.defaults.global.scaleFontColor = "#FFF";

/**
 * @ngdoc function
 * @name griddlersApp.controller:BoardPanelCtrl
 * @description
 * # BoardPanelCtrl
 * Controller of the griddlersApp
 */

angular.module('griddlersApp')
	.controller('BoardPanelCtrl', function ($scope, $routeParams, $interval, BoardService) {
		$scope.workLoadingStatus = {};
		$scope.chart = {
			dataSeries: [ [], [] ],
			labels: [],
			series: [ '% Certain', 'Avg Change' ],
			options: {
				bezierCurveTension: 0.1,
				legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li style=\"color: white; text-shadow: 0px 0px 3px black\"><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

			},
			colors: [ '#FF4444', '#44FF44', '#4444FF' ]
		};

		$scope.iterations = null;
		var currentIter = 0;
		var playPromise;

		setWorkId($routeParams.id);



		$scope.nextIter = function() { 
			currentIter = Math.min($scope.iterations.length - 1, currentIter + 1);
			$scope.iter = $scope.iterations[currentIter];
		};
		$scope.prevIter = function() { 
			currentIter = Math.max(0, currentIter - 1);
			$scope.iter = $scope.iterations[currentIter];
		};
		$scope.play = function() { 
			playPromise = $interval(function() { 
				$scope.nextIter();
				if (currentIter+1 >= $scope.iterations.length) { 
					$interval.cancel(playPromise);
				}
			}, 500);
		};

		$scope.iterBin = function(num_bins) { 
			if (!$scope.iterations) { return 0; }
			var pct = (currentIter + 1)/$scope.iterations.length;
			return Math.round(pct*num_bins)-1;
		}

		$scope.iterationsReady = function() { 
			return ($scope.iterations !== null && $scope.iterations.length > 0);
		};


		function setIterations(iters) {
			$scope.iterations = iters;
			currentIter = 0;
			$scope.iter = $scope.iterations[currentIter];

			$scope.chart.dataSeries = [ 
				iters.map(function(iter) { return iter.stats.pct_certain.toFixed(2); }),
				iters.map(function(iter) { return iter.stats.avg_change.toFixed(2); }),
			];
			$scope.chart.labels = iters.map(function(iter) { return 'Iter #' + iter.iteration_number; });
		};

		function setWorkId(workId) { 
			$scope.iterations = null;
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

		$scope.range = function(num) { 
			return new Array(num);
		}

			
	});
		
