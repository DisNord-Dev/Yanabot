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
import json
import logging
import random
import mysql.connector
import utils.dbutils
with open('config.json', 'r') as fichier:
    config = json.load(fichier)
    

async def roll_stats(self, ctx, row:str="None"):
        if row == "None":
            return logging.warn("NANI, le bot ne fonctione pas bien !!! (Raison: "
            "Pas de variable pour roll_stats")
        mydb = utils.dbutils.init_connection()
        mycursor = mydb.cursor()
        idu = ctx.author.id
        sql = """SELECT {} FROM stats_user WHERE idu=%s""".format(row)
        mycursor.execute(sql, (idu,))
        respond = [r[0] for r in mycursor.fetchall()]
        try:
            respond = respond[0]
        except IndexError:
            return await ctx.send(":x: Tu sait, les fiches c'est pas pour les nuls !")
        num = random.randrange(1, 100, 1)
        logging.info(num)
        utils.dbutils.close_connection(mydb)
        if num <= 5:
            return await ctx.send("<a:blobrainbowdanse:680102742714220625> | Réussite Critique !!!")
        elif num >= 95:
            return await ctx.send("<a:catno:680102811740143624> | Echec Critique !!!")    
        elif respond > num:
            return await ctx.send("<a:bongocat:680115938019901629> | Réussite !")
        elif respond < num:
            return await ctx.send("<a:clapnul:680115868004515934> | Echec !")
        

async def get_and_verify_eligibility(self, ctx):
    roles = []
    rolesu = ctx.author.roles
    for roleu in rolesu:
        roles.append(roleu.id)
    rangroles = [680854724643127306, 678973019632304138, 678973019665858596, 678973020265775117,
                 678973021981245466, 678973022660591636, 680854724643127306, 680854704934486032,
                 680854732675481687, 680854740560904293]
    for role in rangroles:
        if role in roles:
            role = ctx.guild.get_role(role)
            role = role.name
            role = role.split()
            role = role[1]
            role = int(role)
            mydb = utils.dbutils.init_connection()
            mycursor = mydb.cursor()
            idu = ctx.author.id
            sql = """SELECT rang FROM stats_user WHERE idu=%s"""
            val = (idu,)
            mycursor.execute(sql, val)
            respond = [r[0] for r in mycursor.fetchall()]
            respond = respond[0]
            utils.dbutils.close_connection(mydb)
            if role > respond:
                return True
            else:
                return False
    logging.info("Meh")


class Rolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.json', 'r') as fichier:
            self.config = json.load(fichier)
        

    @commands.command()
    async def action(self, ctx):
        """Faire une action simple avec un roll 100"""
        num = random.randrange(1, 100, 1)
        if num <= 5:
            return await ctx.send("<a:blobrainbowdanse:680102742714220625> | Réussite Critique !!!")
        elif num < 50:
            return await ctx.send("<a:bongocat:680115938019901629> | Réussite !")
        elif num < 95:
            return await ctx.send("<a:clapnul:680115868004515934> | Echec !")
        elif num <= 100:
            return await ctx.send("<a:catno:680102811740143624> | Echec Critique !!!")
    

    @commands.group()
    async def roll(self, ctx):
        """Faire un roll complexe avec des stats défini"""
        if ctx.invoked_subcommand is None:
            await ctx.send(":x: Mauvaise commande, faite !help roll dans un channel de bot pour de l'aide !")


    @roll.command()
    async def physique(self, ctx):
        """Faire un roll avec la stat physique"""
        await roll_stats(self, ctx, "physique")
    

    @roll.command()
    async def mental(self, ctx):
        """Faire un roll avec la stat mental"""
        await roll_stats(self, ctx, "mental")


    @roll.command()
    async def social(self, ctx):
        """Faire un roll avec la stat social"""
        await roll_stats(self, ctx, "social")


    @commands.command(name="physique")
    async def physiquep(self, ctx):
        """Faire un roll avec la stat physique"""
        await roll_stats(self, ctx, "physique")


    @commands.command(name="mental")
    async def mentalp(self, ctx):
        """Faire un roll avec la stat mental"""
        await roll_stats(self, ctx, "mental")


    @commands.command(name="social")
    async def socialp(self, ctx):
        """Faire un roll avec la stat social"""
        await roll_stats(self, ctx, "social") 


    @roll.command()
    @commands.has_role(678972972802768896)
    async def init(self, ctx, member:discord.Member, value1:int=0, value2:int=0, value3:int=0):
        """Initialiser les stats d'un utilisateur (Modérateur uniquement)"""
        logging.info(str(value1) + ' ' + str(value2) + ' ' + str(value3))
        verify = True
        if value1 == 0:
            verify = False
        if value2 == 0:
            verify = False
        if value3 == 0:
            verify = False
        if verify == False:
            return await ctx.send(":x: Tu sait, trois valeurs, c'est tout ce que je demande ! MAIS TU LES MET PAS !!!")
        else:
            mydb = utils.dbutils.init_connection()
            mycursor = mydb.cursor()
            idu = member.id
            sql = """INSERT INTO stats_user (idu, physique, mental, social, rang) VALUES (%s, %s, %s, %s, %s)"""
            val = (idu, value1, value2, value3, 1,)
            mycursor.execute(sql, val)
            mydb.commit()
            utils.dbutils.close_connection(mydb)
            return await ctx.send(":white_check_mark: Fait, le joueur " + member.mention + " peut jouer avec ses rolls !")
            

    @roll.command()
    @commands.has_role(678972972802768896)
    async def change(self, ctx, member:discord.Member, row:str="None", value:int=0):
        """Changer une valeur dans la base de données (Modérateur uniquement)"""
        supported_row = ["physique", "mental", "social", "rang"]
        if row in supported_row:
            idu = member.id
            mydb = utils.dbutils.init_connection()
            mycursor = mydb.cursor()
            sql = """UPDATE stats_user SET {}=%s WHERE idu=%s""".format(row)
            val = (value, idu,)
            mycursor.execute(sql, val)
            mydb.commit()
            utils.dbutils.close_connection(mydb)
            return await ctx.send(":white_check_mark: Fait, la valeur {} a été changée en {}".format(row, str(value)))
        else:
            return await ctx.send(":x: Faut choisir entre physique, mental, social ou rang mais pas ce que tu demande !")


    @roll.command()
    async def up(self, ctx, row:str="None"):
        """Apliquer le ou les rang up à une de vos stats"""
        supported_row = ["physique", "mental", "social"]
        if row in supported_row:
            result = await get_and_verify_eligibility(self, ctx)
            if result == True:
                mydb = utils.dbutils.init_connection()
                mycursor = mydb.cursor()
                idu = ctx.author.id
                sql = """SELECT {} FROM stats_user WHERE idu=%s""".format(row)
                val = (idu,)
                mycursor.execute(sql, val)
                respond = [r[0] for r in mycursor.fetchall()]
                respond = respond[0]
                respond = respond + 10
                sql = """UPDATE stats_user SET {}=%s WHERE idu=%s""".format(row)
                val = (respond, idu,)
                mycursor.execute(sql, val)
                mydb.commit()
                sql = """SELECT rang FROM stats_user WHERE idu=%s"""
                val = (idu,)
                mycursor.execute(sql, val)
                respond = [r[0] for r in mycursor.fetchall()]
                respond = respond[0]
                respond = respond + 1
                sql = """UPDATE stats_user SET rang=%s WHERE idu=%s"""
                val = (respond, idu,)
                mycursor.execute(sql, val)
                mydb.commit()
                utils.dbutils.close_connection(mydb)
                return await ctx.send(":white_check_mark: Vous avez level up de 10 la capacité {} !".format(row))
            else:
                return await ctx.send(":x: On peut pas parce que vous n'avez pas rang up, i am so sad !")
        else:
            return await ctx.send(":x: Faut choisir entre physique, mental ou social mais pas ce que tu demande !")
            
    
    @roll.command()
    async def stats(self, ctx):
        """Voir vos stats de rolls"""
        user = ctx.author
        idu = user.id
        mydb = utils.dbutils.init_connection()
        mycursor = mydb.cursor()
        sql = """SELECT * FROM stats_user WHERE idu=%s"""
        val = (idu,)
        mycursor.execute(sql, val)
        respond = mycursor.fetchall()
        utils.dbutils.close_connection(mydb)
        respond = respond[0]
        phy = str(respond[1])
        men = str(respond[2])
        soc = str(respond[3])
        embed=discord.Embed(title="Stats roll de " + user.name + "#" + user.discriminator, color=0x0080ff)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Physique", value=phy, inline=True)
        embed.add_field(name="Mental", value=men, inline=True)
        embed.add_field(name="Social", value=soc, inline=True)
        await ctx.send(embed=embed)

        
def setup(bot):
    bot.add_cog(Rolls(bot))
