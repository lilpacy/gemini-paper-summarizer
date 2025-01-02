#!/usr/bin/env python3
import argparse
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash-exp",
    generation_config={
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
)

def summarize_with_gemini(pdf_path, length="medium", focus=None):
    """
    Generate a summary using Gemini AI.
    
    Args:
        pdf_path (str): Path to the PDF file
        length (str): Length of summary (short/medium/long)
        focus (str, optional): Specific focus area for summary
    
    Returns:
        str: Generated summary
    """
    length_map = {
        'short': 'Provide a concise 3-4 sentence summary.',
        'medium': 'Provide a balanced summary of 5-7 sentences.',
        'long': 'Provide a comprehensive summary covering key points in detail.'
    }
    
    prompt = f"{length_map.get(length, length_map['medium'])}\n"
    if focus:
        prompt += f"Focus specifically on: {focus}\n"
    prompt += "Please read and summarize this academic paper."
    
    file = None
    try:
        file = genai.upload_file(pdf_path, mime_type="application/pdf")
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        chat_session = model.start_chat(history=[
            {"role": "user", "parts": [file]}
        ])
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""
    finally:
        if file:
            genai.delete_file(file.name)
            print(f"Deleted file '{file.display_name}' from: {file.uri}")

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
    
    # Generate summary
    summary = summarize_with_gemini(args.pdf_path, args.length, args.focus)
    
    # Output summary
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"Summary saved to {args.output}")
    else:
        print(summary)

if __name__ == '__main__':
    main()
