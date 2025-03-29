import discord
from discord import app_commands

TOKEN = "TOKEN ADRESİNİZ"

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.members = True
        intents.message_content = True  # Mesaj içeriğine erişim için izin
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı!")

@bot.event
async def on_message_delete(message):
    log_channel = discord.utils.get(message.guild.text_channels, name="log")
    if log_channel:
        await log_channel.send(f"🗑️ Mesaj silindi: {message.author} - {message.content}")

@bot.event
async def on_message_edit(before, after):
    log_channel = discord.utils.get(before.guild.text_channels, name="log")
    if log_channel:
        await log_channel.send(f"✏️ Mesaj düzenlendi:\n**Önce:** {before.content}\n**Sonra:** {after.content}")

@bot.tree.command(name="yardım", description="Mevcut komutları listeler.")
async def yardım(interaction: discord.Interaction):
    embed = discord.Embed(title="📌 Yardım Menüsü", description="Mevcut komutlar listelenmiştir.", color=discord.Color.blue())
    embed.add_field(name="/ban [kullanıcı] [sebep]", value="Kullanıcıyı yasaklar.", inline=False)
    embed.add_field(name="/kick [kullanıcı] [sebep]", value="Kullanıcıyı sunucudan atar.", inline=False)
    embed.add_field(name="/duyuru [kanal] [mesaj]", value="Belirtilen kanala duyuru atar.", inline=False)
    embed.add_field(name="/uyarı [kullanıcı] [sebep]", value="Kullanıcıya uyarı verir.", inline=False)
    embed.add_field(name="/rolver [kullanıcı] [rol]", value="Kullanıcıya rol ekler.", inline=False)
    embed.add_field(name="/rolal [kullanıcı] [rol]", value="Kullanıcıdan rol kaldırır.", inline=False)
    embed.add_field(name="/mute [kullanıcı]", value="Kullanıcıyı susturur.", inline=False)
    embed.add_field(name="/unmute [kullanıcı]", value="Kullanıcının susturmasını kaldırır.", inline=False)
    embed.add_field(name="/kanalkilit", value="Kanalı kilitler.", inline=False)
    embed.add_field(name="/kanalkilitac", value="Kanalın kilidini açar.", inline=False)
    embed.add_field(name="/mesaj [mesaj] - [kanal]", value="Belirtilen kanalda mesaj gönderir.", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mesaj", description="Belirtilen kanalda mesaj gönderir.")
@app_commands.describe(message="Gönderilecek mesaj", channel="Mesajın gönderileceği kanal")
async def mesaj(interaction: discord.Interaction, message: str, channel: discord.TextChannel):
    # Komutun çalıştığı kanal üzerinden mesaj gönderme
    await channel.send(message)
    await interaction.response.send_message(f"Mesaj başarıyla {channel.mention} kanalına gönderildi.", ephemeral=True)

@bot.tree.command(name="ban", description="Bir kullanıcıyı yasaklar.")
@app_commands.describe(member="Yasaklanacak kişi", reason="Yasaklama sebebi")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member.mention} yasaklandı! Sebep: {reason}", ephemeral=True)
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

@bot.tree.command(name="kick", description="Bir kullanıcıyı sunucudan atar.")
@app_commands.describe(member="Atılacak kişi", reason="Atılma sebebi")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member.mention} sunucudan atıldı! Sebep: {reason}", ephemeral=True)
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

@bot.tree.command(name="duyuru", description="Belirtilen kanala duyuru yapar.")
@app_commands.describe(kanal="Duyurunun atılacağı kanal", mesaj="Duyuru mesajı")
async def duyuru(interaction: discord.Interaction, kanal: discord.TextChannel, mesaj: str):
    if interaction.user.guild_permissions.manage_messages:
        await kanal.send(f"📢 **Duyuru:** {mesaj}")
        await interaction.response.send_message("Duyuru gönderildi! ✅", ephemeral=True)
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

@bot.tree.command(name="uyarı", description="Bir kullanıcıya uyarı verir.")
@app_commands.describe(member="Uyarılacak kişi", reason="Uyarı sebebi")
async def uyarı(interaction: discord.Interaction, member: discord.Member, reason: str):
    if interaction.user.guild_permissions.kick_members:
        await member.send(f"⚠️ {interaction.guild.name} sunucusunda uyarıldınız! Sebep: {reason}")
        await interaction.response.send_message(f"⚠️ {member.mention} uyarıldı! Sebep: {reason}", ephemeral=True)
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

@bot.tree.command(name="sesmute", description="Kullanıcıyı sesli kanalda susturur.")
@app_commands.describe(member="Susturulacak kişi")
async def sesmute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.mute_members:
        await member.edit(mute=True)
        await interaction.response.send_message(f"🔇 {member.mention} susturuldu!", ephemeral=True)
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

@bot.tree.command(name="sesmuteac", description="Kullanıcının sesli kanaldaki susturmasını kaldırır.")
@app_commands.describe(member="Susturması kaldırılacak kişi")
async def sesmuteac(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.mute_members:
        await member.edit(mute=False)
        await interaction.response.send_message(f"🔊 {member.mention} artık konuşabilir!", ephemeral=True)
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

bot.run(TOKEN)
