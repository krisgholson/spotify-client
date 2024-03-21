import sys
import urllib.parse


def verse(input: str):
    # print(f'[Is 43:25](https://www.biblegateway.com/passage/?search=Isaiah+43%3A25&version=RSVCE)')
    print(f'[{input}](https://www.biblegateway.com/passage/?search={urllib.parse.quote(input)}&version=RSVCE)')


def main():
    input = sys.argv[1]
    verse(input)


if __name__ == '__main__':
    main()
