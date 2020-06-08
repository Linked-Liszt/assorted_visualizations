import praw
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
sns.set(style='darkgrid')

THREADS_LIST = [
    "gsn4ws", # May 28
    "gt4313", # May 29
    "gtpe24", 
    "gu93m0",
    "guun48",
    "gvf2no",
    "gw3bkn",
    "gwrw6o",
    "gxeq0p",
    "gxwosn", 
    "gygnfo" # Jun 7
]

# Gather Data
reddit = praw.Reddit("personal_bot", user_agent="personal_bot")

num_comments = []
dates = []
for submission_id in THREADS_LIST:
    submission = reddit.submission(id=submission_id)
    num_comments.append(submission.num_comments)
    dates.append(datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d'))
    print(f"Read thread: {submission_id}")
    
# Plot Data
plt.plot(range(len(num_comments)), num_comments)
plt.xticks(range(len(num_comments)), dates)
plt.xlabel("Megathread Date")
plt.ylabel("Number of Comments")
plt.title("Interest in US Protests from r/news Megathread Comments", fontsize=30)
plt.show() 