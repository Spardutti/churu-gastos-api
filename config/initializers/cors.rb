
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'http://localhost:5174', 'http://localhost:5173', "https://churu-gastos.onrender.com" # List origins as separate strings in an array


    resource '*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head],
      credentials: true # Allow cookies to be sent
  end
end
