from app import create_app, db
import sqlite3
import os

app = create_app()

# Get the database path from app config
with app.app_context():
    # The database is in the instance folder
    db_path = 'instance/app.db'
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        exit(1)
    
    print(f"Using database: {db_path}")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if type_id column exists
        cursor.execute("PRAGMA table_info(assets)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"Columns in assets table: {column_names}")
        
        if 'type_id' in column_names and 'asset_type_id' not in column_names:
            print("Renaming type_id to asset_type_id...")
            
            # Create a new table with the correct schema
            cursor.execute("""
            CREATE TABLE assets_new (
                id INTEGER NOT NULL, 
                tag VARCHAR(64), 
                name VARCHAR(64), 
                description TEXT, 
                purchase_date DATETIME, 
                purchase_cost FLOAT, 
                status VARCHAR(20), 
                notes TEXT, 
                created_at DATETIME, 
                updated_at DATETIME, 
                department_id INTEGER, 
                asset_type_id INTEGER, 
                user_id INTEGER, 
                PRIMARY KEY (id), 
                FOREIGN KEY(department_id) REFERENCES departments (id), 
                FOREIGN KEY(asset_type_id) REFERENCES asset_types (id), 
                FOREIGN KEY(user_id) REFERENCES users (id)
            )
            """)
            
            # Copy data from old table to new table
            cursor.execute("""
            INSERT INTO assets_new (
                id, tag, name, description, purchase_date, purchase_cost, 
                status, notes, created_at, updated_at, department_id, 
                asset_type_id, user_id
            )
            SELECT 
                id, tag, name, description, purchase_date, purchase_cost, 
                status, notes, created_at, updated_at, department_id, 
                type_id, user_id
            FROM assets
            """)
            
            # Drop old table and rename new table
            cursor.execute("DROP TABLE assets")
            cursor.execute("ALTER TABLE assets_new RENAME TO assets")
            
            # Commit changes
            conn.commit()
            print("Database updated successfully!")
        elif 'asset_type_id' in column_names:
            print("Column asset_type_id already exists, no changes needed.")
        else:
            print("Column type_id not found. Database schema may be different than expected.")
    
    except Exception as e:
        conn.rollback()
        print(f"Error updating database: {str(e)}")
    
    finally:
        conn.close() 