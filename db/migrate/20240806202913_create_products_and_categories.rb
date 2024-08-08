class CreateProductsAndCategories < ActiveRecord::Migration[7.0]
  def change
    create_table :categories do |t|
      t.string :name

      t.timestamps
    end

    create_table :products do |t|
      t.string :name
      t.references :category, foreign_key: true

      t.timestamps
    end
  end
end
