require 'test_helper'

class StaticPagesControllerTest < ActionController::TestCase
  test "should get measure_human_time" do
    get :measure_human_time
    assert_response :success
  end

end
