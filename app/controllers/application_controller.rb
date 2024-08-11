class ApplicationController < ActionController::API
   before_action :authenticate_request

  private

  def authenticate_request
    token = request.headers['Authorization']&.split(' ')&.last
    decoded_token = TokenService.decode(token)
    @current_user = User.find_by(id: decoded_token[:user_id]) if decoded_token
    render json: { error: 'Unauthorized' }, status: :unauthorized unless @current_user
  end
end
