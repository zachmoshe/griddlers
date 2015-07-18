'use strict';

/**
 * @ngdoc filter
 * @name griddlersApp.filter:percentage
 * @function
 * @description
 * # percentage
 * Filter in the griddlersApp.
 */
angular.module('griddlersApp')
  .filter('percentage', function ($filter) {
    return function (input, precision) {
      return $filter('number')(input * 100, precision) + '%';
    };
  });
