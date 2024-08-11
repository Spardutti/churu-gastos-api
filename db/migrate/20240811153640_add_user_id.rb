class AddUserId < ActiveRecord::Migration[7.0]
  def change
    add_column :products, :user_id, :integer, null: false, default: 1
    add_column :categories, :user_id, :integer, null: false, default: 1
    
    add_index :products, :user_id
    add_index :categories, :user_id
  end
end
