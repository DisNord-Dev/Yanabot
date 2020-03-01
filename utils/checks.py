from discord.ext import commands
import utils.permissions

def iflevelisuporequal(level:int):
    async def predicate(ctx):
        respond = await utils.permissions.get_level_per_roles(ctx)
        return level <= respond
    return commands.check(predicate)