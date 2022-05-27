from discord.ext import commands

class Shutdown(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down")
        await self.client.close()

def setup(client):
    client.add_cog(Shutdown(client))