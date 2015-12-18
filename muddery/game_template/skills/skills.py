"""
Default skills.
"""

import random
from muddery.utils.localized_strings_handler import LS


def skill_example(caller, target, *args, **kwargs):
    """
    It is an example.
    """
    pass


def skill_escape(caller, target, effect=0, *args, **kwargs):
    """
    Escape from this combat.
    args:
        effect: the odds of fail.
    """
    if not caller:
        return

    if not caller.ndb.combat_handler:
        # caller is not in combat.
        return

    rand = random.random()
    if rand < effect:
        return [{"type": "left",
                 "caller": caller.dbref,
                 "success": False}]

    caller.ndb.combat_handler.remove_character(caller)
    caller.msg({"combat_finish": {"escaped": True}})

    return [{"type": "left",
             "caller": caller.dbref,
             "success": True}]


def skill_heal(caller, target, effect=0, *args, **kwargs):
    """
    Heal the caller.
    args:
        effect: the hp value to increase.
    """
    if effect <= 0:
        return

    if not caller:
        return

    target = caller

    if target:
        recover_hp = target.add_hp(effect)
        if recover_hp > 0:
            target.show_status()

    return [{"type": "healed",              # heal result
             "caller": caller.dbref,        # caller's dbref
             "target": target.dbref,        # target's dbref
             "effect": effect,              # effect
             "hp": target.db.hp,            # current hp of the target
             "max_hp": target.max_hp}]      # max hp of the target


def skill_hit(caller, target, effect=0, *args, **kwargs):
    """
    Hit the target.
    args:
        effect: the ratio of the damage.
    """
    if effect <= 0:
        return

    if not caller:
        return

    if not target:
        return

    # calculate the damage
    damage = float(caller.attack) / (caller.attack + target.defence) * caller.attack
    damage = round(damage * effect)
    
    # hurt target
    target.hurt(damage)

    return [{"type": "attacked",            # attack result
             "caller": caller.dbref,        # caller's dbref
             "target": target.dbref,        # target's dbref
             "effect": damage,              # effect
             "hp": target.db.hp,            # current hp of the target
             "max_hp": target.max_hp}]      # max hp of the target


def skill_increase_hp(caller, target, effect=0, *args, **kwargs):
    """
    Passive skill, increase the caller's max_hp.
    args:
        effect: the max_hp value to increase.
    """
    if effect <= 0:
        return

    if not caller:
        return

    target = caller

    if target:
        caller.max_hp += effect
        hp = caller.db.hp + effect
        if hp > caller.max_hp:
            hp = caller.max_hp
        caller.db.hp = hp
