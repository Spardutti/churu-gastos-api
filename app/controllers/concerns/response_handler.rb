module ResponseHandler
  def render_success(data, status = :ok)
    render json: data, status: status
  end

  def render_error(errors, status = :unprocessable_entity)
    formatted_errors = format_errors(errors)
    render json: { errors: formatted_errors }, status: status
  end

  private

  def format_errors(errors)
    errors.full_messages.map { |message| message }
  end
end
