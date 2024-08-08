# Use the official Ruby image from the Docker Hub
FROM ruby:3.3

# Install Node.js and Yarn
RUN apt-get update -qq && apt-get install -y nodejs npm && npm install -g yarn

# Set the working directory
WORKDIR /app

# Copy only the Gemfile and install gems
COPY Gemfile Gemfile.lock ./
RUN gem install bundler && bundle install

# Copy the rest of the application code
COPY . .

# Start the Rails server
CMD ["rails", "server", "-b", "0.0.0.0"]
