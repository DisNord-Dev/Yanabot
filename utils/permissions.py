import json
import logging
with open('config.json', 'r') as fichier:
        config = json.load(fichier)

# Système de permissions basée sur des chiffre (dit level)
# Voici à quoi chaque niveau correspond:
# Niveau 6: Fondateur du serveur ou propiétaire du bot
# Niveau 5: Administrateur du serveur
# Niveau 4: Modérateur du serveur
# Niveau 3: Animateur du serveur
# Niveau 2: Staff en test du serveur
# Niveau 1: Utilisteur ayant une fiche validé
# Niveau 0: C'est tout le monde !

async def get_level_per_roles(ctx):
    fonda = config['roles']['fonda']
    admin = config['roles']['admin']
    mod = config['roles']['mod']
    anim = config['roles']['anim']
    stafft = config['roles']['staff-t']
    fichev = config['roles']['fichev']
    roles = ctx.author.roles
    userr = []
    for role in roles:
        userr.append(role.id)
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner or fonda in userr:
        return 6
    if admin in userr:
        return 5
    if mod in userr:
        return 4
    if anim in userr:
        return 3
    if stafft in userr:
        return 2
    if fichev in userr:
        return 1
    else:
        return 0


def get_roles_per_level(level):
    if level == 6:
        return config['roles']['fonda']
    if level == 5:
        return config['roles']['admin']
    if level == 4:
        return config['roles']['mod']
    if level == 3:
        return config['roles']['anim']
    if level == 2:
        return config['roles']['stafft']
    if level == 1:
        return config['roles']['fichev']

    