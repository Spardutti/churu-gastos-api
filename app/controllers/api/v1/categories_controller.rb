module Api
  module V1
    class CategoriesController < ActionController::API
      include ResponseHandler

      before_action :set_category, only: [:show, :update, :destroy]

      # GET /api/v1/categories
      def index
        @categories = Category.all
        render_success(serialize(@categories))
      end

      # GET /api/v1/categories/:id
      def show
        render_success(serialize(@category))
      end

      # POST /api/v1/categories
      def create
        @category = Category.new(category_params)
        if @category.save
          render_success(serialize(@category), :created)
        else
          render_error(@category.errors)
        end
      end

      # PATCH/PUT /api/v1/categories/:id
      def update
        if @category.update(category_params)
          render_success(serialize(@category))
        else
          render_error(@category.errors)
        end
      end

      # DELETE /api/v1/categories/:id
      def destroy
        @category.destroy
        head :no_content
      end

      private

      def set_category
        @category = Category.find(params[:id])
      end

      def category_params
        params.require(:category).permit(:name)
      end

      def serialize(resource)
        ActiveModelSerializers::SerializableResource.new(resource).as_json
      end
    end
  end
end
