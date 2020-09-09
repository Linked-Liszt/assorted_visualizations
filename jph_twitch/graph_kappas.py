import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import datetime

def script_main():
    args = parse_args()
    messages = extract_messages(args.log_fp)

    kappa_times, kappa_counts = get_kappa_rate(messages, args.window_size)

    plot_kappa_rate(kappa_times, kappa_counts)

def plot_kappa_rate(kappa_times, kappa_counts):
    with plt.xkcd():
        plt.plot_date(kappa_times, kappa_counts, linestyle='-')
        xformatter = mdates.DateFormatter('%H:%M:%S')
        plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        plt.show()

def get_kappa_rate(messages: list, window_size: int) -> (list, list):
    kappa_times = []
    kappa_counts = []
    window_end = datetime.datetime(2000, 1, 1,
                                   minute=int(window_size/60),
                                   second=(window_size % 60))
    kappa_count = 0
    for message in messages:
        if message.time.time() > window_end.time():
            kappa_times.append(window_end)
            kappa_counts.append(kappa_count)
            window_end += datetime.timedelta(seconds=window_size)
            kappa_count = 0
        
        if 'Kappa' in message.text:
            kappa_count += 1
    
    return kappa_times, kappa_counts 
        

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Graph A sliding window of kappa emoji\'s from twitch chat')
    parser.add_argument('log_fp', help='IRC formatted log file to read')
    parser.add_argument('--w', default=60, type=int, help='Sliding window size (seconds)', dest='window_size')

    return parser.parse_args()


def extract_messages(log_fp: str) -> list:
    with open(log_fp, 'r') as log_f:
        raw_lines = log_f.readlines()

    parsed_lines = []
    for line in raw_lines:
        capture = re.search(r'\[(.*)\] <(.*)> (.*)', line)
        # Time, User, Group

        parsed_lines.append(Message(capture.group(1), 
                                    capture.group(2), 
                                    capture.group(3)))
    return parsed_lines


class Message:
    def __init__(self, time_str, user, text):
        self.time_str = time_str
        self.user = user
        self.text = text
        self.time = self._parse_time(time_str)

    def _parse_time(self, time_str):
        split_str = time_str.split(':')
        return datetime.datetime(2000, 1, 1,
                                hour=int(split_str[0]), 
                                minute=int(split_str[1]),
                                second=int(split_str[2]))
                            

if __name__ == '__main__':
    script_main()