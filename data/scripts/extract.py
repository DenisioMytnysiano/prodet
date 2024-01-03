import re
import datetime
from telethon.sync import TelegramClient

CHAT_NAME = "ukrpravda_news"
OUTPUT_FILE = "ukrainian-news.csv"
LOOKBACK_SIZE = 10000

def normalize_line(p: str) -> str:
    if not p:
        return p
    if p.startswith('"'):
        p = p[1:-2]
    p = re.sub(r'http\S+', '', p)
    p = p.replace("\n", "")
    p = p.replace("&nbsp;", "")
    p = p.replace("\xa0", " ")
    p = p.replace("\u200b", " ")
    p = p.replace('""', '"')
    p = p.replace("/", "")
    p = p.replace("...", "")
    p = p.replace("[...]", "")
    p = p.replace("[---]", "")
    p = p.replace("[--]", "")
    p = p.replace("[]", "")
    p = p.replace("[", "")
    p = p.replace("]", "") 
    p = p.replace("(", "")
    p = p.replace(")", "") 
    p = p.replace("**", "")
    p = re.sub(" +", " ", p)
    p = p.replace("підписатися", "")
    p  = p.replace("UPD", "")
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    p = emoji_pattern.sub(r'', p)
    p = p.strip()
    return p

def should_skip_message(message):
    if not message:
        return True
    if len(message.split(" ")) < 8:
        return True
    return "на банку" in message or "тривог" in message or "загроз" in message


def main():
    news = []
    with TelegramClient(NAME, API_ID, API_HASH) as client:
        for message in client.iter_messages(CHAT_NAME, reverse=True, offset_date=datetime.datetime(2022, 2, 24)):
            normalized = normalize_line(message.text)
            if not should_skip_message(normalized):
                news.append(normalized)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as w:
        w.write("text\n")
        w.write("\n".join(news))

if __name__ == "__main__":
    main()


