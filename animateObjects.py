import random
from enum import Enum


"""
Python script to ease damage rolls for the animate objects spell. Rolling 10d20 
for hits was slightly annoying...then our paladin knocked the enemy prone and
we had to roll 10d20 with advantage for hits.
"""

class Advantage(Enum):
    disadvantage = -1
    none = 0
    advantage = 1

def xdy(x: int, y: int) -> list:
    return xdyplus(x,y,0)

def xdyplus(x: int, y: int, modifier: int) -> list:
    rolls = list()
    for i in range(0,x):
        rolls.append(random.randint(1,y)+modifier)
    return rolls

def attackRoll(attackBonus: int, advantage: Advantage, critFloor: int) -> tuple:
    rolls = xdy(2,20)
    if( (advantage is Advantage.advantage and rolls[0] < rolls[1]) or (advantage is Advantage.disadvantage and rolls[0] > rolls[1]) ):    
        roll = rolls[1]
    else:
        roll = rolls[0]
    return (roll+attackBonus,withinCritRange(critFloor,roll))

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
    damage = 0
    for dmg in xdyplus(damageRolls,damageDie,damageModifier):
        damage+=dmg
    if(atkRoll[1]):
        damage+=random.randint(1,damageDie)#xdy(1,damageDie)
    return (atkRoll[0],damage)

def getAttacks(objectSize: str) -> set:
    allAttacks = set()
    print("Enter the number of "+objectSize+" attacks or hit enter to skip.\nFormat: disadv,none,adv")
    adv = str(input())
    if(adv == ''):
        return allAttacks
    adv = adv.split(',')
    allAttacks = allAttacks | getAttacksHelper(objectSize,Advantage.disadvantage, int(adv[0]))
    allAttacks = allAttacks | getAttacksHelper(objectSize,Advantage.none, int(adv[1]))
    allAttacks = allAttacks | getAttacksHelper(objectSize,Advantage.advantage, int(adv[2]))
    return allAttacks

def getAttacksHelper(objectSize: str, advantage: Advantage, attacks: int) -> set:
    attackSizes = {"tiny" : tinyAttack, "small" : smallAttack, "medium" : mediumAttack, "large": largeAttack, "huge": hugeAttack}
    allAttacks = set()
    for x in range(0,attacks):
        attack = (objectSize, attackSizes[objectSize](advantage))
        allAttacks.add(attack)
    return allAttacks


def main():
    totalAttacks = set()
    yes = set(["y","yes"])
    print("Are all of the objects tiny?")
    tiny = str(input())
    totalAttacks = totalAttacks | getAttacks("tiny")
    if(tiny.lower() not in yes):
        totalAttacks = totalAttacks | getAttacks("small")
        totalAttacks = totalAttacks | getAttacks("medium")
        totalAttacks = totalAttacks | getAttacks("large")
        totalAttacks = totalAttacks | getAttacks("huge")

    #see how many hit and how much damage was dealt
    print("Enter the target AC to see the number of hits and total damage dealt, or hit enter to see how each object rolled.")
    targetAC = input()
    if(targetAC != ''):
        targetAC = int(targetAC)
        totalHits = 0
        totalDamage = 0
        for x in totalAttacks:
            if(x[1][0] >= targetAC):
                totalHits+=1
                totalDamage+=x[1][1]
        print("Total Hits:\t",totalHits)
        print("Total Damage:\t",totalDamage)

    
    print("Would you like to see how each object rolled?")
    transparency = str(input())
    if(transparency.lower() in yes):
        print("\nFormat:\t(size, (attack roll, damage roll))\n")
        for x in totalAttacks:
            print(x)


if __name__ == "__main__":
    main()