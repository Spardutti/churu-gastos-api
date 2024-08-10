class ProductSerializer < ActiveModel::Serializer
  attributes :id, :name, :amount, :description, :date
  belongs_to :category, serializer: CategorySerializer
end