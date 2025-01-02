# Gemini Paper Summarizer

## Overview
A command-line tool that uses Gemini API to generate summaries of academic papers.

## Prerequisites
- Python 3.10+
- Gemini API Key (obtain from [Google AI Studio](https://aistudio.google.com/))

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   uv sync
   ```
3. Create a `.env` file in the project directory with your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage
```bash
uv run summarize.py path/to/paper.pdf
```

The tool will generate several markdown files with different types of summaries:
1. A Japanese summary of the entire paper
2. A Japanese translation of the abstract
3. A JSON structure of the paper's chapters and sections
4. Individual summaries for each main section

The output files will be named based on the input PDF filename with a numerical suffix (e.g., `paper-1.md`, `paper-2.md`, etc.).

### Output Format
For each prompt, the tool generates a markdown file containing:
- The original prompt
- The AI-generated response

The section structure will be displayed in both JSON format and as a hierarchical list.

## License
CC0 1.0 Universal
