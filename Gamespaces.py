import copy
import random
import re
import time
from typing import Type

import numpy as np

import Rooms
import config
from config import RoomConfig

random.seed(int(time.time()))
EASY = EZ = 0
BASIC = 1
HARD = 2
HARDCORE = 3
GODMODE = 4


class GameSpace:
    # __room_mapping__: dict[int, tuple[int, int]] | None

    class FloorGenerator(type):
        def __new__(mcs, name, bases, attrs):
            return type.__new__(mcs, name, bases, attrs)

        def __call__(cls, *args, **kwargs):
            tmp_obj = super(GameSpace.FloorGenerator, cls).__call__(*args, **kwargs)
            tmp_obj: GameSpace.Floor
            config_: RoomConfig
            if RoomConfig.has_instance():
                config_ = copy.deepcopy(RoomConfig())
            else:
                config_ = copy.deepcopy(RoomConfig(3, config.Modes.HARDCORE))
            tmp_obj.start_pos = (config_.max_size // 2, config_.max_size // 2)
            max_rooms = config_.total_rooms
            if len(tmp_obj.space[0]) < config_.max_size:
                raise IndexError("the size of the gamespace 2 dimensional array is too short")

            def _mkFloor_recursively(floor: GameSpace.Floor, conf: RoomConfig) -> GameSpace.Floor:
                current_room_number = 0
                return_flag = False
                forced_end_nodes = int(conf.total_rooms * 0.3)
                available_incremental = {"front": (0, 1),
                                         "back": (0, -1),
                                         "left": (1, 0),
                                         "right": (-1, 0)
                                         }
                last_direction_mapping = {"front": "back",
                                          "back": "front",
                                          "left": "right",
                                          "right": "left"
                                          }
                # available_incremental = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                available_rooms = Rooms.rooms_list(normal=True)

                def _choose_room(options, room_number: int) -> Type[Rooms.Room]:
                    nonlocal max_rooms, conf
                    if room_number <= max(int(max_rooms * 0.1 - 2), 2):
                        tmp = random.choice(Rooms.rooms_list(friendly=True, normal=True))
                    elif room_number > max_rooms and conf.max_boss_rooms > 0:
                        # in this case return a Rooms.BossRoom class
                        conf.max_boss_rooms -= 1
                        return Rooms.BossRoom
                    else:
                        for i in range(len(options)):
                            _ = random.randint(0, i)
                            options[i], options[_] = options[_], options[i]
                        tmp = random.choice(options)

                    assert issubclass(tmp[1], Rooms.Room)
                    tmp: tuple[str, Type[Room]]
                    find_statement = f"max_{re.findall(r'[a-zA-Z][^A-Z]*', tmp[0])[0].lower()}_rooms"
                    if hasattr(conf, find_statement):
                        attr = getattr(conf, find_statement)
                        if attr > 0:
                            setattr(conf, find_statement, attr - 1)
                        else:
                            if tmp in options:
                                options.remove(tmp)
                            return _choose_room(options, room_number)
                    else:
                        if not conf.randomly_rtype:
                            return Rooms.NormalRoom

                    return tmp[1]

                def _dfs(pos_x, pos_y, recursive_depth=None, last_rm_number=None, last_direction=None):
                    nonlocal floor, conf, current_room_number, return_flag, \
                        available_incremental, available_rooms, forced_end_nodes, max_rooms, last_direction_mapping

                    if return_flag:
                        if floor.space[pos_x][pos_y] == 0:
                            setattr(floor.space[last_rm_number], last_direction, False)
                        return

                    if conf.total_rooms == 0:
                        current_room_number += 1
                        floor.space[pos_x][pos_y] = Rooms.Stairs()
                        floor.space[pos_x][pos_y].room_number = current_room_number
                        floor.room_mapping[current_room_number] = (pos_x, pos_y)
                        return_flag = True
                        floor.end_pos = (pos_x, pos_y)
                        return
                    if recursive_depth == 0:
                        if floor.space[pos_x][pos_y] == 0:
                            setattr(floor[last_rm_number],  last_direction, False)
                        return
                    current_room_number += 1
                    if current_room_number == 1:
                        choose = random.choice(list(available_incremental.keys()))
                        floor.space[pos_x][pos_y] = Rooms.StartRoom()
                        floor.room_mapping[current_room_number] = (pos_x, pos_y)
                        floor.space[pos_x][pos_y].room_number = current_room_number
                        setattr(floor.space[pos_x][pos_y], choose, True)
                        _dfs(pos_x + available_incremental[choose][0],
                             pos_y + available_incremental[choose][1],
                             last_direction=choose)
                    else:
                        conf.total_rooms -= 1
                        assert not isinstance(floor.space[pos_x][pos_y], Rooms.Room)
                        floor.space[pos_x][pos_y] = _choose_room(available_rooms, current_room_number)()
                        floor.space[pos_x][pos_y].room_number = current_room_number
                        floor.room_mapping[current_room_number] = (pos_x, pos_y)
                        # random.shuffle(list(available_incremental.keys()))
                        if last_direction is not None:
                            setattr(floor.space[pos_x][pos_y], last_direction_mapping[last_direction], True)
                            setattr(floor.space[pos_x][pos_y], "last", last_direction_mapping[last_direction])
                        # print(floor.space[pos_x][pos_y], floor.space[pos_x][pos_y].room_number)
                        local_end_nodes = random.randint(1, 4)
                        # if local_end_nodes == 4 and forced_end_nodes >= 4:
                        #     forced_end_nodes -= 4
                        #     return
                        chooses = list(available_incremental.keys())
                        if last_direction is not None and last_direction_mapping[last_direction] in chooses:
                            chooses.remove(last_direction_mapping[last_direction])
                        random.shuffle(chooses)
                        for choose in chooses:
                            if return_flag:
                                return
                            # if return_flag:
                            #     return
                            if not isinstance(floor.space[pos_x + available_incremental[choose][0]][
                                                  pos_y + available_incremental[choose][1]], Rooms.Room):
                                _ = _ = random.randint(0, 0x5f375a86)
                                if _ % 3 == 1 and forced_end_nodes > 0 and local_end_nodes > 0:
                                    forced_end_nodes -= 1
                                    local_end_nodes -= 1
                                    continue
                                else:
                                    setattr(floor.space[pos_x][pos_y], choose, True)
                                    # print("id:", floor.space[pos_x][pos_y].room_number, choose)
                                    # floor.space[pos_x][pos_y].linked_nodes.append(choose)
                                    if current_room_number >= max_rooms * 0.4:
                                        if recursive_depth is None:
                                            _dfs(pos_x + available_incremental[choose][0],
                                                 pos_y + available_incremental[choose][1],
                                                 recursive_depth=random.randint(4, 7),
                                                 last_rm_number=floor.space[pos_x][pos_y].room_number,
                                                 last_direction=choose)
                                        else:
                                            # print(222)
                                            _dfs(pos_x + available_incremental[choose][0],
                                                 pos_y + available_incremental[choose][1], recursive_depth - 1,
                                                 last_rm_number=floor.space[pos_x][pos_y].room_number,
                                                 last_direction=choose)
                                    else:
                                        _dfs(pos_x + available_incremental[choose][0],
                                             pos_y + available_incremental[choose][1],
                                             last_rm_number=floor.space[pos_x][pos_y].room_number,
                                             last_direction=choose)

                _dfs(floor.start_pos[0], floor.start_pos[1])
                return floor

            return _mkFloor_recursively(tmp_obj, config_)

    class Floor(metaclass=FloorGenerator):
        def __init__(self, size, floor_number):
            self.start_pos: tuple[int, int] | None = None
            self.end_pos: tuple[int, int] | None = None
            self.space: np.matrix[int | Rooms.Room] | None = np.full((size, size), 0, dtype=object)
            self.floor_number = floor_number
            self.room_mapping = dict()
            self.next_floor = None

        def father_room(self, current_room: Rooms.Room | int) -> Rooms.Room | None:
            if isinstance(current_room, int):
                if current_room not in self.room_mapping.key():
                    raise KeyError(f"There's no such key called {current_room} in room mapping! ")
                else:
                    current_room = self[current_room]
            elif isinstance(current_room, Rooms.Room):
                if current_room.room_number not in self.room_mapping.keys():
                    raise KeyError(f"There's no such key called {current_room.room_number} in room mapping! ")
                else:
                    if id(current_room) != id(self[current_room.room_number]):
                        current_room = self[current_room.room_number]
            else:
                raise ValueError("Wrong parameter!")

            if current_room.last is not None:
                return self.next_room(current_room, current_room.last)
            else:
                return None

        def next_room(self, current_room: Rooms.Room | int, direction: str | int):
            """return a Room object if from given direction if there's a way to that room
                else return None"""
            if isinstance(current_room, int):
                if current_room not in self.room_mapping.key():
                    raise KeyError(f"There's no such key called {current_room} in room mapping! ")
                else:
                    current_room = self[current_room]
            elif isinstance(current_room, Rooms.Room):
                if current_room.room_number not in self.room_mapping.keys():
                    raise KeyError(f"There's no such key called {current_room.room_number} in room mapping! ")
                else:
                    if id(current_room) != id(self[current_room.room_number]):
                        current_room = self[current_room.room_number]
            else:
                raise ValueError("Wrong parameter!")

            _ = {"front": (0, 1), "back": (0, -1), "left": (1, 0), "right": (-1, 0)}
            if isinstance(direction, str):
                direction = direction.lower()
                if hasattr(current_room, direction):
                    attribute = getattr(current_room, direction)
                    if attribute:
                        axis = self.room_mapping[current_room.room_number]
                        # print(self.space[axis[0] + _[direction][0], axis[1] + _[direction][1]])
                        return self.space[axis[0] + _[direction][0], axis[1] + _[direction][1]]
                    else:
                        return None
                else:
                    raise ValueError(f"direction can only be 'front', 'back', 'left', 'right'!")
            else:
                raise ValueError(f"type of direction can't be {type(direction)}")

        def __getitem__(self, number):
            axis = self.room_mapping[number]
            return self.space[axis[0]][axis[1]]

    def __init__(self):
        self.config = RoomConfig()
        self.floors: list = [self.Floor(self.config.max_size, floor_number=_ + 1) for _ in
                             range(self.config.floors)]
        self.mklink()

    def mklink(self):
        for floor in range(len(self.floors) - 1):
            x = self.floors[floor]
            y = self.floors[floor + 1]
            x.next_floor = y
            x.space[x.end_pos[0]][x.end_pos[1]].to_next_floor = \
                y.space[y.start_pos[0]][y.start_pos[1]]

    def next_floor(self, floor_number):
        if floor_number < self.config.floors:
            return self.floors[floor_number]
        else:
            return None

    def __getitem__(self, pos):
        return self.floors[pos]

# o = GameSpace()
