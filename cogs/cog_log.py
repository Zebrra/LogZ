#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import discord
from discord.ext import commands
import datetime
import sqlite3

class EventCog(commands.Cog, name="LogsEvent"):

    """Gestionnaire des events"""

    def __init__(self, bot):
        self.bot = bot

#########################
#########################
    # logs for user
#########################
#########################

    @commands.Cog.listener()
    async def on_member_join(self, member):

        db = sqlite3.connect('../config/main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM welcome WHERE guild_id = '{member.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = '{member.guild.id}'")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild

            embed = discord.Embed(
                colour = 0x95efcc,
                description= str(result1[0]).format(members=members, mention=mention, user=user, guild=guild)
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(id=int(result[0]))

            await channel.send(embed=embed)


        cursor.close()
        db.close()
        return


    @commands.Cog.listener()
    async def on_member_remove(self, member):

        db = sqlite3.connect('../config/main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM leave WHERE guild_id = '{member.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM leave WHERE guild_id = '{member.guild.id}'")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild

            embed = discord.Embed(
                colour = 0xefa095,
                description= str(result1[0]).format(members=members, mention=mention, user=user, guild=guild)
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(id=int(result[0]))

            await channel.send(embed=embed)

        cursor.close()
        db.close()
        return



#########################
#########################
    # logs channel
#########################
#########################


    @commands.Cog.listener()
    async def on_message_delete(self, message):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_channel WHERE guild_id = '{message.guild.id}'")
            result = cursor.fetchone()

            channel_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0xF42828,
                description = f"**Le message de {message.author.mention} a été supprimé dans {message.channel.mention}**.\n{message.content}"
            )
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=f"Autheur ID : {message.author.id} | Msg ID : {message.id}")
            embed.timestamp = datetime.datetime.utcnow()

            await channel_log.send(embed=embed)

            cursor.close()
            main.close()
            return
        except:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_channel WHERE guild_id = '{before.guild.id}'")
            result = cursor.fetchone()

            channel_log = self.bot.get_channel(int(result[0]))

            linkable = f"[Voir le message]({after.jump_url}/ \"Hovertext\")"

            embed = discord.Embed(
                color = 0x2859F4,
                description= f"**Message modifier dans {before.channel.mention}** | {linkable}",
            )
            embed.add_field(name="Avant", value=before.content, inline=False)
            embed.add_field(name="Après", value=after.content, inline=False)
            embed.set_author(name=before.author, icon_url=before.author.avatar_url)
            embed.set_footer(text=f"Autheur ID : {after.author.id} | Msg ID : {after.id}")
            embed.timestamp = datetime.datetime.utcnow()

            await channel_log.send(embed=embed)

            cursor.close()
            main.close()
            return
        except:
            return

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_channel WHERE guild_id = '{channel.guild.id}'")
            result = cursor.fetchone()

            channel_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0x28F431, 
            )
            embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()


            if isinstance(channel, discord.CategoryChannel):
                embed.description = f"La catégorie ``{channel}`` a été crée."
                embed.title = "Catégorie"
                embed.set_footer(text=f"Catégorie ID : {channel.id}")
                await channel_log.send(embed=embed)
            
            elif isinstance(channel, discord.VoiceChannel):
                embed.title = f"Salon vocal {channel.name}"
                if channel.category:
                    embed.description = f"Le salon vocal {channel.mention} a été crée dans la catégorie ``{channel.category}``"
                    embed.set_footer(text=f"Catégorie ID : {channel.category.id} | Channel ID : {channel.id}")

                else:
                    embed.description = f"Le salon vocal {channel.mention} a été crée"
                    embed.set_footer(text=f"Channel ID : {channel.id}")

                await channel_log.send(embed=embed)

            else:
                embed.title = f"Salon textuel {channel.name}"
                if channel.category:
                    embed.description = f"Le salon {channel.mention} a été crée dans la catégorie ``{channel.category}``"
                    embed.set_footer(text=f"Catégorie ID : {channel.category.id} | Channel ID : {channel.id}")

                else:
                    embed.description = f"Le salon {channel.mention} a été crée"
                    embed.set_footer(text=f"Channel ID : {channel.id}")

                await channel_log.send(embed=embed)

            cursor.close()
            main.close()
            return

        except:
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_channel WHERE guild_id = '{channel.guild.id}'")
            result = cursor.fetchone()

            channel_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0xF42828, 
            )
            embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()


            if isinstance(channel, discord.CategoryChannel):
                embed.description = f"La catégorie ``{channel}`` a été supprimée."
                embed.title = "Catégorie"
                embed.set_footer(text=f"Catégorie ID : {channel.id}")
                await channel_log.send(embed=embed)
            
            elif isinstance(channel, discord.VoiceChannel):
                embed.title = "Salon vocal"
                if channel.category:
                    embed.description = f"Le salon vocal {channel} a été supprimé de la catégorie ``{channel.category}``"
                    embed.set_footer(text=f"Catégorie ID : {channel.category.id} | Channel ID : {channel.id}")

                else:
                    embed.description = f"Le salon vocal {channel} a été supprimé"
                    embed.set_footer(text=f"Channel ID : {channel.id}")

                await channel_log.send(embed=embed)

            else:
                embed.title = "Salon textuel"
                if channel.category:
                    embed.description = f"Le salon {channel} a été supprimé de la catégorie ``{channel.category}``"
                    embed.set_footer(text=f"Catégorie ID : {channel.category.id} | Channel ID : {channel.id}")

                else:
                    embed.description = f"Le salon {channel.mention} a été supprimé"
                    embed.set_footer(text=f"Channel ID : {channel.id}")

                await channel_log.send(embed=embed)

            cursor.close()
            main.close()
            return

        except:
            return


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):

        try:

            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_channel WHERE guild_id = '{after.guild.id}'")
            result = cursor.fetchone()

            channel_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0x2859F4, 
            )
            embed.set_author(name=after.guild.name, icon_url=after.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            if isinstance(after) == isinstance(before):
                return

            if isinstance(after, discord.CategoryChannel):
                embed.description = f"La catégorie ``{before.name}`` a été modifée."
                embed.title = "Catégorie"
                embed.add_field(name="Avant", value=f"``{before.name}``", inline=False)
                embed.add_field(name="Après", value=f"``{after.name}``", inline=False)
                embed.set_footer(text=f"Catégorie ID : {after.id}")
                await channel_log.send(embed=embed)
            
            elif isinstance(after, discord.VoiceChannel):
                embed.title = f"Salon vocal {after.name}"
                if after.category:
                    embed.description = f"Le salon vocal {before.name} a été modifié dans la catégorie ``{after.category}``"
                    embed.add_field(name="Avant", value=f"``{before.name}``", inline=False)
                    embed.add_field(name="Après", value=f"{after.mention}", inline=False)
                    embed.set_footer(text=f"Catégorie ID : {after.category.id} | Channel ID : {after.id}")

                else:
                    embed.description = f"Le salon vocal {before.name} a été modifié"
                    embed.add_field(name="Avant", value=f"``{before.name}``", inline=False)
                    embed.add_field(name="Après", value=f"{after.mention}", inline=False)
                    embed.set_footer(text=f"Channel ID : {after.id}")

                await channel_log.send(embed=embed)

            else:
                embed.title = f"Salon textuel {after.name}"
                if after.category:
                    embed.description = f"Le salon {before.name} a été modifié dans la catégorie ``{after.category}``"
                    embed.add_field(name="Avant", value=f"``{before.name}``", inline=False)
                    embed.add_field(name="Après", value=f"{after.mention}", inline=False)
                    embed.set_footer(text=f"Catégorie ID : {after.category.id} | Channel ID : {after.id}")

                else:
                    embed.description = f"Le salon {before.name} a été modifié"
                    embed.add_field(name="Avant", value=f"``{before.name}``", inline=False)
                    embed.add_field(name="Après", value=f"{after.mention}", inline=False)
                    embed.set_footer(text=f"Channel ID : {after.id}")

                await channel_log.send(embed=embed)

            cursor.close()
            main.close()
            return
        
        except:
            return


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        # join = after.channel.name
        # leave = before.channel.name
        # switch = before.channel.name => after.channel.name
        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_channel WHERE guild_id = '{member.guild.id}'")
            result = cursor.fetchone()

            channel_log = self.bot.get_channel(int(result[0]))

            join_embed = discord.Embed(
                color = 0x28F431
            )
            join_embed.set_author(name=member, icon_url=member.avatar_url)
            join_embed.set_footer(text=f"Membre ID : {member.id}")
            join_embed.timestamp = datetime.datetime.utcnow()

            if before.channel is None:
                join_embed.description = f"**{member.mention} a rejoins le salon vocal {after.channel.mention}**"
                await channel_log.send(embed=join_embed)

            elif after.channel is None:
                left_embed = discord.Embed(
                    color = 0xF42828,
                    description= f"**{member.mention} a quitté le salon vocal {before.channel.mention}**"
                )
                left_embed.set_author(name=member, icon_url=member.avatar_url)
                left_embed.set_footer(text=f"Membre ID : {member.id}")
                left_embed.timestamp = datetime.datetime.utcnow() 

                await channel_log.send(embed=left_embed)           

            else:
                if before.channel == after.channel:
                    return
                join_embed.description = f"**{member.mention} a changé de salon vocal {before.channel.mention} -> {after.channel.mention}**"
                await channel_log.send(embed=join_embed)

            cursor.close()
            main.close()
            return
        
        except:
            return




#########################
#########################
    # logs admin
#########################
#########################


    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_admin WHERE guild_id = '{guild.id}'")
            result = cursor.fetchone()

            admin_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0xF42828,

            )
            embed.set_author(name=guild.name, icon_url=guild.icon_url)
            embed.set_footer(text=f"Membre banni ID : {user.id}")
            embed.timestamp = datetime.datetime.utcnow()


            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
            logs = logs[0]
            if logs.target == user:
                if logs.reason != None:
                    embed.description = f"**{user} a été banni du serveur pour le motif suivant :**\n**```{logs.reason}```**"
                else:
                    embed.description = f"**{user} a été banni du serveur** (aucun motif n'a été spécifié)."

                await admin_log.send(embed=embed)
            
            cursor.close()
            main.close()
            return
        
        except:
            return


    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_admin WHERE guild_id = '{guild.id}'")
            result = cursor.fetchone()

            admin_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0x2859F4,
            )
            embed.set_author(name=guild.name, icon_url=guild.icon_url)
            embed.set_footer(text=f"Membre ID : {user.id}")
            embed.timestamp = datetime.datetime.utcnow()

            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.unban).flatten()
            logs = logs[0]
            if logs.target == user:
                if logs.reason != None:
                    embed.description = f"**{user.mention} ({user.name}) a été débanni du serveur. Le motif de son ban :>**\n**```{logs.reason}```**"
                else:
                    embed.description = f"**{user.mention} ({user.name}) a été débanni du serveur** (aucun motif n'a été trouvé)."

                await admin_log.send(embed=embed)
            
            cursor.close()
            main.close()
            return
        
        except:
            return


    @commands.Cog.listener()
    async def on_guild_role_create(self, role):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_admin WHERE guild_id = '{role.guild.id}'")
            result = cursor.fetchone()

            admin_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0x28F431,
                description = f"**Le rôle {role.mention} viens d'être crée.**"
            )
            embed.set_author(name=role.guild.name, icon_url=role.guild.icon_url)
            embed.set_footer(text=f"Role ID : {role.id}")
            embed.timestamp = datetime.datetime.utcnow()

            await admin_log.send(embed=embed)

            cursor.close()
            main.close()
            return
        
        except:
            return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_admin WHERE guild_id = '{role.guild.id}'")
            result = cursor.fetchone()

            admin_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0xF42828,
                description = f"**Le rôle ``{role.name}`` viens d'être supprimé.**"
            )
            embed.set_author(name=role.guild.name, icon_url=role.guild.icon_url)
            embed.set_footer(text=f"Role ID : {role.id}")
            embed.timestamp = datetime.datetime.utcnow()

            await admin_log.send(embed=embed)

            cursor.close()
            main.close()
            return

        except:
            return

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_admin WHERE guild_id = '{after.guild.id}'")
            result = cursor.fetchone()

            admin_log = self.bot.get_channel(int(result[0]))

            embed = discord.Embed(
                color = 0x2859F4,
                description = f"**Le rôle ``{before.name}`` viens d'être modifié.**"
            )
            embed.set_author(name=after.guild, icon_url=after.guild.icon_url)
            embed.set_footer(text=f"Role ID : {after.id}")
            embed.add_field(name="**Avant**", value=f"``{before.name}``", inline=False)
            embed.add_field(name="**Après**", value=f"``{after.name}`` | {after.mention}", inline=False)
            embed.timestamp = datetime.datetime.utcnow()

            await admin_log.send(embed=embed)

            cursor.close()
            main.close()
            return
        
        except:
            return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        # print(before)
        # print(after)
        # print(before.nickname)
        # print(before.display_name)
        # print(before.roles)
        # # print(before.role)

        # shorter, longer = sorted([after.roles, before.roles], key=len)
        # print(shorter)
        # print(longer)

        try:
            main = sqlite3.connect('../config/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id FROM setup_admin WHERE guild_id = '{after.guild.id}'")
            result = cursor.fetchone()

            admin_log = self.bot.get_channel(int(result[0]))

            if len(before.roles) < len(after.roles):
                new_role = next(role for role in after.roles if role not in before.roles)

                embed = discord.Embed(
                    color = 0x28F431,
                    description= f"**{after.mention} a reçu le rôle {new_role.mention}**"
                )
                embed.set_author(name=after.name, icon_url=after.avatar_url)
                embed.set_footer(text=f"Membre ID : {after.id}")
                embed.timestamp = datetime.datetime.utcnow()

                await admin_log.send(embed=embed)

            if len(before.roles) > len(after.roles):
                old_role = next(role for role in before.roles if role not in after.roles)

                embed = discord.Embed(
                    color = 0xF42828,
                    description= f"**{after.mention} a perdu le rôle {old_role.mention}**"
                )
                embed.set_author(name=after.name, icon_url=after.avatar_url)
                embed.set_footer(text=f"Membre ID : {after.id}")
                embed.timestamp = datetime.datetime.utcnow()
                
                await admin_log.send(embed=embed)

            if before.display_name != after.display_name:
                embed = discord.Embed(
                    color = 0x2859F4,
                    description= f"**{after.mention} viens de changer son pseudo.**"
                )
                embed.set_author(name=after, icon_url=after.avatar_url)
                embed.set_footer(text=f"Membre ID : {after.id}")
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name="Avant", value=before.display_name, inline=False)
                embed.add_field(name="Après", value=after.display_name, inline=False)

                await admin_log.send(embed=embed)
            

            cursor.close()
            main.close()
            return
        
        except:
            return


def setup(bot):
    bot.add_cog(EventCog(bot))
    print("The cog EventLog is loaded")