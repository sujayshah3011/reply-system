# Social Media Reply Generator

A FastAPI and Streamlit application that generates authentic, human-like replies to social media posts using Google's Gemini AI.

## Features

- Generate platform-specific replies for Twitter, LinkedIn, and Instagram
- Tone and intent matching for more authentic responses
- Database storage of generated replies
- Support for both SQLite (local) and Neon.tech PostgreSQL (cloud) databases

## Setup

1. Clone the repository:

   ```
   git clone <your-repository-url>
   cd Social-Media-Replier
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key
   - (Optional) Configure Neon.tech database settings

## Database Configuration

The application supports two database options:

### SQLite (Default)

- No additional configuration needed
- Data is stored locally in `replies.db`

### Neon.tech PostgreSQL

1. Create a Neon.tech account and database
2. In your `.env` file:
   - Set `USE_NEON=true`
   - Set `NEON_DB_URL` to your Neon.tech connection string

## Running the Application

1. Start the FastAPI backend:

   ```
   uvicorn app:app --reload
   ```

2. In a separate terminal, start the Streamlit frontend:

   ```
   streamlit run streamlit_app.py
   ```

3. Open your browser and navigate to:
   - FastAPI Swagger UI: http://localhost:8000/docs
   - Streamlit UI: http://localhost:8501

## API Endpoints

- `GET /`: Health check endpoint
- `POST /reply`: Generate a reply for a social media post

## License

[MIT License](LICENSE)
