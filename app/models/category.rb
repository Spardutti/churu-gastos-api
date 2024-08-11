class Category < ApplicationRecord
    validates :name, presence: true 
    validates :name, uniqueness: { scope: :user_id }
    validates :user_id, presence: true

    has_many :products
    belongs_to :user
end
