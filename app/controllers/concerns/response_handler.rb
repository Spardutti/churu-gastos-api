module ResponseHandler
  extend ActiveSupport::Concern

  included do
    private

    def render_success(data, status = :ok)
      render json: { status: 'ok', data: data }, status: status
    end

    def render_error(errors, status = :unprocessable_entity)
      render json: { status: 'error', errors: errors }, status: status
    end
  end
end
