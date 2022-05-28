from discord.ext import commands

class Session(commands.Cog):
    def __init__(self):
        self.players = []
        self.game = ""