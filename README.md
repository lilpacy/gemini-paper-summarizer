# Gemini Paper Summarizer

## Overview
A command-line tool that uses Google's Gemini AI to generate summaries of academic papers.

## Prerequisites
- Python 3.10+
- Gemini AI API Key (obtain from [Google AI Studio](https://aistudio.google.com/))

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   uv sync
   ```
3. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
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
Creative Commons Zero v1.0 Universal (CC0 1.0)
