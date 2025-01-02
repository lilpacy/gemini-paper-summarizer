# Gemini Paper Summarizer

## Overview
A command-line tool that uses Google's Gemini AI to generate summaries of academic papers.

## Prerequisites
- Python 3.8+
- Google AI API Key (obtain from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google AI API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage
```bash
python summarize.py path/to/paper.pdf [options]
```

### Options
- `-l, --length`: Summary length (short, medium, long)
- `-f, --focus`: Specific focus area of summary
- `-o, --output`: Output file for summary

## License
MIT License
