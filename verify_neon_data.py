import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

def verify_neon_data():
    """Verify that data was stored in the Neon.tech database."""
    load_dotenv()
    
    # Check if Neon is enabled
    use_neon = os.getenv("USE_NEON", "false").lower() == "true"
    if not use_neon:
        print("Neon.tech is not enabled. Set USE_NEON=true in your .env file.")
        return False
    
    # Get database URL
    db_url = os.getenv("NEON_DB_URL")
    if not db_url:
        print("NEON_DB_URL is not set in your .env file.")
        return False
    
    try:
        # Create engine and test connection
        engine = create_engine(db_url)
        
        # Query the database
        with engine.connect() as connection:
            # Get the count of records
            count_result = connection.execute(text("SELECT COUNT(*) FROM replies"))
            count = count_result.fetchone()[0]
            
            # Get the most recent records
            result = connection.execute(text("SELECT * FROM replies ORDER BY id DESC LIMIT 10"))
            rows = result.fetchall()
            
            # Convert to DataFrame for better display
            if rows:
                df = pd.DataFrame(rows, columns=result.keys())
                
                # Print the results
                print(f"Total records in database: {count}")
                print("\nMost recent records:")
                print(df[['id', 'platform', 'post_text', 'generated_reply', 'timestamp']])
                
                return True
            else:
                print("No records found in the database.")
                return False
                
    except Exception as e:
        print(f"Error querying Neon.tech database: {str(e)}")
        return False

if __name__ == "__main__":
    verify_neon_data()