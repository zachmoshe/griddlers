require 'sidekiq/api'

class RequestController < ApplicationController

  respond_to :json, :html


  def show
    @bpr = BoardProcessingRequest.find(params[:id])

    respond_with @bpr
  end

  def create
    board = Board.load(params[:board])
    strategy = JSON.load(params[:strategy])
    request_params = JSON.load(params[:request_params])

    bpr = BoardProcessingRequest.new board: board, strategy: strategy, request_params: request_params
    bpr.save!
    bpr.submit!

    redirect_to request_path(bpr, format: :html)
  end

  protected
end
