# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20140920093840) do

  create_table "board_processing_requests", force: true do |t|
    t.text     "board"
    t.text     "strategy"
    t.text     "request_params"
    t.text     "result"
    t.datetime "submitted_at"
    t.datetime "started_at"
    t.datetime "completed_at"
    t.string   "sidekiq_jid"
    t.string   "status"
  end

  add_index "board_processing_requests", ["completed_at"], name: "index_board_processing_requests_on_completed_at"
  add_index "board_processing_requests", ["status"], name: "index_board_processing_requests_on_status"

end
