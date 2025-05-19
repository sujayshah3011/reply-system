import streamlit as st
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

def main():
    st.set_page_config(page_title="Social Media Replies Viewer", page_icon="📊", layout="wide")
    st.title("Social Media Replies Viewer")
    
    # Load environment variables
    load_dotenv()
    
    # Check if Neon is enabled
    use_neon = os.getenv("USE_NEON", "false").lower() == "true"
    db_url = os.getenv("NEON_DB_URL")
    
    if not use_neon or not db_url:
        st.error("Neon.tech database is not configured. Please check your .env file.")
        return
    
    try:
        # Create engine and connect to database
        engine = create_engine(db_url)
        
        # Query the database
        with engine.connect() as connection:
            # Get all records
            result = connection.execute(text("SELECT * FROM replies ORDER BY id DESC"))
            rows = result.fetchall()
            
            if not rows:
                st.warning("No replies found in the database.")
                return
            
            # Convert to DataFrame
            df = pd.DataFrame(rows, columns=result.keys())
            
            # Display statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Replies", len(df))
            with col2:
                st.metric("Platforms", len(df['platform'].unique()))
            with col3:
                platform_counts = df['platform'].value_counts().to_dict()
                platform_str = ", ".join([f"{k}: {v}" for k, v in platform_counts.items()])
                st.metric("Platform Distribution", platform_str)
            
            # Filter options
            st.subheader("Filter Replies")
            platforms = ["All"] + sorted(df['platform'].unique().tolist())
            selected_platform = st.selectbox("Select Platform", platforms)
            
            # Apply filters
            filtered_df = df
            if selected_platform != "All":
                filtered_df = df[df['platform'] == selected_platform]
            
            # Display replies
            st.subheader(f"Viewing {len(filtered_df)} Replies")
            
            for i, row in filtered_df.iterrows():
                with st.expander(f"{row['platform'].upper()} - {row['post_text'][:100]}..."):
                    st.write(f"**Post:**")
                    st.write(row['post_text'])
                    st.write(f"**Generated Reply:**")
                    st.write(row['generated_reply'])
                    st.write(f"**Timestamp:** {row['timestamp']}")
    
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    main()