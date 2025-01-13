import os, argparse, json

from .section import Section
from . import gemini

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Load after reading environment variables
import google.generativeai as genai

max_rpm  = 10  # maximum requests per minute

model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash-exp",
    generation_config={
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
    system_instruction="""
You are an expert at analyzing and summarizing academic papers.
Please use $TeX$ to write mathematical equations.
Please only return the results, and do not include any comments.
日本語は「だ・である調」を使用してください。
""".strip(),
)

prompts = [
    ("# Abstract", "論文の最初にあるAbstractを日本語に翻訳してください。"),
    ("# 概要", "日本語で、一行の文章で要約してください。"),
    ("## 問題意識", "論文はどのような問題を解決しようとしていますか？日本語で回答してください。"),
    ("## 手法", "論文はどのような手法を提案していますか？日本語で回答してください。"),
    ("## 新規性", "論文はどのような新規性がありますか？日本語で回答してください。"),
    ("# 章構成", """章構成を翻訳せずにJSONの配列で出力してください。例:
```json
[
  "1 Introduction",
  "1.1 Background",
  "2 Methods",
  "2.1 Data",
  "2.1.1 Dataset"
]
```"""),
]
sprompt = ("セクション「%s」を日本語で要約してください。", "」「")

def summarize_with_gemini(pdf_path, output, output_dir):
    if output:
        outdir, ext = os.path.splitext(output)
        if not ext:
            output += ".md"
    else:
        outdir = os.path.splitext(pdf_path)[0]
        output = outdir + ".md"
    if output_dir:
        outdir = os.path.join(output_dir, os.path.basename(outdir))
        output = os.path.join(output_dir, os.path.basename(output))
    file = None
    result = ""
    i = 0
    sections = Section()
    seclen = 0
    stats = {}
    try:
        while True:
            i += 1
            if i <= len(prompts):
                title = prompts[i - 1][0]
                prompt = prompts[i - 1][1]
            elif (j := i - len(prompts) - 1) < seclen:
                title = "## " + sections.children[j].title
                prompt = sprompt[0] % sprompt[1].join(sections.children[j].flatten())
            else:
                break
            md = os.path.join(outdir, f"{i:03d}.md")
            if os.path.exists(md):
                print(f"Skipping existing file: {md}")
                with open(md, "r", encoding="utf-8") as f:
                    text = f.read()

                # Get the section structure
                if i == len(prompts) and "```json" in text:
                    json_str = text.split("```json")[2].split("```")[0]
                    sections.append(json.loads(json_str))
                    seclen = len(sections.children)
                lines = text.rstrip().splitlines()

                # Get the statistics and the response
                k = -1
                for j, line in enumerate(lines):
                    if line.startswith("> "):
                        k = j
                    elif k < 0:
                        gemini.update_stats(stats, *gemini.get_kv(line))
                k += 1
                while k < len(lines) and not lines[k]:
                    k += 1
                rtext = "\n".join(lines[k:]) + "\n"
            else:
                # Upload the file
                if not file:
                    file = genai.upload_file(pdf_path, mime_type="application/pdf")
                    print(f"Uploaded file '{file.display_name}' as: {file.uri}")

                # Prepare the prompt
                plines = prompt.rstrip().splitlines()
                text = f"# Prompt {i}\n\n"
                if seclen:
                    print(f"Prompt {i}/{len(prompts) + seclen}: {plines[0]}")
                else:
                    print(f"Prompt {i}: {plines[0]}")

                # Get the response and statistics
                rtext, usage = gemini.generate_content(model, max_rpm, file, prompt)

                # Get the section structure
                if i == len(prompts) and "```json" in rtext:
                    json_str = rtext.split("```json")[1].split("```")[0]
                    sections.append(json.loads(json_str))
                    seclen = len(sections.children)
                    rtext += "\n" + str(sections)

                # Calculate and show the statistics
                for k, v in gemini.iter_stats(usage):
                    gemini.update_stats(stats, k, v)
                    text += f"{k}: {v}\n"
                text += "\n"
                gemini.show_stats(usage)

                # Add the prompt and response
                for line in plines:
                    text += f"> {line}\n"
                text += "\n" + rtext

                # Save the file
                os.makedirs(outdir, exist_ok=True)
                with open(md, "w", encoding="utf-8") as f:
                    f.write(text)

            # Remove JSON from the section structure
            if i == len(prompts) and (json_start := rtext.find("```json")) >= 0:
                if (json_end := rtext.find("```", json_start + 7)) >= 0:
                    if (section_start := rtext.find("\n\n", json_end)) >= 0:
                        rtext = rtext[section_start+2:]

            # Add to the result
            if i > 1:
                result += "\n"
            result += title + "\n\n" + rtext
    finally:
        if file:
            genai.delete_file(file.name)
            print(f"Deleted file '{file.display_name}' from: {file.uri}")

    gemini.set_stats(stats)
    return result, output, stats

def main():
    parser = argparse.ArgumentParser(description='Summarize academic papers using Gemini API')
    parser.add_argument('pdf_paths', nargs='+', help='Path(s) to one or more PDF files')
    parser.add_argument('-d', '--output-dir', help='Output directory for intermediate files')
    parser.add_argument('-o', '--output', help='Output file for summary')
    args = parser.parse_args()
    pdfs = len(args.pdf_paths)
    if args.output:
        if args.output_dir:
            parser.error("Output directory (-d) cannot be specified when an output file (-o) is provided.")
        if pdfs > 1:
            parser.error("Output file (-o) cannot be specified when multiple PDF files are provided.")

    for i, pdf_path in enumerate(args.pdf_paths, 1):
        if i > 1:
            print()
        if pdfs > 1:
            print(f"==== PDF {i}/{pdfs}: {pdf_path}")
        summary, output, stats = summarize_with_gemini(pdf_path, args.output, args.output_dir)
        with open(output, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved: {output}")
        print("Statistics:")
        gemini.show_stats(stats, "- ")

if __name__ == '__main__':
    main()
