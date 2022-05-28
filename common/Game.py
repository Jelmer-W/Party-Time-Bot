from discord.ext import commands


class Game(commands.Cog):

    def __init__(self, client):
        self._client = client
        self._max_players = 0
        self._min_players = 0
        self._game_name = ""
        self._game_command = ""

    @property
    def max_players(self):
        return self._max_players

    @property
    def min_players(self):
        return self._min_players

    @max_players.setter
    def set_max_players(self, max_players):
        self._max_players = max_players

    @min_players.setter
    def set_min_players(self, min_players):
        self._min_players = min_players