from discord.ext import commands
from server import prefix
from common.Game import Game

import random
import os
import time


def instructions():
    msg = f"Start a game by typing `{prefix}ws`.\n"
    msg += f"Guess the scrambled word by typing `{prefix}ws [guess]`.\n"
    msg += f"Shuffle the letters from the word by typing `{prefix}ws shuffle`.\n"
    msg += f"Show the word again by typing `{prefix}ws repeat`.\n"
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
        self.shuffledWord = ""
        self.authorid = 0
        self.authorname = ""
        self.started = False
        self.guesses = 1
        self.timer = time.time()
        self.noShuffles = 2


    async def isGameStarted(self, ctx):
        if not self.started:
            await ctx.send("There is no game running at the moment.")
        elif not self.authorid is ctx.author.id:
            await ctx.send(self.authorname + " is currently playing the game. Please wait until their game is finished.")
        return (self.started and (self.authorid is ctx.author.id))


    async def checkAnswer(self, ctx, guess):
        if self.answer == guess:
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
        return self.answer == guess


    async def startGame(self, ctx, *args):
        await ctx.send(f"Guess the scrambled word by typing `{prefix}ws [guess]`.\n")
        with open(os.path.join(os.path.dirname(__file__), '../common/wordlist.txt'),
                  'r') as f:                                                            # List with possible words in a separate file
            wordList = [line.strip() for line in f]
            self.answer = random.choice(wordList).lower()
        self.authorid = ctx.author.id
        self.authorname = ctx.author.name
        self.started = True
        self.timer = time.time()
        self.guesses = 1
        self.noShuffles = 2
        responses = list(self.answer)
        random.shuffle(responses)
        self.shuffledWord = ""
        for x in responses:
            self.shuffledWord += x
        await ctx.send("`" + self.shuffledWord + "`")


    @commands.group(name='wordscramble', aliases=['ws'], invoke_without_command=True)
    async def wordscramble(self, ctx, *args):
        if not self.started:                                # Creating a game
            await self.startGame(ctx, *args)
        else:                                               # Checking whether guessed word is the correct word
            if not await self.isGameStarted(ctx):
                return
            elif not args:
                await ctx.send("Please enter your guess before starting a new game.")
            else:
                await self.checkAnswer(ctx, args[0].lower())
        return


    @wordscramble.command(aliases=[])
    async def help(self, ctx):
        self.help_message = ctx.send(instructions())
        await self.help_message
        return


    @wordscramble.command()
    async def quit(self, ctx):
        if await self.isGameStarted(ctx):
            await ctx.send("The word was `" + self.answer + "`.")
            await ctx.send("Quitting the game...")
            self.started = False


    @wordscramble.command()
    async def shuffle(self, ctx):
        if await self.isGameStarted(ctx):
            if self.noShuffles == 0:
                await ctx.send("Shuffles remaining: " + str(self.noShuffles))
                return
            await ctx.send("Shuffles remaining: " + str(self.noShuffles - 1))
            self.noShuffles -= 1
            responses = list(self.shuffledWord)
            random.shuffle(responses)
            self.shuffledWord = ""
            for x in responses:
                self.shuffledWord += x
            await ctx.send("`" + self.shuffledWord + "`")


    @wordscramble.command()
    async def repeat(self, ctx):
        if await self.isGameStarted(ctx):
            await ctx.send("`" + self.shuffledWord + "`")


def setup(client):
    client.add_cog(WordScramble(client))
