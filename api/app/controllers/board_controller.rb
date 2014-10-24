class BoardController < ApplicationController


  def show
    id_i = params[:id].to_i rescue not_found
    @board = boards[id_i-1]
    not_found unless @board
  end


  protected
  def not_found
    raise ActionController::RoutingError.new('Not Found')
  end

  def boards
    [
        {
            id: 1,
            board: lancs_board(23).empty
        },
        {
            id: 2,
            board: jsimlo_board("fish").empty
        },
        {
            id: 3,
            board: jsimlo_board("cow").empty
        },
        {
            id: 4,
            board: jsimlo_board("alien").empty
        },
        {
            id: 5,
            board: jsimlo_board("eagle").empty
        },
    ]
  end

  def jsimlo_board(board_name)
    JsimloParser.new.parse Rails.root.join('public', 'griddlers_archive', 'jsimlo.sk', "#{board_name}.sgriddler")
  end

  def lancs_board(board_number)
    NONParser.new.parse Rails.root.join('public', 'griddlers_archive', 'lancs.ac.uk', "#{board_number}.non")
  end

end
