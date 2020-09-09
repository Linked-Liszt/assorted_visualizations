import argparse
import graph_kappas as gk


def script_main():
    args = parse_args()
    emojis = []
    messsages = gk.extract_messages(args.log_fp)
    for message in messsages:
        for word in message.text.split():
            if word.startswith('jph') and word not in emojis:
                emojis.append(word)
    print(emojis)


def parse_args():
    parser = argparse.ArgumentParser(description='Extract used emojis from stream chat')
    parser.add_argument('log_fp', help='IRC formatted log file to read')
    return parser.parse_args()


if __name__ == "__main__":
    script_main()