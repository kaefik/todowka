"""
Migration script to add reminder and recurrence fields to tasks table
Run this script to update the database schema
"""
import sqlite3
import sys
from pathlib import Path

def migrate_database():
    db_path = Path(__file__).parent.parent.parent / "database.db"
    
    if not db_path.exists():
        print(f"Database file not found at {db_path}")
        return
    
    print(f"Connecting to database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(tasks)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    
    print(f"Existing columns: {sorted(existing_columns)}")
    
    # Add reminder_enabled column
    if 'reminder_enabled' not in existing_columns:
        print("Adding column: reminder_enabled")
        cursor.execute("""
            ALTER TABLE tasks ADD COLUMN reminder_enabled BOOLEAN DEFAULT 0
        """)
    else:
        print("Column reminder_enabled already exists, skipping")
    
    # Add recurrence_type column
    if 'recurrence_type' not in existing_columns:
        print("Adding column: recurrence_type")
        cursor.execute("""
            ALTER TABLE tasks ADD COLUMN recurrence_type TEXT
        """)
    else:
        print("Column recurrence_type already exists, skipping")
    
    # Add recurrence_config column
    if 'recurrence_config' not in existing_columns:
        print("Adding column: recurrence_config")
        cursor.execute("""
            ALTER TABLE tasks ADD COLUMN recurrence_config TEXT
        """)
    else:
        print("Column recurrence_config already exists, skipping")
    
    # Add timezone column
    if 'timezone' not in existing_columns:
        print("Adding column: timezone")
        cursor.execute("""
            ALTER TABLE tasks ADD COLUMN timezone TEXT DEFAULT 'UTC'
        """)
    else:
        print("Column timezone already exists, skipping")
    
    conn.commit()
    print("\nMigration completed successfully!")
    
    # Verify columns
    cursor.execute("PRAGMA table_info(tasks)")
    columns = cursor.fetchall()
    print("\nUpdated table structure:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Update existing tasks to have default values
    print("\nUpdating existing tasks...")
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    print(f"Total tasks: {total_tasks}")
    
    if total_tasks > 0:
        cursor.execute("UPDATE tasks SET reminder_enabled = 0 WHERE reminder_enabled IS NULL")
        updated = cursor.rowcount
        print(f"Updated {updated} tasks with default reminder_enabled")
        
        cursor.execute("UPDATE tasks SET timezone = 'UTC' WHERE timezone IS NULL")
        updated = cursor.rowcount
        print(f"Updated {updated} tasks with default timezone")
    
    conn.commit()
    print("\nAll updates completed!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    migrate_database()

