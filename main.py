import discord
from discord.ext import commands
from discord import Embed
from keep_alive import keep_alive
from discord.ext import tasks
from discord.ext.commands import has_permissions
import youtube_dl

client = commands.Bot(command_prefix='!')
import os
import requests


@client.event
async def on_ready():
    print("Your bot is ready")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name='Hears for the Ears'))
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


@client.event
async def on_message_edit(before, after):
    channel = discord.utils.get(before.guild.channels, name="logs")
    embed = discord.Embed(title="Message Edited", description=before.author, color=before.author.color)
    embed.add_field(name="Before", value=before.content, inline=False)
    embed.add_field(name="After", value=after.content, inline=False)
    await channel.send(embed=embed)

@client.event
async def on_message_delete(ctx):
    channel = discord.utils.get(ctx.guild.channels, name="logs")
    embed = discord.Embed(description=ctx.author, color=ctx.author.color)
    embed.add_field(name="Message Deleted", value=ctx.content)
    await channel.send(embed=embed)

@client.event
async def on_member_join(ctx):
    channel = discord.utils.get(ctx.guild.channels, name="hi")
    embed = discord.Embed(description=ctx.author, color=ctx.author.color)
    embed.add_field(name=f"""Welcome to the server {ctx.mention}!""", value=ctx.content)
    await channel.send(embed=embed)

@commands.has_permissions(administrator=True)
@client.command()
async def purge(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


@client.command(aliases=["join", "JOIN", "PLAY"])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current song to end or use the 'stop' command")

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',

        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command(aliases=["exit", "EXIT", "LEAVE"])
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Bot is not connected to any voice channel.")


@client.command(aliases=["PAUSE"])
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Bot is not playing any audio.")


@client.command(aliases=["RESUME"])
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(aliases=['dm'])
async def DM(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)
    await ctx.message.delete()


@client.command(aliases=['KICK'])
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == None:
        member = ctx.author
        await ctx.send("Please use the format: `!kick [member] `optional` [reason]`")
        return
    else:
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked <:glue:757555434927423551>')



@client.command(aliases=['BAN'])
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member == None:
        member = ctx.author
        await ctx.send("Please use the format: `!ban [member] `optional` [reason]`")
        return
    else:
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned <:glue:757555434927423551>')



@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"User {user.mention} has been unbanned <:glue:757555434927423551>")


@client.command(aliases=["PFP", "avatar"])
async def pfp(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
        await ctx.send("Please use the format: `!pfp [member]`")
        return
    else:
        icon_url = member.avatar_url
        avatarEmbed = discord.Embed(title=f"{member.name}\'s Profile Pic", color=0xFFA500)
        avatarEmbed.set_image(url=f"{icon_url}")
        avatarEmbed.timestamp = ctx.message.created_at
        await ctx.send(embed=avatarEmbed)


@client.command(aliases=["PING", "Ping"])
async def ping(ctx):
    await ctx.send('Pong! `(better than table tennis)`: {0}ms'.format(round(client.latency, 2)))


@client.command(aliases=["inv"])
async def invite(ctx):
    link = await ctx.channel.create_invite(xkcd=True, max_age=0, max_uses=0)

    await ctx.send(f"> {link}")


snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

keep_alive()
client.run('OTU4MDIzMjQ4OTcxNDMxOTg2.YkHSrQ.y0YJQpU2QwaRnQRwKb48WCtJu4I')
