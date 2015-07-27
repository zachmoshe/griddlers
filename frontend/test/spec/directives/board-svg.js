'use strict';

describe('Directive: boardSvg', function () {

  // load the directive's module
  beforeEach(module('griddlersApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<board-svg></board-svg>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the boardSvg directive');
  }));
});
