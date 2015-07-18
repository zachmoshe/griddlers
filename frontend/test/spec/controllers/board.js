'use strict';

describe('Controller: BoardCtrl', function () {

  // load the controller's module
  beforeEach(module('griddlersApp'));

  var BoardCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    BoardCtrl = $controller('BoardCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(BoardCtrl.awesomeThings.length).toBe(3);
  });
});
