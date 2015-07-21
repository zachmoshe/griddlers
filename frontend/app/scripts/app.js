'use strict';

/* globals AWS */

/* AWS configuration */
AWS.config.region = window.griddlersConfig.awsRegion;
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
	IdentityPoolId: window.griddlersConfig.cognitoPoolId,
});


/**
 * @ngdoc overview
 * @name frontendApp
 * @description
 * # frontendApp
 *
 * Main module of the application.
 */
angular
	.module('griddlersApp', [
		'ngAnimate',
		'ngCookies',
		'ngResource',
		'ngRoute',
		'ngSanitize',
		'ngTouch',
		'chart.js'
	])
	.config(function ($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'views/main.html',
				controller: 'MainCtrl',
				controllerAs: 'main'
			})
			.when('/board', {
				templateUrl: 'views/board.html',
				controller: 'BoardCtrl',
				controllerAs: 'board'
			})
			.otherwise({
				redirectTo: '/'
			});
	});

