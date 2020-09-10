import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import re
import datetime
import graph_kappas as gk

EMOJIS = ['jphWaifu', 'jphF', 'jphFine', 'jphSad', 'jphYusuke', 'jphPout',
          'jphPickle', 'jphClawfist', 'jphWhaaat', 'jphDragonS', 'jphAngrysip', 'jphGeno',
          'jphMorg', 'jphPlothole', 'jphJeAoi', 'jphBoy', 'jphEater', 'jph4reel',
          'jphIQ', 'jphNo', 'jphDead', 'jphYADUN', 'jphTrain', 'jph2Bucket',
          'jphLili']

def script_main() -> None:
    args = parse_args()

    emoji_counts = {}
    for emoji in EMOJIS:
        emoji_counts[emoji] = 0

    messages = gk.extract_messages(args.log_fp)
    for message in messages:
        split_text = [word.strip() for word in message.text.split(' ')]
        for emoji in EMOJIS:
            if emoji in split_text:
                emoji_counts[emoji] += 1

    plot_emojis(emoji_counts)

def plot_emojis(emoji_counts: dict) -> None:
    labels = []
    counts = []
    for emoji in sorted(emoji_counts, key=emoji_counts.get):
        labels.append(emoji)
        counts.append(emoji_counts[emoji])

    axis_size = 20
    tick_size = 12
    plt.rc('xtick',labelsize=tick_size)
    plt.rc('ytick',labelsize=tick_size)

    cmap = plt.cm.ScalarMappable(cmap='rainbow')
    colors = np.arange(len(counts))
    colors = colors/len(counts)
    rgb_colors = cmap.to_rgba(colors)

    ind = list(range(len(counts)))
    plt.barh(ind, counts, color=rgb_colors)
    plt.yticks(ind, labels)

    for i, value in enumerate(counts):
        plt.text(value + 1, i - 0.2, str(value))

    plt.title('Unique Emote Usage for Stream:\n 09/09/2020', fontsize=30)
    plt.xlabel('Number of Messages Containing Emote', fontsize=axis_size)
    plt.ylabel('Emote', fontsize=axis_size)


    plt.show()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Graph emoji usage from a stream')
    parser.add_argument('log_fp', help='IRC formatted log file to read')
    return parser.parse_args()


if __name__ == "__main__":
    script_main()