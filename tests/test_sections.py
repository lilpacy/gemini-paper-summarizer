import json
import io

from gp_summarize.section import Section

def get_result(json_str):
    root = Section()
    root.append(json.loads(json_str))
    sio = io.StringIO()
    root.show(file=sio)
    return sio.getvalue()

def test_basic_hierarchy():
    json_str = '''[
        "1 Introduction",
        "1.1 Background",
        "1.2 Related Work",
        "2 Methods",
        "2.1 Data",
        "2.1.1 Dataset"
    ]'''
    expected = """
- 1 Introduction
  - 1.1 Background
  - 1.2 Related Work
- 2 Methods
  - 2.1 Data
    - 2.1.1 Dataset
""".lstrip()
    result = get_result(json_str)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

def test_deep_hierarchy():
    json_str = '''[
        "1 First",
        "1.1 Second",
        "1.1.1 Third",
        "1.1.1.1 Fourth"
    ]'''
    expected = """
- 1 First
  - 1.1 Second
    - 1.1.1 Third
      - 1.1.1.1 Fourth
""".lstrip()
    result = get_result(json_str)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

def test_multiple_top_level_sections():
    json_str = '''[
        "1 First Section",
        "1.1 Sub A",
        "2 Second Section",
        "2.1 Sub B",
        "3 Third Section"
    ]'''
    expected = """
- 1 First Section
  - 1.1 Sub A
- 2 Second Section
  - 2.1 Sub B
- 3 Third Section
""".lstrip()
    result = get_result(json_str)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

def test_hierarchy_skip():
    json_str = '''[
        "1 First",
        "1.1 Second",
        "1.1.1 Third",
        "1.2 Back to Second Level"
    ]'''
    expected = """
- 1 First
  - 1.1 Second
    - 1.1.1 Third
  - 1.2 Back to Second Level
""".lstrip()
    result = get_result(json_str)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"
