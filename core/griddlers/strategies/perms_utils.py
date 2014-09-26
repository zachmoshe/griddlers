import numpy as np
import itertools

ALL_PERMS_MEMOIZE = {}

def all_perms(l, seqs):
  # check cache
  cache_key = str( (l,seqs) )
  if cache_key in ALL_PERMS_MEMOIZE:
    return ALL_PERMS_MEMOIZE[cache_key]

  # handle end cases
  len_seqs = len(seqs)
  sum_seqs = sum(seqs)

  if l<=0: return []
  if len_seqs == 0: return [np.zeros(l, dtype="int")]
  if sum_seqs + len_seqs - 1 > l: return [] #not enough space

  perms = []

  # iterate possible start indexes for the first block
  first, seqs = seqs[0], seqs[1:]
  max_index_for_first = l - first 

  for i in range( max_index_for_first + 1):
    curr_perm = np.zeros(l, dtype="int")
    curr_perm[i : i+first] = 1

    if len(seqs) > 0:
      remaining_length = l - i - first - 1
      remaining_perms = all_perms(remaining_length, seqs)

      for p in remaining_perms:
        new_perm = np.array(curr_perm)
        new_perm[-remaining_length : ] = p
        perms += [ new_perm ] 
    else:
      perms += [ curr_perm ]

  #add to cache and return
  ALL_PERMS_MEMOIZE[cache_key] = perms
  return perms


def precalculate_all_perms(board):
  # pre calcualte all perms
  perms_output = {}
  for idx, row in enumerate(board.rows()):
    all_perms_key = (len(row), str(board.constraints.rows[idx]))
    if all_perms_key not in perms_output:
      perms_output[all_perms_key] = all_perms(len(row), board.constraints.rows[idx])
  for idx, col in enumerate(board.columns()):
    all_perms_key = (len(col), str(board.constraints.columns[idx]))
    if all_perms_key not in perms_output:
      perms_output[all_perms_key] = all_perms(len(col), board.constraints.columns[idx])
  return perms_output



def all_perms_gen(l, seqs):
  num_free_whites = l-sum(seqs)-len(seqs)+1
  num_boxes = len(seqs)+1

  if num_free_whites < 0:
    return
  if l<=0:
    return
  if len(seqs) == 0:
    yield np.zeros(l)
    return

  whites_must_haves = np.ones(num_boxes)
  whites_must_haves[0] = 0
  whites_must_haves[-1] = 0
  blacks = [ np.ones(i) for i in seqs ]

  if num_free_whites == 0:
    all_possible_white_perms = [ tuple([0]*num_boxes) ]
  else:
    all_possible_white_perms = unlabeled_balls_in_labeled_boxes(num_free_whites, [num_free_whites]*num_boxes)

  zeros = {}
  for i in range(l-sum(seqs)+1):
    zeros[i] = np.zeros(i)

  for white_perm in all_possible_white_perms:
    whites = whites_must_haves + white_perm
    whites = [ zeros[i] for i in whites ]
    
    perm = [ item for sublist in itertools.zip_longest(whites, blacks) for item in sublist ]
    perm = list(itertools.chain(*[i for i in perm if i is not None]))
    yield np.array(perm)
    


# Code was taken from Combinatorics package. (couldn't install it)
# ----------------------------------------------------------------
def unlabeled_balls_in_labeled_boxes(balls, box_sizes):
   """
   OVERVIEW

   This function returns a generator that produces all distinct distributions of
   indistinguishable balls among labeled boxes with specified box sizes
   (capacities).  This is a generalization of the most common formulation of the
   problem, where each box is sufficiently large to accommodate all of the
   balls, and is an important example of a class of combinatorics problems
   called 'weak composition' problems.


   CONSTRUCTOR INPUTS

   n: the number of balls

   box_sizes: This argument is a list of length 1 or greater.  The length of
   the list corresponds to the number of boxes.  `box_sizes[i]` is a positive
   integer that specifies the maximum capacity of the ith box.  If
   `box_sizes[i]` equals `n` (or greater), the ith box can accommodate all `n`
   balls and thus effectively has unlimited capacity.


   ACKNOWLEDGMENT

   I'd like to thank Chris Rebert for helping me to convert my prototype
   class-based code into a generator function.
   """
   if not isinstance(balls, int):
      raise TypeError("balls must be a non-negative integer.")
   if balls < 0:
      raise ValueError("balls must be a non-negative integer.")

   if not isinstance(box_sizes,list):
      raise ValueError("box_sizes must be a non-empty list.")

   capacity= 0
   for size in box_sizes:
      if not isinstance(size, int):
          raise TypeError("box_sizes must contain only positive integers.")
      if size < 1:
          raise ValueError("box_sizes must contain only positive integers.")
      capacity+= size

   if capacity < balls:
      raise ValueError("The total capacity of the boxes is less than the "
        "number of balls to be distributed.")

   return _unlabeled_balls_in_labeled_boxes(balls, box_sizes)


def _unlabeled_balls_in_labeled_boxes(balls, box_sizes):
   """
   This recursive generator function was designed to be returned by
   `unlabeled_balls_in_labeled_boxes`.
   """

   # If there are no balls, all boxes must be empty:
   if not balls:
      yield len(box_sizes) * (0,)

   elif len(box_sizes) == 1:

      # If the single available box has sufficient capacity to store the balls,
      # there is only one possible distribution, and we return it to the caller
      # via `yield`.  Otherwise, the flow of control will pass to the end of the
      # function, triggering a `StopIteration` exception.
      if box_sizes[0] >= balls:
          yield (balls,)

   else:

      # Iterate over the number of balls in the first box (from the maximum
      # possible down to zero), recursively invoking the generator to distribute
      # the remaining balls among the remaining boxes.
      for balls_in_first_box in range( min(balls, box_sizes[0]), -1, -1 ):
         balls_in_other_boxes= balls - balls_in_first_box

         for distribution_other in _unlabeled_balls_in_labeled_boxes(
           balls_in_other_boxes, box_sizes[1:]):
            yield (balls_in_first_box,) + distribution_other

   # end three alternative blocks

# end def _unlabeled_balls_in_labeled_boxes(balls, box_sizes)


