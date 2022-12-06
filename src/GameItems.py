"""contains items which need to use in game"""
class BasicItemType:
    ...


class Weapons(BasicItemType):
    class BasicWeapon:
        name = "test weapon"
        atk: int | None = None
        grade: str | None = None
        slot: int = -1
        info: str | None = None
        mkt_value: int | None = None

        @classmethod
        def get_description(cls) -> dict:
            return {
                "atk": cls.atk,
                "grade": cls.grade,
                "info": cls.info,
                "slot": cls.slot,
                "mkt_value": cls.mkt_value
            }

    class Blade(BasicWeapon):
        name = "blade"
        atk = 10
        info = "A normal blade in test"
        grade = "B"
        slot = 0
        mkt_value = 10

    class Fish(BasicWeapon):
        name = "fish"
        atk = 1
        info = "Not capable for eating"
        grade = "SS"
        slot = 0
        mkt_value = 114514

    class Stick(BasicWeapon):
        name = "stick"
        atk = 2
        info = "Some main character from different RPG game taken this as their first weapon"
        grade = "C"
        slot = 0
        mkt_value = 0

    class Katana(BasicWeapon):
        name = "katana"
        atk = 20
        info = "A very traditional Japanese katana"
        grade = "A"
        slot = 0
        mkt_value = 40

    class Dagger(BasicWeapon):
        name = "dagger"
        atk = 20
        info = "A rusty dagger"
        grade = "B"
        slot = 0
        mkt_value = 5

    class SharpenKnife(BasicWeapon):
        name = "sharpen knife"
        atk = 15
        info = "Sharpen Knife! Can't take this into HarrowHaikou"
        grade = "A"
        slot = 0
        mkt_value = 25

    class Bomb(BasicWeapon):
        name = "bomb"
        atk = 20
        info = "An explosive item! Very dangerous"
        grade = "B"
        slot = 0
        mkt_value = 100

    class Bow(BasicWeapon):
        name = "bow"
        atk = 15
        info = "A Bow and some arrows"
        grade = "B"
        slot = 0
        mkt_value = 20


class Heals(BasicItemType):
    class BasicHeal:
        name = ""
        heal: int | None = None
        grade: str | None = None
        info: str | None = None
        mkt_value: int | None = None

        @classmethod
        def get_description(cls) -> dict:
            return {
                "heal": cls.heal,
                "grade": cls.grade,
                "info": cls.info,
                "mkt_value": cls.mkt_value
            }

    class Orange(BasicHeal):
        name = "orange"
        heal = 30
        grade = "A"
        info = "A legendary stuff...at least in HarrowHaikou"

    class KFCCrazyFood(BasicHeal):
        name = "KFC Crazy Food"
        heal = 80
        grade = "A"
        info = "It's Crazy Thursday!!! V me 50"

    class DogFood(BasicHeal):
        name = "Dog food"
        heal = 50
        grade = "B"
        info = "Even it is for dogs, but at least taste not bad"

    class Water(BasicHeal):
        name = "water"
        verb = "drink"
        heal = 15
        grade = "C"
        info = "A bottle of water! But it is not clean......"

    class HarrowHaikouLunch(BasicHeal):
        name = "Harrow Haikou lunch"
        heal = -1919810
        grade = "D"
        info = "Even dogs don't want it to appear in their dinner, may be you should drop it"

    class Bread(BasicHeal):
        name = "bread"
        heal = 25
        grade = "B"
        info = "A bread....taste not very good"

    class RoastedBeef(BasicHeal):
        name = "roasted beef"
        heal = 50
        grade = "A"
        info = "This beef taste very good! "


class Accessory(BasicItemType):
    class BasicAccessory:
        name = ""
        defence: int | None = None
        grade: str | None = None
        slot: int = -1
        info: str | None = None
        mkt_value: int | None = None

        @classmethod
        def get_description(cls) -> dict:
            return {
                "defence": cls.defence,
                "grade": cls.grade,
                "info": cls.info,
                "slot": cls.slot,
                "mkt_value": cls.mkt_value
            }

    class QieErXi(BasicAccessory):
        name = "切尔西"
        defence = 30
        grade = "SS"
        info = "英雄可以受委屈, 但是你不能踩我的切尔西"
        slot = 3
        mkt_value = 1000

    class HarrowHaikouHILAUniform(BasicAccessory):
        name = "Harrow Haikou HILA Uniform"
        defence = 20
        grade = "A"
        info = "Everyday Alvin and other Harrow Haikou HILA students wear this to school"
        slot = 1
        mkt_value = 200

    class OldJeans(BasicAccessory):
        name = "old jeans"
        defence = 5
        grade = "B"
        slot = 2
        info = "A very normal outfit"
        mkt_value = 8

    class DirtyShirt(BasicAccessory):
        name = "dirty shirt"
        defence = 3
        grade = "C"
        slot = 1
        info = "A very dirty shirt"
        mkt_value = 3

    class HarrowStrawHat(BasicAccessory):
        name = "harrow straw hat"
        defence = 10
        grade = "A"
        slot = 0
        info = "Teacher will give you a sanction if you don't bring it to school"
        mkt_value = 50

    class PirateStrawHat(BasicAccessory):
        name = "pirate straw hat"
        defence = 20
        grade = "SS"
        slot = 0
        info = "King of pirates!!!"
        mkt_value = 5000

# print(Heals.KFCCrazyFood.heal)
