import collections
import copy
import inspect
import os
import sys
import time
from typing import Any

import Entities
import GameItems
import Gamespaces
import Skills
from config import RoomConfig

# config = RoomConfig(floors=3, mode=config.Modes.BASIC)

""" This file contains classes(Events) that provides what looks like during the game and most of the logic part of 
    user's operation.
    Also some data structure I defined to help my code."""


class multidict(collections.defaultdict):
    def __init__(self):
        super(multidict, self).__init__(list)

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if key not in super().keys():
            super().__setitem__(key, list())
        super().__getitem__(key).append(value)


def println(contents: str, end='\n', speed=0.015):
    for i in contents:
        print(i, end='')
        sys.stdout.flush()
        time.sleep(speed)
    print(end=end)


class BasicEvent:
    ...


class GameOverEvent(BasicEvent):
    def __init__(self, status):
        super(GameOverEvent, self).__init__()
        self.game_exit_status = status
        self.exit_game()

    def exit_game(self):
        print("Game Over!")
        if self.game_exit_status == -1:
            println("You lose")
        sys.exit(0)


class GameEvent(BasicEvent):
    def __init__(self):
        super(GameEvent, self).__init__()

    @staticmethod
    def rules():
        println("This is a very simple game\n"
                "You need to control a player to escape from the [Dungeon] \n"
                "You may encounter monsters and you need to fight against them! \n"
                , end='\n\n')
        time.sleep(0.4)
        println("Before you play this game, you can modify your options for the game")
        time.sleep(0.4)
        println("If you entered into a Stairs room you can go to the next floor,\n"
                "until there's no more floor, you win!")
        println("If you died, you lose!", end='\n\n')
        time.sleep(0.4)
        println("Some monster is stronger than you, \n"
                "You can equip some accessories or weapons from your [inventory].", end='\n\n')
        time.sleep(0.4)
        input("Press [Enter] to continue.....")

    def run(self):
        print(f"\n{'=' * 10}Monster Game{'=' * 10}\n")
        print("1. New Game")
        print("2. Load Game")
        print("3. Version")
        print("4. game rules")
        println("\nChoose your [option]:")
        choose = None
        while choose is None:
            print(">>> ", end='')
            try:
                tmp = int(input())
                if tmp not in range(1, 4 + 1):
                    print("Invalid input!")
                else:
                    choose = tmp
            except Exception as e:
                del e
                print("Invalid input!")
        name = None
        match choose:
            case 1:
                RoomConfig()
                name = input("input your name \n>>> ")
            case 2:
                println("This option is not available yet!")
                return self.run()
            case 3:
                println("Game version: Alpha 0.01 (latest)")
                input("Press [Enter] to continue")
                return self.run()
            case 4:
                self.rules()
                return self.run()
            case _:
                return self.run()
        flag = False
        main_event = None
        while not flag:
            try:
                if name is not None:
                    main_event = GamespaceEvent(player_name=name)
                else:
                    main_event = GamespaceEvent()
            except Exception as e:
                del e
            else:
                flag = True
        main_event.run()


class GamespaceEvent(BasicEvent):
    def __init__(self, player_name="Alvin"):
        self.gamespace = Gamespaces.GameSpace()
        self.player = Entities.Player.BasicPlayer(player_name)
        self.set_default_values()

    def set_default_values(self):
        self.player.pick_up(GameItems.Heals.KFCCrazyFood())
        self.player.pick_up(GameItems.Heals.KFCCrazyFood())
        self.player.pick_up(GameItems.Heals.RoastedBeef())
        self.player.pick_up(GameItems.Heals.KFCCrazyFood())
        self.player.pick_up(GameItems.Heals.KFCCrazyFood())

    def run(self):
        for floor in self.gamespace.floors:
            FloorEvent(floor, self.player)
        println("You Win!")


class InventoryEvent(BasicEvent):
    def __init__(self, player: Entities.Player.BasicPlayer, in_fight: bool = False):
        super(InventoryEvent, self).__init__()
        self.is_in_fight = in_fight
        self.player = player
        self._available_operation = {
            'e',  # equip
            'q',  # quit
            'u',  # use
            'd',  # drop
        }
        self._available_operation_in_fight = {
            'u',  # use
            'q',  # quit
            'd'  # drop
        }

    def _display(self):
        print(f"{'-' * 10}Inventory{'-' * 10}")
        buffer = [None, None]
        for i, v in enumerate(self.player.inventory_list):
            if v is None:
                buffer[i % 2] = f"{i + 1}.[Blank]"
            else:
                buffer[i % 2] = f"{i + 1}.[{v.name}]"
            if (i + 1) % 2 == 0:
                print(buffer[0].ljust(30, ' '), buffer[1].ljust(30, ' '))
        print(f"name: {self.player.name}")
        print(f"money: {self.player.wallet.value()}")
        print(f"health: {self.player.health}")
        print(f"atk: {self.player.atk}{' ' * 5}defence: {self.player.defence}")

    def _get_inventory_option(self):
        tmp = None
        println(f"Enter your command: ")
        print(f"(q)uit{' ' * 5}(u)se item{' ' * 5}(d)rop item{' ' * 5}(e)quip")
        while tmp is None:
            try:
                print(">>> ", end='')
                _ = input()
                if _ not in self._available_operation:
                    print("Invalid input")
                else:
                    tmp = _
            except Exception as _:
                del _
                print("Invalid input")
        return tmp

    def _get_inventory_index(self):
        tmp = None
        println("Enter the item index you want to use \n(or (q)uit):")
        while tmp is None:
            try:
                print(">>> ", end='')
                _ = input()
                if _ == 'q':
                    return None
                else:
                    _ = int(_)
                if _ - 1 not in range(self.player.inventory_length):
                    print("Invalid input")
                else:
                    tmp = _ - 1
            except Exception as _:
                del _
                print("Invalid input")

        return tmp

    def _handel_inventory_option(self, option):
        if self.is_in_fight and option in self._available_operation_in_fight:
            println("You can't do this during fight!")
            return self.run()
        match option:
            case 'q':
                return
            case 'u':
                index = self._get_inventory_index()
                if index is None:
                    return self._handel_inventory_option(self._get_inventory_option())
                if self.player.inventory_list[index] is None:
                    println("* You can do nothing with an [Blank] inventory")
                    return self._handel_inventory_option(option)
                else:
                    self.player.recover(self.player.inventory_list[index])
                    if hasattr(self.player.inventory_list[index], "verb"):
                        println(
                            f"You {self.player.inventory_list[index].verb} the {self.player.inventory_list[index].name}")
                    else:
                        println(f"You eat the {self.player.inventory_list[index].name}")
                    if hasattr(self.player.inventory_list[index], "info"):
                        println(self.player.inventory_list[index].info)
                    println(f"You recovered {self.player.inventory_list[index].heal} hp!")
                    self.player.inventory_list[index] = None
                    return self.run()
            case 'd':
                index = self._get_inventory_index()
                if index is None:
                    return self._handel_inventory_option(self._get_inventory_option())
                if self.player.inventory_list[index] is None:
                    println("* You can do nothing with an [Blank] inventory")
                    return self._handel_inventory_option(option)
                else:
                    println(f"* You dropped a {self.player.inventory_list[index]} in position {index + 1}!")
                    self.player.drop(index)
                    return self.run()
            case 'e':
                index = self._get_inventory_index()
                if index is None:
                    return self._handel_inventory_option(self._get_inventory_option())
                if isinstance(self.player.inventory_list[index], GameItems.Weapons.BasicWeapon):
                    if not self.player.weapon_slot[self.player.inventory_list[index].slot]:
                        self.player.equip_weapon(self.player.inventory_list[index])
                    else:
                        if self.player.inventory_list.find_available_pos() is not None:
                            self.player.unequip_weapon(wep_pos=self.player.inventory_list[index].slot)
                            self.player.equip_weapon(self.player.inventory_list[index])
                        else:
                            println("Your inventory is full!")
                            time.sleep(0.2)
                            return self.run()
                    time.sleep(0.2)
                elif isinstance(self.player.inventory_list[index], GameItems.Accessory.BasicAccessory):
                    if not self.player.accessory_slot[self.player.inventory_list[index].slot]:
                        self.player.equip_accessory(self.player.inventory_list[index])
                    else:
                        if self.player.inventory_list.find_available_pos() is not None:
                            self.player.unequip_accessory(acc_pos=self.player.inventory_list[index].slot)
                            self.player.equip_accessory(self.player.inventory_list[index])
                        else:
                            println("Your inventory is full!")
                            return self.run()
                else:
                    println("You can't equip this!")
                    return self.player_inventory()
                println(f"You equipped a {self.player.inventory_list[index].__class__.__name__}")
                self.player.inventory_list[index] = None
                return self.run()

        return self.run()

    def run(self):
        if self.player.check_status() == -1:
            return
        else:
            self._display()
            opt = self._get_inventory_option()
            self._handel_inventory_option(opt)


class FloorEvent(BasicEvent):
    def __init__(self, floor, player: Entities.Player.BasicPlayer):

        super(FloorEvent, self).__init__()
        self.floor: Gamespaces.GameSpace.Floor = floor
        self.player = player

        self.player_location = 1  # start room
        self.is_end_of_floor = False
        self.post_init()
        self.run()

    def check_status(self):
        if self.player.check_status() == -1:
            return GameOverEvent(-1)

    def player_inventory(self):
        self.player.inventory_list()
        self.check_status()

    def post_init(self):
        print(f"\n{'=' * 20}Floor {self.floor.floor_number}{'=' * 20}", end='\n\n')

    def display_options(self):
        print(f"\n{'-' * 10}Choose a direction which you want move to{'-' * 10}")
        _ = ("front", "back", "left", "right")
        available_options = []
        index = 0
        for i, option in enumerate(_):
            if getattr(self.floor[self.player_location], option):
                print(f"{(index := index + 1)}. {option}")
                available_options.append(option)
        print(
            f"{(index := index + 1)}. back to last room {f'({_})' if (_ := self.floor[self.player_location].last) is not None else '(Blank)'}")
        println("\nChoose your direction(or (q)uit to choose room options): ")
        choose = None
        while choose is None:
            try:
                print(">>> ", end='')
                _ = input()
                if _ == 'q':
                    return
                else:
                    _ = int(_)
                if _ in range(1, index + 1):
                    choose = _
                else:
                    print("Invalid input!")
            except ValueError:
                print("Invalid input!")
        if choose == index:
            if self.floor[self.player_location].last is not None:
                println("* You backed to the last room of where you came to this room")
                self.player_location = self.floor.father_room(self.floor[self.player_location]).room_number
            else:
                println("* There's no last room!")
        elif (not self.floor[self.player_location].is_friendly) and self.floor[self.player_location].status == 1:
            println("* You can't pass through a room which contains an enemy!")
            return
        else:
            println(f"* You choose to go {available_options[choose - 1]}")
            self.player_location = self.floor.next_room(self.floor[self.player_location],
                                                        available_options[choose - 1]).room_number

    def run(self):
        while not self.is_end_of_floor:
            if self.player.check_status() == -1:
                GameOverEvent(-1)
            event_key = RoomEvent(self.player, self.floor[self.player_location]).run()
            match event_key:
                case 'i':
                    self.player_inventory()
                case 'r':
                    return
                case _:
                    self.display_options()


class RoomEvent(BasicEvent):
    def __init__(self, player, room):
        super(RoomEvent, self).__init__()
        self.player = player
        self.room = room

    def room_options(self):
        options = self.room.options()
        print(f"\nChoose your options:")
        index = 0
        if self.room.status:
            for i, v in enumerate(options):
                print(f"{i + 1}. {' '.join(v[0].split('_'))}")
                index = i + 1
        print(f"{index + 1}. move to the next room")
        index += 1
        choose = None
        println(f"\nEnter the action number\n"
                f"(or (i)nventory)")
        while choose is None:
            try:
                print(">>> ", end='')
                tmp = input()
                match tmp:
                    case 'i':
                        return tmp
                    case _:
                        tmp = int(tmp)
                        if tmp in range(1, index + 1) or tmp == -1:
                            choose = tmp
                        else:
                            print("Invalid input!")
            except ValueError:
                print("Invalid input!")
        if choose == index:
            return
        elif choose == -1:
            println(f"This room's number is: {self.room.room_number}\n")
            time.sleep(0.4)
            return self.room_options()
        else:
            args = inspect.getargs(options[choose - 1][1].__code__).args
            # print(args)
            r = None
            match len(args):
                case 0:
                    r = options[choose - 1][1]()
                case 1:
                    r = options[choose - 1][1](self.room)
                case 2:
                    r = options[choose - 1][1](self.room, self.player)
                case _:
                    println("This room operation is not available!")
        if r == 'r':
            return r
        return self.room_options()

    def run(self) -> str | None:
        println(f"\n\nYou entered to a {self.room.__class__.__name__} room!")
        return self.room_options()


class FightEvent(BasicEvent):
    def __init__(self, player: Entities.Player.BasicPlayer, enemy: Entities.Monsters.BasicMonster | Any):
        super(FightEvent, self).__init__()
        self.player: Entities.Player.BasicPlayer = player
        self.enemy: Entities.Monsters.BasicMonster = enemy
        self.round_cnt = 1
        self.rounds_dmg_to_player = multidict()
        self.is_escaped = False
        self.is_end_of_game = False

    def end_of_game(self):
        if self.player.status == -1:
            GameOverEvent(-1)
        else:
            if self.is_escaped:
                achieved_coins = 0
            elif self.enemy.status == -1:
                achieved_coins = self.enemy.coins
            else:
                raise ValueError("The game is not over")
            self.player.wallet.add_money(achieved_coins)
            println(f"You earned {achieved_coins} coins")
            self.is_end_of_game = True

    def end_of_round(self):
        if self.is_end_of_game:
            return
        if self.player.status == 0:
            self.player.status = 1
        if self.player.in_defence == 1:
            self.player.in_defence = 0
        self.calc_rounds_effect()

    def check_status(self):
        time.sleep(0.2)
        if self.enemy.health <= 0:
            self.enemy.status = -1
            print("-" * 30)
            self.end_of_game()
            # sys.exit()
        elif self.player.health <= 0:
            self.player.status = -1
            self.end_of_game()
            # sys.exit()
        elif self.is_escaped:
            self.end_of_game()
            # sys.exit()

    def current_status(self):
        print(f"<{self.player.name}>:".ljust(15, ' '), end='')
        print(f"hp: {self.player.health}".ljust(15, ' '))
        print(f"<{self.enemy.name}>:".ljust(15, ' '), end='')
        print(f"hp: {self.enemy.health}".ljust(15, ' '))

    def dmg_to_player_pt(self, dmg):
        self.player.health -= dmg
        print(f"<{self.player.name}> - {dmg} hp")

    def dmg_to_enemy_pt(self, dmg):
        self.enemy.health -= dmg
        print(f"<{self.enemy.name}> - {dmg} hp")

    def player_fight(self):
        println(f"*You damage your enemy by your [{self.player.weapon_slot[0].name}]")
        time.sleep(0.4)
        dmg_cnt = self.player.atk
        if Skills.calc_rate(self.player.strike_rate):
            println("* There is a strike attack happens!")
            time.sleep(0.4)
            dmg_cnt = self.player.atk * (1 + (self.player.strike_rate * 0.8))

        self.dmg_to_enemy_pt(dmg_cnt)
        # print(f"{self.enemy.name} -{dmg_cnt} hp")
        time.sleep(0.4)

    def player_defence(self):
        self.player.in_defence = True
        println("Now you are in defence mode!")
        time.sleep(0.4)

    def display_inventory(self):
        print(f"{'-' * 10}Inventory{'-' * 10}")
        buffer = [None, None]
        for i, v in enumerate(self.player.inventory_list):
            if v is None:
                buffer[i % 2] = f"{i + 1}.[Blank]"
            else:
                buffer[i % 2] = f"{i + 1}.[{v.name}]"
            if (i + 1) % 2 == 0:
                print(buffer[0].ljust(30, ' '), buffer[1].ljust(30, ' '))

    @staticmethod
    def _get_inventory_option():
        tmp = None
        println(f"Enter your command: ")
        print(f"(q)uit{' ' * 5}(u)se item{' ' * 5}(d)rop item")
        while tmp is None:
            try:
                print(">>> ", end='')
                _ = input()
                if _ not in ('q', 'u', 'd'):
                    print("Invalid input")
                else:
                    tmp = _
            except Exception as _:
                del _
                print("Invalid input")
        return tmp

    def _get_inventory_index(self):
        tmp = None
        println("Enter the item index you want to use \n(or (q)uit):")
        while tmp is None:
            try:
                print(">>> ", end='')
                _ = input()
                if _ == 'q':
                    return None
                else:
                    _ = int(_)
                if _ - 1 not in range(self.player.inventory_length):
                    print("Invalid input")
                else:
                    tmp = _ - 1
            except Exception as _:
                del _
                print("Invalid input")

        return tmp

    def _handel_inventory_option(self, option):
        if option == 'q':
            print('\n')
            print(f"Round {self.round_cnt}: ")
            return self.user_operation()
        elif option == 'u':
            index = self._get_inventory_index()
            if index is None:
                return self._handel_inventory_option(self._get_inventory_option())
            if isinstance(self.player.inventory_list[index], GameItems.Heals.BasicHeal):
                self.player.recover(self.player.inventory_list[index])
                if hasattr(self.player.inventory_list[index], "verb"):
                    println(
                        f"You {self.player.inventory_list[index].verb} the {self.player.inventory_list[index].name}")
                else:
                    println(f"You eat the {self.player.inventory_list[index].name}")
                if hasattr(self.player.inventory_list[index], "info"):
                    println(self.player.inventory_list[index].info)
                println(f"You recovered {self.player.inventory_list[index].heal} hp!")
                self.player.inventory_list[index] = None

            else:
                if self.player.inventory_list[index] is None:
                    println("* You can do nothing with an [Blank] inventory")
                else:
                    if hasattr(self.player.inventory_list[index], "name"):
                        println(f"You can't use {self.player.inventory_list[index].name} during fight!")
                    else:
                        println(f"You can't use {self.player.inventory_list[index]} during fight!")
                return self._handel_inventory_option(option)
        elif 'd':
            index = self._get_inventory_index()
            if index is None:
                return self._handel_inventory_option(self._get_inventory_option())
            if self.player.inventory_list[index] is None:
                println("* You can do nothing with an [Blank] inventory")
                return self._handel_inventory_option(option)
            else:
                println(f"* You dropped a {self.player.inventory_list[index]} in position {index + 1}!")
                self.player.drop(index)

    def player_heal(self):
        self.display_inventory()
        comm = self._get_inventory_option()
        self._handel_inventory_option(comm)

    def player_escape(self):
        if self.enemy.health / 100 < self.enemy.escape_rate:
            self.is_escaped = True
            println("You escaped...")
        else:
            println("You can't escape!", end='\n\n')
            return self.user_operation()

    def user_operation(self):
        if self.player.status == 0:
            println("* You can't move in this round!")
            return
        println("*Your turn!")
        choose = None
        println("Choose your action: ")
        print(f"1. Fight \n"
              f"2. Defence \n"
              f"3. Heal \n"
              f"4. Escape\n")
        self.current_status()
        println(f"\nEnter the action number")
        while choose is None:
            try:
                print(">>> ", end='')
                _ = int(input())
                if _ in range(1, 4 + 1):
                    choose = _
                else:
                    print("Invalid input!")
            except ValueError:
                print("Invalid input!")
        match choose:
            case 1:
                self.player_fight()
            case 2:
                self.player_defence()
            case 3:
                self.player_heal()
            case 4:
                self.player_escape()

    @staticmethod
    def calc_dmg(dmg):
        return dmg * (1 + ((5 + RoomConfig().mode) / 10))

    def calc_dmg_to_player(self, dmg):
        return (dmg + self.enemy.atk * 0.6) * (1 + ((2 + RoomConfig().mode) / 10)) * (1 - self.player.defence / 100)

    def calc_rounds_effect(self):
        indexes = []
        for index, effects_list in self.rounds_dmg_to_player.items():
            # print("effect_list",effects_list)
            for effects in effects_list:
                # print(effects_list)
                # print("effects",effects)
                if not isinstance(effects, dict):
                    continue
                # print(effects)
                effects["round"] -= 1
                if effects["round"] >= 0:
                    if "round-descript" not in effects.keys():
                        println(effects["descript"])
                    else:
                        println(effects["round-descript"])
                    for k, v in effects.items():
                        if k == "extra-dmg":
                            self.dmg_to_player_pt(self.calc_dmg(v))
                        elif k == "immobile":
                            self.player.status = 0
                else:
                    indexes.append(index)
        for i in indexes:
            self.rounds_dmg_to_player.pop(i)

    def get_after_effect_for_enemy(self, skill):
        enemy_buff = skill.others
        if isinstance(enemy_buff, dict):
            for k, v in enemy_buff.items():
                for k1, v1 in v.items():
                    if k1 == "dmg":
                        println(enemy_buff[k]["descript"])
                        self.dmg_to_enemy_pt(v1)

    def get_enemy_options_name(self, skill, dmg):
        skill = skill
        description = skill.description
        buff = skill.effect
        enemy_buff = skill.others
        effects = []
        # print(buff)
        for k, v in buff.items():
            # print(2)
            rate = v["active"]()
            # print(rate)
            if rate:
                # print(1919810)
                effects.append(v["descript"])
                if v["round"] > 0:
                    self.rounds_dmg_to_player[k] = copy.copy(v)
        description_to_print = []  # comprehension doesn't work I don't know why
        for stmt in description:
            if stmt is None:
                for i in effects:
                    description_to_print.append(i)
                    # print(114514)
            else:
                description_to_print.append(stmt)
        description_to_print[0] = description_to_print[0].format(attacker=self.enemy.name,
                                                                 skill=skill.__class__.__name__,
                                                                 defender="You")
        description_to_print[-1] = description_to_print[-1].format(dmg=dmg,
                                                                   defender="You")
        return description_to_print

    def enemy_attack(self):
        skill = self.enemy.attack()

        dmg_cnt = self.calc_dmg_to_player(skill.dmg)
        # print(f"{skill.dmg} {RoomConfig().mode} {(1 + ((5 + RoomConfig().mode) // 10)) } {dmg_cnt}")
        description = self.get_enemy_options_name(skill, dmg_cnt)
        print()
        println("* Enemy's turn")
        for _ in description:
            println(_)
            time.sleep(0.2)
        if self.player.in_defence:
            println("Because you're in defence mode, some damages are decreased!")
            dmg_cnt *= 0.8
        self.dmg_to_player_pt(dmg_cnt)
        self.get_after_effect_for_enemy(skill)
        time.sleep(0.4)

    def npc_operation(self):
        self.enemy_attack()

    def run(self):
        print(f"{'=' * 15}Fight{'=' * 15}", end="\n\n")

        while not self.is_end_of_game:
            print(f"Round {self.round_cnt}: ")

            time.sleep(0.4)
            self.user_operation()
            self.check_status()
            if self.is_end_of_game:
                break
            self.npc_operation()
            self.round_cnt += 1

            self.enemy.update_round()
            self.check_status()
            self.end_of_round()

            if not self.is_end_of_game:
                input("Press [Enter] to continue...")
                os.system("cls")


class PlayerFight(BasicEvent):
    ...


if __name__ == "__main__":
    # game_event = GameEvent()
    # game_event.run()
    println("==Test==")
    # RoomEvent()

    player = Entities.Player.BasicPlayer()
    FightEvent(player=player, enemy=Entities.Boss.ZombieSamurai()).run()
    # player.pick_up(GameItems.Heals.KFCCrazyFood())
    # player.pick_up(GameItems.Heals.KFCCrazyFood())
    # player.pick_up(GameItems.Heals.KFCCrazyFood())
    # player.pick_up(GameItems.Heals.KFCCrazyFood())
    # player.pick_up(GameItems.Heals.KFCCrazyFood())
    # player.equip_accessory(accessory=GameItems.Accessory.HarrowHaikouHILAUniform())
    # monster = Entities.Monsters.Skeleton()
    # o = FightEvent(player, monster)
    # o.run()
    # print(monster.health, player.wallet())
# if __name__ == "__main__":
#     o = multidict()
#     o["1"] = 1
#     o['1'] = 2
#     print(o)
