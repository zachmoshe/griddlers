class AddIndexBoardProcessingRequest < ActiveRecord::Migration
  def change
    add_index :board_processing_requests, :completed_at
  end
end
