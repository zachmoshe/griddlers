require 'test_helper'

class RequestControllerTest < ActionController::TestCase
  test "should get show_lancs" do
    get :show_lancs
    assert_response :success
  end

  test "should get create" do
    get :create
    assert_response :success
  end

end
