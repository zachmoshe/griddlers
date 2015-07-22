'use strict';

describe('Controller: ArchiveCtrl', function () {

  // load the controller's module
  beforeEach(module('griddlersApp'));

  var ArchiveCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ArchiveCtrl = $controller('ArchiveCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(ArchiveCtrl.awesomeThings.length).toBe(3);
  });
});
