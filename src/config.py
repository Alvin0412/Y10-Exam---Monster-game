from dataclasses import dataclass
from typing import Any

from Singleton import Singleton

"""Contains a class of user-defined options for gamespace generate"""


@dataclass
class Modes:
    # do not make a instance of this class, Enum class is not working
    EASY = EZ = 0
    BASIC = 1
    HARD = 2
    # HARDCORE = 3
    # GODMODE = 4
    DEFAULT = BASIC

    def __call__(self, *args, **kwargs):
        raise ValueError()


@dataclass
class RoomConfig(metaclass=Singleton):
    """A """
    floors: int | None | Any = None
    mode: int | None | Any = None

    def __post_init__(self):
        assert isinstance(self.floors, int) or self.floors is None
        assert isinstance(self.mode, int) or self.mode is None
        self.max_size = 150  # will generate 150*150 sized matrix nparray
        if self.floors is None:
            self.floors = int(input("Enter a total floors number below \n>>> "))
        if self.mode is None:
            available_options = [(getattr(Modes, v), v) for i, v in enumerate(dir(Modes)) if v.isupper()]
            available_options.sort(key=(lambda x: x[0]))
            for i,j in available_options:
                print(f"{i}. {j}")
            mode = input("Enter your mode below \n>>> ")
            if not mode.isnumeric():
                if hasattr(Modes, f"{mode.upper()}"):
                    self.mode = getattr(Modes, f"{mode.upper()}")
                else:
                    raise NameError("Undefined mode!")
            else:
                checkmode = tuple(getattr(Modes, i) for i in tuple(i for i in dir(Modes) if i.isupper()))
                if int(mode) in checkmode:
                    self.mode = int(mode)
                else:
                    raise NameError("Undefined mode!")
                # print((int(mode) if int(mode) in (for i in dir(super()) if i.isupper()) else 0))
                # self.mode = (int(mode) if int(mode) in (for i in dir(super()) if i.isupper()) else 0)
        self.max_boss_rooms = 1
        match self.mode:
            case 0:
                self.total_rooms = 10
                self.max_monster_rooms = 2
                self.max_weapon_rooms = 2
                self.max_accessory_rooms = 1
                self.max_heal_rooms = 2
                self.randomly_rtype = False
            case 1:
                self.total_rooms = 20
                self.max_monster_rooms = 5
                self.max_weapon_rooms = 3
                self.max_accessory_rooms = 2
                self.max_heal_rooms = 6
                self.randomly_rtype = True
            case 2:
                self.total_rooms = 30
                self.max_monster_rooms = 6
                self.max_weapon_rooms = 5
                self.max_accessory_rooms = 4
                self.max_heal_rooms = 8
                self.randomly_rtype = True
            case 3:
                self.total_rooms = 50
                self.max_monster_rooms = 13
                self.max_weapon_rooms = 6
                self.max_accessory_rooms = 6
                self.max_heal_rooms = 15
                self.randomly_rtype = True
