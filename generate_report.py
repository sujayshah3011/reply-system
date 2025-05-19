import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
import sys

def generate_report(output_file="report.csv"):
    """Generate a detailed report of all replies in the database."""
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
            # Get all records
            result = connection.execute(text("SELECT * FROM replies ORDER BY id"))
            rows = result.fetchall()
            
            # Convert to DataFrame
            if rows:
                df = pd.DataFrame(rows, columns=result.keys())
                
                # Print summary
                print(f"Total records in database: {len(df)}")
                print(f"Platforms: {df['platform'].value_counts().to_dict()}")
                
                # Save to CSV
                df.to_csv(output_file, index=False)
                print(f"Report saved to {output_file}")
                
                # Print sample
                print("\nSample of generated replies:")
                for i, row in df.sample(min(5, len(df))).iterrows():
                    print(f"\nPlatform: {row['platform']}")
                    print(f"Post: {row['post_text'][:100]}...")
                    print(f"Reply: {row['generated_reply'][:100]}...")
                    print("-" * 50)
                
                return True
            else:
                print("No records found in the database.")
                return False
                
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return False

if __name__ == "__main__":
    output_file = "report.csv"
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    
    generate_report(output_file)