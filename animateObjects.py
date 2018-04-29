import random
from enum import Enum

class Advantage(Enum):
    disadvantage = -1
    none = 0
    advantage = 1

def xdy(x: int, y: int) -> list:
    return xdyplus(x,y,0)

def xdyplus(x: int, y: int, modifier: int) -> list:
    rolls = list()
    for i in range(1,x)
        rolls.append(random.randint(1,y)+modifier)
    return rolls

def attackRoll(attackBonus: int, advantage: Advantage, critFloor: int) -> tuple:
    rolls = xdy(2,20)
    if( (advantage is Advantage.advantage and rolls[0] < rolls[1]) or (advantage is Advantage.disadvantage and rolls[0] > rolls[1]) ):    
        roll = rolls[1]
    else:
        roll = rolls[0]
    return tuple(roll+attackBonus,withinCritRange(critFloor,roll))

def withinCritRange(critFloor: int, roll: int) -> bool:
    return critFloor <= roll

def tinyAttack(advantage: Advantage) -> tuple:
    return attack(advantage,8,4,4,1)

def smallAttack(advantage: Advantage) -> tuple:
    return attack(advantage,6,2,8,1)

def mediumAttack( advantage: Advantage) -> tuple:
    return attack(advantage,5,1,6,2)

def largeAttack(advantage: Advantage) -> tuple:
    return attack(advantage,6,2,10,2)

def hugeAttack(advantage: Advantage) -> tuple:
    return attack(advantage,8,4,12,2)

def attack(advantage: Advantage, attackModifier: int, damageModifier: int, damageDie: int, damageRolls: int) -> tuple:
    atkRoll = attackRoll(attackModifier,advantage,20)
    damage = xdyplus(damageRolls,damageDie,damageModifier)
    if(atkRoll[1]):
        damage+=xdy(1,damageDie)
    return tuple(atkRoll,damage)