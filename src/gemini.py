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
    return model.generate_content(args, stream=True)
