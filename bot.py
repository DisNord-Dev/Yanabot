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


import sys, traceback
import discord
from discord.ext import commands
import logging
import time
import schedule
import asyncio
import json


with open('config.json', 'r') as fichier:
    config = json.load(fichier)


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
token = config['bot']['token']


initial_extensions = ['jishaku',
                      'cogs.misc',
                      'cogs.actions',
                      'cogs.rolls']
bot = commands.Bot(command_prefix=config['bot']['prefix'])


@bot.event
async def on_ready():
    logging.info(f'\n\nBot en cours de fonctionnemnt en tant que: {bot.user.name} - {bot.user.id}\n'
          f'Version de discord.py: {discord.__version__}\n')
    game = discord.Game(name="gérer le serveur de Fantasya -- !help")
    await bot.change_presence(activity=game, status=discord.Status.online)
    logging.info(f'Bot prêt pour observer le RP !')
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


bot.run(token, bot=True, reconnect=True)
