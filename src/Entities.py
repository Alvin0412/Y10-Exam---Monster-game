import copy
import random

import numpy as np

import Events
import GameItems
import Skills

"""contains entity need to generate during game and player's character"""


class Inventory:
    def __init__(self, length, player=None):
        self.max_length = length
        self.slot_array = np.array([None for _ in range(self.max_length)])
        self.player = player

    def find_available_pos(self) -> None | int:
        for p, v in enumerate(self.slot_array):
            if v is None:
                return p
        return None

    def __getitem__(self, pos):
        return self.slot_array[pos]

    def __setitem__(self, pos, value):
        self.slot_array[pos] = value

    def __str__(self):
        return f"{self.slot_array}"

    def __call__(self):
        print(self.player)
        if self.player is not None:
            return Events.InventoryEvent(self.player).run()
        else:
            super.__call__()

class Wallet:
    def __init__(self):
        self._wallet = 0

    def add_money(self, value):
        self._wallet += value

    def pay(self, other, value):
        if not hasattr(other, "wallet"):
            raise ValueError("Can't pay to an object which don't have 'wallet' attribute")
        if value > self._wallet:
            raise ValueError("No enough money!")
        else:
            self._wallet -= value
            other.add_money(value)

    def value(self):
        return copy.deepcopy(self._wallet)

    def __call__(self, *args, **kwargs):
        return self.value()


class EntityGroup:
    ...


class Entity:
    inventory_length = 10
    acc_slot_length = 4
    wep_slot_length = 1

    def __init__(self):
        self.name: str = ""
        self.status = 1  # -1 for dead, 0 for immobile, 1 for alive
        self.default_atk = 0
        self.default_defence = 0
        self.atk = 0
        self.health = 0
        self.health_limit = self.health
        self.defence = 0
        self.strike_rate = 0.0
        self.inventory_list = Inventory(self.inventory_length)
        self.accessory_slot = np.array([None, None, None, None])
        self.weapon_slot = np.array([None])

    def calc_acc_defence(self):
        cnt = 0
        for accessory in self.accessory_slot:
            if isinstance(accessory, GameItems.Accessory.BasicAccessory):
                cnt += accessory.defence
        return cnt

    def calc_weapon_atk(self):
        if self.weapon_slot[0] is None:
            return 0
        return self.weapon_slot[0].atk

    def update_defence(self):
        self.defence = self.default_defence + self.calc_acc_defence()

    def update_atk(self):
        self.atk = self.default_atk + self.calc_weapon_atk()

    def recover(self, heal: GameItems.Heals.BasicHeal):
        _ = self.health + heal.heal
        if _ > self.health_limit:
            self.health = self.health_limit
            return
        self.health = _


class Monsters(EntityGroup):
    class BasicMonster(Entity):
        def __init__(self):
            super(Monsters.BasicMonster, self).__init__()
            self.total_stage: int = 0
            self.round_cnt: int = 0
            self.difficulty: int | None = None
            self.health = 100
            self.health_limit = self.health
            self.normal_skills: list[function] = list()
            self.special_skills: list[function] = list()
            self.default_atk = 15
            self.default_defence = 5
            self.drop_rate: float = 0.0
            self.escape_rate: float = 0.0
            self.coins = 0

        def is_drop(self):
            assert self.drop_rate < 1, "drop rate must be less than 1"
            arr1 = [1, 0]
            arr2 = [self.drop_rate, 1 - self.drop_rate]
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

        def attack(self) -> Skills.BasicSkill | None:
            if len(self.normal_skills) == 0:
                return None
            return self.normal_skills[self.round_cnt % len(self.normal_skills)]()

        def update_round(self):
            self.round_cnt += 1

        def drop(self):
            if self.is_drop():
                _ = [it for it in np.concatenate((self.weapon_slot, self.accessory_slot)) if i is not None]
                return _
            else:
                return None

    class Skeleton(BasicMonster):
        def __init__(self):
            super(Monsters.Skeleton, self).__init__()
            self.name = "Skeleton"
            self.health = 100
            self.health_limit = self.health
            self.default_atk = 15
            self.default_defence = 5
            self.weapon_slot[0] = GameItems.Weapons.Bow()
            self.status = 1
            self.normal_skills = [Skills.NormalSkill.NormalAttack, Skills.NormalSkill.SnipeArrow]
            self.special_skills = []
            self.drop_rate = 0.35
            self.escape_rate = 0.5
            self.coins = random.randint(5, 15)

            self.update_defence()
            self.update_atk()

        def attack(self):
            return super().attack()

    class Zombie(BasicMonster):
        def __init__(self):
            super(Monsters.Zombie, self).__init__()
            self.name = "Zombie"
            self.health = 125
            self.health_limit = self.health
            self.default_atk = 10
            self.default_defence = 15
            self.weapon_slot[0] = GameItems.Weapons.Blade()
            self.status = 1
            self.normal_skills = [Skills.NormalSkill.NormalAttack]
            self.special_skills = []
            self.drop_rate = 0.58
            self.escape_rate = 0.7
            self.coins = random.randint(2, 10)

            self.update_defence()
            self.update_atk()

    class InfectedMiner(BasicMonster):
        def __init__(self):
            super(Monsters.InfectedMiner, self).__init__()
            self.name = "InfectedMiner"
            self.self_del = 2
            self.health = 155
            self.health_limit = self.health
            self.default_atk = 25
            self.default_defence = 20
            self.weapon_slot[0] = GameItems.Weapons.Bomb()
            self.status = 1
            self.normal_skills = [Skills.NormalSkill.NormalAttack, Skills.NormalSkill.BombGrab,
                                  Skills.SpecialSkill.ExplosiveBeam]
            self.special_skills = []
            self.drop_rate = 0.25
            self.escape_rate = 0.3
            self.coins = random.randint(40, 55)

            self.update_defence()
            self.update_atk()

        def attack(self):
            tmp = super().attack()
            if self.health <= self.health_limit * 0.15:
                if self.self_del != 0:
                    tmp_skill = Skills.NormalSkill.NormalAttack()
                    tmp_skill.effect["normal"]["descript"] = "Be prepared! The big one is coming!"
                    tmp_skill.effect["normal"]["active"] = lambda: 1
                    self.self_del -= 1
                    return tmp_skill
                else:
                    tmp_skill = Skills.NormalSkill.NormalAttack()
                    tmp_skill.effect["normal"]["descript"] = ""
                    tmp_skill.effect["normal"]["active"] = lambda: 0
                    return Skills.NormalSkill.SelfDestruct()
            return tmp


class Boss(EntityGroup):
    class BasicBoss(Monsters.BasicMonster):
        def __init__(self):
            super(Boss.BasicBoss, self).__init__()

    class ZombieSamurai(BasicBoss):
        def __init__(self):
            super(Boss.ZombieSamurai, self).__init__()
            self.name = "Zombie samurai"
            self.health = 300
            self.health_limit = self.health
            self.default_atk = 35
            self.default_defence = 0
            self.weapon_slot[0] = GameItems.Weapons.Katana()
            self.status = 1
            self.normal_skills = [Skills.NormalSkill.NormalAttack, Skills.NormalSkill.Stab,
                                  Skills.NormalSkill.AirSlash, Skills.NormalSkill.Stab]
            self.special_skills = [Skills.SpecialSkill.TripleFireSlash, Skills.SpecialSkill.Annihilate]
            self.coins = 120

            self.update_atk()
            self.update_defence()

        def attack(self) -> Skills.BasicSkill | None:
            rt = super().attack()
            if self.round_cnt % 6 == 0 and self.round_cnt != 0:
                return random.choice(self.special_skills)()
            if self.health <= self.health_limit * 0.65:
                if self.round_cnt % 3 == 0 and self.round_cnt != 0:
                    return self.special_skills[(self.round_cnt // 3) % 2]()
            return rt


class Player(EntityGroup):
    class BasicPlayer(Entity):
        def __init__(self, name="Alvin"):
            super(Player.BasicPlayer, self).__init__()
            self.name = name
            self.health = 200
            self.health_limit = self.health
            self.default_atk = 20
            self.default_defence = 10  # shouldn't be more than 100
            self.inventory_list: Inventory
            self.strike_rate = 0.2
            self.in_defence = False

            self.wallet = Wallet()
            self.inventory_list = Inventory(self.inventory_length,player=self)
            self.weapon_slot[0] = GameItems.Weapons.Stick()
            self.inventory_list[1] = GameItems.Heals.Water()
            self.inventory_list[2] = GameItems.Accessory.OldJeans()

            self.status = 1

            self.update_atk()
            self.update_defence()

        def equip_accessory(self, accessory: GameItems.Accessory.BasicAccessory):
            if not isinstance(accessory, GameItems.Accessory.BasicAccessory):
                raise ValueError("Wrong accessory: invalid type")
            else:
                if accessory.slot > 3 or accessory.slot < 0:
                    raise ValueError("Wrong accessory: invalid slot size")
                else:
                    if self.accessory_slot[accessory.slot] == 0 or self.accessory_slot[accessory.slot] is None:
                        self.accessory_slot[accessory.slot] = accessory
                    else:
                        if self.inventory_list.find_available_pos() is not None:
                            self.unequip_accessory(accessory.slot)
                            self.accessory_slot[accessory.slot] = accessory
                        else:
                            raise ValueError("Inventory has no space!")

            self.update_defence()

        def equip_weapon(self, weapon: GameItems.Weapons.BasicWeapon):
            if not isinstance(weapon, GameItems.Weapons.BasicWeapon):
                raise ValueError("Wrong weapon: invalid type")
            else:
                if weapon.slot > 3 or weapon.slot < 0:
                    raise ValueError("Wrong weapon: invalid slot range")
                else:
                    if self.weapon_slot[weapon.slot] == 0 or self.weapon_slot[weapon.slot] is None:
                        self.weapon_slot[weapon.slot] = weapon
                    else:
                        if self.inventory_list.find_available_pos() is not None:
                            self.unequip_weapon(weapon.slot)
                            self.weapon_slot[weapon.slot] = weapon
                        else:
                            raise ValueError("Inventory has no space!")

            self.update_atk()

        # noinspection DuplicatedCode
        def unequip_accessory(self, acc_pos: int, inv_pos: int | None = None):
            assert isinstance(acc_pos, int), \
                ValueError("Slot index must be integer")
            assert acc_pos in range(0, self.acc_slot_length), \
                ValueError("Slot index out of range!")

            if self.inventory_list.find_available_pos() is not None:
                acc = self.accessory_slot[acc_pos]
                if inv_pos is None:
                    self.accessory_slot[acc_pos] = None
                    new_pos = self.inventory_list.find_available_pos()
                    self.inventory_list[new_pos] = acc
                else:
                    assert isinstance(inv_pos, int), \
                        ValueError("Inventory index must be integer!")
                    assert inv_pos in range(0, self.inventory_length), \
                        ValueError("Inventory index out of range!")
                    if self.inventory_list[inv_pos] is None:
                        self.inventory_list[inv_pos] = acc
                    else:
                        raise ValueError(f"This position is already been used!")

            else:
                raise ValueError("Can't unequip: Inventory is full!")
            self.update_defence()

            # if type(inv_pos) != int:

        def unequip_weapon(self, wep_pos: int, inv_pos: int | None = None):
            assert isinstance(wep_pos, int), \
                ValueError("Slot index must be integer")
            assert wep_pos in range(0, self.wep_slot_length), \
                ValueError("Slot index out of range!")

            if self.inventory_list.find_available_pos() is not None:
                wep = self.weapon_slot[wep_pos]
                if inv_pos is None:
                    self.weapon_slot[wep_pos] = None
                    new_pos = self.inventory_list.find_available_pos()
                    self.inventory_list[new_pos] = wep
                else:
                    assert isinstance(inv_pos, int), \
                        ValueError("Inventory index must be integer!")
                    assert inv_pos in range(0, self.inventory_length), \
                        ValueError("Inventory index out of range!")
                    if self.inventory_list[inv_pos] is None:
                        self.inventory_list[inv_pos] = acc
                    else:
                        raise ValueError(f"This position is already been used!")

            else:
                raise ValueError("Can't unequip: Inventory is full!")
            self.update_atk()

        def pick_up(self, item, pos: int = None):
            # should to do it in another way but There's no much time left
            if self.inventory_list.find_available_pos() is not None:
                if isinstance(pos, int) or pos is None:
                    if isinstance(pos, int):
                        if self.inventory_list[pos] is not None:
                            new_pos = pos
                        else:
                            raise ValueError("This inventory position is not empty")
                    else:
                        new_pos = self.inventory_list.find_available_pos()
                    self.inventory_list[new_pos] = item
                else:
                    raise ValueError("Inventory index must bu integer!")
            else:
                raise ValueError("Inventory is full!")

        def drop(self, pos: int):
            assert isinstance(pos, int), \
                "Inventory index must be integer"
            assert pos in range(0, self.inventory_length), \
                "Inventory index out of range!"
            item = self.inventory_list[pos]
            self.inventory_list[pos] = None
            return item

        def check_status(self):
            if self.health <= 0:
                self.status = -1
            return self.status


#
# o = Monsters.Skeleton()
# for _ in range(20):
#     print(o.attack())
#     o.update_round()
if __name__ == "__main__":
    j = Player.BasicPlayer()
    print(j.accessory_slot)
    print(j.inventory_list.slot_array)
    j.equip_weapon(GameItems.Weapons.Stick())
    j.pick_up(GameItems.Heals.KFCCrazyFood())
    j.pick_up(GameItems.Heals.KFCCrazyFood())
    j.pick_up(GameItems.Heals.KFCCrazyFood())
    j.pick_up(GameItems.Heals.KFCCrazyFood())
    j.pick_up(GameItems.Heals.KFCCrazyFood())
    j.pick_up(GameItems.Heals.KFCCrazyFood())
    for i in j.inventory_list:
        print(i)
