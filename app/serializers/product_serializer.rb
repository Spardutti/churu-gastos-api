class ProductSerializer < ActiveModel::Serializer
  attributes :id, :name
  belongs_to :category, serializer: CategorySerializer
end