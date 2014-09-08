class NONParser
  def parse(non_url)
    non_str = open(non_url).read

    rows_c = non_str.match(/rows.*\n\n/m).to_s.split("\n")[1..-1].map{ |r| r.split(",").map &:to_i }
    cols_c = non_str.match(/columns.*/m).to_s.split("\n")[1..-1].map{ |r| r.split(",").map &:to_i }
    board = Board.new matrix: Board.two_dim_matrix(rows_c.size, cols_c.size),
                      rows_constraints: rows_c,
                      columns_constraints: cols_c

    board
  end

end