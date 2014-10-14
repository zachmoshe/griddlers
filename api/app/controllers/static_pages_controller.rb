class StaticPagesController < ApplicationController
  def measure_human_time
    @boards = [
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
      # {
      #     id: 6,
      #     board: jsimlo_board("hurdler").empty
      # },
    ]
  end




  protected

  def jsimlo_board(board_name)
    JsimloParser.new.parse Rails.root.join('public', 'griddlers_archive', 'jsimlo.sk', "#{board_name}.sgriddler")
  end
  def lancs_board(board_number)
    NONParser.new.parse Rails.root.join('public', 'griddlers_archive', 'lancs.ac.uk', "#{board_number}.non")
  end
end
