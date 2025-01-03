import json, src.summarize

def test_and_print(json_str, name=""):
    print(f"\nTest{f' {name}' if name else ''}:")
    print("Input:", json_str)
    root = src.summarize.Section()
    root.append(json.loads(json_str))
    print("Output:")
    root.show()

# テストケース1: 基本的な階層構造
test_and_print('''[
    "1 Introduction",
    "1.1 Background",
    "1.2 Related Work",
    "2 Methods",
    "2.1 Data",
    "2.1.1 Dataset"
]''', "基本的な階層構造")

# テストケース2: 深い階層構造
test_and_print('''[
    "1 First",
    "1.1 Second",
    "1.1.1 Third",
    "1.1.1.1 Fourth"
]''', "深い階層構造")

# テストケース3: 複数のトップレベルセクション
test_and_print('''[
    "1 First Section",
    "1.1 Sub A",
    "2 Second Section",
    "2.1 Sub B",
    "3 Third Section"
]''', "複数のトップレベルセクション")

# テストケース4: 階層をスキップするケース
test_and_print('''[
    "1 First",
    "1.1 Second",
    "1.1.1 Third",
    "1.2 Back to Second Level"
]''', "階層をスキップするケース")
