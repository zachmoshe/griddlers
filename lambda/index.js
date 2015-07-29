console.log('Loading function');

var aws = require('aws-sdk');
var Promise = require('bluebird');

var ec2 = new aws.EC2({apiVersion: '2015-04-15'});
Promise.promisifyAll(Object.getPrototypeOf(ec2));

var appName = 'dev-griddlers'

exports.handler = function(event, context) {
	var message =JSON.parse(event.Records[0].Sns.Message);
	console.log('Got the following work:', JSON.stringify(message));

	// set user-data command for the worker (run the init script that is already on the image and shutdown when the polling service finishes)
	userDataCommands = [ 
		"#!/bin/bash",
		"sudo su - app -c /etc/griddlers/app_init_script.sh",
		"sudo shutdown -h now"
	];

	// look for spot requests that are open/active and with the same app's tag
	descSpotInstanceParams = { 
		Filters: [
			{ Name: 'state', Values: [ 'open', 'active' ] },
			{ Name: 'tag:app', Values: [ appName ] }
			]      
	};

	// params for spot-instance-request
	requestSpotInstancesParams = {
		SpotPrice: '0.03',
		InstanceCount: 1,
		Type: 'one-time',
		LaunchSpecification: { 
			ImageId: 'ami-ac9cd6db',
			InstanceType: 'm4.large',
			IamInstanceProfile: {
				Name: 'dev_griddlers_worker'
			},
			KeyName: 'zachmoshe',
			Monitoring: {
				Enabled: true
			},
			SecurityGroups: [
				'enable-ssh-access'
			],
			UserData: new Buffer(userDataCommands.join("\n")).toString('base64')
		}
	}

	// first check how many spot requests do we have at the moment
	ec2.describeSpotInstanceRequestsAsync(descSpotInstanceParams)
	.then(function(data) { 
		var spotInstanceRequestIds = data.SpotInstanceRequests.map(function(spr) { 
			return spr.SpotInstanceRequestId;
		});
		console.log("Got " + spotInstanceRequestIds.length +  " spot instance request running: " + JSON.stringify(spotInstanceRequestIds));
		
		if ((data.SpotInstanceRequests.length === 0) || (data.SpotInstanceRequests.length === 1 && message.was_terminated === true)) { 
			console.log("Requesting a new spot instance...");
			return ec2.requestSpotInstancesAsync(requestSpotInstancesParams);
		} else { 
			console.log("There are already spot instance running for application " + appName + " : " + JSON.stringify(spotInstanceRequestIds));
			context.succeed();
			throw "OK";
		}
	})
	// avoid a race-condition if the spot request isn't created yet but we try to set tags on it (happened to me...)
	.then(function(data) { 
		console.log("sleeping for 1 second to avoid race-condition with the creation of the spot instance request...");
		return Promise.delay(1000).then(function() { return data });
	})
	// tag the spot request as our app
	.then(function(data) { 
		console.log("Spot instances requested - " + data.SpotInstanceRequests[0].SpotInstanceRequestId);
		return ec2.createTagsAsync( { Resources: [ data.SpotInstanceRequests[0].SpotInstanceRequestId ], Tags: [ { Key: 'app', Value: appName } ] } );
	})
	// that's it - done!
	.then(function(data) { 
		console.log("Tag app:" + appName + " attached");
		context.succeed();
	})
	.catch(function(err) { 
		// "OK" is thrown to break the then() chain in case that there are already enough running sprs
		if (err === "OK") {
			context.succeed();
		} else {
			context.fail("Error: " + JSON.stringify(err));
		}
	});
};