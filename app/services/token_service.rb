# app/services/token_service.rb
class TokenService
  HMAC_SECRET = Rails.application.secret_key_base

  def self.encode(payload, exp = 24.hours.from_now)
    payload[:exp] = exp.to_i
    JWT.encode(payload, HMAC_SECRET, 'HS256')
  end

  def self.decode(token)
    decoded = JWT.decode(token, HMAC_SECRET, true, algorithm: 'HS256')
    HashWithIndifferentAccess.new(decoded.first)
  rescue
    nil
  end
end
