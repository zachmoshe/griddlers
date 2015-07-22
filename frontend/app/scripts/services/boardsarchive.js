'use strict';

/*globals AWS */


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
 	var S3 = new AWS.S3();
 	var SQS = new AWS.SQS();
 	Promise.promisifyAll(Object.getPrototypeOf(S3));
 	Promise.promisifyAll(Object.getPrototypeOf(SQS));


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
		// Read the board from the archive dir
		return $http.get(board.board)
		.then(function(resp) { 
				// upload the request data to S3
				var board = resp.data;
				var workId = CryptoJS.SHA256(Math.random().toString()).toString().slice(0,16);
				var s3Bucket = window.griddlersConfig.s3WorkBucket;
				var s3Key = workId + '/request';

				return S3.putObjectAsync({
					Bucket: s3Bucket,
					Key: s3Key,
					Body: JSON.stringify(strategy) + "\n" + JSON.stringify(requestParams) + "\n" + JSON.stringify(board)
				}).then(function(s3Resp) { 
					return { Bucket: s3Bucket, Key: s3Key };
				});
			})
		.then(function(s3Location) { 
				// Send a message to SQS
				return SQS.sendMessageAsync({ 
					QueueUrl: window.griddlersConfig.sqsWorkQueueUrl,
					MessageBody: JSON.stringify(s3Location)
				}).then(function() { 
					return true;
				});
			});

	};
});
