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

class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.json', 'r') as fichier:
            self.config = json.load(fichier)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        logging.info("Yeah, cette partie sert à rien car elle n'est pas codée !")


def setup(bot):
    bot.add_cog(Actions(bot))
