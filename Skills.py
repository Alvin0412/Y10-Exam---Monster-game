import functools
import random
import time
import typing


def calc_rate(drop_rate):
    assert drop_rate < 1, "drop rate must be less than 1"
    arr1 = [True, False]
    arr2 = [drop_rate, 1 - drop_rate]
    sup_list = [len(str(_).split(".")[-1]) for _ in arr2]
    top = 10 ** max(sup_list)
    new_rate = [int(_ * top) for _ in arr2]
    rate_arr = []
    for _ in range(1, len(new_rate) + 1):
        rate_arr.append(sum(new_rate[:_]))
    rand = random.randint(1, top)
    data = None
    for _ in range(len(rate_arr)):
        if rand <= rate_arr[_]:
            data = arr1[_]
            break
    return data


random.seed(time.time())


class BasicSkill:
    def __init__(self):
        self.dmg = 0
        self.description: list[str | typing.Any] = [
            "<{attacker}> used the [{skill}] to {defender}",
            None,
            "caused {dmg} damages to {defender}!"
        ]  # therefore you can only change [1] to modify attributes
        self.effect: dict = {}
        self.others: dict = {}

    # @classmethod
    # def get_dmg(cls) -> dict:
    #     if not importlib.util.find_spec("time"):
    #         importlib.import_module("time")
    #     return {
    #         "name": cls.__name__.capitalize(),
    #         "dmg": cls.dmg,
    #         "description": cls.description,
    #         "effect": cls.effect,
    #         "others": cls.others
    #     }


class SpecialSkill:
    class ExplosiveBeam(BasicSkill):
        def __init__(self):
            super(SpecialSkill.ExplosiveBeam, self).__init__()
            self.dmg = 20
            self.effect = {
                "blind": {
                    "active": functools.partial(calc_rate, 0.3),
                    "round": 1,
                    "descript": "Shining light blind your eyes: You can not move for 1 round",
                    "extra-dmg": 5,
                    "immobile": True
                }
            }

            self.others = None

    class FireVortex(BasicSkill):
        def __init__(self):
            super(SpecialSkill.FireVortex, self).__init__()
            self.dmg = 25
            self.effect = {
                "burn": {
                    "active": functools.partial(calc_rate, 0.8),
                    "round": 3,
                    "descript": "The fire keeps burning on your body",
                    "extra-dmg": 7.5
                }
            }

            self.others = None

    class TripleFireSlash(BasicSkill):
        def __init__(self):
            super(SpecialSkill.TripleFireSlash, self).__init__()
            self.dmg = 20
            rate = calc_rate(0.8)
            self.effect = {
                "burning slash": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The flame-slashes slicing everything in their way!",
                    "extra-dmg": 15
                },
                "burn1": {
                    "active": lambda: rate,
                    "round": 3,
                    "descript": "The fire keeps burning on your body, seems more painful than normal fire",
                    "extra-dmg": 10
                },
                "burn2": {
                    "active": lambda: rate,
                    "round": 0,
                    "descript": "The fire keeps burning on your body!",
                    "extra-dmg": 15
                }
            }

    class DivineArrow(BasicSkill):
        def __init__(self):
            super(SpecialSkill.DivineArrow, self).__init__()
            self.dmg = 50
            self.effect = {
                "bleeding": {
                    "active": functools.partial(calc_rate, 0.7),
                    "round": 2,
                    "descript": "The piercing arrow snipe through your body! You are in serious bleeding",
                    "extra-dmg": 15
                }
            }

            self.others = None

    class RevolvingRavager(BasicSkill):
        def __init__(self):
            super(SpecialSkill.RevolvingRavager, self).__init__()
            self.dmg = 67.5
            self.effect = {
                "tornado": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The enemy use their weapon to form a red and black tornado.\n"
                                "It drags you away withs an explosion!"
                }
            }
            self.others = None

    class InfernalHurricane(BasicSkill):
        def __init__(self):
            super(SpecialSkill.InfernalHurricane, self).__init__()
            self.dmg = 37.5
            self.effect = {
                "stuns": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "A large fire-hurricane drags you away"
                },
                "burn": {
                    "active": functools.partial(calc_rate, 0.8),
                    "round": 3,
                    "descript": "The fire keeps burning on your body",
                    "extra-dmg": 10
                }
            }
            self.others = None

    class InjectionShot(BasicSkill):
        def __init__(self):
            super(SpecialSkill.InjectionShot, self).__init__()
            self.dmg = 48
            self.effect = {
                "stuns": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "A lightning-like projectile shoots out of enemy's weapon, \n"
                                "it snipe through your body and cause some serious electronic shock"
                },
                "shock": {
                    "active": lambda: 1,
                    "round": 3,
                    "round-descript": "You were shocked by electricity",
                    "extra-dmg": 8
                },
                "bleeding": {
                    "active": functools.partial(calc_rate, 0.8),
                    "round": 2,
                    "round-descript": "You are in bleeding",
                    "extra-dmg": 5
                }
            }
            self.others = None

    class Annihilate(BasicSkill):
        def __init__(self):
            super(SpecialSkill.Annihilate, self).__init__()
            self.dmg = 25
            self.effect = {
                "slash": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The enemy closed their eyes, "
                                "randomly slashes everything around them with in a very high speed"
                },
                "slash1": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The slash approached to you! you can't escape this!",
                    "extra-dmg": 8
                },
                "slash2": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The slash approached to you again!",
                    "extra-dmg": 7
                },
                "slash3": {
                    "active": functools.partial(calc_rate,0.8),
                    "round": 0,
                    "descript": "The slash approached to you again and again!",
                    "extra-dmg": 6
                },
                "slash4": {
                    "active": functools.partial(calc_rate, 0.7),
                    "round": 0,
                    "descript": "The slash hit you again!",
                    "extra-dmg": 10
                },
                "slash5": {
                    "active": functools.partial(calc_rate, 0.5),
                    "round": 0,
                    "descript": "The slash hit you again!Who knows when there's an end",
                    "extra-dmg": 5
                }
            }


class NormalSkill:
    class NormalAttack(BasicSkill):
        def __init__(self):
            super(NormalSkill.NormalAttack, self).__init__()
            self.dmg = 1
            self.effect = {
                "normal": {
                    "active": lambda: 0,
                    "round": 0,
                    "descript": "",
                    "extra-dmg": 0
                }
            }
            self.others = None

    class BombGrab(BasicSkill):
        def __init__(self):
            super(NormalSkill.BombGrab, self).__init__()
            self.dmg = 15
            self.effect = {
                "explosive": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The enemy grab up a bomb and throw it to your face"
                }
            }
            self.others = None

    class ExplosivePunch(BasicSkill):
        def __init__(self):
            super(NormalSkill.ExplosivePunch, self).__init__()
            self.dmg = 16
            self.effect = {
                "explosive": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The enemy throws punches within explosions"
                }
            }
            self.others = {
                "self damage": {
                    "dmg": -10,
                    "descript": "But the enemy also got some damages!"
                }
            }

    class SelfDestruct(BasicSkill):
        def __init__(self):
            super(NormalSkill.SelfDestruct, self).__init__()
            self.dmg = 60
            self.effect = {
                "explosion": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The enemy try to destroy themself to make a big explosion!"
                }
            }
            self.others = {
                "self damage": {
                    "dmg": 1145141919810,
                    "descript": "The enemy destroy it self"
                }
            }

    class SnipeArrow(BasicSkill):
        def __init__(self):
            super(NormalSkill.SnipeArrow, self).__init__()
            self.dmg = 15
            self.effect = {
                "bleeding": {
                    "active": functools.partial(calc_rate, 0.8),
                    "round": 2,
                    "descript": "The enemy snipe on your body accurately! You start to bleeding",
                    "round-descript": "You are in bleeding!",
                    "extra-dmg": 5
                }
            }
            self.others = None

    class ExecutionStab(BasicSkill):
        def __init__(self):
            super(NormalSkill.ExecutionStab, self).__init__()
            self.dmg = 25
            self.effect = {
                "bleeding": {
                    "active": lambda: 1,
                    "round": 1,
                    "descript": "The enemy stab through your body! You are in bleeding",
                    "round-descript": "You are in bleeding!",
                    "extra-dmg": 7
                }
            }
            self.others = None

    #
    #
    class AirSlash(BasicSkill):
        def __init__(self):
            super(NormalSkill.AirSlash, self).__init__()
            self.dmg = 20
            self.effect = {
                "bleeding": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The enemy slices the air and release a slash, it hits you!"
                }
            }
            self.others = None

    class Stab(BasicSkill):
        def __init__(self):
            super(NormalSkill.Stab, self).__init__()
            self.dmg = 13
            self.effect = {
                "bleeding": {
                    "active": lambda: 1,
                    "round": 0,
                    "descript": "The enemy dash to front of you and stab you!"
                }
            }
            self.others = None

    # class TornadoSlash(BasicSkill):
    #     def __init__(self):
    #         super(TornadoSlash, fself).__init__()

    class Assassinate(BasicSkill):
        def __init__(self):
            super(NormalSkill.Assassinate, self).__init__()
            self.dmg = 20
            self.effect = {
                "stab": {
                    "active": functools.partial(calc_rate, 0.7),
                    "round": 3,
                    "descript": "The enemy stab you when you lose your focus! You are now in bleeding",
                    "extra-dmg": 8
                }
            }
            self.others = None

    # class RagingWind(BasicSkill):
    #     def __init__(self):
    #         super(RagingWind, self).__init__()

    # class ScatterShot(BasicSkill):
    #     def __init__(self):
    #         super(ScatterShot, self).__init__()

# pprint.pp(SpecialSkill.ExplosiveBeam.get_dmg())
# a = SpecialSkill.ExplosiveBeam.get_dmg()
# pprint.pp(a['description'][0] % "Alvin")
# if inspect.isbuiltin(a['description'][1]):
#     a['description'][1](1)
# else:
#     pprint.pp(a['description'][1])
# pprint.pp(a['description'][2])
# pprint.pp(a['description'][3] % (100,"Alvin"))
# description = a['description']
# for i, v in enumerate(description):
#     if inspect.isbuiltin(v):
#         v(0.5)
#     else:
#         if i == 0:
#             pprint.pp(v % "Alvin")
#         elif i == len(description) - 1:
#             pprint.pp(v % (a['dmg'], "Danny"))
#         else:
#             pprint.pp(v)
#     time.sleep(0.3)
