import discord
from discord.ext import commands
import datetime
import sqlite3


class SetupCog(commands.Cog, name="CogSetupLog"):

    """Paramétrage des logs.."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def welcome(self,ctx):

        """Entrer la commande pour plus d'informations.."""

        embed = discord.Embed(
            colour = 0x0D165A
        )
        embed.add_field(name="Configuration de la commande Welcome :", value="<prefixe> welcome channel <#channel>\n<prefixe> welcome message <message>")
        embed.add_field(name="Paramètre pour le message :", value="members = nombre de membres du serveur.\nmention = permet de mentionner le membre.\nuser = affiche le pseudo du membre.\nguild = affiche le nom du serveur.", inline=False)
        await ctx.send(embed=embed)


    @welcome.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('config/main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM welcome WHERE guild_id = '{ctx.guild.id}'")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO welcome(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Le salon '{channel.mention}' a bien été modifié")
            elif result is not None:
                sql = ("UPDATE welcome SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Le salon '{channel.mention}' a bien été modifié")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @welcome.command()
    async def message(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('config/main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = '{ctx.guild.id}'")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO welcome(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, text)
                await ctx.send(f"Le message '{text}' a bien été modifié")
            elif result is not None:
                sql = ("UPDATE welcome SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Le message '{text}' a bien été modifié")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()


    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def leave(self,ctx):

        """Entrer la commande pour plus d'informations.."""

        embed = discord.Embed(
            colour = 0x0D165A
        )
        embed.add_field(name="Configuration de la commande Leave :", value="<prefixe> leave log_channel <#channel>\n<prefixe> leave log_message <message>", inline=False)
        embed.add_field(name="Paramètre pour le message :", value="members = nombre de membres du serveur.\nmention = permet de mentionner le membre.\nuser = affiche le pseudo du membre.\nguild = affiche le nom du serveur.", inline=False)
        await ctx.send(embed=embed)

    @leave.command()
    async def log_channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('config/main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM leave WHERE guild_id = '{ctx.guild.id}'")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO leave(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Le salon '{channel.mention}' a bien été modifié")
            elif result is not None:
                sql = ("UPDATE leave SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Le salon '{channel.mention}' a bien été modifié")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @leave.command()
    async def log_message(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('config/main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM leave WHERE guild_id = '{ctx.guild.id}'")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO leave(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, text)
                await ctx.send(f"Le message '{text}' a bien été modifié")
            elif result is not None:
                sql = ("UPDATE leave SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Le message '{text}' a bien été modifié")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_channel(self, ctx):

        """Permet de setup le salon de logs-channel"""

        guild_id = ctx.guild.id
        guild = self.bot.get_guild(guild_id)

        main = sqlite3.connect('config/main.sqlite')
        cursor = main.cursor()
        cursor.execute(f"SELECT channel_id, channel_name FROM setup_channel WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            category = discord.utils.get(guild.categories, name="LOGS")

            if category is None:
                new_category = await guild.create_category(name="LOGS")
                category = guild.get_channel(new_category.id)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            }

            channel_log = await category.create_text_channel("🤖│channel-logs", overwrites=overwrites)
            channel_log_id = channel_log.id

            sql = ("INSERT INTO setup_channel(guild_id, channel_id, channel_name) VALUES(?,?,?)")
            val = (guild.id, channel_log_id, str(channel_log))
            cursor.execute(sql, val)
            main.commit()
            cursor.close()
            main.close()

            embed = discord.Embed(
                color = 0x2859F4,
                description = f"Le channel {str(channel_log.mention)} a bien été crée et enregistré dans la base de données"
            )
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.set_footer(text=f"ID channel : {channel_log_id}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)

        else:
            channel = self.bot.get_channel(result[0])

            embed = discord.Embed(
                color = 0xff3c33,
                description = f"Le channel {channel.mention} existe déjà"
            )
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.set_footer(text=f"ID channel : {result[0]}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_admin(self, ctx):

        """Permet de setup le salon de logs-admin"""

        guild_id = ctx.guild.id
        guild = self.bot.get_guild(guild_id)

        main = sqlite3.connect('config/main.sqlite')
        cursor = main.cursor()
        cursor.execute(f"SELECT channel_id, channel_name, category_id FROM setup_admin WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            category = discord.utils.get(guild.categories, name="LOGS")

            if category is None:
                new_category = await guild.create_category(name="LOGS")
                category = guild.get_channel(new_category.id)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            }

            channel_log = await category.create_text_channel("🤖│admin-logs", overwrites=overwrites)
            channel_log_id = channel_log.id

            sql = ("INSERT INTO setup_admin(guild_id, channel_id, channel_name, category_id) VALUES(?,?,?,?)")
            val = (guild.id, channel_log_id, str(channel_log), category.id)
            cursor.execute(sql, val)
            main.commit()
            cursor.close()
            main.close()

            embed = discord.Embed(
                color = 0x2859F4,
                description = f"Le channel {str(channel_log.mention)} a bien été crée et enregistré dans la base de données"
            )
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.set_footer(text=f"ID channel : {channel_log_id}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)

        else:
            channel = self.bot.get_channel(result[0])

            embed = discord.Embed(
                color = 0xff3c33,
                description = f"Le channel {channel.mention} existe déjà"
            )
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.set_footer(text=f"ID channel : {result[0]}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete_log_db(self, ctx):

        """Permet de supprimer les channel de logs et de vider la base de données.\n(a utiliser avec parcimonie\nPenser également a reset le terminal du bot pour ne pas le perdre dans une erreur d'event..)"""

        try:
            main = sqlite3.connect('config/main.sqlite')
            cursor = main.cursor()

            admin_cursor = cursor.execute(f"SELECT channel_id, category_id FROM setup_admin WHERE guild_id = '{ctx.guild.id}'")
            result_admin_cursor = admin_cursor.fetchone()

            channel_cursor = cursor.execute(f"SELECT channel_id FROM setup_channel WHERE guild_id = '{ctx.guild.id}'")
            result_channel_cursor = channel_cursor.fetchone()


            admin_log_channel =  self.bot.get_channel(result_admin_cursor[0])

            channel_log_channel = self.bot.get_channel(result_channel_cursor[0])

            embed = discord.Embed(
                color = 0xF42828,
                description = f"Les salons ``{channel_log_channel}`` et ``{admin_log_channel}``\nont été supprimé du serveur {ctx.guild} ainsi que la base de données vidée."
            )
            embed.set_author(name=ctx.guild, icon_url=ctx.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)

            await channel_log_channel.delete()
            await admin_log_channel.delete()

            admin_cursor.execute(f"DELETE FROM setup_admin WHERE guild_id = '{ctx.guild.id}'")
            main.commit()
            channel_cursor.execute(f"DELETE FROM setup_channel WHERE guild_id = '{ctx.guild.id}'")
            main.commit()

            cursor.close()
            main.close()
            return

        except:
            await ctx.send("J'ai relevé une erreur ! La base de données est probablement déjà vide.")
            return

def setup(bot):
    bot.add_cog(SetupCog(bot))
    print("The cog Setup Log is loaded")
