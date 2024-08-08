class Product < ApplicationRecord
    validates :name, presence: true, uniqueness: true
    validates :category_id, presence: true

    belongs_to :category
end
