"""A Markov chain generator that can tweet random messages."""

import os
import discord
from random import choice



def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ''
    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

    return chains


def make_text(chains, char_limit=4000):
    """Take dictionary of Markov chains; return random text."""

    keys = list(chains.keys())
    key = choice(keys)

    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).
        if char_limit and len(' '.join(words)) > char_limit:
            break
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return ' '.join(words)


# Get the filenames from the user through a command line prompt, ex:\

# python markov.py green-eggs.txt shakespeare.txt
filenames = ['green-eggs.txt', 'twister.txt']

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# print(make_text(chains))

client = discord.Client()

random_phrase = (['Toast is always good toasted', "Never swim with a toaster plugged in", "The sun is a bright star, shoot for that",
                   "A faithful friend is a strong defense", " A fresh start will put you on your way", "Believe it can be done",
                   "Disbelief destroys the magic", "Don't make extra work for yourself", "Don't spend time, invest it."
                   ])
thankful_phrase = ['Why thank you sir/madam', "I am glad you noticed me", "I am just trying to do my best"]
greeting = ['hello there', 'Yes, what can I share with you?', 'I am a good bot', "Hello"]

@client.event
async def on_ready():
    print(f'Successfully connected! Logged in as {client.user}.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if 'good bots' in message.content.lower():
        await message.channel.send(choice(thankful_phrase))
    

    if 'tell me something' in message.content.lower():
        await message.channel.send(make_text(chains))
    
    if 'words of wisdom' in message.content.lower():
        await message.channel.send(choice(random_phrase))

    if  'wise man' in message.content.lower():
        await message.channel.send(choice(greeting))

    if 'hello' in message.content.lower():
        await message.channel.send(choice(greeting))



client.run(os.environ["DISCORD_TOKEN"])

# remember to run source secrets.sh to make a path