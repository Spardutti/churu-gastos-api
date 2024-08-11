class Api::V1::AuthController < ApplicationController
  skip_before_action :authenticate_request, only: :create

  def create
    user = User.find_by(email: params[:email])
    if user&.valid_password?(params[:password])
      token = TokenService.encode(user_id: user.id)
      render json: { status: 'success', user: { token: token, email: user.email } }, status: :ok
    else
      render json: { status: 'error', message: 'Invalid email or password' }, status: :unauthorized
    end
  end

  def show
    user = authenticate_request
    if user
      render json: { status: 'success', user: { email: user.email } }, status: :ok
    else
      render json: { status: 'error', message: 'Unauthorized' }, status: :unauthorized
    end
  end

  private

  # Method to authenticate the request based on token
  def authenticate_request
    token = request.headers['Authorization']&.split(' ')&.last
    decoded_token = TokenService.decode(token)
    user_id = decoded_token[:user_id] if decoded_token
    User.find_by(id: user_id)
  rescue
    nil
  end
   
end
