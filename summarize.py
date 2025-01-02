#!/usr/bin/env python3
import os
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

prompts = [
    "日本語で要約してください。"
]

def summarize_with_gemini(pdf_path):
    """
    Generate a summary using Gemini AI.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        str: Generated summary
    """
    
    pdf_bn = os.path.splitext(os.path.basename(pdf_path))[0]
    file = None
    result = ""
    try:
        file = genai.upload_file(pdf_path, mime_type="application/pdf")
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        chat_session = model.start_chat(history=[
            {"role": "user", "parts": [file]}
        ])
        for i, prompt in enumerate(prompts, 1):
            response = chat_session.send_message(prompt)
            text = f"# Prompt {i}\n\n> {prompt}\n\n{response.text.rstrip()}\n"
            with open(f"{pdf_bn}-{i}.md", "w", encoding="utf-8") as f:
                f.write(text)
            if i:
                result += "\n"
            result += text
    except Exception as e:
        print(f"Error generating summary: {e}")
    finally:
        if file:
            genai.delete_file(file.name)
            print(f"Deleted file '{file.display_name}' from: {file.uri}")
    return result

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
    output = args.output or (os.path.splitext(os.path.basename(args.pdf_path))[0] + ".md")
    with open(output, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary saved: {output}")

if __name__ == '__main__':
    main()
