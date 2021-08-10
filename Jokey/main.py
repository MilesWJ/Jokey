from datetime import datetime
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from json import loads
from itertools import cycle
from random import choice
from urllib import request

TOKEN = REDACTED
GUILD_ID = 872638182469021727

# Slash commands enabled, use those instead. ("application.commands" on discord.com/developers)
Jokey = commands.Bot(command_prefix="/")
slash = SlashCommand(Jokey, sync_commands=True)

URL = "https://v2.jokeapi.dev/joke/Any?type=twopart"

status = cycle(
    ["Minecraft",
     "Garry's Mod",
     "Grand Theft Auto V",
     "Terraria"
     "League of Legends"]
)


# ------------------------------------------------------------- #


# Bot Presence Loop
@tasks.loop(seconds=3600)
async def status_loop():
    await Jokey.change_presence(activity=discord.Game(next(status)))


# ------------------------------------------------------------- #


# Bot Running Indicator
@Jokey.event
async def on_ready():
    print(f"\n{Jokey.user} is running! (Started at {datetime.now()})")
    status_loop.start()


# ------------------------------------------------------------- #


# Help Command
@slash.slash(
    name="help",
    description="Returns a list of available commands.",
    guild_ids=[GUILD_ID],
)
async def _help(ctx: SlashContext):
    messages = ["Here you go!", "Hope this helps!"]

    with open("command_list.txt", "r") as command_list:
        all_commands = command_list.read()

    help_command_embed = discord.Embed(
        title="ALL AVAILABLE COMMANDS",
        color=discord.Color.blue(),
        description=all_commands,
    )

    help_command_embed.set_author(name="Jokey", icon_url=Jokey.user.avatar_url)

    await ctx.send(embed=help_command_embed)


# ------------------------------------------------------------- #


# Ping Command
@slash.slash(
    name="ping",
    description="Returns bot latency.",
    guild_ids=[GUILD_ID],
)
async def _ping(ctx: SlashContext):
    await ctx.send(f"Pong! ({round(Jokey.latency*1000)}ms)")


# ------------------------------------------------------------- #


# Invite Command
@slash.slash(
    name="invite",
    description="Returns the bot invite link.",
    guild_ids=[GUILD_ID],
)
async def _invite(ctx: SlashContext):
    invite_link = "https://discord.com/api/oauth2/authorize?client_id=873627985327030284&permissions=2147560512&scope=bot%20applications.commands"
    # Required Scopes: bot, application.commands
    # Required Permissions: Use Slash Commands, Send Messages, Read Message History, Manage Messages, View Channels, Add Reactions
    # Permissions Integer: 2147560512

    invite_command_embed = discord.Embed(
        title="BOT INVITE LINK",
        color=discord.Color.blue(),
        description=invite_link
    )
    invite_command_embed.set_author(
        name="Jokey", icon_url=Jokey.user.avatar_url)

    await ctx.send(embed=invite_command_embed)


# ------------------------------------------------------------- #


# Clear Command
@slash.slash(
    name="clear",
    description="Clears a suggested amount of messages.",
    guild_ids=[GUILD_ID],
    options=[
        create_option(
            name="amount",
            description="How many messages would you like to clear?",
            required=True,
            option_type=4,
        )
    ]
)
@commands.has_permissions(manage_messages=True)
async def _clear(ctx: SlashContext, amount: int):
    # Required Permissions: Manage Messages

    if amount > 0:

        if amount == 1:
            await ctx.send(f"Clearing **{amount}** message...")
        else:
            await ctx.send(f"Clearing **{amount}** messages...")

        await ctx.channel.purge(limit=amount + 1)

    else:
        await ctx.send(f"{ctx.author.mention} clear amount must be greater than 0.")


# ------------------------------------------------------------- #


# Joke Command (1/2)
def request_joke(url):
    r = request.urlopen(url)

    data = r.read()
    json_data = loads(data)

    information = [json_data["setup"], json_data["delivery"]]

    joke = f"{information[0]} {information[1]}"

    return joke


# Joke Command (2/2)
@slash.slash(
    name="joke",
    description="Returns a random joke.",
    guild_ids=[GUILD_ID],
)
async def _joke(ctx: SlashContext):
    joke = await ctx.send(request_joke(URL))

    await joke.add_reaction("👍")
    await joke.add_reaction("👎")


# ------------------------------------------------------------- #


if __name__ == "__main__":
    print(f"\nStarting bot...")
    Jokey.run(TOKEN)
