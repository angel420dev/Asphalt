import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def cleanup(ctx):
    """ Deletes all channels in the server """
    guild = ctx.guild
    try:
        delete_channel_tasks = [channel.delete() for channel in guild.channels]
        await asyncio.gather(*delete_channel_tasks)
        print("All channels deleted successfully.")
        await ctx.send("All channels have been deleted!")
    except Exception as e:
        print(f"Error deleting channels: {e}")
        await ctx.send(f"An error occurred: {e}")

bot.run("BOT_TOKEN")

