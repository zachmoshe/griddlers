require 'test_helper'

class GriddlersArchiveControllerTest < ActionController::TestCase
  test "should get show_lancs" do
    get :show_lancs
    assert_response :success
  end

end
