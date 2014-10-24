# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/


onClick = (ev) ->
  setCell(this)

setCell = (cell) ->
  if not @solverActive
    return
  if @stopwatchIntervalId != null
    selectedColor = $('.board-solver-color.btn-primary').attr('type')
    $(cell).attr("type", selectedColor)
    if checkBoardComplete()
      boardDone()
  else
    sw = $('#stopwatch')
    if not sw.attr('isShaken')
      sw.attr 'isShaken', true
      $('#stopwatch').effect('shake', { direction: 'right', distance: 3 }, 400, -> sw.removeAttr 'isShaken')

cellMouseOver = (ev) ->
  row = (parseInt $(this).attr('row')) + 1
  col = parseInt $(this).attr('col')
  $('.board-row-consts-cell').removeAttr 'hovered-row'
  $('.board-line').eq(row).find('.board-row-consts-cell').attr 'hovered-row', 'hovered-row'
  $('.board-column-consts-cell').removeAttr 'hovered-col'
  $('.board-column-consts-cell').eq(col).attr 'hovered-col', 'hovered-col'

  if ev.which == 1 and ev.button == 0 # left button pressed
    setCell(this)

setChosenColor = (color) ->
  $('.board-solver-color').removeClass 'btn-primary'
  $('.board-solver-color[type="'+color+'"]').addClass 'btn-primary'

@colorChoose = (colorButton) ->
  color = $(colorButton).attr 'type'
  setChosenColor color

detectColorChange = (ev) ->
  val = ev.keyCode || ev.which
  $('.board-solver-color').removeAttr('checked')
  if val==49 # 1
    req_type = 'black'
  else if val==50 #2
    req_type = 'white'
  else if val==51 #3
    req_type = 'guess-black'
  else if val==52 #3
    req_type = 'guess-white'
  else if val==48 #0
    req_type = 'unknown'
  else
    return

  setChosenColor req_type

@clearGuesses = () ->
  $('.board-cell[type="guess-black"]').attr 'type', 'unknown'
  $('.board-cell[type="guess-white"]').attr 'type', 'unknown'

@makeGuessesPermanent = () ->
  $('.board-cell[type="guess-black"]').attr 'type', 'black'
  $('.board-cell[type="guess-white"]').attr 'type', 'white'

paddy = (n,p) ->
  pad_char = '0'
  pad = new Array(1 + p).join(pad_char)
  return (pad + n).slice(-pad.length)



@stopwatchPlayClicked = () ->
  if not @solverActive
    return
  trackBoardSolver('stopwatch_resumed', @board_id)
  if @stopwatchIntervalId is null
    @stopwatchIntervalId = setInterval(advanceStopwatch, 1000)

@stopwatchPauseClicked = () ->
  if not @solverActive
    return
  trackBoardSolver('stopwatch_paused', @board_id)
  clearInterval(@stopwatchIntervalId)
  @stopwatchIntervalId = null
  $('.board .board-cell').css 'background-color', 'lightgreen'

advanceStopwatch = () ->
  sw = $('#stopwatch')
  seconds = parseInt(sw.attr 'seconds') + 1
  sw.attr 'seconds', seconds

  h = Math.floor(seconds / 3600)
  m = Math.floor((seconds%3600) / 60)
  s = seconds % 60
  stopwatchText = paddy(h,2) + ":" + paddy(m,2) + ":" + paddy(s,2)

  sw.text(stopwatchText)

generateSequence = (l) ->
  line = l.map (i,x) ->
    $(x).attr('type')=='black' ? 1 : 0
  seqs = []
  curr_seq = 0
  for x in line
    if x == true
      curr_seq += 1
    else if curr_seq > 0
      seqs.push(curr_seq)
      curr_seq = 0
  if curr_seq>0
    seqs.push(curr_seq)
  seqs

checkBoardComplete = ->
  if $('.board .board-cell[type="unknown"]').length + $('.board .board-cell[type="guess-black"]').length + $('.board .board-cell[type="guess-white"]').length > 0
    return false

  # check rows
  for rowConsts, i  in @row_consts
    currSeq = generateSequence($('.board .board-line').eq(i+1).find('.board-cell'))  # first row is the consts
    if currSeq.toString() != rowConsts.toString()  # yes.. I know...
      return false
  # check cols
  for colConsts, i in @column_consts
    currSeq = generateSequence($('.board .board-line').map (j,x) ->
      $(x).find('.board-cell')[i]
    )
    if currSeq.toString() != colConsts.toString()
      return false

  return true

boardDone = ->
  $('.board').css 'border', '3px solid green'
  stopwatchPauseClicked()
  minutes = Math.floor($('#stopwatch').attr('seconds')/60)
  $('.board').after('<div class="welldone">Well Done!! It took you ' + minutes + ' minutes')
  trackBoardSolver('board_finished', @board_id)

  clientId = 'unknown_cliend_id'
  ga (tracker) ->
    clientId = tracker.get 'clientId'
  if window.location.hostname.match('griddlers.ninja').length > 0
    $.post('https://docs.google.com/forms/d/124-Nn8KB11aa9A3j6X2MwZgcs1n4phlLPnPYG7xA2uM/formResponse', {"entry.1214389103": 'Board #'+@board_id.toString(), "entry.655763736": minutes, "entry.1544471406": clientId })
  @solverActive = false


@stopwatchIntervalId = null
@initializeBoard = (board) ->
  @solverActive = true
  $(document).keypress(detectColorChange);

  board.find('.board-cell').css 'cursor', 'cell'
  board.find(".board-cell").attr("type", "unknown")
  board.find(".board-cell").mouseenter(cellMouseOver)
  board.find(".board-cell").mousedown( 'click', onClick)

  # initialize rows and columns constraints
  @row_consts = JSON.parse($('boarddata').attr('row_constraints'))
  @column_consts = JSON.parse($('boarddata').attr('column_constraints'))
  @board_id = $('boarddata').attr('board_id')

  # start the stopwatch
  @stopwatchIntervalId = setInterval(advanceStopwatch, 1000)

  trackBoardSolver('board_started', @board_id)