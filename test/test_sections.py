import json, io
from src.section import Section

def test(name, json_str, expected):
    root = Section()
    root.append(json.loads(json_str))
    sio = io.StringIO()
    root.show(file=sio)
    result = sio.getvalue()
    if result == expected:
        print("[OK]", name)
    else:
        print("[NG]", name)
        print("Result:")
        print(result.rstrip())
        print("Expected:")
        print(expected.rstrip())

test("基本的な階層構造", '''[
    "1 Introduction",
    "1.1 Background",
    "1.2 Related Work",
    "2 Methods",
    "2.1 Data",
    "2.1.1 Dataset"
]''', """
- 1 Introduction
  - 1.1 Background
  - 1.2 Related Work
- 2 Methods
  - 2.1 Data
    - 2.1.1 Dataset
""".lstrip())

test("深い階層構造", '''[
    "1 First",
    "1.1 Second",
    "1.1.1 Third",
    "1.1.1.1 Fourth"
]''', """
- 1 First
  - 1.1 Second
    - 1.1.1 Third
      - 1.1.1.1 Fourth
""".lstrip())

test("複数のトップレベルセクション", '''[
    "1 First Section",
    "1.1 Sub A",
    "2 Second Section",
    "2.1 Sub B",
    "3 Third Section"
]''', """
- 1 First Section
  - 1.1 Sub A
- 2 Second Section
  - 2.1 Sub B
- 3 Third Section
""".lstrip())

test("階層をスキップするケース", '''[
    "1 First",
    "1.1 Second",
    "1.1.1 Third",
    "1.2 Back to Second Level"
]''', """
- 1 First
  - 1.1 Second
    - 1.1.1 Third
  - 1.2 Back to Second Level
""".lstrip())
