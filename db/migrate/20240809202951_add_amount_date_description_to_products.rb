class AddAmountDateDescriptionToProducts < ActiveRecord::Migration[7.0]
  def change
    add_column :products, :amount, :decimal, precision: 10, scale: 2, default: 0.0
    add_column :products, :date, :date, default: -> { 'CURRENT_DATE' }
    add_column :products, :description, :text, default: ""
  end
end
