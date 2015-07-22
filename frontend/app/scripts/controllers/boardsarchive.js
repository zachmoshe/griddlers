'use strict';

/**
 * @ngdoc function
 * @name griddlersApp.controller:ArchiveCtrl
 * @description
 * # ArchiveCtrl
 * Controller of the griddlersApp
 */
angular.module('griddlersApp')
	.controller('BoardsArchiveCtrl', function ($scope, BoardsArchiveService, $modal) {
		$scope.boards = [];

		BoardsArchiveService.getIndex().then(function(allBoards) { 
			$scope.boards = allBoards;
		});

		$scope.openSubmitWindow = function (board) {
			var modalInstance = $modal.open({
				animation: true,
				templateUrl: 'submitModalContent.html',
				controller: 'ModalInstanceCtrl',
				resolve: {
					board: function () {
						return board;
					}
				}
			});

			modalInstance.result.then(function (modalResp) {
				BoardsArchiveService.submitBoard(board, modalResp.strategy, modalResp.requestParams);
			}, function () {
			});
		};
	});


angular.module('griddlersApp')
	.controller('ModalInstanceCtrl', function ($scope, $modalInstance, board) {
		$scope.board = board;

		$scope.requestParams = {};
		$scope.strategy = { name: 'naive-probs' };

		$scope.submit = function () {
			$modalInstance.close({ requestParams: $scope.requestParams, strategy: $scope.strategy });
		};

		$scope.cancel = function () {
			$modalInstance.dismiss('cancel');
		};
	});