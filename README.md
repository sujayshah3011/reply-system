# Social Media Reply Generator

A FastAPI and Streamlit application that generates authentic, human-like replies to social media posts using Google's Gemini AI and stores them in a Neon.tech PostgreSQL database.

## Features

- Generate platform-specific replies for Twitter, LinkedIn, and Instagram
- Tone and intent matching for more authentic responses
- Database storage of generated replies
- Support for both SQLite (local) and Neon.tech PostgreSQL (cloud) databases
- Batch processing of posts from CSV files
- Web interface for viewing stored replies

<img width="1437" alt="Screenshot 2025-05-20 at 1 10 53 PM" src="https://github.com/user-attachments/assets/0e18fe76-3151-4fea-9b9f-4a0e4cdbe740" />


## Project Structure

| File                 | Description                                                                 |
| -------------------- | --------------------------------------------------------------------------- |
| `app.py`             | FastAPI backend application that handles API requests and generates replies |
| `streamlit_app.py`   | Streamlit frontend for submitting individual posts and viewing replies      |
| `database.py`        | Database module that supports both SQLite and Neon.tech PostgreSQL          |
| `process_csv.py`     | Script to process posts from a CSV file and store replies in the database   |
| `view_replies.py`    | Streamlit application to view all replies stored in the database            |
| `generate_report.py` | Script to generate a CSV report of all replies in the database              |
| `requirements.txt`   | List of Python dependencies                                                 |
| `.env.example`       | Example environment variables file                                          |

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/sujayshah3011/reply-system
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
   - Set `NEON_DB_URL` to your Neon.tech connection string (format: `postgresql://username:password@hostname/database`)

## Commands and Functionality

### Running the Main Application

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

### Processing CSV Files

Process posts from a CSV file and store generated replies in the database:

```
python process_csv.py [csv_file_path] [limit]
```

- `csv_file_path`: Path to the CSV file (default: `posts.csv`)
- `limit`: Optional number of posts to process (default: all posts)

Example:

```
python process_csv.py posts.csv 5  # Process first 5 posts
python process_csv.py posts.csv     # Process all posts
```

### Viewing Replies in the Database

Launch a web interface to view all replies stored in the database:

```
streamlit run view_replies.py
```

This will open a browser window with a dashboard showing:

- Total number of replies
- Platform distribution
- Filtering options
- Expandable view of each reply

### Generating Reports

Generate a CSV report of all replies in the database:

```
python generate_report.py [output_file]
```

- `output_file`: Path to save the CSV report (default: `report.csv`)

Example:

```
python generate_report.py my_report.csv
```

## API Endpoints

- `GET /`: Health check endpoint
- `POST /reply`: Generate a reply for a social media post

### POST /reply

Request body:

```json
{
  "platform": "Twitter", // or "LinkedIn" or "Instagram"
  "post_text": "Your post text here"
}
```

Response:

```json
{
  "platform": "Twitter",
  "post_text": "Your post text here",
  "generated_reply": "The generated reply",
  "timestamp": "2023-05-19T12:34:56.789012"
}
```

## License

[MIT License](LICENSE)
