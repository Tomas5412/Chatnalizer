from chatparser import parseChat
from chatfetcher import chatFetch
import sys


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Run this with the path to the file to use as an argument!")
    else:
        path = sys.argv[1]
        messages = chatFetch(path)
        parseChat(messages)