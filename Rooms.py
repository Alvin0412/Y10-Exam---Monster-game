import copy
import inspect
import random
import sys
import time
from typing import Type

import Entities
import Events
import GameItems


def println(contents: str, end='\n', speed=0.015):
    for i in contents:
        print(i, end='')
        sys.stdout.flush()
        time.sleep(speed)
    print(end=end)


random.seed(int(time.time()))


class ItemSelector:
    @staticmethod
    def _select_items(item_type: Type[GameItems.BasicItemType], **item_options) -> list:
        if not issubclass(item_type, GameItems.BasicItemType):
            raise ValueError("item_type should be one of the items types")
        available_options = inspect.getmembers(item_type, lambda x: inspect.isclass(x))
        # if "test_values" in item_options.keys() and item_options["test_values"]:
        #     available_options = list(
        #         filter((lambda x: hasattr(x[0], "test_values") and getattr(x[0], "test_values")),available_options))
        if "grade" in item_options.keys():
            if not isinstance(item_options["grade"], tuple):
                item_options["grade"] = tuple([item_options["grade"]])
            available_options = list(
                filter((lambda x: not x[0].startswith("_") and getattr(x[1], "grade", None) in item_options[
                    "grade"] and "Basic" not in x[0]),
                       available_options))
        else:
            # print(available_options[0][1].atk)
            available_options = list(
                filter((lambda x: not x[0].startswith("_") and "Basic" not in x[0]),
                       available_options))
        available_options = [_[1] for _ in available_options]
        # print(available_options)
        return available_options


class EntitiesSelector:
    @staticmethod
    def _select_entities(entity_type: Type[Entities.EntityGroup], **item_options):
        if not issubclass(entity_type, Entities.EntityGroup):
            raise ValueError("entity_type should be one of the entity types!")
        available_options = inspect.getmembers(entity_type, lambda x: inspect.isclass(x))
        available_options = list(
            filter((lambda x: not x[0].startswith("_") and "Basic" not in x[0]), available_options))
        available_options = [_[1] for _ in available_options]

        return available_options


class Node:
    RoomType_id = 0

    def __init__(self):
        self.front: bool = False
        self.back: bool = False
        self.left: bool = False
        self.right: bool = False

        self.last: str | None = None

    def _get_directions(self):
        return [self.front, self.back, self.left, self.right]


class Room(Node):
    RoomType_id = 1

    def __init__(self, roomid=None):
        super(Room, self).__init__()
        self.properties = set()
        self.description = ""
        self.status: int = 1
        self.room_number: int | None = roomid
        self.is_friendly: bool | None = None

    def options(self) -> list | None:
        if self.status:
            methods = inspect.getmembers(self.__class__, lambda a: inspect.isfunction(a))
            methods = [i + tuple([i[1].__doc__]) if not i[1].__doc__ is None else i for i in methods]  # 添加说明文档
            methods = list(filter(lambda x: x[0] != "options" and not x[0].startswith('_'), methods))
            return methods
        return None


class MonsterRoom(Room, EntitiesSelector):
    RoomType_id = 2

    def __init__(self):
        super(MonsterRoom, self).__init__()
        self.monsters: Entities.Monsters.BasicMonster = random.choice(self._select_entities(Entities.Monsters))()
        self.is_friendly = False
        self.description = f"A room that contains a monster"

    def options(self) -> list | None:
        methods = super().options()
        return methods

    def fight(self, player):
        if self.monsters.health > 0:
            Events.FightEvent(enemy=self.monsters, player=player).run()
            if self.monsters.health <= 0:
                self.status = 0
            return
        else:
            return println("The enemy is already dead!")


class StartRoom(Room):
    RoomType_id = 3

    def __init__(self):
        super(StartRoom, self).__init__()
        # print(self.__class__.mro())
        self.is_friendly = True
        self.description = f"here to start your game lol"


class NormalRoom(Room, ItemSelector):
    RoomType_id = 4

    def __init__(self):
        super(NormalRoom, self).__init__()
        self.is_friendly = True
        self.description = f"A very Normal room......or may be not, guess what is in side?"
        self.is_used = 0

    def find_something(self, player: Entities.Player.BasicPlayer):
        """To search what is hidden in this room, however the chance is very low"""
        println("You are trying to find something in this room.....")
        time.sleep(0.6)
        println(f"You found {'.' * random.randint(3, 7)} ", end='')
        if self.is_used == 0:
            _ = 0x5f375a86
            num = 0 if self.room_number is None else self.room_number
            if (_ % random.randint(1, 9) + num) % 8 == 0:
                cls_type = inspect.getmembers(GameItems,
                                              lambda x: inspect.isclass(x) and x.__name__ != "BasicItemType")
                _ = [None, "C", "B", "A", "SS"]
                _x = [0] * 80 + [1] * 10 + [2] * 5 + [3] * 3 + [4] * 2
                choose = _[random.choice(_x)]
                if choose is not None:
                    self.is_used = 1
                    # print(cls_type, choose)
                    print("something!(真的运气好)")
                    if player.inventory_list.find_available_pos() is not None:
                        player.pick_up(self._select_items(random.choice(cls_type)[1], grade=choose))
                    else:
                        println("You backpack is full!")
                        println("And then the thing you found just vanished")
                    time.sleep(0.4)
                    return
        self.is_used = 1
        print("nothing")
        time.sleep(0.4)
        return


class HealRoom(Room, ItemSelector):
    def __init__(self, size=4):
        super(HealRoom, self).__init__()
        self.is_friendly = True
        self.max_heals = size
        self.heals = self._choose_heals()

    def _choose_heals(self):
        available_options = self._select_items(GameItems.Heals)
        options = list()
        if len(available_options):
            for _ in range(random.randint(1, self.max_heals)):  # 随机1-2次
                if len(available_options) == 0:
                    break
                heal = random.choice(available_options)
                available_options.remove(heal)
                options.append(heal())

        return options

    def pick_a_heal_up(self, player: Entities.Player.BasicPlayer):
        """to pick up a weapon in this room"""
        if not len(self.heals):
            println("no more heals in this room!")
        else:
            if player.inventory_list.find_available_pos() is not None:
                _ = self.heals.pop()
                player.pick_up(_)
                println(f"You picked up a {_.__class__.__name__}")
            else:
                println(f"Your backpack is full!")
        time.sleep(0.2)

    def pick_up_all_heals(self, player: Entities.Player.BasicPlayer):
        _ = copy.copy(self.heals)
        # self.weapons = []
        if not _:
            _ = None
            println("no more heals in this room!")
        else:
            if player.inventory_list.find_available_pos() is None:
                println("Your backpack is full!")
            else:
                for i, v in enumerate(_):
                    if player.inventory_list.find_available_pos() is None:
                        println(f"Your backpack is full after you picked up {i + 1} heals")
                        break
                    player.pick_up(v)
                self.heals = _
        time.sleep(0.2)


class AccessoryRoom(Room, ItemSelector):
    def __init__(self, size=2):
        super(AccessoryRoom, self).__init__()
        self.is_friendly = True
        self.max_accessories = size
        self.accessories = self._choose_accessories()

    def _choose_accessories(self):
        available_options = self._select_items(GameItems.Accessory)
        options = list()

        if len(available_options):
            for _ in range(random.randint(1, self.max_accessories)):  # 随机1-2次
                if len(available_options) == 0:
                    break
                accessory = random.choice(available_options)
                available_options.remove(accessory)
                options.append(accessory())

        return options

    def pick_a_accessory_up(self, player: Entities.Player.BasicPlayer):
        """to pick up a weapon in this room"""
        if not len(self.accessories):
            println("no more accessory in this room!")
        else:
            if player.inventory_list.find_available_pos() is not None:
                _ = self.accessories.pop()
                player.pick_up(_)
                println(f"You picked up a {_}")
            else:
                println(f"Your backpack is full!")
        time.sleep(0.2)

    def pick_up_all_accessories(self, player: Entities.Player.BasicPlayer):
        _ = copy.copy(self.accessories)
        # self.weapons = []
        if not _:
            _ = None
            println("no more weapons in this room!")
        else:
            if player.inventory_list.find_available_pos() is None:
                println("Your backpack is full!")
            else:
                for i, v in enumerate(_):
                    if player.inventory_list.find_available_pos() is None:
                        println(f"Your backpack is full after you picked up {i + 1} items")
                        break
                    player.pick_up(v)
                self.accessories = _
        time.sleep(0.2)


class WeaponRoom(Room, ItemSelector):
    RoomType_id = 5

    def __init__(self, size=3):
        super(WeaponRoom, self).__init__()
        if size > 15:
            raise ValueError("A room should only contains maximum 15 items")
        self.is_friendly = True
        self.max_weapons = size
        self.weapons = self._choose_weapons()

    def _choose_weapons(self):
        available_options = self._select_items(GameItems.Weapons, grade=("SS", "A", "B", "C"))
        options = list()
        if len(available_options):
            for _ in range(random.randint(1, self.max_weapons)):  # 随机1-2次
                if len(available_options) == 0:
                    break
                weapon = random.choice(available_options)
                available_options.remove(weapon)
                options.append(weapon())

        return options

    def pick_a_weapon_up(self, player: Entities.Player.BasicPlayer):
        """to pick up a weapon in this room"""
        if not len(self.weapons):
            println("no more weapons in this room!")
        else:
            if player.inventory_list.find_available_pos() is not None:
                _ = self.weapons.pop()
                player.pick_up(_)
                println(f"You picked up a {_}")
            else:
                println(f"Your backpack is full!")
        time.sleep(0.2)

    def pick_up_all_weapons(self, player: Entities.Player.BasicPlayer):
        _ = copy.copy(self.weapons)
        # self.weapons = []
        if not _:
            _ = None
            println("no more weapons in this room!")
        else:
            if player.inventory_list.find_available_pos() is None:
                println("Your backpack is full!")
            else:
                for i, v in enumerate(_):
                    if player.inventory_list.find_available_pos() is None:
                        println(f"Your backpack is full after you picked up {i + 1} items")
                        break
                    player.pick_up(v)
                self.weapons = _
        time.sleep(0.2)

    def options(self) -> list | None:
        methods = super().options()
        return methods


class BossRoom(Room, EntitiesSelector):
    RoomType_id = 6

    def __init__(self):
        super(BossRoom, self).__init__()
        self.is_friendly = False
        self.boss: Entities.Boss.BasicBoss = random.choice(self._select_entities(Entities.Boss))()
        self.description = f"A boss room which may be contains something you want"

    def fight(self, player):
        if self.boss.health > 0:
            println("------Boss Fight------")
            Events.FightEvent(enemy=self.boss, player=player).run()
            if self.boss.health <= 0:
                self.status = 0
            return
        else:
            return println("The enemy is already dead!")


class Stairs(Room):
    RoomType_id = 7

    def __init__(self):
        super(Stairs, self).__init__()
        self.is_friendly = True
        self.to_next_floor: Room | None = None

    @staticmethod
    def upstairs():
        println("Are you sure you want to go upstairs?\n"
                f"(y)es{' ' * 5}(n)o")
        char = input()
        if char == 'y':
            return 'r'
        else:
            return


def rooms_list(**kwargs):
    cls_ = inspect.getmembers(__import__("Rooms"), inspect.isclass)
    # if len(kwargs.keys()) <= 1:
    cls_ = list(filter(lambda x: "Room" in x[0], cls_))
    if "friendly" in kwargs.keys():
        cls_ = list(filter(lambda x: x[1]().is_friendly == kwargs["friendly"], cls_))
    if "normal" in kwargs.keys():
        cls_ = list(
            filter(lambda x: kwargs["normal"] == (x[0] not in ('Room', 'Stairs', 'StartRoom', 'BossRoom')), cls_))
    # else:
    #     raise ValueError("You should only pass 1 parameter in this function")
    return cls_


if __name__ == "__main__":
    # print(rooms_list(normal=True, friendly=True))
    # o = WeaponRoom()
    # print(o.weapons)
    # print(o.pick_a_weapon_up())
    # print(rooms_list(normal=True, friendly=True))
    # print(o.options())
    ...
    # print(rooms_list(friendly=True, normal=True))
    # print(EntitiesSelector()._select_entities(Entities.Player))
