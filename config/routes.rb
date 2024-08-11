Rails.application.routes.draw do
  devise_for :users
  namespace :api do
    namespace :v1 do
      resources :products, only: [:index, :show, :create, :update, :destroy]
      resources :categories, only: [:index, :show, :create, :update, :destroy]

      post 'register', to: 'registrations#create'
      post 'login', to: 'auth#create'
      delete 'logout', to: 'sessions#destroy'
    end
  end

  # Defines the root path route ("/")
  root to: proc { [200, {}, ['API is running']] }
end
