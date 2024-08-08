module Api
  module V1
    class ProductsController < ActionController::API
      include ResponseHandler

      before_action :set_product, only: [:show, :update, :destroy]

      # GET /api/v1/products
      def index
        @products = Product.all
        render_success(serialize(@products))
      end

      # GET /api/v1/products/:id
      def show
        render_success(serialize(@product))
      end

      # POST /api/v1/products
      def create
        @product = Product.new(product_params)
        if @product.save
          render_success(serialize(@product), :created)
        else
          render_error(@product.errors)
        end
      end

      # PATCH/PUT /api/v1/products/:id
      def update
        if @product.update(product_params)
          render_success(serialize(@product))
        else
          render_error(@product.errors)
        end
      end

      # DELETE /api/v1/products/:id
      def destroy
        @product.destroy
        head :no_content
      end

      private

      def set_product
        @product = Product.find(params[:id])
      end

      def product_params
        params.require(:product).permit(:name, :category_id)
      end

      def serialize(resource)
        ActiveModelSerializers::SerializableResource.new(resource).as_json
      end
    end
  end
end
