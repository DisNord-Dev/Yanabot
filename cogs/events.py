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
import sqlite3
conn = sqlite3.connect('bot.db')
conn.text_factory = str
cursor = conn.cursor()


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.json', 'r') as fichier:
            self.config = json.load(fichier)


    @commands.command()
    @commands.has_role("Conseil des Divins")
    async def create_event(self, ctx, name:str="None", memberteam:int=0, teams:int=1):
        if name == "None":
            return await ctx.send("Votre évenement n'a pas de nom, sans nom c'est trise !")
        if memberteam == 0:
            return await ctx.send("Il me faut savoir combien peuvent rejoindre un groupe, sinon tu veut être seul face à ton destin !")

        cursor.execute("""INSERT INTO events(idevent, name, teams, maxT, term)
        VALUES(?, ?, ?, ?, ?)""", (idrecup, ))


def setup(bot):
    bot.add_cog(Events(bot))
