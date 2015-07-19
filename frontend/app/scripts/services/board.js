'use strict';

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

		this.loadWorkResults = function(workID, callback) { 
			S3.getObject({ 
				Bucket: griddlersConfig.s3WorkBucket,
				Key: workID + '/results.json'
			}, function(err, data) { 
				if (err) { callback(err); }
				else { 
					try { 
						var obj = JSON.parse(data.Body);
						callback(null, obj);
					} catch (e) { 
						callback(e);
					}
				}
			});
		};


			
	});
