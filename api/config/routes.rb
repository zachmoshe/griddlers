require 'sidekiq/web'

Rails.application.routes.draw do

  get 'griddlers_archive/show_lancs'

  resources :request, only: [:show, :create], defaults: {format: :json}

  scope 'archive', controller: :griddlers_archive do
    get '/1', action: 'show_lancs'
    get '/2', action: 'show_jsimlo'
  end


  mount Sidekiq::Web => '/sidekiq'
end