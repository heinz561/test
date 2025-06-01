import discord
from discord.ext import commands
from discord.ui import View, Button
import os
import random

from flask import ctx

from discord.ext import commands
from discord import DeletedReferencedMessage, app_commands, async_, message
import io
from datetime import datetime

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

CATEGORY_ID = 1378293328956751873  
ARCHIVE_CHANNEL_ID = 1375103948079366184

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

class RankSelectView(View):
    def __init__(self, user: discord.User, channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.user = user
        self.channel = channel
        self.clicked = False

    async def disable_all(self, interaction: discord.Interaction, selection: str, label: str):
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)


        new_name = f"{selection}-{self.user.name}".lower().replace(" ", "-")
        await self.channel.edit(name=new_name)

        rand_note = random.randint(1, 1000)


        await self.channel.send(
            f"**Mister A&L FC • EAFC Boosting Services BOT**\n\n"
            f"{self.user.mention}\n\n"
            f"Your desired purchase:\n\n"
            f"\"{label}\"\n\n"
            f"**Paypal: alservices@outlook.de **\n"
            f"Please send the desired amount and add as extra note \"**{rand_note}**\""
        )




    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("🚫 Only the requester can select a rank.", ephemeral=True)
            return False
        if self.clicked:
            await interaction.response.send_message("✅ You already selected a rank.", ephemeral=True)
            return False
        self.clicked = True
        return True

    @discord.ui.button(label="🏆 Rank 1 – 45€", style=discord.ButtonStyle.primary, custom_id="rank_15")
    async def rank_15(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_all(interaction, "15wins", button.label)

    @discord.ui.button(label="🎯 Rank 2 – 40€", style=discord.ButtonStyle.primary, custom_id="rank_13")
    async def rank_13(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_all(interaction, "13wins", button.label)

    @discord.ui.button(label="⚽ Rank 3 – 35€", style=discord.ButtonStyle.primary, custom_id="rank_12")
    async def rank_12(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_all(interaction, "12wins", button.label)

    @discord.ui.button(label="🥅 Rank 4 – 30€", style=discord.ButtonStyle.primary, custom_id="rank_11")
    async def rank_11(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_all(interaction, "11wins", button.label)


clicked_users = set()
MAX_CLICKS = 20

class WLView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.green, custom_id="wl_button")
    async def wl_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        global clicked_users

        user = interaction.user
        guild = interaction.guild

        if user.id in clicked_users:
            await interaction.response.send_message("⚠️You already pressed this button", ephemeral=True)
            return

        if len(clicked_users) >= MAX_CLICKS:
            await interaction.response.send_message("❌ 20 Users Max", ephemeral=True)
            return

        clicked_users.add(user.id)

        temp_channel_name = f"wl-{user.name}".replace(" ", "-").lower()

        existing = discord.utils.get(guild.text_channels, name=temp_channel_name)
        if existing:
            await interaction.response.send_message(f"⚠️ You already have a Fut Champs channel: {existing.mention}", ephemeral=True)
            return

        category = discord.utils.get(guild.categories, id=CATEGORY_ID)
        if not category:
            await interaction.response.send_message("❌ Kategorie konnte nicht gefunden werden.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await guild.create_text_channel(temp_channel_name, overwrites=overwrites, category=category)

        await channel.send(
            f"**Mister A&L FC • EAFC Boosting Services BOT**\n\n"
            f"Greetings {user.mention}!\n"
            f"By using our service you accept the <#1375304603226210325>.\n"
            f"Which Rank would you like to get?",
            view=RankSelectView(user, channel)
        )

        await interaction.response.send_message(f"✅ Your WL channel has been created: {channel.mention}", ephemeral=True)

        
        if len(clicked_users) >= MAX_CLICKS:
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            await interaction.message.edit(view=self)

#==========Neuer command für wl============

@bot.command(name="wl")
async def wl(ctx):
    embed = discord.Embed(
        title="🏆 Weekend League Boosting",
        description="Buy now our **FUT Champions** Service! 🔥\n\n"
                    "📋 **Pricelist:**",
        color=discord.Color.from_rgb(255, 215, 0)
    )

    embed.add_field(name="🥇 Rank 1", value="**45 €**\n", inline=True)
    embed.add_field(name="🥈 Rank 2", value="**40 €**\n", inline=True)
    embed.add_field(name="🥉 Rank 3", value="**35 €**\n", inline=True)
    embed.add_field(name="🎯 Rank 4", value="**30 €**\n", inline=True)

    embed.set_image(url="https://media.discordapp.net/attachments/1336723327275765805/1375815811314487346/Screenshot_2025-05-23_234006.png")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1077/1077012.png")
    embed.set_footer(text="Only on PC!")

    await ctx.send(embed=embed, view=WLView())


#==========Neuer command für paid============
@bot.command(name="paid")
async def paid(ctx):
    await ctx.send(
        "**email:** \n"
        "**Passwort:** \n"
        "**Backup Code:** \n"
        "⮑ Open the EA app <https://www.ea.com/de-de/> and go to your Profile Settings\n"
        "↳ Click on Security and then on 2 Faktor Authentific\n"
        "↳ Now Click on ,,Show Backup-Codes\"\n\n"
        "**Reminder:** Send all 6 Backup Codes (if any Code doesn’t work)\n\n"
        "_We would recommend now not to go in your EA Account in the next 24–48h but we will give you an exact time._"
    )


    #========Neuer command für delete============

@bot.command(name="del")
async def del_channel(ctx):
    await ctx.channel.send("Channel will be deleted in 5 seconds.")
    import asyncio
    await asyncio.sleep(5)    
    target_channel = bot.get_channel(1375103948079366184)
    if target_channel:
        await target_channel.send("Channel deleted successfully.")
    await ctx.channel.delete()

    #==========Neuer command für close============

@bot.command(name="close")
async def close_channel(ctx):

    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)


    await ctx.send("🔒 Ticket is getting closed...")


    transcript = ""
    async for msg in ctx.channel.history(limit=None, oldest_first=True):
        time = msg.created_at.strftime("%Y-%m-%d %H:%M")
        author = msg.author.display_name
        content = msg.content or "[Kein Inhalt / Embed / Datei]"
        transcript += f"[{time}] {author}: {content}\n"


    file_buffer = io.StringIO(transcript)
    file_name = f"ticket_{ctx.channel.name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    file = discord.File(fp=io.BytesIO(file_buffer.getvalue().encode()), filename=file_name)


    archive_channel = bot.get_channel(ARCHIVE_CHANNEL_ID)
    if archive_channel is None:
        await ctx.send("❌ Fehler: not found.")
        return


    await archive_channel.send(
        content=f"🗂 Archiviertes Ticket von {ctx.channel.mention} (`{ctx.channel.name}`):",
        file=file
    )


    await ctx.send("✅ Done.")

#===========Neuer command für verify============

@bot.command(name="verify")
async def verify(ctx):
    await ctx.send("✅ Verified!", ephemeral=True)
    await ctx.author.add_roles(ctx.guild.get_role(1375101187472363530))

 #==========Neuer command für zeit 10-14 ============  
@bot.command(name="10")
async def zehn(ctx):
    await ctx.send("Your appointment is from 10 am- 2 pm. CEST "
                  "If our team doesnt finish in time a new appointment will be scheduled")

#==========Neuer command für zeit 14-18 ============  
@bot.command(name="14")
async def vierzehn(ctx):
    await ctx.send("Your appointment is from 2 pm- 6 pm. CEST "
                  "If our team doesnt finish in time a new appointment will be scheduled")

#==========Neuer command für zeit 18-22 ============   
@bot.command(name="18")
async def achtzehn(ctx):
    await ctx.send("Your appointment is from 6 pm- 10 pm. CEST "
                  "If our team doesnt finish in time a new appointment will be scheduled")

#==========Neuer command für zeit 22-2 ============





bot.run(os.environ['DISCORD_TOKEN'])
