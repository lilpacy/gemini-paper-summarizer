import math, time
from datetime import datetime

interval = 60 + 5  # with margin

timestamps = []

# Limit the number of requests per minute
def generate_content(model, max_rpm, *args):
    if 0 < max_rpm <= len(timestamps):
        t = timestamps[-max_rpm]
        if (td := (datetime.now() - t).total_seconds()) < interval:
            wait = math.ceil(interval - td)
            print(f"Waiting {wait} seconds...")
            time.sleep(wait)
    timestamps.append(datetime.now())

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
    if not rtext.endswith("\n"):
        print(flush=True)
    rtext = rtext.rstrip() + "\n"

    # Get the statistics
    chunk_dict = chunk.to_dict()
    if "usage_metadata" in chunk_dict:
        usage = chunk_dict["usage_metadata"]
        usage["prompt_eval_duration"] = (time2 - time1).total_seconds()
        usage["prompt_eval_rate"] = usage["prompt_token_count"] / usage["prompt_eval_duration"]
        usage["candidate_eval_duration"] = (time3 - time2).total_seconds()
        usage["candidate_eval_rate"] = usage["candidates_token_count"] / usage["candidate_eval_duration"]
    else:
        usage = {}

    return rtext, usage
