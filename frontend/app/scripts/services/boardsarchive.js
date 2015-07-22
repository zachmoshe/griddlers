'use strict';

/**
 * @ngdoc service
 * @name griddlersApp.boardsarchive
 * @description
 * # boardsarchive
 * Service in the griddlersApp.
 */
 var ARCHIVE_PREFIX = "/griddlers_archive"

 angular.module('griddlersApp')
 .service('BoardsArchiveService', function ($http) {
 	this.getIndex = function() { 
 		return $http.get(ARCHIVE_PREFIX + "/index.json").then(function(resp) { 
 			resp.data.forEach(function(d) { 
 				d.svg = ARCHIVE_PREFIX + '/' + d.svg;
 				d.board = ARCHIVE_PREFIX + '/' + d.board;
 			});

 			return resp.data;
 		});
 	};

 	this.submitBoard = function(board, strategy, requestParams) { 
 		console.log("should submit board: ", board, " with stragegy:", strategy, " and params:", requestParams);
 	};
 });
