class JsimloParser
  def parse(file)
    str = open(file).read

    header, size, matrix_str, cols_rev_str, rows_rev_str = str.split("\r\n\r\n")

    matrix = matrix_str.split("\r\n").map{ |r| r.split(" ").map{ |c| c=='.' ? 0 : 1 } }
    cols_constraints = cols_rev_str.split("\r\n").map{ |r| r.split(" ").map(&:to_i).reverse }
    rows_constraints = rows_rev_str.split("\r\n").map{ |r| r.split(" ").map(&:to_i).reverse }

    board = Board.new matrix: matrix,
                      rows_constraints: rows_constraints,
                      columns_constraints: cols_constraints

  end
end