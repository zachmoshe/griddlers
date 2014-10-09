class GriddlersArchiveController < ApplicationController

  LANCS_AC_UK_CACHE_KEY = :lancs_ac_uk_griddlers_archive
  LANCS_AC_UK_ARCHIVE_DIR = "#{Rails.root.to_s}/public/griddlers_archive/lancs.ac.uk"

  def show_lancs
    unless Rails.cache.read(LANCS_AC_UK_CACHE_KEY)
       all_boards = Dir.glob("#{LANCS_AC_UK_ARCHIVE_DIR}/*.non.solved").map do |filename|
        full_board = Board.load(JSON.load(open(filename).read))
        empty_board = full_board.empty
        {
            full_board: full_board,
            empty_board: empty_board
        }
      end
      Rails.cache.write LANCS_AC_UK_CACHE_KEY, all_boards
    end

    @board_origin = 'preparsed-lancs'
    @all_boards = Rails.cache.read LANCS_AC_UK_CACHE_KEY
    @strategies = Rails.application.config.griddlers[:strategies]
    render 'show_boards'
  end


  JSIMLO_ARCHIVE_DIR = "#{Rails.root.to_s}/public/griddlers_archive/jsimlo.sk"
  JSIMLO_CACHE_KEY = :jsimlo_griddlers_archive
  def show_jsimlo
    unless Rails.cache.read(JSIMLO_CACHE_KEY)
      all_boards = Dir.glob("#{JSIMLO_ARCHIVE_DIR}/*.sgriddler").map do |filename|
        full_board = JsimloParser.new.parse(filename)
        empty_board = full_board.empty
        {
            full_board: full_board,
            empty_board: empty_board
        }
      end
      Rails.cache.write JSIMLO_CACHE_KEY, all_boards
    end

    @board_origin = 'preparsed-jsimlo'
    @all_boards = Rails.cache.read JSIMLO_CACHE_KEY
    @strategies = Rails.application.config.griddlers[:strategies]

    render'show_boards'
  end


end
