#    Yanabot - A Discord Bot for roleplay server
#    Copyright (C) 2O20 HeartsDo
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
import asyncio
import json
import logging
import utils.checks
import utils.dbutils
import utils.permissions

async def apply_strike(self, ctx, type:str=None, staff:discord.Member=None, number:int=0, reason:str="None"):
        idu = staff.id
        mydb = utils.dbutils.init_connection()
        mycursor = mydb.cursor()
        levelexec = await utils.permissions.get_level_per_roles(ctx)
        grantall = False
        if levelexec == 6:
            grantall = True
        mycursor.execute("""SELECT * FROM staffs WHERE idu=%s""", (idu,))
        respond = mycursor.fetchall()
        respond = respond[0]
        try:
            levelmem = respond[1]
            ostrike = respond[2]
        except IndexError:
            return await ctx.send(":x: Cette personne n'est pas membre du staff ou n'est pas dans le registre, veillez ressayer !")
        if grantall == False:
            if levelmem <= 5:
                return await ctx.send(":x: Les collègues administrateurs ne peuvent pas se strike entre eux, faut demander au Resp. Staff de résoudre à cela !")
        if type == "add":
            cstrike = ostrike + number
        if type == "remove":
            cstrike = ostrike - number
        mycursor.execute("""UPDATE staffs SET strike=%s WHERE idu=%s""", (cstrike, idu,))
        mydb.commit()
        mycursor.execute("""INSERT INTO strike_reason (idu, orignalstrike, currentstrike, reason) VALUES (%s, %s, %s, %s);""", (idu, ostrike, cstrike, reason))
        mydb.commit()
        await ctx.send(":ok_hand:")
        if type == "add":
            await self.logchannel.send(":closed_book: Le staff {}#{} à reçu {} strike(s) par {}#{} pour la raison suivante: {}".format(staff.name, staff.discriminator, number, ctx.author.name, ctx.author.discriminator, reason))
        if type == "remove":
            await self.logchannel.send(":green_book: Le staff {}#{} s'est vu enlevé {} strike(s) par {}#{} pour la raison suivante: {}".format(staff.name, staff.discriminator, number, ctx.author.name, ctx.author.discriminator, reason))
        utils.dbutils.close_connection(mydb)


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.json', 'r') as fichier:
            self.config = json.load(fichier)
        self.logchannel = self.bot.get_channel(self.config['bot']['logchan'])
        

    @commands.command()
    @utils.checks.iflevelisuporequal(5)
    async def checkup(self, ctx):
        message = """:notepad_spiral: __**C'est l'heure du checkup de la semaine !**__

Tous les membres du staff doivent fournir un petit phrase sur vos activités de la semaine passé, dans le but de maintenir un staff actif.
Faillir à ce checkup vous expose à un strike (à partir de 3 strike ou de 4 strike pour un administrateur, vous risquer de voir vos privilèges révoquée.)

Si vous êtes absent pendant une période, merci de nous le dire également, on notera et on l'affichera lors des prochains checkup !

Cordialement,
Un Resp. Staff pour Fantasya RP

Ping: <@&678973022379704330>"""
        channel = self.bot.get_channel(id=686149004978815007)
        await channel.send(message)
        await ctx.send(":white_check_mark: Checkup publié !")


    @commands.command()
    @utils.checks.iflevelisuporequal(5)
    async def strike(self, ctx, staff:discord.Member=None, number:int=0, reason:str="None"):
        if staff == None or number == 0 or reason == "None":
            return await ctx.send(":x: Donner moi un membre du staff, un nombres de strike et une raison pour donner un strike !")
        await apply_strike(self, ctx, "add", staff, number, reason)


    @commands.command()
    @utils.checks.iflevelisuporequal(5)
    async def pardon(self, ctx, staff:discord.Member=None, number:int=0, reason:str="None"):
        if staff == None or number == 0 or reason == "None":
            return await ctx.send(":x: Donner moi un membre du staff, un nombres de strike et une raison pour enlever un strike !")
        await apply_strike(self, ctx, "remove", staff, number, reason)


def setup(bot):
    bot.add_cog(Staff(bot))
