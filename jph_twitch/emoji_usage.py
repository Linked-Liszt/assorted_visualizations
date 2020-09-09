import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import datetime
import graph_kappas as gk

EMOJIS = ['jphWaifu', 'jphF', 'jphFine', 'jphSad', 'jphYusuke', 'jphPout',
          'jphPickle', 'jphClawfist', 'jphWhaaat', 'jphDragonS', 'jphAngrysip', 'jphGeno',
          'jphMorg', 'jphPlothole', 'jphJeAoi', 'jphBoy', 'jphEater', 'jph4reel',
          'jphIQ', 'jphNo', 'jphDead', 'jphYADUN', 'jphTrain', 'jph2Bucket',
          'jphLili']

def script_main():
    args = parse_args()

    emoji_counts = {}
    for emoji in EMOJIS:
        emoji_counts[emoji] = 0

    messages = gk.extract_messages(args.log_fp)
    for messages in messages:
        split_text = message.split(' ')
        for emoji in EMOJIS:
            if emoji in split_text:
                emoji_counts[emoji] += 1

def parse_args():
    parser = argparse.ArgumentParser(description='Graph emoji usage from a stream')
    parser.add_argument('log_fp', help='IRC formatted log file to read')
    return parser.parse_args()


if __name__ == if __name__ == "__main__":
    script_main()