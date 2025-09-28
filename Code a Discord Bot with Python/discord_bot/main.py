import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions"
)
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")

# Logging
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)
secret_role = "Gamer"

# ========== Events ==========


@bot.event
async def on_ready():
    print(f"✅ Bot is ready: {bot.user.name}")


@bot.event
async def on_member_join(member):
    await member.send(f"👋 Welcome to the server {member.name} 🎉")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 🚫 Bad word filter
    bad_words = ["shit", "fuck", "noob"]
    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        try:
            await message.author.send(
                "⚠️ Your message was deleted because it contained inappropriate language."
            )
        except:
            pass
        return

    # 🤖 AI response to every non-command message
    if message.content and not message.content.startswith("!"):
        user_question = message.content.strip()
        ai_response = get_ai_response(user_question)
        await message.channel.send(ai_response)
        return

    await bot.process_commands(message)


# ========== Commands ==========


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} ✅ assigned to {secret_role}")
    else:
        await ctx.send("❌ Role not found.")


@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} ❌ removed from {secret_role}")
    else:
        await ctx.send("❌ Role not found.")


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 New Poll", description=question, color=0x3498DB)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


@bot.command()
async def ticket(ctx):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True),
    }
    ticket_channel = await guild.create_text_channel(
        f"ticket-{ctx.author.name}", overwrites=overwrites
    )
    await ticket_channel.send(
        f"{ctx.author.mention} 🎫 Your ticket has been created. Please describe your issue."
    )
    await ctx.send("✅ Ticket created!")


@bot.command()
async def close(ctx):
    if ctx.channel.name.startswith("ticket-"):
        await ctx.channel.delete()
    else:
        await ctx.send("❌ This command can only be used in a ticket channel.")


@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("🤫 Welcome to the secret club!")


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("🚫 You don’t have permission for this!")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Clear messages from the chat"""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Cleared {amount} messages.", delete_after=5)


# ========== AI Integration (OpenRouter) ==========


# ========== AI Integration (OpenRouter) ==========


def get_ai_response(user_input: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful Discord bot."},
            {"role": "user", "content": user_input},
        ],
    }

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions", headers=headers, json=data
        )
        print("RAW RESPONSE:", response.text)  # Debugging ke liye

        if response.status_code == 200:
            res_json = response.json()

            if "choices" in res_json and len(res_json["choices"]) > 0:
                choice = res_json["choices"][0]

                reply = (
                    choice.get("message", {}).get("content")
                    or choice.get("text")
                    or choice.get("delta", {}).get("content")
                )

            if reply and reply.strip():  # ✅ Empty space handle
                # Yahan pe signature line add kar di
                return f"{reply.strip()}\n\n---\n👨‍💻 Developed by Afaq Ul Islam"
            else:
                return "⚠️ AI ne khali jawab bheja. Dobara try karo."

            return "⚠️ AI ne koi valid response nahi diya."

        else:
            return f"⚠️ API Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"❌ Failed to fetch AI response: {str(e)}"


# ========== Run Bot ==========
bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
