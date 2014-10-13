class Board
  include ActiveModel::Model
  include ActiveModel::Validations

  extend ActiveModel::Callbacks
  define_model_callbacks :initialize, only: :after
  after_initialize :allow_empty_matrix

  validates_presence_of :rows_constraints, :columns_constraints
  validate :matrix_and_constraints_sizes_match
  validate :matrix_values_between_0_1

  attr_accessor :matrix, :rows_constraints, :columns_constraints


  def initialize(attributes={})
    raise ArgumentError, "can't initialize a board without constraints" unless attributes[:rows_constraints] and attributes[:columns_constraints]
    super(attributes)
    run_callbacks :initialize
  end


  def shape
    [ rows_constraints.size, columns_constraints.size ]
  end

  def empty
    out = self.dup
    out.matrix = self.class.two_dim_matrix(*shape)
    out
  end

  def self.load json
    if json.is_a? String
      obj = JSON.parse json, symbolize_names: true
    else
      obj = json.with_indifferent_access
    end

    Board.new matrix: obj[:matrix],
              rows_constraints: obj[:constraints][:rows],
              columns_constraints: obj[:constraints][:columns]
  end

  def self.dump obj
    JSON.dump(
        {
            matrix: obj.matrix,
            constraints: {
                rows: obj.rows_constraints,
                columns: obj.columns_constraints,
            },
        }
    )
  end

  def dump
    self.class.dump self
  end




  protected

  def allow_empty_matrix
    unless matrix and not matrix.empty?
      num_rows = rows_constraints.size
      num_cols =  columns_constraints.size
      uniform_dist = 1.0 / (num_rows*num_cols)
      self.matrix = self.class.two_dim_matrix(num_rows, num_cols)
    end
  end


  def self.two_dim_matrix(rows, cols)
    Array.new(rows) { Array.new(cols) { 1.0/(rows*cols)} }
  end


  def matrix_and_constraints_sizes_match
    num_rows_cons = rows_constraints.length
    num_cols_cons = columns_constraints.length
    num_rows_mat = matrix.length
    num_cols_mat = matrix.map{ |row| row.length }.uniq

    if num_cols_mat.length > 1
      errors.add :matrix, "Illegal matrix. Should be a rectangle"
    end
    num_cols_mat_uniq = num_cols_mat.first

    if num_rows_cons != num_rows_mat
      errors.add :rows_constraints, "Number of rows constraints doesn't match matrix"
    end
    if num_cols_cons != num_cols_mat_uniq
      errors.add :columns_constraints, "Number of columns constraints doesn't match matrix"
    end
  end

  def matrix_values_between_0_1
    unless matrix.map{ |row| row.map{ |cell| (0.0..1.0) === cell }.all? }.all?
      errors.add :matrix, "All matrix values must be between 0 to 1"
    end
  end

end
