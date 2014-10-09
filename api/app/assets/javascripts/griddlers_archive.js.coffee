# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

@boardChosen = (board, boards_selector) ->
  boards_selector.removeClass 'panel-primary chosen-board'
  boards_selector.addClass 'panel-info'
  board.removeClass 'panel-info'
  board.addClass 'panel-primary chosen-board'

@strategyChanged = (strategy_name) ->
  $(".strategies-panel").hide()
  $('.strategies-panel[strategy-name="' + strategy_name + '"]').show()

