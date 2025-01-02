import os, argparse

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
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
    "日本語で要約してください。",
    """章構成を JSON で出力してください。例:
```json
[
  {
    "title": "Introduction",
    "sub": [
      {
        "title": "Background"
      }
    ]
  }
]
```""",
]

def summarize_with_gemini(pdf_path):
    """
    Generate a summary using Gemini AI.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        str: Generated summary
    """
    
    pdf_fn = os.path.splitext(pdf_path)[0]
    file = None
    chat_session = None
    result = ""
    try:
        for i, prompt in enumerate(prompts, 1):
            md = f"{pdf_fn}-{i}.md"
            if os.path.exists(md):
                with open(md, "r", encoding="utf-8") as f:
                    text = f.read()
                print(f"Skipping existing file: {md}")
            else:
                if not file:
                    file = genai.upload_file(pdf_path, mime_type="application/pdf")
                    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
                    chat_session = model.start_chat(history=[
                        {"role": "user", "parts": [file]}
                    ])
                response = chat_session.send_message(prompt)
                text = f"# Prompt {i}\n\n"
                for line in prompt.rstrip().split("\n"):
                    text += f"> {line}\n"
                text += f"\n{response.text.rstrip()}\n"
                with open(md, "w", encoding="utf-8") as f:
                    f.write(text)
            if i > 1:
                result += "\n"
            result += text
    except Exception as e:
        print(f"Error generating summary: {e}")
    finally:
        if file:
            genai.delete_file(file.name)
            print(f"Deleted file '{file.display_name}' from: {file.uri}")
    return result, pdf_fn + ".md"

def main():
    """
    Main CLI entry point for paper summarization.
    """
    parser = argparse.ArgumentParser(description='Summarize academic papers using Gemini AI')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output file for summary')
    args = parser.parse_args()

    summary, output = summarize_with_gemini(args.pdf_path)
    with open(args.output or output, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary saved: {output}")

if __name__ == '__main__':
    main()
