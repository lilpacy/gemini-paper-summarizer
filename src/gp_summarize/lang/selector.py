import locale

languages = {
    "ja": "ja",
    "Japanese": "ja",
}

def get_language(lang):
    for k, v in languages.items():
        if lang.startswith(k):
            return v
    return ""

def init(lang):
    system_lang = get_language(lang if lang else locale.getlocale()[0])
    match system_lang:
        case "ja":
            from . import ja as lang_module
        case _:
            from . import en as lang_module
    return lang_module
