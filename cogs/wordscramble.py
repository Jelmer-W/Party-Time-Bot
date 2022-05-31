from discord.ext import commands
from server import prefix
from common.Game import Game

import random
import os
import time


def instructions():
    msg = f"Start the game by typing `{prefix}ws`.\n"
    msg += f"Guess the scrambled word by typing `{prefix}ws [guess]`.\n"
    msg += f"Quit an existing game by typing `{prefix}ws quit`.\n"
    msg += f"Open this help menu by typing `{prefix}ws help`.\n"
    return msg


class WordScramble(Game):

    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self._game_name = "wordscramble"
        self._game_command = f"{prefix}wordscramble"
        self.help_message = ""
        self.answer = ""
        self.authorid = 0
        self.started = False
        self.guesses = 1
        self.timer = time.time()

    @commands.group(name='wordscramble', aliases=['ws'], invoke_without_command=True)
    async def wordscramble(self, ctx, *args):
        if args:
            if args[0].lower() == "help":                   # Showing help message
                self.help_message = ctx.send(instructions())
                await self.help_message
                return
        if not self.started:                                # Creating a game
            await ctx.send(f"Guess the scrambled word by typing `{prefix}ws [guess]`.\n")
            with open(os.path.join(os.path.dirname(__file__), '../common/wordlist.txt'), 'r') as f:     # List with possible words in a separate file
                wordList = [line.strip() for line in f]
                self.answer = random.choice(wordList).lower()
            self.authorid = ctx.author.id
            self.started = True
            self.timer = time.time()
            responses = list(self.answer)
            random.shuffle(responses)
            msg = ""
            for x in responses:
                msg += x
            await ctx.send(msg)
        else:                                               # Checking whether guessed word is the correct word
            if self.authorid is not ctx.author.id:
                return
            if not args:
                await ctx.send("Please enter your guess before starting a new game.")
            else:
                if args[0].lower() == "quit":
                    await ctx.send("The word was `" + self.answer + "`.")
                    await ctx.send("Quitting the game...")
                    self.started = False
                elif self.answer == args[0].lower():
                    if self.guesses == 1:
                        await ctx.send("Congratulations! You guessed the word in " + str(self.guesses) + " guess.")
                    else:
                        await ctx.send("Congratulations! You guessed the word in " + str(self.guesses) + " guesses.")
                    elapsedtime = time.time() - self.timer
                    await ctx.send("It only took you " + str(round(elapsedtime)) + " seconds!")
                    self.started = False
                else:
                    await ctx.send("Wrong! Try again.")
                    self.guesses += 1


def setup(client):
    client.add_cog(WordScramble(client))
