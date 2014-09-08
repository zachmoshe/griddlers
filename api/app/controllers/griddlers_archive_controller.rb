class GriddlersArchiveController < ApplicationController

  LANCS_AC_UK_CACHE_KEY = :lancs_ac_uk_griddlers_archive
  MAIN_LANCS_AC_UK_URL = "http://www.comp.lancs.ac.uk/~ss/nonogram"

  def show_lancs
    unless Rails.cache.read(LANCS_AC_UK_CACHE_KEY)
      html = Nokogiri::HTML(open("#{MAIN_LANCS_AC_UK_URL}/archive"))
      all_boards = html.css("table.puzzles tr").map do |tr|
        cells = tr.css("td");
        {
            board: NONParser.new.parse("#{MAIN_LANCS_AC_UK_URL}/#{cells[0].css("a @href").to_s}"),
            grid_svg: cells[4].css("a @href").to_s
        } unless cells.empty?
      end.compact
      Rails.cache.write LANCS_AC_UK_CACHE_KEY, all_boards
    end
    @all_boards = Rails.cache.read LANCS_AC_UK_CACHE_KEY

  end


  JSIMLO_ARCHIVE_DIR = "#{Rails.root.to_s}/public/griddlers_archive/jsimlo.sk"

  def show_jsimlo
    @all_boards = Dir.glob("#{JSIMLO_ARCHIVE_DIR}/*.sgriddler").map do |filename|
      full_board = JsimloParser.new.parse(filename)
      empty_board = full_board.empty
      {
        full_board: full_board,
        empty_board: empty_board
      }
    end

  end


end
