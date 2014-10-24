require 'sidekiq/web'

Rails.application.routes.draw do

  get 'willyouhelpme' => 'static_pages#measure_human_time'

  # Here just for manual uses (on development machine)
  #get 'board_pdf/:id' => 'static_pages#board_pdf'

  root to: redirect("request")

  resources :request, only: [:index, :new], defaults: {format: :html}
  resources :request, only: [:show, :create], defaults: {format: :json}

  scope 'archive', controller: :griddlers_archive, as: :archive do
    get '/1', action: 'show_lancs'
    get '/2', action: 'show_jsimlo'
  end

  get 'board/:id' => 'board#show', as: 'show_board'


  mount Sidekiq::Web => '/sidekiq'
end