# Gemini Paper Summarizer

## Overview

A command-line tool that uses Gemini API to generate summaries of academic papers.

Note: Currently, the output is in Japanese only.

## Examples

Note: The following examples are in Japanese.

- [Attention Is All You Need](https://7shi.hateblo.jp/entry/2025/01/04/204353)
- [Large Concept Models: Language Modeling in a Sentence Representation Space](https://7shi.hateblo.jp/entry/2025/01/04/232224)
- [Text Embeddings Reveal (Almost) As Much As Text](https://7shi.hateblo.jp/entry/2025/01/05/203512)

- [DeepSeek LLM: Scaling open-source language models with longtermism.](https://7shi.hateblo.jp/entry/2025/01/07/225023)
- [DeepSeek-V2: A strong, economical, and efficient Mixture-of-Experts language model.](https://7shi.hateblo.jp/entry/2025/01/07/234352)
- [DeepSeek-Coder-V2: Breaking the barrier of closed-source models in code intelligence.](https://7shi.hateblo.jp/entry/2025/01/07/235825)
- [DeepSeek-V3 Technical Report](https://7shi.hateblo.jp/entry/2025/01/08/000133)

## Prerequisites

- Python 3.10+
- Gemini API Key (obtain from [Google AI Studio](https://aistudio.google.com/))

Note: If you find it difficult to set up the environment locally, please refer to the following Google Colab Notebook by @shoei05 (explained in Japanese):

- [論文要約 gemini-paper-summarizer を Google Colab で使用する](https://colab.research.google.com/drive/1yj02UYLNjXvz4nInB5zGzvrcawaJ_Mua?usp=sharing)

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
uv run gp-summarize path/to/paper.pdf
```

The tool will generate several markdown files with different types of summaries:

1. A Japanese translation of the abstract
2. A Japanese summary of the entire paper
3. A JSON structure of the paper's chapters and sections
4. Individual summaries (not translations) for each main section
5. Summaries of 1-4 above combined into a single file

The output files will be named based on the input PDF filename. Files 1-4 above will be saved in a directory and numbered continuously (e.g., `paper/001.md`, `paper/002.md`, etc.). The combined file will be named `paper.md`.

Note: If the process is interrupted (e.g. by Ctrl+C or by a 429 rate limit error, etc.), the process can be re-run smoothly, because any existing output files will be skipped.

### Output Format

For each prompt, the tool generates a markdown file containing:

- Title (prompt number)
- Statistics information about tokens
- Prompt
- AI-generated response

The section structure will be displayed in both JSON format and as a hierarchical list.

## License

CC0 1.0 Universal
