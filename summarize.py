#!/usr/bin/env python3
import argparse
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def read_pdf_file(pdf_path):
    """
    Read PDF file as binary data
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        bytes: PDF file content
    """
    try:
        with open(pdf_path, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        sys.exit(1)

def summarize_with_gemini(pdf_data, length='medium', focus=None):
    """
    Generate a summary using Gemini AI.
    
    Args:
        pdf_data (bytes): PDF file content
        length (str): Length of summary (short/medium/long)
        focus (str, optional): Specific focus area for summary
    
    Returns:
        str: Generated summary
    """
    # Validate API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: Google API key not found. Set GEMINI_API_KEY in .env file.")
        sys.exit(1)

    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash-exp",
    )
    
    # Construct prompt
    length_map = {
        'short': 'Provide a concise 3-4 sentence summary.',
        'medium': 'Provide a balanced summary of 5-7 sentences.',
        'long': 'Provide a comprehensive summary covering key points in detail.'
    }
    
    prompt = f"{length_map.get(length, length_map['medium'])}\n"
    if focus:
        prompt += f"Focus specifically on: {focus}\n"
    prompt += "Please read and summarize this academic paper."
    
    try:
        response = model.generate_content([prompt, pdf_data])
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        sys.exit(1)

def main():
    """
    Main CLI entry point for paper summarization.
    """
    parser = argparse.ArgumentParser(description='Summarize academic papers using Gemini AI')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-l', '--length', 
                        choices=['short', 'medium', 'long'], 
                        default='medium', 
                        help='Length of summary')
    parser.add_argument('-f', '--focus', 
                        help='Specific focus area for summary')
    parser.add_argument('-o', '--output', 
                        help='Output file for summary')
    
    args = parser.parse_args()
    
    # Read PDF file
    pdf_data = read_pdf_file(args.pdf_path)
    
    # Generate summary
    summary = summarize_with_gemini(pdf_data, args.length, args.focus)
    
    # Output summary
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"Summary saved to {args.output}")
    else:
        print(summary)

if __name__ == '__main__':
    main()
