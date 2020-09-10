import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import datetime

def script_main():
    args = parse_args()
    messages = extract_messages(args.log_fp)

    lul_times, lul_counts = get_lul_rate(messages, args.window_size)

    plot_lul_rate(lul_times, lul_counts, args.window_size)

def plot_lul_rate(lul_times: list, lul_counts: list, window_size: int) -> None:
    axis_size = 20
    tick_size = 15
    plt.rc('xtick',labelsize=tick_size)
    plt.rc('ytick',labelsize=tick_size)

    plt.title('"Empirical" Stream Entertainment Measurement:\nvia LUL Emote Frequency\n09/09/2020', fontsize=25)
    plt.plot_date(lul_times, lul_counts, linestyle='-', marker=',')
    plt.xlabel(f'Stream Time ({window_size} second window)', fontsize=axis_size)
    plt.ylabel('LUL Messages in Window', fontsize=axis_size)
    xformatter = mdates.DateFormatter('%H:%M:%S')
    plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)

    plt.show()

def get_lul_rate(messages: list, window_size: int) -> (list, list):
    lul_times = []
    lul_counts = []
    window_end = datetime.datetime(2000, 1, 1,
                                   minute=int(window_size/60),
                                   second=(window_size % 60))
    lul_count = 0
    for message in messages:
        if message.time.time() > window_end.time():
            lul_times.append(window_end)
            lul_counts.append(lul_count)
            window_end += datetime.timedelta(seconds=window_size)
            lul_count = 0

        if 'LUL' in message.text:
            lul_count += 1

    return lul_times, lul_counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Graph A sliding window of lul emoji\'s from twitch chat')
    parser.add_argument('log_fp', help='IRC formatted log file to read')
    parser.add_argument('--w', default=60, type=int, help='Sliding window size (seconds)', dest='window_size')

    return parser.parse_args()


def extract_messages(log_fp: str) -> list:
    with open(log_fp, 'r', encoding='utf-8') as log_f:
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