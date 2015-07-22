'use strict';

describe('Service: boardsarchive', function () {

  // load the service's module
  beforeEach(module('griddlersApp'));

  // instantiate service
  var boardsarchive;
  beforeEach(inject(function (_boardsarchive_) {
    boardsarchive = _boardsarchive_;
  }));

  it('should do something', function () {
    expect(!!boardsarchive).toBe(true);
  });

});
