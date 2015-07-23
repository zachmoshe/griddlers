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
		'chart.js',
		'ui.bootstrap'
	])
	.config(function ($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'views/main.html',
				controller: 'MainCtrl',
				controllerAs: 'main'
			})
			.when('/board/:id', {
				templateUrl: 'views/boardpanel.html',
				controller: 'BoardPanelCtrl',
				controllerAs: 'board'
			})
			.when('/archive', {
				templateUrl: 'views/boardsarchive.html',
				controller: 'BoardsArchiveCtrl',
				controllerAs: 'archive'
			})
			.otherwise({
				redirectTo: '/'
			});
	});

