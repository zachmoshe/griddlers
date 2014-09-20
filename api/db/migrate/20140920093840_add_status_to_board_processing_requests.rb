class AddStatusToBoardProcessingRequests < ActiveRecord::Migration
  def change
    add_column :board_processing_requests, :status, :string
    add_index :board_processing_requests, :status
  end
end
