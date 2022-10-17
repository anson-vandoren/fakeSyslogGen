import datetime
import random
import sys

# open ./wordlist.txt and read in all words
wordlist = []
with open('wordlist.txt', 'r') as f:
    wordlist = f.readlines()

# open messages.txt and read in all messages
fakeMessages = []
with open('messages.txt', 'r') as f:
    for line in f:
        fakeMessages.append(line.lower())

join_words = [
    "and",
    "or",
    "but",
    "so",
    "yet",
    "after",
    "while",
]

appname_extensions = [
    '.exe',
    '.jar',
    '.py',
    '.sh',
    '.bat',
    '.cmd',
    '.ps1',
]

def generate_rfc_5424_message(num_messages):
    messages = []
    for i in range(num_messages):
        # pri is 1-3 digit number from 0-191
        pri = f"<{random.randint(0, 191)}>"
        # version is 1
        version = "1"
        # generate UTC timestamp from current time in the format YYYY-MM-DDTHH:MM:SS.sssZ
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # hostname is 1-255 ascii characters, choose from wordlist and append 4 digits
        hostname = f"{random.choice(wordlist).strip()}{random.randint(1000, 9999)}"
        # appname is 1-48 ascii characters, choose two words from wordlist
        appname = f"{random.choice(wordlist).strip()}{random.choice(wordlist).strip().title()}{random.choice(appname_extensions)}"
        # procid is 1-128 ascii characters, but use a number for simplicity
        procid = f"{random.randint(1000, 99999)}"
        # msgid is 1-32 ascii characters, choose 3 title-case words from wordlist
        msgid = f"{random.choice(wordlist).strip().title()}{random.choice(wordlist).strip().title()}{random.choice(wordlist).strip().title()}"
        # make one STRUCTURED-DATA element with 1-5 SD-PARAMs
        sd_id = f"{random.choice(wordlist).strip().title()}"
        sd_params = []
        for i in range(random.randint(1, 5)):
            param_name = f"{random.choice(wordlist).strip().title()}"
            # choose either a random word or a number for the value
            if random.randint(0, 1) == 0:
                param_value = f"{random.choice(wordlist).strip()}"
            else:
                param_value = f"{random.randint(1000, 99999)}"
            sd_params.append(f"{param_name}=\"{param_value}\"")
        sd = f"[{sd_id} {' '.join(sd_params)}]"
        # choose a random message from messages

        msg = f"{random.choice(fakeMessages).strip()} {random.choice(join_words)} {random.choice(fakeMessages).strip()}"
        # capitalize the first letter of the message
        msg = f"{msg[0].upper()}{msg[1:]}"
        # assemble the message
        message = f"{pri}{version} {timestamp} {hostname} {appname} {procid} {msgid} {sd} {msg}\n"
        messages.append(message)
    return messages

def main():
    # args should be number of messages to generate and output file
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: main.py <number of messages> <output file>")
        sys.exit(1)
    
    # get number of messages to generate
    num_messages = int(args[0])

    # get output file
    output_file = args[1]

    # generate messages
    messages = generate_rfc_5424_message(num_messages)

    # write messages to output file
    with open(output_file, 'w') as f:
        f.writelines(messages)
    
if __name__ == "__main__":
    main()