require 'sidekiq/web'

Rails.application.routes.draw do

  root to: redirect("request")

  resources :request, only: [:index, :new], defaults: {format: :html}
  resources :request, only: [:show, :create], defaults: {format: :json}

  scope 'archive', controller: :griddlers_archive, as: :archive do
    get '/1', action: 'show_lancs'
    get '/2', action: 'show_jsimlo'
  end


  mount Sidekiq::Web => '/sidekiq'
end