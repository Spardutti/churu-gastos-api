class ApplicationController < ActionController::Base
    # Skip CSRF token verification for API requests
  before_action :skip_session_storage

  private

  def skip_session_storage
    # Skip session storage for API requests
    request.format.json?
  end
end
