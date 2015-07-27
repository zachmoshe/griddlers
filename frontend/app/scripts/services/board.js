'use strict';

/*globals AWS */

/**
 * @ngdoc service
 * @name griddlersApp.board
 * @description
 * # board
 * Service in the griddlersApp.
 */
angular.module('griddlersApp')
	.service('BoardService', function () {
		var S3 = new AWS.S3();
		Promise.promisifyAll(Object.getPrototypeOf(S3));
 	
		var RESPONSE_BETWEEN_POLLS_MS = 1000 * 60; // 1 minute

 		function getRequestS3Location(workId) { 
 			return { Bucket: window.griddlersConfig.s3WorkBucket, Key: workId + '/request' };
 		}
 		function getResponseS3Location(workId) { 
 			return { Bucket: window.griddlersConfig.s3WorkBucket, Key: workId + '/response' };
 		}


		this.waitForWork = function(workId, statusUpdateCallback) { 
			return S3.headObjectAsync( getRequestS3Location(workId) )
			.then(function() { 

				function getResponse(workId) { 
					return S3.getObjectAsync( getResponseS3Location(workId) )
					.catch(function() { 
						statusUpdateCallback("WAITING");
						return Promise.delay(RESPONSE_BETWEEN_POLLS_MS).then(function() { 
							return getResponse(workId);
						});
					});
				}

				// check if response is there and wait if it isn't 
				return getResponse(workId);
			})
			.then(function(resp) { 
				var resp_body = JSON.parse(resp.Body);
				if (resp_body.status === "success") { 
					return resp_body.iterations;
				} else {
					throw resp_body.status + ": " + resp_body.message;
				}
			})
			.catch(function(ex) { 
				if (ex.code === 'NotFound') { 
					throw "Illegal work ID";
				} else {
					throw ex;
				}
			});
			
		};


		this.getRandomBoards = function(numBoards) { 
			return S3.listObjectsAsync({ 
				Bucket: window.griddlersConfig.s3WorkBucket
			})
			.then(function(resp) { 
				var files = resp.Contents;
				return files
				.filter(function(file) { 
					return file.Size > 200 && file.Key.endsWith('/response');
				})
				.map(function(file) { 
					return file.Key.split('/')[0];
				})
				.slice(0,numBoards);
			});
		};

	});
