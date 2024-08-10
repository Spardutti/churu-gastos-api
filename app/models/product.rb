class Product < ApplicationRecord
  # Validations
  validates :name, presence: true
  validates :category_id, presence: true
  validates :amount, presence: true, numericality: { greater_than_or_equal_to: 0 }
  validates :date, presence: true

  # Associations
  belongs_to :category

  # Callbacks
  before_validation :set_default_date, if: -> { date.blank? }

  private

  def set_default_date
    self.date = Date.today
  end
end
