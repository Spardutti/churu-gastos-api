# app/controllers/auth_controller.rb
class Api::V1::AuthController < ApplicationController
  skip_before_action :authenticate_request, only: :create

  def create
    user = User.find_by(email: params[:email])
    if user&.valid_password?(params[:password])
      token = TokenService.encode(user_id: user.id)
      render json: { status: 'success', data: { token: token, email: user.email } }, status: :ok
    else
      render json: { status: 'error', message: 'Invalid email or password' }, status: :unauthorized
    end
  end
end
