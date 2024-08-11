class Api::V1::RegistrationsController < ApplicationController
  skip_before_action :authenticate_request, only: :create
  
  def create
    user = User.new(user_params)
    if user.save
      render json: { status: 'success', user: user }, status: :created
    else
      render json: { status: 'error', errors: user.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def user_params
    params.require(:user).permit(:email, :password)
  end
end
