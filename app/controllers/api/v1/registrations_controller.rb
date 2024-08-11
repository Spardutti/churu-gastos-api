class Api::V1::RegistrationsController < ApplicationController
  skip_before_action :authenticate_request, only: :create
  include ResponseHandler
  
  def create
    user = User.new(user_params)
    if user.save
      render_success(serialize(user), :created)
    else
      render_error(user.errors.full_messages.join(', '), :unprocessable_entity)
    end
  end

  private

  def user_params
    params.require(:user).permit(:email, :password)
  end
end
