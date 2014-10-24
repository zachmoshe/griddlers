@trackFormSubmit = (label) ->
  ga "send", "event", "BoardRequests", "submit", label
  return

@trackHelpMeBoardDownload = (board_id) ->
  ga "send", "event", "WillYouHelpMe", "download_board", board_id
  return

@trackSocialInteraction = (site) ->
  ga "send", "event", "SocialContactInteraction", "click_link", site
  return

@trackBoardSolver = (event, board_id) ->
  ga 'send', 'event', 'BoardSolver', event, board_id

parse_constraints = (cons_str) ->
  cons = cons_str.split('\n')
  return cons.map (con_str) ->
    con_str.trim().split(" ").filter(Boolean).map (str) ->
      parseInt str


@generateBoardSubmitForm = (form, type) ->
  try
    board_value = ""
    if type=='preparsed'
      if not $('.board-panel.chosen-board').length
        alert 'Choose a board first'
        return false

      board_value = $(".board-panel.chosen-board").attr 'board_str'

    else if type=='manual'
      rows = $('#rows-constraints-textarea')
      cols = $('#cols-constraints-textarea')
      rows_str = rows.val()
      cols_str = cols.val()
      if rows_str=="" or cols_str==""
        alert 'both constraints are mandatory'
        return false
      rows_parsed = parse_constraints(rows_str)
      cols_parsed = parse_constraints(cols_str)

      board = { "matrix": [], "constraints": {"rows": rows_parsed, "columns": cols_parsed } }
      board_value = JSON.stringify(board);

    board = document.createElement 'input'
    board.type = 'hidden'
    board.name = 'board'
    board.value = board_value
    form.appendChild board


    strategy_name = document.createElement 'input'
    strategy_name.type = 'hidden'
    strategy_name.name = 'strategy[name]'
    strategy_name.value = $('.strategies-panel:visible').attr('strategy-name')
    form.appendChild strategy_name

    $('.strategies-panel:visible input').each (ind, input) ->
      input = input.cloneNode()
      if input.value != ""
        if input.type=='checkbox' and input.checked
          input.value = 'true'
        input.type = 'hidden'

        form.appendChild input


  catch err
    console.log err
    return false
