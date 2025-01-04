import sys, os, argparse, json, io

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
    },
    system_instruction=" ".join([
        "You are an expert at analyzing and summarizing academic papers.",
        "Please use $TeX$ to write mathematical equations.",
        "Please only return the results, and do not include any comments.",
    ]),
)

prompts = [
    ("# Abstract", "論文の最初にあるAbstractを日本語に翻訳してください。"),
    ("# 概要", "日本語で、一行の文章で要約してください。"),
    ("## 問題意識", "論文はどのような問題を解決しようとしていますか？日本語で回答してください。"),
    ("## 手法", "論文はどのような手法を提案していますか？日本語で回答してください。"),
    ("## 新規性", "論文はどのような新規性がありますか？日本語で回答してください。"),
    ("# 章構成", """章構成を JSON の配列で出力してください。例:
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
sprompt = "セクション「%s」を日本語で要約してください。"

class Section:
    def __init__(self, title=""):
        self.title = title
        self.num = title.split(" ")[0]
        self.parent = None
        self.children = []
      
    def is_parent(self, section):
        return section.num.startswith(self.num + ".")

    def show(self, indent=-1, file=sys.stdout):
        if indent >= 0:
            print(("  " * indent) + "- " + self.title, file=file)
        for child in self.children:
            child.show(indent + 1, file)

    def __str__(self):
        sio = io.StringIO()
        self.show(file=sio)
        return sio.getvalue()

    def flatten(self):
        sections = [self.title]
        for child in self.children:
            sections += child.flatten()
        return sections

    def append(self, titles):
        last_child = self.children[-1] if self.children else None
        for i in range(len(titles)):
            section = Section(titles[i])
            if last_child and last_child.is_parent(section):
                return last_child.append(titles[i:])
            elif self.parent and not self.is_parent(section):
                return self.parent.append(titles[i:])
            self.children.append(section)
            section.parent = self
            last_child = section

def summarize_with_gemini(pdf_path):
    pdf_fn = os.path.splitext(pdf_path)[0]
    file = None
    result = ""
    i = 0
    sections = Section()
    seclen = 0
    try:
        while True:
            i += 1
            if i <= len(prompts):
                title = prompts[i - 1][0]
                prompt = prompts[i - 1][1]
            elif (j := i - len(prompts) - 1) < seclen:
                title = "## " + sections.children[j].title
                prompt = sprompt % "」「".join(sections.children[j].flatten())
            else:
                break
            md = f"{pdf_fn}-{i}.md"
            if os.path.exists(md):
                print(f"Skipping existing file: {md}")
                with open(md, "r", encoding="utf-8") as f:
                    text = f.read()
                if i == len(prompts):
                    json_str = text.split("```json")[2].split("```")[0]
                    sections.append(json.loads(json_str))
                    seclen = len(sections.children)
                lines = text.rstrip().splitlines()
                k = -1
                for j, line in enumerate(lines):
                    if line.startswith("> "):
                        k = j
                    elif k >= 0:
                        break
                k += 1
                while k < len(lines) and not lines[k]:
                    k += 1
                rtext = "\n".join(lines[k:]) + "\n"
            else:
                if not file:
                    file = genai.upload_file(pdf_path, mime_type="application/pdf")
                    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
                plines = prompt.rstrip().splitlines()
                if seclen:
                    print(f"Prompt {i}/{len(prompts) + seclen}: {plines[0]}")
                else:
                    print(f"Prompt {i}: {plines[0]}")
                response = model.generate_content([file, prompt], stream=True)
                text = f"# Prompt {i}\n\n"
                for line in plines:
                    text += f"> {line}\n"
                rtext = ""
                for chunk in response:
                    chunk_text = chunk.text
                    print(chunk_text, end="", flush=True)
                    rtext += chunk_text
                if not rtext.endswith("\n"):
                    print(flush=True)
                rtext = rtext.rstrip() + "\n"
                if i == len(prompts):
                    json_str = rtext.split("```json")[1].split("```")[0]
                    sections.append(json.loads(json_str))
                    seclen = len(sections.children)
                    rtext += "\n" + str(sections)
                text += "\n" + rtext
                with open(md, "w", encoding="utf-8") as f:
                    f.write(text)
            if i > 1:
                result += "\n"
            result += title + "\n\n" + rtext
    except Exception as e:
        print(f"Error generating summary at line {sys.exc_info()[2].tb_lineno}: {e}")
    finally:
        if file:
            genai.delete_file(file.name)
            print(f"Deleted file '{file.display_name}' from: {file.uri}")
    return result, pdf_fn + ".md"

def main():
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
