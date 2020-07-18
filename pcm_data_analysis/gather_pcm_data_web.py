import praw
import pandas as pd
from datetime import datetime
import json
import requests as r
import time

REDDIT = praw.Reddit("personal_bot", user_agent="personal_bot")
OUT_FP = 'pcm_data.json'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
URL = 'https://www.reddit.com/r/politicalcompassmemes/top.json?sort=top&t=all'


def handle_error(e_str, submission_data):
    print(e_str)
    with open(OUT_FP, 'w') as out_f:
        out_f.write(json.dumps(submission_data, sort_keys=True, indent=2))
    response = input('"s" to stop')
    if response == 's':
        exit()

def process_submission(submission, submission_data):
    author_id = submission['author']

    if author_id not in submission_data:
        submission_data[author_id] = {
            'flair': submission['author_flair_text'],
            'submissions': {}
        }

    if submission['id'] not in submission_data[author_id]['submissions']:
        submission_data[author_id]['submissions'][submission['id']] = {
            'created_utc': submission['created_utc'],
            'domain': submission['domain'],
            'total_awards_received': submission['total_awards_received'],
            'num_comments': submission['num_comments'],
            'score': submission['score'],
            'upvote_ratio': submission['upvote_ratio']
        }
    else:
        raise ValueError("Duplicated Post")

def process_page(response_json, submission_data, count):
    submissions = response_json['data']['children']

    for submission in submissions:
        try:
            process_submission(submission['data'], submission_data)

            count += 1
            print(f'Processed {count} threads.')
        except Exception as e:
            handle_error(repr(e), submission_data)

    return count

def main():
    count = 0
    submission_data = {}

    try:
        url = URL
        while count < 1000:
            time.sleep(2)
            response = r.get(url, headers=HEADERS)
            if response.status_code == 200:
                response_json = response.json()
                count = process_page(response_json, submission_data, count)

                next_page = response_json['data']['after']
                if next_page is not None:
                    print('New Page...')
                    url = URL + '&after=' + next_page

            else:
                handle_error('Bad response', submission_data)

    except Exception as e:
        handle_error(repr(e), submission_data)

    with open(OUT_FP, 'w') as out_f:
        out_f.write(json.dumps(submission_data, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()