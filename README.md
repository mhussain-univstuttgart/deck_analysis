# Pitch Deck Tracker

A web application that helps track changes in pitch decks using AI-powered analysis. The application allows users to upload PDF pitch decks and automatically analyzes the differences between versions, providing insights into content changes, meaning changes, additions, removals, and tone changes.

## Features

- Upload PDF pitch decks
- Automatic text extraction from PDFs
- AI-powered analysis of changes between versions
- Modern, responsive UI
- Real-time feedback on changes

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd deck_tracking
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python main.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload your pitch deck PDF files through the web interface

4. View the analysis results showing the differences between versions

## Project Structure

```
deck_tracking/
├── api/
│   ├── app/
│   │   ├── __init__.py      # Flask app initialization
│   │   └── routes.py        # API routes
│   └── utils/
│       ├── pdf_utils.py     # PDF processing utilities
│       └── ai_utils.py      # OpenAI integration
├── web/
│   └── templates/
│       └── index.html       # Main template (HTML, CSS, JS combined)
├── uploads/                 # Directory for uploaded PDFs
├── .env                    # Environment variables
├── main.py                 # Application entry point
└── requirements.txt        # Project dependencies
```

## Security Notes

- The application limits file uploads to PDF files only
- Maximum file size is set to 16MB
- Files are stored with timestamped names to prevent overwrites
- API keys should be kept secure and never committed to version control

## License

MIT License 