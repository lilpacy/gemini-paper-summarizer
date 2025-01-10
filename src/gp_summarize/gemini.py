import math, time, re
from datetime import datetime, timedelta

interval = 60 + 1  # with margin

timestamps = []

# Limit the number of requests per minute
def generate_content(model, max_rpm, *args):
    # Wait due to rate limiting
    if 0 < max_rpm <= len(timestamps):
        t = timestamps[-max_rpm]
        if (td := (datetime.now() - t).total_seconds()) < interval:
            wait = math.ceil(interval - td)
            print(f"Waiting {wait} seconds...")
            time.sleep(wait)

    # Get the response
    time1 = datetime.now()
    time2 = None
    rtext = ""
    response = model.generate_content(args, stream=True)
    for chunk in response:
        if not time2:
            time2 = datetime.now()
        chunk_text = chunk.text
        print(chunk_text, end="", flush=True)
        rtext += chunk_text
    time3 = datetime.now()
    timestamps.append(time3)
    if not rtext.endswith("\n"):
        print(flush=True)
    rtext = rtext.rstrip() + "\n"

    # Get the statistics
    chunk_dict = chunk.to_dict()
    if "usage_metadata" in chunk_dict:
        usage = chunk_dict["usage_metadata"]
        usage["prompt_eval_duration"    ] = int((time2 - time1).total_seconds() * 1000)  # in ms
        usage["candidates_eval_duration"] = int((time3 - time2).total_seconds() * 1000)  # in ms
        set_stats(usage)
    else:
        usage = {}

    return rtext, usage

def set_stats(st):
    dur1 = st.get("prompt_eval_duration"    , 0)
    dur2 = st.get("candidates_eval_duration", 0)
    if dur1 < 1 or dur2 < 1:
        return
    st["prompt_eval_rate"    ] = f'{st["prompt_token_count"    ] / (dur1 / 1000):.2f} tps'
    st["candidates_eval_rate"] = f'{st["candidates_token_count"] / (dur2 / 1000):.2f} tps'

def get_kv(line):
    if m := re.match(r"^([a-zA-Z_]+): (.*)$", line):
        k, v = m.group(1), m.group(2)
        if v.isdigit():
            return k, int(v)
        return k, v
    else:
        return None, None

def update_stats(st, k, v):
    if not k:
        return
    st.setdefault(k, 0)
    if not k.endswith("_rate"):
        st[k] += v

def iter_stats(st):
    keys = [
        "cached_content_token_count",
        "prompt_token_count",
        "prompt_eval_duration",
        "prompt_eval_rate",
        "candidates_token_count",
        "candidates_eval_duration",
        "candidates_eval_rate",        
        "total_token_count",
    ]
    st_keys = list(st.keys())
    for k in keys:
        if k in st:
            v = st[k]
            if k.endswith("_duration"):
                yield k, v, timedelta(milliseconds=v)
            else:
                yield k, v, v
            st_keys.remove(k)
    for k in st_keys:
        yield k, st[k], st[k]
