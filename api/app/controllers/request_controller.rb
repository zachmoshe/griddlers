require 'sidekiq/api'

class RequestController < ApplicationController
  protect_from_forgery :except => :create

  respond_to :json, except: [:index]
  respond_to :html

  def index
    @latest = BoardProcessingRequest.where(status: ['success', 'partially-success']).order(:completed_at).reverse_order.limit(10)
  end


  def show
    @bpr = BoardProcessingRequest.find(params[:id])

    respond_with @bpr
  end

  def create
    board, strategy, request_params = create_params
    board = Board.load(board)

    unless (cookies['BOARDS_SUBMIT_SECRET'] and cookies['BOARDS_SUBMIT_SECRET']==ENV['BOARDS_SUBMIT_SECRET']) or
           board.shape.select{ |n| n > 35 }.empty?
      flash[:alert] = 'Girddlers Ninja is currently in beta stage. Boards bigger than 35x35 are not allowed.'
      redirect_to :back
      return
    end

    bpr = BoardProcessingRequest.new board: board, strategy: strategy, request_params: request_params
    bpr.save!
    bpr.submit!

    redirect_to request_path(bpr, format: :html)
  end

  def new
    @strategies = Rails.application.config.griddlers[:strategies]
  end

  protected
  def create_params
    board = params.require(:board)
    # Enable those checks again when I have a GUI that generates proper JSON params. With the current poor HTML forms it's hard to do that dynamically
    #board.require(:matrix)
    #board.require(:constraints)
    #board[:constraints].require(:rows)
    #board[:constraints].require(:columns)

    strategy = params.require(:strategy)
    request_params = params[:request_params] || {}

    [board, strategy, request_params]
  end

end
