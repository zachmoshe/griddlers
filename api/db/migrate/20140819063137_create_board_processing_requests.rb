class CreateBoardProcessingRequests < ActiveRecord::Migration
  def change
    create_table :board_processing_requests do |t|
      t.text :board
      t.text :strategy
      t.text :request_params
      t.text :result
      t.datetime :submitted_at
      t.datetime :started_at
      t.datetime :completed_at
      t.string :sidekiq_jid
    end
  end
end
