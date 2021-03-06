__author__ = 'Daniel'

def find_spell_target(game, criteria_function=lambda target: True):
    def filter_function(target):
        return criteria_function(target) and target.spell_targettable()

    targets = game.other_player.minions.copy()
    targets.extend(game.current_player.minions)
    targets.append(game.other_player)
    targets.append(game.current_player)

    targets = [target for target in targets if filter_function(target)]
    return targets


def find_battlecry_target(game):
    targets = game.other_player.minions.copy()
    targets.extend(game.current_player.minions)
    targets.append(game.other_player)
    targets.append(game.current_player)

    return targets


def find_enemy_spell_target(game, criteria_function=lambda target: True):
    def filter_function(target):
        return criteria_function(target) and target.spell_targettable()

    targets = game.other_player.minions.copy()
    targets.append(game.other_player)

    targets = [target for target in targets if filter_function(target)]
    return targets


def find_minion_spell_target(game, criteria_function=lambda target: True):
    def filter_function(target):
        return criteria_function(target) and target.spell_targettable()

    targets = game.other_player.minions.copy()
    targets.extend(game.current_player.minions)

    targets = [target for target in targets if filter_function(target)]
    return targets


def find_minion_battlecry_target(game):
    targets = game.other_player.minions.copy()
    targets.extend(game.current_player.minions)
    if len(targets) is 0:
        return None
    return targets


def find_enemy_minion_spell_target(game, criteria_function=lambda target: True):
    def filter_function(target):
        return criteria_function(target) and target.spell_targettable()

    targets = game.other_player.minions.copy()

    targets = [target for target in targets if filter_function(target)]
    return targets

def find_enemy_minion_battlecry_target(game):
    targets = game.other_player.minions.copy()
    if len(targets) is 0:
        return None
    return targets

def find_friendly_minion_battlecry_target(game):
    targets = game.current_player.minions.copy()
    if len(targets) is 0:
        return None
    return targets