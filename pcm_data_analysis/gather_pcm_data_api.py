import praw
import pandas as pd
from datetime import datetime
import json
import requests as r
import time

REDDIT = praw.Reddit("personal_bot", user_agent="personal_bot")
OUT_FP = 'pcm_data.json'


def handle_error(e_str, submission_data):
    print(e_str)
    with open(OUT_FP, 'w') as out_f:
        out_f.write(json.dumps(submission_data, sort_keys=True, indent=2))
    response = input('"s" to stop')
    if response == 's':
        exit()

def process_submission(submission, submission_data):
    if submission.author is None:
        author_id = '[deleted]'
    else:
        author_id = submission.author.name

    if author_id not in submission_data:
        submission_data[author_id] = {
            'flair': submission.author_flair_text,
            'submissions': {}
        }

    if submission.id not in submission_data[author_id]['submissions']:
        submission_data[author_id]['submissions'][submission.id] = {
            'created_utc': submission.created_utc,
            'domain': submission.domain,
            'total_awards_received': submission.total_awards_received,
            'num_comments': submission.num_comments,
            'score': submission.score,
            'upvote_ratio': submission.upvote_ratio
        }
    else:
        raise ValueError("Duplicated Post")


def main():
    count = 0
    submission_data = {}

    try:
        for submission in REDDIT.subreddit('politicalcompassmemes').top('all', limit=100000):
            try:
                process_submission(submission, submission_data)
                count += 1
                print(f'Processed Submissions: {count}')

                if count > 100000:
                    break

                if (count % 1000) == 0:
                    with open(OUT_FP, 'w') as out_f:
                        out_f.write(json.dumps(submission_data, sort_keys=True, indent=2))

            except Exception as e:
                handle_error(repr(e), submission_data)
    except Exception as e:
        handle_error(repr(e), submission_data)

    with open(OUT_FP, 'w') as out_f:
        out_f.write(json.dumps(submission_data, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()