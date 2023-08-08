import sys

import pygame
import random
import json
import os
import math
import pickle
import keyboard
def sqrt(a):
    return a ** .5
# Import images
IMAGES = {}
for i in os.listdir("newImages"):
    if i not in ["font"]:
        IMAGES[f"images/{i}"] = pygame.image.load(f'newImages/{i}')

FONT = {}
for i in os.listdir("newImages/font"):
    FONT[i[-5].lower()] = pygame.image.load(f'newImages/font/{i}')
def getDirection(x, y):
    if abs(x) > abs(y):
        return 'd' if x > 0 else 'a'
    else:
        return 's' if y > 0 else 'w'
# Classes
class InventoryBox:
    def __init__(self, centerx, centery, sprite=IMAGES['images/inventoryBox.png']):
        self.sprite = sprite
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
class helmetSlotMarker:
    def __init__(self):
        self.sprite = IMAGES['images/helmetSlot.png']
        self.place = self.sprite.get_rect()
        self.place.centerx = 1035
        self.place.centery = 695
class armorSlotMarker:
    def __init__(self):
        self.sprite = IMAGES['images/armorSlot.png']
        self.place = self.sprite.get_rect()
        self.place.centerx = 1095
        self.place.centery = 695
class leggingsSlotMarker:
    def __init__(self):
        self.sprite = IMAGES['images/leggingsSlot.png']
        self.place = self.sprite.get_rect()
        self.place.centerx = 1155
        self.place.centery = 695
helmetSlotMarker = helmetSlotMarker()
armorSlotMarker = armorSlotMarker()
leggingsSlotMarker = leggingsSlotMarker()
class plainAnimation:
    def __init__(self, animation, centerx, centery):
        self.animation = animation
        self.sprite = IMAGES[f'{str(animation[0])}']
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.frame = 0
    def showAndUpdate(self):
        p.display.blit(self.sprite, self.place)
        self.frame += 1
        if self.frame == len(self.animation):
            try:
                coordinateToRoom(p.room)[1].plainAnimations.remove(self)
            except ValueError:
                pass
        else:
            self.sprite = IMAGES[f'{str(self.animation[self.frame])}']
def getAngle(x, y):
    try:
        return math.acos(x / sqrt(x ** 2 + y ** 2)) * - sign(y) * 180 / math.pi
    except ZeroDivisionError:
        return random.randint(0, 360)
class Bullet:
    def __init__(self, hr, vr, damage, firer, melee=0, linger=400,
                 sprite=None, piercing=0, centerx=None, centery=None,
                 knockback=(0, 0, 0), delay=0, positionCalculatedOnFire=1,
                 showWhileDelayed=1, elements=(), splash=0, mark=None,  specialEndEffect='',
                 specialEffects=(), specialEffectConditions=(), rotated=1, animation=None):
        self.piercing = piercing
        self.hurtTargets = []
        self.specialEndEffect = specialEndEffect
        self.damage = damage
        self.elements = elements
        self.splash = splash
        self.mark = mark
        if self.mark is not None:
            self.markSprite = self.mark[1]
            self.markEffect = self.mark[0]
            self.markShatterCondition = self.mark[2]
            self.markShatterEffect = self.mark[3]
        self.rotated = rotated
        self.linger = linger
        self.specialEffects = specialEffects
        self.specialEffectConditions = specialEffectConditions
        self.melee = melee
        self.showWhileDelayed = showWhileDelayed
        self.firer = firer
        self.hr = hr
        self.vr = vr
        self.knockback = knockback
        self.delay = delay

        # Set correct sprite based on firer
        if firer == p:
            if p.inventory[p.activeItem].type == "Mandible":
                self.sprite = IMAGES['images/playerMelee.png']
            elif p.inventory[p.activeItem].type == "NanotechRevolver":
                self.sprite = IMAGES['images/playerProjectile.png']
            elif p.inventory[p.activeItem].type == "FerroSandShotgun":
                self.sprite = IMAGES['images/playerProjectile.png']
        else:
            if self.firer.type == "ironAngel" or self.firer.type == "wobbegong":
                self.sprite = IMAGES['images/ironAngelProjectile.png']
            elif self.firer.type == "antlion":
                if self.melee == 1:
                    self.sprite = IMAGES['images/lionMelee.png']
                else:
                    self.sprite = IMAGES['images/playerMelee.png']
            elif self.firer == p and p.inventory[p.activeItem].type == "Mandible":
                self.sprite = IMAGES['images/playerMelee.png']

        if not sprite == None:
            self.sprite = sprite
            self.animation = [self.sprite]
        self.frame = 0
        # Gets the coordinates for usage later
        self.place = self.sprite.get_rect()
        self.place.centerx = self.firer.place.centerx
        self.place.centery = self.firer.place.centery
        self.positionCalculatedOnFire = positionCalculatedOnFire

        # If firer is the player, add some offset to the bullet.
        if self.firer == p and self.melee == 1:
            a = self.place.height / 2 + 40
            b = self.place.width / 2 + 15
            disy = pygame.mouse.get_pos()[1] - p.place.centery
            disx = pygame.mouse.get_pos()[0] - p.place.centerx

            try:
                disyoverdisx = disy / disx
                self.shiftx = a * b * sign(disx) / sqrt(a ** 2 + disyoverdisx ** 2 * b ** 2)
            except ZeroDivisionError:
                self.shiftx = 0

            try:
                disxoverdisy = disx / disy
                self.shifty = a * b * sign(disy) / sqrt(b ** 2 + disxoverdisy ** 2 * a ** 2)
            except ZeroDivisionError:
                self.shifty = 0

            self.place.centerx = p.place.centerx + self.shiftx
            self.place.centery = p.place.centery + self.shifty
        if centerx != None:
            self.place.centerx = centerx
        if centery != None:
            self.place.centery = centery
        if animation is not None:
            self.animation = animation
            self.sprite = self.animation[0]
        else:
            self.animation = [self.sprite] * 2
        self.center = [self.place.centerx, self.place.centery]
    def move(self):
        spearExplosion = []
        for i in range(1, 8):
            for j in range(2):
                spearExplosion.append(IMAGES[f'images/spearExplosion{i}.png'])
        if self.delay < 1:
            if self.melee:
                self.linger -= self.firer.totalSpeed
            else:
                self.linger -= 1
            if self.linger <= 0:
                try:
                    self.firer.bullets.remove(self)
                    if type(self.firer) == Foe:
                        coordinateToRoom(p.room)[1].enemyBullets.remove(self)
                except ValueError:
                    pass
                exec(self.specialEndEffect)
            else:
                self.center[0] += self.hr
                self.center[1] += self.vr
            self.sprite = self.animation[self.frame]
            if self.frame > 0:
                self.center[0] -= (self.sprite.get_rect().width - self.animation[self.frame - 1].get_rect().width) / 2
                self.center[1] -= (self.sprite.get_rect().height - self.animation[self.frame - 1].get_rect().height) / 2
            self.frame += 1
            if self.rotated:
                self.sprite = pygame.transform.rotate(self.sprite, getAngle(self.hr, self.vr))
            if self.frame == len(self.animation):
                self.frame = 0
            if self.melee:
                if self.firer.place.top <= 0 and self.firer.vr < 0:
                    pass
                elif self.firer.place.bottom >= 900 and self.firer.vr > 0:
                    pass
                else:
                    self.center[1] += self.firer.vr * self.firer.speed

                if self.firer.place.left <= 0 and self.firer.hr < 0:
                    pass
                elif self.firer.place.right >= 1600 and self.firer.hr > 0:
                    pass
                else:
                    self.center[0] += self.firer.hr * self.firer.speed

            self.place.centerx = self.center[0]
            self.place.centery = self.center[1]
            for condition in self.specialEffectConditions:
                if eval(condition):
                    exec(self.specialEffects[self.specialEffectConditions.index(condition)])
            p.display.blit(self.sprite, self.place)

        else:
            self.delay -= 1
            if self.positionCalculatedOnFire:
                self.center[0] += self.firer.hr * self.firer.speed
                self.center[1] += self.firer.vr * self.firer.speed
            if self.showWhileDelayed:
                p.display.blit(self.sprite, self.place)
class Item:
    def __init__(self, dropChance, type, qty=1, maxStackSize=1, dr=0, altAttackCharge=0, armorSlot=None):
        self.dropChance = dropChance
        self.type = type
        self.dragged = 0
        self.qty = qty
        self.armorSlot = armorSlot
        self.stackSize = maxStackSize
        self.dr = dr
        self.altAttackCharge = altAttackCharge
        self.chargeProgress = 0
        self.description = ''
        try:
            self.sprite = spritesForInventoryItems[self.type]
        except KeyError:
            self.sprite = IMAGES['images/playerProjectile.png']
        self.place = self.sprite.get_rect()
        if self.type == 'NanotechRevolver':
            self.description = 'the nanotech revolver shoots metal bullets that mark enemies, making them take extra damage. hitting the marked enemy with fire damage will shatter the mark, inflicting damage.'
        elif self.type == 'FerroSandShotgun':
            self.description = 'left click to fire a spread of sand pellets that inflict area damage. right click to fire a piercing spear that explodes upon taking metal damage.'
        else:
            self.description == f'{self.type} is a material.'
class DroppedItem:
    def __init__(self, item, centerx, centery, maxStackSize=1, dr=0, altAttackCharge=0, armorSlot=None):
        self.item = item
        self.stackSize = maxStackSize
        self.dr = dr
        self.altAttackCharge = altAttackCharge
        self.armorSlot = armorSlot
        try:
            self.sprite = spritesForInventoryItems[self.item]
        except KeyError:
            self.sprite = IMAGES['images/playerProjectile.png']
        self.place = self.sprite.get_rect()

        self.place.centerx = centerx
        self.place.centery = centery
class Word:
        def __init__(self, word, left, top, essentiallyJustP):
            self.word = word
            self.totalWidth = 0
            self.place = pygame.Rect(left, top, self.totalWidth, 14)
            self.recipient = essentiallyJustP
            self.centerx = left + self.totalWidth / 2
            self.centery = top + 7

            for letter in word:
                self.totalWidth += FONT[letter].get_rect().width + 3

        def write(self):
            left = self.place.left
            for i in range(len(self.word)):
                if self.word[i] == '.' or self.word == ',':
                    self.recipient.display.blit(FONT[self.word[i]], pygame.Rect(left + i * 3, self.place.top + 10,
                                                                 FONT[self.word[i]].get_rect().width,
                                                                 FONT[self.word[i]].get_rect().height))
                else:
                    self.recipient.display.blit(FONT[self.word[i]], pygame.Rect(left + i * 3, self.place.top,
                                                                 FONT[self.word[i]].get_rect().width,
                                                                 FONT[self.word[i]].get_rect().height))
                left += FONT[self.word[i]].get_rect().width

        def checkMouseCollision(self):
            if abs(self.centerx - pygame.mouse.get_pos()[0]) < self.totalWidth / 2 and abs(self.centery - pygame.mouse.get_pos()[1]) < 7:
                return 1
            else:
                return 0
class textBox:
    def __init__(self, text, width, top, left, willBeP):
        self.width = width
        self.text = text.lower()
        self.wordListRev = self.text.split()
        self.wordList = []
        for i in range(len(self.wordListRev)):
            self.wordList.append(self.wordListRev[-1])
            self.wordListRev.pop(-1)
        self.left = left
        self.top = top
        self.willBeP = willBeP
        row = 1
        self.trueWords = []
        wordsLeft = self.wordList.copy()
        while len(wordsLeft) > 0:
            rowWidth = 0
            try:
                while rowWidth + 18 * (len(wordsLeft[-1]) + 2) <= self.width:
                    self.trueWords.append(Word(wordsLeft[-1], rowWidth + 18 + self.left, row * 25 + 10 + self.top, self.willBeP))
                    rowWidth += self.trueWords[-1].totalWidth + 10
                    wordsLeft.pop(-1)
            except IndexError:
                pass
            row += 1
        self.height = row * 25 + 20
    def show(self):
        self.willBeP.display.fill((150, 150, 150), pygame.Rect(self.left, self.top, self.width, self.height))
        for word in self.trueWords:
            word.write()
        self.willBeP.display.blit(pygame.transform.scale(IMAGES['images/textBox.png'], (self.width, self.height)), pygame.Rect(self.left, self.top, self.width, self.height))
class teleporter:
    def __init__(self, coordinate, centerx, centery, destinationCoordinate, destinationCenterx, destinationCentery, sprite):
        self.coordinate = coordinate
        self.sprite = IMAGES[sprite]
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.destinationCoordinate = destinationCoordinate
        self.destinationCenterx = destinationCenterx
        self.destinationCentery = destinationCentery
        self.initialDestinationCenterx = self.destinationCenterx
        self.initialDestinationCentery = self.destinationCentery
        self.initialDestinationCoordinate = self.destinationCoordinate
        self.saveCode = f'room.teleporters.append(teleporter({self.coordinate}, {self.place.centerx}, {self.place.centery}, {self.destinationCoordinate}, {self.destinationCenterx}, {self.destinationCentery}, "{sprite}"))'
class CraftingBox:
    def __init__(self):
        self.sprite = IMAGES['images/craftingBox.png']
        self.place = self.sprite.get_rect()
        self.place.centerx = 1390
        self.place.centery = 450
class Player:
    def __init__(self):

        self.sprite = IMAGES['images/walkingAnimation_s1.png']
        self.place = self.sprite.get_rect()
        self.knockbackAfflictions = []
        self.dr = 0
        self.mapShown = 0
        self.time = 12
        self.place.bottom = 450
        self.place.left   = 805
        self.activeItem          = 0
        self.animationFrame      = 0
        self.dashFramesRemaining = 0
        self.fireCooldown        = 0
        self.firing              = 0
        self.healingByKill       = 65
        self.song = None
        self.hp                  = 130
        self.hr                  = 0
        self.hrWhileDashing      = 0
        self.heat = 0
        self.heatHarm = 0
        self.invincibility       = 0
        self.inventoryShown      = 0
        self.maxHP               = 130
        file = 0
        self.pause               = 0
        self.stamina             = 0
        self.staminaRegenRate    = 1.5
        self.slideFramesRemaning = 0
        self.speed               = 1
        self.vr                  = 0
        self.vrWhileDashing      = 0
        self.direction           = 's'
        self.bullets             = []
        self.center              = [self.place.centerx, self.place.centery]
        self.emptySlots          = []
        self.room                = [0, 0, 0]
        self.hotbar              = {}
        self.menuScreen = 'titleScreen'
        self.startGame = 0
        self.recipes = {
            ('sandstone',): (Item(0, 'bagOfSand'),),
            tuple(['desertWood'] * 10): (Item(0, 'desertWoodHelmet', dr=5, armorSlot='helmet'),),
            tuple(['desertWood'] * 20): (Item(0, 'desertWoodChestplate', dr=15, armorSlot='chestplate'),),
            tuple(['desertWood'] * 15): (Item(0, 'desertWoodLeggings', dr=10, armorSlot='leggings'),),
        }
        self.walkingAnimation    = {'w': [], 'a': [], 's': [], 'd': []}
        self.craftButton         = Word('craft', 1355, 650, self)
        self.display             = pygame.display.set_mode((1600, 900))

        self.idleAnimation = {
            'd': [IMAGES['images/newWalkingAnimation_d1.png']],
            'w': [IMAGES['images/newWalkingAnimation_w1.png']],
            'a': [IMAGES['images/newWalkingAnimation_a1.png']],
            's': [IMAGES['images/newWalkingAnimation_s1.png']]
        }
        self.inventory = []
        self.saveCode = []
        for number in range(100):
            self.inventory.append(Item(1, "empty"))
            self.emptySlots.append(Item(1, "empty"))
        # Load walking animation sprites
        for i in range(1, 5):
            for o in range(20):
                self.walkingAnimation['w'].append(pygame.image.load(f'images/newWalkingAnimation_w{i}.png'))
                self.walkingAnimation['a'].append(pygame.image.load(f'images/newWalkingAnimation_a{i}.png'))
                self.walkingAnimation['s'].append(pygame.image.load(f'images/newWalkingAnimation_s{i}.png'))
                self.walkingAnimation['d'].append(pygame.image.load(f'images/newWalkingAnimation_d{i}.png'))
        try:
            self.load(file)
        except IndexError:
            self.inventory = []
            self.saveCode = []
            for number in range(100):
                self.inventory.append(Item(1, "empty"))
                self.emptySlots.append(Item(1, "empty"))
            try:
                with open(f'roomInfo{file}.json', 'w') as roomInfo:
                    json.dump({}, roomInfo)
                with open(f'biomes{file}.json', 'w') as roomInfo:
                    json.dump({}, roomInfo)
            except FileNotFoundError:
                pass
            rooms.rooms = [Room([0, 0], 'desert', 1)]
            rooms.roomCoordinates = [[0, 0]]
            rooms.makeRooms(16, 'desert')
        self.saveStatTypes = [key for key in vars(self).keys()]
        for stat in self.saveStatTypes:
            try:
                test = open('filler.json', 'x')
            except FileExistsError:
                test = open('filler.json', 'w')
            try:
                json.dump(vars(self)[stat], test)
            except TypeError:
                self.saveStatTypes.remove(stat)
            test.close()
        self.animation = self.idleAnimation[self.direction]
        self.undirectedAnimation = self.idleAnimation
        print(self.saveStatTypes)
        self.save()
        self.updateStats()
    def dropItem(self, item):
        for i in range(item.qty):
            coordinateToRoom(self.room)[1].droppedItems.append(DroppedItem(item.type, self.place.centerx, self.place.centery, maxStackSize=item.stackSize, dr=item.dr, altAttackCharge=item.altAttackCharge, armorSlot=item.armorSlot))
    def getQtyOfFoeTypeInRoom(self, type):
        qty = 0
        for foe in coordinateToRoom(self.room)[1].foes:
            if foe.type == type:
                qty += 1
        return qty
    def prepareToSave(self):
        for stat in self.saveStatTypes:
            try:
                test = open('filler.json', 'x')
            except FileExistsError:
                test = open('filler.json', 'w')
            try:
                json.dump(vars(self)[stat], test)
            except TypeError:
                self.saveStatTypes.remove(stat)
            test.close()
        self.saveCode = []
        try:
            self.saveStatTypes.remove('display')
        except ValueError:
            pass
        while 'file' in self.saveStatTypes:
            self.saveStatTypes.remove('file')
        for stat in self.saveStatTypes:
            if type(vars(self)[stat]) == str:
                self.saveCode.append(f'self.{stat} = "{eval(f"self.{stat}")}"')
            else:
                self.saveCode.append(f'self.{stat} = {eval(f"self.{stat}")}')
        self.saveCode = tuple(self.saveCode)
    def craft(self):
        ingredients = []

        for item in self.inventory:
            if checkNotDamageCollision(item, theCraftingBox) and item.type != 'empty':
                for i in range(item.qty):
                    ingredients.append(item.type)

        ingredients = tuple(sorted(ingredients))

        try:
            for item in self.recipes[ingredients]:
                self.updateStats()
                self.addItemToInventory(item, self.place.centerx, self.place.centery)
        except KeyError:
            pass
            for item in self.inventory[40: 100]:
                if item.type != 'empty':
                    try:
                        self.inventory[self.inventory.index(self.emptySlots[0])] = item
                    except IndexError:
                        self.dropItem(item)
        for item in self.inventory[40: 100]:
            item.qty = 0

            if item.type != 'empty':
                try:
                    self.inventory[self.inventory.index(self.emptySlots[0])] = item
                except IndexError or ValueError:
                    self.dropItem(item)
            self.updateStats()

    def save(self):
        try:
            inventory = open(f'inventory{file}.json', "x")
        except FileExistsError:
            inventory = open(f'inventory{file}.json', "w")
        items = []
        for item in self.inventory:
            items.append([item.type, item.qty, item.stackSize, item.dr, item.altAttackCharge, item.armorSlot])

        json.dump(items, inventory)
        inventory.close()
        roomCoordsInfo = {}
        for room in rooms.rooms:
            room.prepareToSave()
            self.prepareToSave()
            roomCoordsInfo[f'[{room.coordinate[0]}, {room.coordinate[1]}, {room.coordinate[2]}]'] = tuple(tuple(room.saveCode))
        try:
            roomCoords = open(f'roomCoords{file}.json', 'x')
        except FileExistsError:
            roomCoords = open(f'roomCoords{file}.json', 'w')
        json.dump(roomCoordsInfo, roomCoords)
        roomCoords.close()
        try:
            playerInfo = open(f'playerInfo{file}.json', 'x')
        except FileExistsError:
            playerInfo = open(f'playerInfo{file}.json', 'w')
        json.dump(self.saveCode, playerInfo)
        playerInfo.close()
        roomBiomes = {}
        for room in rooms.rooms:
            roomBiomes[f'[{room.coordinate[0]}, {room.coordinate[1]}, {room.coordinate[2]}]'] = room.biome
        try:
            biomes = open(f'biomes{file}.json', 'x')
        except FileExistsError:
            biomes = open(f'biomes{file}.json', 'w')
        json.dump(roomBiomes, biomes)
    def load(self, file):
        with open(f'inventory{file}.json', "r") as inventory:
            storage = json.load(inventory)
            self.inventory = [Item(100, i[0], qty=i[1], maxStackSize=i[2], dr=i[3], altAttackCharge=i[4], armorSlot=i[5]) for i in storage]
        num = 1
        self.song = None
        self.rooms = [Room([0, 0], "desert", 1)]
        self.roomCoordinates = [[0, 0, 0]]
        with open(f'biomes{file}.json', 'r') as roomBiomes:
            biomes = json.load(roomBiomes)
            for coord in [key for key in biomes.keys()]:
                rooms.rooms.append(Room(eval(coord)[0: 2], biomes[coord], num, depth=eval(coord)[2]))
                rooms.rooms[-1].foes = []
                rooms.rooms[-1].destructibleMaterialSources = []
                rooms.rooms[-1].traps = []
                rooms.rooms[-1].teleporters = []
        with open(f'roomCoords{file}.json', 'r') as roomInfoCoords:
            roomInfo = json.load(roomInfoCoords)
            for coord in [key for key in roomInfo.keys()]:
                for room in rooms.rooms:
                    if room.coordinate == eval(coord):
                        for effect in roomInfo[coord]:
                            print(effect)
                            exec(effect)

        with open(f'playerInfo{file}.json', 'r') as playerStats:
            playerSaveInfo = json.load(playerStats)
            for line in playerSaveInfo:
                exec(line)
        self.menuScreen = None

        self.hr = (keyboard.is_pressed('d') - keyboard.is_pressed('a')) * 10
        self.vr = (keyboard.is_pressed('s') - keyboard.is_pressed('w')) * 10
    def healByKill(self):
        self.hp += self.healingByKill
        if self.hp > self.maxHP:
            self.hp = self.maxHP

    def addItemToInventory(self, item, centerx, centery):
        for obj in self.inventory:
            if obj.type == item.type:
                for number in range(getLesser(item.stackSize - obj.qty, item.qty)):
                    if obj.qty < obj.stackSize and item.qty > 0:
                        obj.qty += 1
                        item.qty -= 1
                    else:
                        break

        while item.qty > 0:
            if len(self.standardInventory) - len(self.emptySlots) < 30:
                self.updateStats()
                self.inventory[self.inventory.index(self.emptySlots[0])] = Item(item.dropChance, item.type, qty=item.qty, maxStackSize=item.stackSize, dr=item.dr, altAttackCharge=item.altAttackCharge)
                item.qty = 0
                self.emptySlots.pop(0)
            else:
                self.updateStats()
                coordinateToRoom(self.room)[1].droppedItems.append(DroppedItem(item.type, centerx, centery, maxStackSize=item.stackSize, dr=item.dr, altAttackCharge=item.altAttackCharge))
                item.qty -= 1

        self.updateStats()

    def loot(self, items, centerx, centery):
        for item in items:
            if not type(item) == None:
                if random.randint(1, 100) <= item.dropChance:
                    self.addItemToInventory(item, centerx, centery)
                    self.updateStats()
                    self.save()

    def animationSwap(self, animation, direction):
        self.animation = animation[direction]
        self.undirectedAnimation = animation
        self.animationFrame = 0

    def turn(self, direction):
        self.animation = self.undirectedAnimation[direction]

    def checkDroppedItemCollision(self):
        for item in coordinateToRoom(self.room)[1].droppedItems:
            if checkNotDamageCollision(self, item):
                self.addItemToInventory(Item(0, item.item, maxStackSize=item.stackSize, dr=item.dr, altAttackCharge=item.altAttackCharge, armorSlot=item.armorSlot), item.place.centerx, item.place.centery)
                self.save()
                try:
                    coordinateToRoom(self.room)[1].droppedItems.remove(item)
                except ValueError:
                    pass

    def updateStats(self):
        self.time += 0.1
        if self.time >= 360:
            self.time = 0
        print(self.inventory[self.activeItem].altAttackCharge, self.inventory[self.activeItem].chargeProgress)
        try:
            try:
                exec(coordinateToRoom(self.room)[1].defaultHeatEffect)
            except NameError:
                pass
        except TypeError:
            pass
        if self.heat > 75:
            self.hp = 0
        if self.time >= 225 or self.time < 45:
            self.heat = 0
        self.speed               = 0.46
        self.dashFramesRemaining -= 1
        self.dr = 0
        self.staminaRegenRate    = 1.5
        if pygame.mouse.get_pressed()[2] and self.inventory[self.activeItem].chargeProgress < self.inventory[
            self.activeItem].altAttackCharge and self.inventory[self.activeItem].altAttackCharge > 0:
            self.inventory[self.activeItem].chargeProgress += 1
        if 15 < abs(self.heat):
            self.dr -= 25
        if 30 < abs(self.heat):
            self.hp -= 0.01
        if 50 < abs(self.heat):
            self.hp -= 0.03
        for item in self.inventory:
            if item.qty<= 0:
                self.inventory[self.inventory.index(item)] = Item(0, 'empty')
        self.accessories         = self.inventory[30:37]
        self.standardInventory  = self.inventory[0:30]
        try:
            self.sprite              = self.animation[self.animationFrame]
        except IndexError:
            self.sprite = self.animation[0]
        self.recipes = {
            ('sandstone',): (Item(0, 'bagOfSand'),),
            tuple(['desertWood'] * 10): (Item(0, 'desertWoodHelmet', dr=5),),
            tuple(['desertWood'] * 20): (Item(0, 'desertWoodChestplate', dr=15),),
            tuple(['desertWood'] * 15): (Item(0, 'desertWoodLeggings', dr=10),),
        }

        if self.checkForAccessory('wobbegongCloak'):
            self.staminaRegenRate += 0.35
        self.stamina -= self.staminaRegenRate
        if self.stamina < 0:
            self.stamina = 0

        if self.slideFramesRemaning > 0:
            self.speed *= 4
        self.slideFramesRemaning -= 1

        if self.firing:
            self.direction = getDirection(pygame.mouse.get_pos()[0] - self.place.centerx, pygame.mouse.get_pos()[1] - self.place.centery)

        elif self.hr != 0 or self.vr != 0:
            self.direction = getDirection(self.hr, self.vr)

        if self.hr == 0 and self.vr == 0 and self.undirectedAnimation == self.walkingAnimation:
            self.animation = self.idleAnimation[self.direction]
            self.undirectedAnimation = self.idleAnimation

        self.turn(self.direction)
        if self.animationFrame >= len(self.animation):
            self.animationFrame = 0

            if not self.hr and not self.vr:
                self.animation = self.idleAnimation[self.direction]
                self.undirectedAnimation = self.idleAnimation
            else:
                self.animation = self.walkingAnimation[getDirection(self.hr, self.vr)]
                self.undirectedAnimation = self.walkingAnimation

        for i in range(10):
            self.hotbar[i] = self.inventory[i].type

        self.emptySlots = [item for item in self.standardInventory if item.type == 'empty']

        if len(self.emptySlots) == 30:
            self.inventory[0] = Item(0, 'NanotechRevolver')
            self.standardInventory[0] = self.inventory[0]
            self.emptySlots.pop(0)
        for item in self.inventory[40: 100]:
            if not checkNotDamageCollision(item, theCraftingBox):
                self.inventory[self.inventory.index(item)] = Item(0, 'empty')
                if item.type != 'empty':
                    try:
                        self.inventory[self.inventory.index(self.emptySlots[0])] = item
                    except IndexError:
                        self.dropItem(item)

            self.standardInventory = self.inventory[0: 30]
            self.emptySlots = [item for item in self.standardInventory if item.type == 'empty']
        self.emptyExtraSlots = [i for i in self.inventory[40: 100] if i.type == 'empty']
        self.allEmptySlots = [item for item in self.inventory if item.type == 'empty']
        if self.inventory[37].armorSlot == 'helmet':
            self.dr += self.inventory[37].dr
        if self.inventory[38].armorSlot == 'chestplate':
            self.dr += self.inventory[38].dr
        if self.inventory[39].armorSlot == 'leggings':
            self.dr += self.inventory[39].dr
        self.center[0] -= (self.sprite.get_rect().width - self.animation[self.animationFrame - 1].get_rect().width) / 2
        self.center[1] -= (self.sprite.get_rect().height - self.animation[self.animationFrame - 1].get_rect().height) / 2
    def detectInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS and self.inventoryShown:
                    for item in self.inventory:
                        if item.dragged and not item.type == 'empty':
                            for number in range(item.qty):
                                coordinateToRoom(p.room)[1].droppedItems.append(DroppedItem(item.type, 800, 450, maxStackSize=item.stackSize, dr=item.dr, altAttackCharge=item.altAttackCharge, armorSlot=item.armorSlot))
                            self.inventory[self.inventory.index(item)] = Item(0, 'empty')
                            self.updateStats()

                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                if event.key == pygame.K_p:
                    exec(input(':'))
                if event.key == pygame.K_w:
                    self.vr -= 10
                if event.key == pygame.K_a:
                    self.hr -= 10
                if event.key == pygame.K_s:
                    self.vr += 10
                if event.key == pygame.K_d:
                    self.hr += 10
                if event.key == pygame.K_m:
                    if self.mapShown:
                        self.mapShown = 0
                    else:
                        self.mapShown = 1

                if event.key == pygame.K_l:
                    self.inventoryShown = not self.inventoryShown

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.dash()

                if event.key == pygame.K_TAB or pygame.key.get_mods() & pygame.KMOD_CTRL or pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.slide()
                for i in range(10):
                    swap = 0
                    exec(f"if event.key == pygame.K_{i}: self.activeItem = {i}")
                    exec(f"if event.key == pygame.K_{i}: swap = 1")
                    if swap:
                        for item in self.inventory:
                            item.chargeProgress = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.vr += 10
                if event.key == pygame.K_a:
                    self.hr += 10
                if event.key == pygame.K_s:
                    self.vr -= 10
                if event.key == pygame.K_d:
                    self.hr -= 10

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inventoryShown:
                    if pygame.mouse.get_pressed()[0]:
                        if self.craftButton.checkMouseCollision():
                            self.craft()

                        dragging = False

                        for item in self.inventory:
                            if item.dragged == 1:
                                dragging = True
                                draggedItem = item
                                shallDrop = 1
                                break

                        if dragging:
                            if checkNotDamageCollision(draggedItem, theCraftingBox):
                                for item in self.inventory[40: 100]:
                                    if item.type == 'empty':
                                        draggedItem.dragged = 0
                                        item1 = self.inventory.index(draggedItem)
                                        item2 = self.inventory.index(item)
                                        self.inventory[item1] = item
                                        self.inventory[item2] = draggedItem
                                        shallDrop = 0
                                        break

                            for item in self.inventory:
                                if detectMouseCollision(item) == 1 and not item == draggedItem:
                                    self.updateStats()
                                    if item.type == draggedItem.type:
                                        qtyShift = getLesser(item.stackSize - item.qty, draggedItem.qty)
                                        item.qty += qtyShift
                                        draggedItem.qty -= qtyShift
                                    else:
                                        item1 = self.inventory.index(item)
                                        item2 = self.inventory.index(draggedItem)
                                        self.inventory[item1] = draggedItem
                                        self.inventory[item2] = item
                                        item.dragged = 1
                                        draggedItem.dragged = 0
                                    self.updateStats()
                                    shallDrop = 0
                            if shallDrop:
                                self.updateStats()
                                for item in self.inventory[0: 40]:
                                    item.dragged = 0
                        else:
                            for item in self.inventory[0: 40]:
                                if detectMouseCollision(item) == 1:
                                    item.dragged = 1
                    elif pygame.mouse.get_pressed()[2]:

                        dragging = 0
                        for i in self.inventory:
                            if i.dragged and i.type != 'empty':
                                dragging = 1
                                draggedItem = i
                                break
                        for i in self.inventory:
                            if detectMouseCollision(i) and i.type != 'empty':
                                self.updateStats()
                                if dragging:
                                    if draggedItem.type == i.type and draggedItem.qty < draggedItem.stackSize:
                                        draggedItem.qty += 1
                                        i.qty -= 1

                                        if i.qty < 1:
                                            indexI = self.inventory.index(i)
                                            self.inventory[indexI] = Item(0, draggedItem.type, qty=draggedItem.qty, maxStackSize=draggedItem.stackSize)
                                            self.inventory[self.inventory.index(draggedItem)] = Item(0, 'empty')
                                            self.inventory[indexI].dragged = 1
                                        self.updateStats()

                                else:
                                    IndexI = self.inventory.index(i)
                                    self.inventory[IndexI] = Item(0, i.type, qty=i.qty - 1, maxStackSize=i.stackSize)
                                    if i.qty > 1:
                                        self.inventory[self.inventory.index(self.allEmptySlots[0])] = i
                                    else:
                                        self.inventory[IndexI].qty += 1
                                        self.inventory[IndexI].dragged = 1
                                    i.qty = 1
                                    i.dragged = 1
                        self.updateStats()
                else:
                    if pygame.mouse.get_pressed()[0]:
                        self.firing = 1
            if event.type == pygame.MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[0]:
                    self.firing = 0
                if self.inventory[self.activeItem].altAttackCharge > 0 and not pygame.mouse.get_pressed()[2]:
                    if self.inventory[self.activeItem].chargeProgress == self.inventory[self.activeItem].altAttackCharge:
                        exec(f'self.useAlt{self.inventory[self.activeItem].type}()')
                    self.inventory[self.activeItem].chargeProgress = 0
    def switchSong(self):
        if coordinateToRoom(self.room)[1].biome == "desert" and self.room[2] == 0:
            if len(coordinateToRoom(self.room)[1].foes) > 0:
                play('music/desertFight.mp3')
            else:
                play('music/desertCalm.mp3')
        elif self.room[2] == 1:
            play('music/shelter.mp3')
    def checkForAccessory(self, item_type):
        return item_type in [i.type for i in self.accessories]
    def useTheSpark(self):
        self.bullets.append(Bullet(pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0] * 10,
                                   pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1] * 10,
                                   2, self, sprite=IMAGES['images/ferroSandShotgunShot.png'],
                                   elements=["heat"], mark=('for effect in ["self.hp -= .2", "self.totalSpeed *= 1.4"]: exec(effect)', IMAGES['images/fireMarkSprite.png'], '1 == 2', ''),
                                   ))
        self.fireCooldown = 30

    def showInventory(self):
        self.display.blit(theCraftingBox.sprite, theCraftingBox.place)
        self.craftButton.write()

        for i in range(30):
            self.inventory[i].place.left = i * 60 - 600 * floorIfPositive(i / 10) + 590
            self.inventory[i].place.top  = 280 + 130 * floorIfPositive(i / 10)
            self.display.blit(
                InventoryBox(
                    i * 60 - 600 * floorIfPositive(i / 10) + 610,
                    305 + 130 * floorIfPositive(i / 10)
                ).sprite,
                InventoryBox(
                    i * 60 - 600 * floorIfPositive(i / 10) + 610,
                    305 + 130 * floorIfPositive(i / 10)
                ).place
            )

            if self.inventory[i].dragged:
                self.inventory[i].place.centerx = pygame.mouse.get_pos()[0]
                self.inventory[i].place.centery = pygame.mouse.get_pos()[1]

        for i in range(7):
            self.inventory[i + 30].place.left = i * 60 + 590
            self.inventory[i + 30].place.top = 670
            self.display.blit(
                InventoryBox(i * 60 + 610, 695, sprite=IMAGES['images/accessoryBox.png']).sprite,
                InventoryBox(i * 60 + 610, 695).place
            )

            if self.inventory[i + 30].dragged == 1:
                self.inventory[i + 30].place.centerx = pygame.mouse.get_pos()[0]
                self.inventory[i + 30].place.centery = pygame.mouse.get_pos()[1]
        for i in range(3):
            self.inventory[i + 37].place.left = i * 60 + 1010
            self.inventory[i + 37].place.top = 670
            self.display.blit(
                InventoryBox(i * 60 + 1035, 695, sprite=IMAGES['images/accessoryBox.png']).sprite,
                InventoryBox(i * 60 + 1035, 695).place
            )
            if self.inventory[i + 37].dragged:
                self.inventory[i + 37].place.centerx = pygame.mouse.get_pos()[0]
                self.inventory[i + 37].place.centery = pygame.mouse.get_pos()[1]
        if self.inventory[38].type == 'empty' or self.inventory[38].dragged:
            self.display.blit(armorSlotMarker.sprite, armorSlotMarker.place)
        if self.inventory[37].type == 'empty' or self.inventory[37].dragged:
            self.display.blit(helmetSlotMarker.sprite, helmetSlotMarker.place)
        if self.inventory[39].type == 'empty' or self.inventory[39].dragged:
            self.display.blit(leggingsSlotMarker.sprite, leggingsSlotMarker.place)
        for item in self.inventory:
            if item.type != 'empty':
                self.display.blit(item.sprite, item.place)
                if item.qty > 1:
                    word = Word(str(item.qty), item.place.centerx, item.place.centery, self)
                    word.write()
        for item in self.inventory:
            if item.type != 'empty':
                if detectMouseCollision(item):
                    mouseMarker.sprite = IMAGES['images/mouseMarkerArrow2.png']
                    showBox = 1
                    for thing in self.inventory:
                        if thing.dragged:
                            showBox = 0
                            break
                    if showBox:
                        box = textBox(item.description, 300, item.place.centery, item.place.centerx, self)
                        box.show()

    def showHealthAndStaminaAndHeatAndCharge(self):
        # Display bar
        hpBarSprite = IMAGES['images/healthBar.png'].get_rect()
        hpBarSprite.x += 10
        self.display.blit(
            IMAGES['images/healthBar.png'],
            hpBarSprite
        )
        self.display.blit(IMAGES['images/heatMeter.png'], pygame.Rect(10, 200, 40, 100))
        # HP
        self.display.fill("#cd300e", pygame.Rect(41, 30, self.hp * 130 / self.maxHP, 18))
        self.display.fill('#ff7c2c', pygame.Rect(16, 281 - self.heat, 26, returnUnlessNegative(self.heat)))
        # Stamina
        self.display.fill("#351c75", pygame.Rect(41, 89, 96 - 96 * returnUnlessNegative(self.stamina) / 315, 14))
        if self.inventory[self.activeItem].altAttackCharge > 0:
            self.display.blit(IMAGES['images/chargeBar.png'], pygame.Rect(1580, 300, 12, 25))
            self.display.fill((63, 127, 63),
                pygame.Rect(1583, 322 - 19 * self.inventory[self.activeItem].chargeProgress / self.inventory[self.activeItem].altAttackCharge, 6,
                19 * self.inventory[self.activeItem].chargeProgress / self.inventory[self.activeItem].altAttackCharge))
    def move(self):
        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]

        self.detectInput()
        self.updateStats()


        if self.dashFramesRemaining < 1:
            self.center[1] += self.vr * self.speed
            self.center[0] += self.hr * self.speed
        else:
            self.center[1] += self.vrWhileDashing
            self.center[0] += self.hrWhileDashing

        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]

        for material in coordinateToRoom(self.room)[1].destructibleMaterialSources:
            while checkNotDamageCollision(self, material):
                if self.place.top < material.place.bottom and self.place.bottom > material.place.top:
                    self.center[0] += sign(self.center[0] - material.place.centerx)
                    if self.center[0] == material.place.centerx:
                        self.center[0] += negativeOrPositive()
                    self.place.centerx = self.center[0]
                if self.place.left < material.place.right and self.place.right > material.place.left:
                    self.center[1] += sign(self.center[1] - material.place.centery)
                    if self.center[1] == material.place.centery:
                        self.center[1] += negativeOrPositive()
                    self.place.centery = self.center[1]

        for projectile in self.bullets:
            if projectile.melee == 1:
                projectile.place.x += self.hr * self.speed
                projectile.place.y += self.vr * self.speed

        if self.center[1] + self.place.height / 2 > 900:
            if [self.room[0], self.room[1] - 1, self.room[2]] in rooms.roomCoordinates and coordinateToRoom(self.room)[1].foes == [] and 750 < self.center[0] < 850:
                coordinateToRoom(self.room)[1].enemyBullets = []
                self.room[1] -= 1
                self.bullets = []
                self.center[1] = self.place.height / 2 + 50
                self.center[0] = 800
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
                print('v')
                for material in coordinateToRoom(self.room)[1].destructibleMaterialSources:
                    if checkNotDamageCollision(self, material):
                        material.hp = 0
                for room in rooms.rooms:
                    if room.coordinate[2] == self.room[2] and ((room.coordinate[1] == self.room[1] and abs(room.coordinate[0] - self.room[0]) < 2) or (room.coordinate[0] == self.room[0] and abs(room.coordinate[1] - self.room[1]) < 2)):
                        room.found = 1
                self.save()
            else:
                self.center[1] = 900 - self.place.height / 2

        if self.center[0] - self.place.width / 2 < 0:
            if [self.room[0] - 1, self.room[1], self.room[2]] in rooms.roomCoordinates and coordinateToRoom(self.room)[1].foes == [] and 400 < self.center[1] < 500:
                coordinateToRoom(self.room)[1].enemyBullets = []
                self.room[0] -= 1
                self.center[0] = 1550 - self.place.width / 2
                self.bullets = []
                print('v')
                self.center[1] = 450
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
                for material in coordinateToRoom(self.room)[1].destructibleMaterialSources:
                    if checkNotDamageCollision(self, material):
                        material.hp = 0
                for room in rooms.rooms:
                    if room.coordinate[2] == self.room[2] and ((room.coordinate[1] == self.room[1] and abs(room.coordinate[0] - self.room[0]) < 2) or (room.coordinate[0] == self.room[0] and abs(room.coordinate[1] - self.room[1]) < 2)):
                        room.found = 1
                self.save()
            else:
                self.center[0] = self.place.width / 2

        if self.center[1] - self.place.height / 2 < 0:
            if [self.room[0], self.room[1] + 1, self.room[2]] in rooms.roomCoordinates and coordinateToRoom(self.room)[1].foes == [] and 750 < self.center[0] < 850:
                coordinateToRoom(self.room)[1].enemyBullets = []
                self.room[1] += 1
                self.center[1] = 850 - self.place.height / 2
                self.center[0] = 800
                self.bullets = []
                self.dashFramesRemaining = -1
                self.stamina = 0
                print('v')
                rooms.readdFoes()
                self.switchSong()
                for material in coordinateToRoom(self.room)[1].destructibleMaterialSources:
                    if checkNotDamageCollision(self, material):
                        material.hp = 0
                for room in rooms.rooms:
                    if room.coordinate[2] == self.room[2] and ((room.coordinate[1] == self.room[1] and abs(room.coordinate[0] - self.room[0]) < 2) or (room.coordinate[0] == self.room[0] and abs(room.coordinate[1] - self.room[1]) < 2)):
                        room.found = 1
                self.save()
            else:
                self.center[1] = self.place.height / 2

        if self.place.center[0] + self.place.width / 2 > 1600:
            if [self.room[0] + 1, self.room[1], self.room[2]] in rooms.roomCoordinates and coordinateToRoom(self.room)[1].foes == [] and 400 < self.center[1] < 500:
                coordinateToRoom(self.room)[1].enemyBullets = []
                self.room[0] += 1
                self.center[0] = self.place.width / 2 + 50
                self.center[1] = 450
                self.bullets = []
                print('v')
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
                for material in coordinateToRoom(self.room)[1].destructibleMaterialSources:
                    if checkNotDamageCollision(self, material):
                        material.hp = 0
                for room in rooms.rooms:
                    if room.coordinate[2] == self.room[2] and ((room.coordinate[1] == self.room[1] and abs(room.coordinate[0] - self.room[0]) < 2) or (room.coordinate[0] == self.room[0] and abs(room.coordinate[1] - self.room[1]) < 2)):
                        room.found = 1
                self.save()
            else:
                self.center[0] = 1600 - self.place.width / 2

        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]
    def useNanotechRevolver(self):
        if self.inventory[self.activeItem].type == "NanotechRevolver":
            if self.fireCooldown < 1 and self.firing == 1:
                pathx = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0] * 3
                pathy = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1] * 3
                self.fireCooldown = 20

                self.bullets.append(Bullet(
                    pathx * 10,
                    pathy * 10,
                    1.4, self,
                    sprite=IMAGES['images/basicRangeProjectile_d.png'], elements=['metal'],
                    mark=('self.dr -= 0.5', IMAGES['images/nanotechRevolverMark.png'], '"heat" in self.recentElementDamages',
                          'self.hp -= 5')))
    def useFerroSandShotgun(self):
        if self.fireCooldown < 1:
            for number in range(5):
                player_pos = [self.place.centerx, self.place.centery]
                mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
                pathx = semirandomPathWithoutPlace(player_pos, mouse_pos)[0] * 8
                pathy = semirandomPathWithoutPlace(player_pos, mouse_pos)[1] * 8
                self.bullets.append(Bullet(
                    pathx, pathy, 0.6, self, sprite=IMAGES['images/ferroSandShotgunShot.png'], splash=1))
            self.fireCooldown = 20
    def useAltFerroSandShotgun(self):
        element = "'metal'"
        explosionCode = f'p.bullets.append(Bullet(0, 0, 0, p, linger=14, sprite=spearExplosion[0], piercing=999999, centerx=self.place.centerx, centery=self.place.centery, rotated=0, animation=spearExplosion))'
        self.bullets.append(Bullet(pathWithoutPlaceAttribute([self.place.centerx, self.place.centery], pygame.mouse.get_pos())[0] * 25,
                                   pathWithoutPlaceAttribute([self.place.centerx, self.place.centery], pygame.mouse.get_pos())[1] * 25,
                                   25, self, linger=32, sprite=IMAGES['images/ferroSandShotgunSpear2.png'],
                                   piercing=100, knockback=[pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0] * 5,
                                   pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1] * 5, 5],
                                   specialEndEffect='p.bullets.append(Bullet(0, 0, 0, p, '
                                                    'linger=100000, sprite=IMAGES["images/ferroSandShotgunSpearInGround3.png"], piercing=10000, '
                                                     'centerx=self.place.centerx, centery=self.place.centery, '
                                                      f'specialEffects=("for foe in coordinateToRoom(p.room)[1].foes: foe.hp -= returnUnlessNegative(30 - getDistance(self, foe) / 50)", "{explosionCode}", "p.bullets.remove(self)"),'
                                                       f'specialEffectConditions=("checkCollisionWithElementalPlayerBullets({element}, self) and True", "checkCollisionWithElementalPlayerBullets({element}, self)", "True and checkCollisionWithElementalPlayerBullets({element}, self) and self.linger > 42"),'
                                                        'rotated=0))'))
    def useActiveItem(self):
        if self.firing and self.fireCooldown < 1 and self.dashFramesRemaining < 1 and self.slideFramesRemaning < 1:
            try:
                exec(f'self.use{self.inventory[self.activeItem].type}()')
            except AttributeError:
                pass
            self.inventory[self.activeItem].chargeProgress = 0
        self.fireCooldown -= 1

    def fireSemirandomNoAttack(self, damage):
        player_pos = [self.place.centerx, self.place.centery]
        mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        pathx = semirandomPathWithoutPlace(player_pos, mouse_pos)[0] * 8
        pathy = semirandomPathWithoutPlace(player_pos, mouse_pos)[1] * 8
        self.bullets.append(Bullet(
            pathx, pathy,damage, self, sprite=IMAGES['images/basicSpreadProjectile_d.png'], splash=100))

    def basicFireBlast(self):
        for number in range(10):
            self.fireSemirandomNoAttack(0.06)

    def useMandible(self):
        self.fireCooldown = 40

        # Swing
        self.bullets.append(Bullet(0, 0, 8, self, melee=1, linger=20, sprite=IMAGES['images/lionMelee.png']))

        # Fire
        player_pos = [self.place.centerx, self.place.centery]
        mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        self.bullets.append(Bullet(pathWithoutPlaceAttribute(player_pos, mouse_pos)[0] * 6, pathWithoutPlaceAttribute(player_pos, mouse_pos)[1] * 6, 5, self, piercing=1))

    def dash(self):
        if self.stamina < 1:
            self.stamina = 315
            self.dashFramesRemaining = 30
            self.invincibility = 45
            self.hrWhileDashing = 35 * pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0]
            self.vrWhileDashing = 35 * pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1]

            for i in self.bullets:
                if i.melee:
                    self.bullets.remove(i)

    def slide(self):
        if self.stamina < 216 and self.dashFramesRemaining < 1 and self.slideFramesRemaning < 1:
            self.slideFramesRemaning = 15
            self.stamina += 100
            for i in self.bullets:
                if i.melee == 1:
                    self.bullets.remove(i)

class Foe:
    def __init__(self, kind, centerx, centery, **extraStats):
        self.fireCooldown          = 0
        self.knockbackAfflictions  = []
        self.hr                    = 0
        self.dr = 0
        self.markShatterCondition = '1 == 2'
        self.markShatterEffect = ''
        self.healsOnKill = 1
        self.multifaced            = 0
        self.markEffect = ''
        self.vr                    = 0
        self.vulnerable            = 1
        self.wobbegongDashCooldown = 120
        self.wobbegongDashing      = 0
        self.type                  = kind
        self.recentElementDamages = []
        self.bullets               = []
        self.drops                 = []
        self.markSprite = None
        self.totalSpeed = 1
        if self.type == "antlion":
            self.attack       = 0
            self.hp           = 100
            self.speed        = 0
            self.vulnerable   = 0
            self.antlionPause = random.randint(15, 70)
            self.drops        = [Item(3, "Mandible")]
            self.sprites      = [IMAGES['images/antlion.png'], IMAGES['images/activeLionPit.png']]
            self.sprite       = IMAGES['images/activeLionPit.png']

        elif self.type == "ironAngel":
            self.sprite = IMAGES['images/ironAngel.png']
            self.hp = 100
            self.attack = 40
            self.speed = 0
            self.drops = [Item(1, "FerroSandShotgun", altAttackCharge=120), Item(100, 'ferroSand', qty=random.randint(1, 2), maxStackSize=99),
                          Item(100, 'ferroSteel', qty=random.randint(1, 2), maxStackSize=99)]

        elif self.type == "wobbegong":
            self.sprite = IMAGES['images/wobbegong_a.png']
            self.hp = 100
            self.attack = 80
            self.multifaced = 1
            self.dsprite = IMAGES['images/wobbegong_d.png']
            self.ssprite = IMAGES['images/wobbegong_s.png']
            self.asprite = IMAGES['images/wobbegong_a.png']
            self.wsprite = IMAGES['images/wobbegong_w.png']
            self.speed = 2 / sqrt(2)
            self.drops = [Item(1, 'wobbegongCloak')]
        elif self.type == 'blobSummoner':
            self.speed = 1
            self.hp = 200
            self.attack = 50
            self.sprite = IMAGES['images/blobSummoner.png']
            self.drops = []
        elif self.type == 'blobSummon':
            self.hp = 3
            self.speed = 2
            self.healsOnKill = 0
            self.sprite = IMAGES['images/activeLionPit.png']
            self.drops = []
            self.undergroundFramesAsBlobSummon = 45
            self.vulnerable = 0
            self.attack = 0
        elif self.type == 'meleeBlob':
            self.sprite = IMAGES['images/meleeBlob.png']
            self.hp = 40
            self.drops = []
            self.attack = 75
        if self.type != "wobbegong":
            self.wsprite = self.sprite
            self.dsprite = self.sprite
            self.asprite = self.sprite
            self.ssprite = self.sprite
        else:
            self.dsprite = IMAGES['images/wobbegong_d.png']
            self.ssprite = IMAGES['images/wobbegong_s.png']
            self.asprite = IMAGES['images/wobbegong_a.png']
            self.wsprite = IMAGES['images/wobbegong_w.png']
        self.place         = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.center        = [self.place.centerx, self.place.centery]
        self.directionalSprites = {'w': self.wsprite, 'a': self.asprite, 's': self.ssprite, 'd': self.dsprite}
        self.speed = 1
        for var in extraStats.keys():
            exec(f'self.{var} = {extraStats[var]}')
        self.saveStatTypes = [key for key in vars(self).keys()]
        for stat in self.saveStatTypes:
            try:
                 test = open('filler.json', 'x')
            except FileExistsError:
                test = open('filler.json', 'w')
            try:
                json.dump(vars(self)[stat], test)
            except TypeError:
                self.saveStatTypes.remove(stat)
            test.close()
        print(self.saveStatTypes)
        self.saveCode = f'room[coordinate].foes.append(Foe("{self.type}", {self.place.centerx}, {self.place.centery}))'
        self.deathLoadCode = f'room.foes.append(Foe("{self.type}", {self.place.centerx}, {self.place.centery}))'
    def prepareToSave(self):
        print(self.saveStatTypes)
        self.saveCode = f'room.foes.append(Foe("{self.type}", {self.place.centerx}, {self.place.centery}'
        for stat in self.saveStatTypes:
            try:
                test = open('filler.json', 'x')
            except FileExistsError:
                test = open('filler.json', 'w')
            try:
                json.dump(vars(self)[stat], test)
            except:
                self.saveStatTypes.remove(stat)
            test.close()
        for stat in self.saveStatTypes:
            if type(vars(self)[stat]) == str or type(vars(self)[stat]) == pygame.Surface or type(vars(self)[stat]) == pygame.Rect:
                pass
            else:
                self.saveCode += f', {stat}={vars(self)[stat]}'
        self.saveCode += '))'
    def updateStats(self):
        self.speed = 1
        self.totalSpeed = 1
        self.dr = 0
        exec(self.markEffect)
        if eval(self.markShatterCondition):
            exec(self.markShatterEffect)
            print('yay')
            self.markEffect = ''
            self.markShatterCondition = '1 == 2'
            self.markShatterEffect = ''
            self.markSprite = None
        self.recentElementDamages = []
    def move(self):
        self.updateStats()
        if self.type != 'antlion':
            if self.type == "wobbegong":
                if not self.wobbegongDashing:
                    self.hr = path(self, p)[0] * 0.2
                    self.vr = path(self, p)[1] * 0.2
                    if self.wobbegongDashCooldown < 1:
                        self.hr = path(self, p)[0] * 0.5
                        self.vr = path(self, p)[1] * 0.5
                        self.wobbegongDashing = 1
                        self.wobbegongDashCooldown = random.randint(120, 240) / self.totalSpeed
                self.wobbegongDashCooldown -= 1

            elif self.type == "ironAngel":
                self.vr = 0
                self.hr = 0
            elif self.type == 'blobSummoner':
                self.hr = 0
                self.vr = 0
            elif self.type == 'blobSummon':
                if self.undergroundFramesAsBlobSummon < 1:
                    self.vulnerable = 1
                    self.attack = 40
                    self.hr = path(self, p)[0] * 0.25
                    self.vr = path(self, p)[1] * 0.25
                    self.sprite = IMAGES['images/blobSummon.png']
                    self.dsprite = self.sprite
                    self.asprite = self.sprite
                    self.wsprite = self.sprite
                    self.ssprite = self.sprite
                    self.directionalSprites = {'w': self.wsprite, 'a': self.asprite, 's': self.ssprite,
                                               'd': self.dsprite}
                else:
                    self.hr = 0
                    self.vr = 0
                    self.undergroundFramesAsBlobSummon -= 1
            elif self.type == 'meleeBlob':
                self.hr = path(self, p)[0] * 0.1
                self.vr = path(self, p)[1] * 0.1
            self.center[0] += self.hr * self.speed * self.totalSpeed
            self.center[1] += self.vr * self.speed * self.totalSpeed
            self.place.centerx = self.center[0]
            self.place.centery = self.center[1]

            for material in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                while checkNotDamageCollision(self, material) == 1 and material.hp > 0:
                    checkCollision(self, material)
                    if self.wobbegongDashing:
                        self.spreadShotAsWobbegong()
                        self.wobbegongDashing = 0

                    checkCollision(self, material)

                    self.center[0] -= self.hr * 1.1
                    self.center[1] -= self.vr * 1.1
                    self.place.centery = self.center[1]
                    self.place.centerx = self.center[0]

            self.sprite = self.directionalSprites[getDirection(self.hr, self.vr)]

            if self.place.left <= 0:
                self.place.left = 0

            elif self.place.right >= 1600:
                self.place.right = 1600

            if self.place.top <= 0:
                self.place.top = 0

            elif self.place.bottom >= 900:
                self.place.bottom = 900

            if (self.place.left == 0 or self.place.right == 1600 or self.place.top == 0 or self.place.bottom == 900) and self.type == "wobbegong" and self.wobbegongDashing:
                self.spreadShotAsWobbegong()
                self.wobbegongDashing = 0
            for i in self.knockbackAfflictions:
                if i[2] < 1:
                    try:
                        self.knockbackAfflictions.remove(i)
                    except ValueError:
                        pass
                else:
                    self.center[0] += i[0]
                    self.center[1] += i[1]
                    i[2] -= 1
        p.display.blit(self.sprite, self.place)

    def fireStraight(self, target): # Not used in this class
        self.bullets.append(Bullet(path(self, target)[0] * self.totalSpeed, path(self, target)[1] * self.totalSpeed, 34, self))
    def swingAsMeleeBlob(self):
        if self.fireCooldown < 1:
            self.bullets.append(Bullet(path(self, p)[0] * self.totalSpeed / 3, path(self, p)[1] * self.totalSpeed / 3, 75, self, linger=60, sprite=IMAGES['images/playerMelee.png']))
            self.fireCooldown = random.randint(100, 150)
        self.fireCooldown -= self.totalSpeed
    def summonAsBlobSummoner(self):
        if self.fireCooldown < 1:
            if p.getQtyOfFoeTypeInRoom('blobSummon') < 40:
                for number in range(15):
                    coordinateToRoom(p.room)[1].foes.append(Foe('blobSummon', p.place.centerx + random.randint(-400, 400), p.place.centery + random.randint(-400, 400)))
                self.fireCooldown = random.randint(300, 350) / self.totalSpeed
            else:
                for number in range(15):
                    newBulletCenter = [p.place.centerx + random.randint(-400, 400), p.place.centery + random.randint(-400, 400)]
                    self.bullets.append(Bullet(pathWithoutPlaceAttribute(newBulletCenter, p.center)[0] * 5,
                                               pathWithoutPlaceAttribute(newBulletCenter, p.center)[1] * 5,
                                               65, self, sprite=IMAGES['images/IAP.png'],
                                               centerx=newBulletCenter[0], centery=newBulletCenter[1],
                                               delay=random.randint(200, 250), positionCalculatedOnFire=0))
                self.fireCooldown = random.randint(200, 250)
        self.fireCooldown -= self.totalSpeed

    def fireStraightToPoint(self, point): # Not used in this class
        self.bullets.append(Bullet(
            pathWithoutPlaceAttribute(self.center, point)[0] * self.totalSpeed,
            pathWithoutPlaceAttribute(self.center, point)[1] * self.totalSpeed, 34, self
        ))

    def spreadShotAsWobbegong(self):
        if self.type == 'wobbegong':
            for number in range(7):
                self.fireSemirandom(p, 0)

    def attackAsAntlion(self):
        self.antlionPause -= self.totalSpeed

        if self.antlionPause < 1:
            if self.vulnerable:
                self.sprite       = IMAGES['images/activeLionPit.png']
                self.antlionPause = 25
                self.vulnerable   = 0
                self.place.centerx = p.place.centerx
                self.place.centery = p.place.centery
            else:
                self.sprite       = IMAGES['images/antlion.png']
                self.antlionPause = 70
                self.vulnerable   = 1

                self.bullets.append(Bullet(0, 0, 100, self, melee=1, linger = 65, centery=self.place.centery + 30))

                for i in range(2):
                    self.bullets.append(
                        Bullet(semirandomPath(self, p)[0] * self.totalSpeed,
                        semirandomPath(self, p)[1] * self.totalSpeed,
                        100, self, linger=150
                    ))

    def firePredictivelyAsLobster(self): # Not used in this class
        self.fireCooldown -= self.totalSpeed

        if -100 <self.fireCooldown < 1:
            self.firePredictivelyToPlayer(12)

        if self.fireCooldown < -100:
            self.fireCooldown = 60

    def firePredictivelyToPlayer(self, speed):
        self.bullets.append(Bullet(
            predictivePathToPlayer(self, speed)[0] * self.totalSpeed,
            predictivePathToPlayer(self, speed)[1] * self.totalSpeed,
            35, self, sprite=IMAGES['images/ironAngelProjectile.png']
        ))

    def fireSemirandom(self, target, delay):
        self.bullets.append(Bullet(
            semirandomPath(self, target)[0] * 1.5 * self.totalSpeed,
            semirandomPath(self, target)[1] * 1.5 * self.totalSpeed,
            65, self, delay=delay
        ))

    def spreadShotAsIronAngel(self):
        if self.fireCooldown < 1:
            self.fireCooldown = 130
            for i in range(9):
                self.fireSemirandom(p, 0)
        else:
            self.fireCooldown -= self.totalSpeed

class mouseMarker:
    def __init__(self):
        self.sprite = IMAGES['images/mouseMarkerTarget2.png']
        self.place = self.sprite.get_rect()

    def update_position(self):
        self.place.centerx, self.place.centery = pygame.mouse.get_pos()[:2]

class Room:
    def __init__(self, coordinate, biome, num, depth=0):
        self.biome = biome
        if depth == 1:
            self.shelterZone = [self]
            self.blobSpawnTimerAsShelter = 300
        self.teleporters = []
        self.mapImage = IMAGES[f'images/mapImage{random.randint(1, 6)}.png']
        self.found = 0
        self.coordinate = [coordinate[0], coordinate[1], depth]
        self.plainAnimations = []
        if self.biome == 'desert' and self.coordinate[2] == 0:
            self.defaultHeatEffect = 'self.heat += 0.006'
            self.layout = random.randint(1, 4)
            self.foe_types = ['ironAngel', 'wobbegong', 'antlion']
            self.background = 'images/desertBackground.bmp'
            self.potentialMaterialSources = [destructibleMaterialSource(80, 450, 'sandstone'),
                                            destructibleMaterialSource(80, 450, 'desertTree'),
                                             destructibleMaterialSource(80, 450, 'fossilFuel'),
                                             destructibleMaterialSource(80, 450, 'skeleton'),
                                             destructibleMaterialSource(80, 450, 'amethyst'),
                                             destructibleMaterialSource(80, 450, 'shellPile'),
                                             destructibleMaterialSource(80, 450, 'cactus'),
                                             ]
        if self.coordinate[2] == 1:
            self.background = 'images/altShelterBackgroundBMP.bmp'
            self.defaultHeatEffect = 'self.heat = 0'
            self.layout = 7
            self.foe_types = ['blobSummon']
            self.potentialMaterialSources = []
        self.destructibleMaterialSources = []
        self.difficulty = random.randint(0, 5)
        self.resources = random.randint(0, 3 + floorIfPositive(self.difficulty / 2))
        if abs(self.coordinate[0]) < 2 and abs(self.coordinate[1]) < 2 and self.coordinate[2] == 0:
            self.found = 1
        self.antlions      = []
        self.doors         = []
        self.enemyBullets  = []
        self.foes          = []
        self.ironAngels   = []
        self.droppedItems = []
        self.p_bullets     = []
        self.traps         = []
        self.wobbegongs    = []
        self.blobSummons = []
        self.blobSummoners = []
        self.meleeBlobs = []
        self.cleared = 0
        self.potentialPitsX = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
        self.potentialPitsY = [50, 850, 450, 300, 600, 600, 300, 50, 850]

        try:
            if type(coordinateToRoom([coordinate[0], coordinate[1], 0])) == tuple and depth:
                self.biome = coordinateToRoom([coordinate[0], coordinate[1], 0])[1].biome
        except NameError:
            pass



        self.backgroundLocation = IMAGES[self.background].get_rect()
        self.backgroundLocation.left = 0
        self.backgroundLocation.top = 0


        if not self.coordinate == [0, 0, 0] and not self.difficulty == 5:
            if self.layout == 1:
                self.foes = [
                    Foe("ironAngel", 50, 50),
                    Foe("ironAngel", 50, 850),
                    Foe("ironAngel", 1560, 850),
                    Foe("ironAngel", 1560, 50)
                ]

                if self.difficulty <= 1:
                    self.foes.pop(random.randint(0, 3))
                    self.foes.pop(random.randint(0, 2))

                elif self.difficulty == 1:
                    self.foes.append(Foe("ironAngel", 800, 450))

                elif self.difficulty == 2:
                    self.traps.append(PitTrap(800, 450))
                    self.foes.pop(random.randint(0, 3))

                elif self.difficulty > 2:
                    self.foes.pop(x := random.randint(0, 1))
                    self.foes.pop(x + 1)
                    self.foes.append(Foe("wobbegong", 800, 450))

            elif self.layout == 2:
                self.foes = [Foe("wobbegong", 800, 450)]
                if self.difficulty == 1:
                    for i in range(5):
                        self.traps.append(PitTrap(
                            800 + random.randint(-i * 40, i * 40),
                            450 + random.randint(-i * 40, i * 40)
                        ))

                elif self.difficulty == 2:
                    self.foes = [Foe("wobbegong", 50, 50), Foe("wobbegong", 1560, 850)]
                    self.traps.append(PitTrap(805, 450))

                elif self.difficulty > 2:
                    self.foes = [Foe("wobbegong", 50, 50), Foe("wobbegong", 1550, 850), Foe("ironAngel", 800, 450)]

            elif self.layout == 3:
                self.foes = [Foe("wobbegong", 800, 450), Foe("antlion", 50, 50), Foe("antlion", 1550, 850)]
                if self.difficulty == 0:
                    self.foes.pop(0)

                elif self.difficulty == 1 or self.difficulty > 2:
                    self.foes.pop(2)

                elif self.difficulty == 2:
                    self.traps = [
                        PitTrap(800, 187),
                        PitTrap(800, 563),
                        PitTrap(400, 450),
                        PitTrap(1200, 450),
                        PitTrap(800, 450)
                    ]

                if self.difficulty > 2:
                    for i in range(9):
                        self.traps.append((PitTrap(self.potentialPitsX[i], self.potentialPitsY[i])))
                        self.traps.append(PitTrap(30 + 70 * i, 20 + 50 * i))

            elif self.layout == 4:
                for i in range(27):
                    self.traps.append(PitTrap(400, i * 35 + 27))

                for i in range(27):
                    self.traps.append(PitTrap(1200, i * 35 + 27))

                self.potentialPitsX = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
                self.potentialPitsY = [50, 850, 450, 300, 600, 600, 300, 50, 700]

                for i in range(9):
                    self.traps.append(PitTrap(self.potentialPitsX[i], self.potentialPitsY[i]))
            elif self.layout == 5:
                self.foes = [Foe('meleeBlob', 50, 50), Foe('meleeBlob', 1550, 50),
                             Foe('meleeBlob', 1550, 850), Foe('meleeBlob', 50, 850), Foe('blobSummoner', 800, 50)]
                if self.difficulty == 0:
                    self.foes = [self.foes[0]]
                elif self.difficulty == 1:
                    self.foes = self.foes[0: 4]
                elif self.difficulty > 1:
                    self.foes = self.foes[0: 4] + [Foe('meleeBlob', 800, 450), Foe('meleeBlob', 550, 450),
                                                   Foe('meleeBlob', 1050, 450), Foe('meleeBlob', 800, 200)]
            elif self.layout == 6:
                self.foes = [Foe('blobSummoner', 50, 50), Foe('blobSummoner', 1550, 850)]
                if self.difficulty == 0:
                    self.foes = [Foe('blobSummon', 800, 450)]
                elif self.difficulty > 1:
                    self.foes.append(Foe('meleeBlob', 800, 450))
                if self.difficulty > 2:
                    self.foes.append(Foe('meleeBlob', 1550, 850))
                    self.foes.append(Foe('meleeBlob', 50, 850))
            if self.difficulty > 3 and self.biome == 'desert' and self.coordinate[2] == 0:
                for difficulty in range(self.difficulty * 2):
                    self.traps.append(PitTrap(
                        random.choice(self.potentialPitsX) + random.randint(-50, 50),
                        random.choice(self.potentialPitsY) + random.randint(-30, 30)
                    ))
            for enemy in self.foes:
                if enemy.type == "ironAngel":
                    self.ironAngels.append(enemy)
                elif enemy.type == "wobbegong":
                    self.wobbegongs.append(enemy)
                elif enemy.type == "antlion":
                    self.antlions.append(enemy)
                elif enemy.type == 'meleeBlob':
                    self.meleeBlobs.append(enemy)
                elif enemy.type == 'blobSummoner':
                    self.blobSummoners.append(enemy)
                elif enemy.type == 'blobSummon':
                    self.blobSummons.append(enemy)
        self.num = num
        self.initialFoes        = self.foes # Not used anywhere in this class
        self.initialIronAngels  = self.ironAngels # Not used anywhere in this class
        self.initialWobbegongs  = self.wobbegongs # Not used anywhere in this class
        self.initialAntlions    = self.antlions # Not used anywhere in this class
        self.initialTraps       = self.traps # Not used anywhere in this class
        self.classlist = [self.antlions, self.ironAngels, self.wobbegongs, self.meleeBlobs, self.blobSummoners, self.blobSummons]
        if self.coordinate != [0, 0, 0] and self.coordinate[2] != 1:
            for number in range(self.resources):
                for i in range(1000):
                    newMaterialSourceLocation = [random.randint(200, 1400), random.randint(200, 700)]
                    newMaterialSourceType = self.potentialMaterialSources[random.randint(0, len(self.potentialMaterialSources) - 1)]
                    self.destructibleMaterialSources.append(destructibleMaterialSource(newMaterialSourceLocation[0], newMaterialSourceLocation[1],
                                                                                       newMaterialSourceType.type))
                    collides = 0
                    for foe in self.foes:
                        if checkNotDamageCollision(foe, self.destructibleMaterialSources[-1]):
                            collides = 1
                    for thing in self.destructibleMaterialSources:
                        if checkNotDamageCollision(thing, self.destructibleMaterialSources[-1]) and not thing == self.destructibleMaterialSources[-1]:
                            collides = 1
                    if collides:
                        self.destructibleMaterialSources.pop(-1)
                    else:
                        break
        self.deathLoadCode = [foe.deathLoadCode for foe in self.foes]
    def prepareToSave(self):
        for foe in self.foes:
            foe.prepareToSave()
        self.saveCode = ['room.foes = []']
        self.saveCode += [foe.saveCode for foe in self.foes] + [resource.saveCode for resource in self.destructibleMaterialSources] + [teleport.saveCode for teleport in self.teleporters]
        self.saveCode.append(f'room.found = {self.found}')
        self.saveCode.append(f'room.cleared = {self.cleared}')
        self.saveCode.append(f'room.background = "{self.background}"')
        self.saveCode = tuple(self.saveCode)
    def updateBullets(self):
        for enemy in self.foes:
            for bullet in enemy.bullets:
                if not bullet in self.enemyBullets:
                    self.enemyBullets.append(bullet)

        for attack in self.enemyBullets:
            if attack.melee == 1 and not attack.firer in self.foes:
                self.enemyBullets.remove(attack)
    def updateFoes(self):
        self.wobbegongs = []
        self.blobSummons = []
        self.blobSummoners = []
        self.meleeBlobs = []
        self.ironAngels = []
        self.antlions = []
        if self.coordinate[2] == 1:
            self.blobSpawnTimerAsShelter -= 1
            if self.blobSpawnTimerAsShelter < 1:
                self.blobSpawnTimerAsShelter = 300
                self.foes.append(Foe('blobSummon', p.center[0] + random.randint(-500, 500), p.center[1] + random.randint(-500, 500)))
        for enemy in self.foes:
            if enemy.type == "ironAngel" and not enemy in self.ironAngels:
                self.ironAngels.append(enemy)
            elif enemy.type == "wobbegong" and not enemy in self.wobbegongs:
                self.wobbegongs.append(enemy)
            elif enemy.type == "antlion" and not enemy in self.antlions:
                self.antlions.append(enemy)
            elif enemy.type == 'blobSummoner' and not enemy in self.blobSummoners:
                self.blobSummoners.append(enemy)
            elif enemy.type == 'meleeBlob' and not enemy in self.meleeBlobs:
                self.meleeBlobs.append(enemy)
            elif enemy.type == 'blobSummon' and not enemy in self.blobSummons:
                self.blobSummons.append(enemy)

    def spawnFoes(self):
        if not self.coordinate == [0, 0, 0]:
            if random.randint(1, 3) == 2 and len(self.foes) < 2 and not self.layout == 4:
                self.foes.append(Foe(self.foe_types[random.randint(0, len(self.foe_types) - 1)], random.randint(500, 1100), random.randint(300, 600)))
            self.updateFoes()

            if random.randint(1, 4) == 1 and len(self.traps) < 4 and self.biome == 'desert' and self.coordinate[2] == 0:
                self.traps.append(PitTrap(random.randint(500, 1100), random.randint(300, 600)))

class PitTrap:
    def __init__(self, centerx, centery):
        self.attack = 34

        self.sprite = IMAGES['images/lionPit.png']

        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.saveCode = f'room.traps.append(PitTrap(self.place.centerx, self.place.centery))'
class Rooms:
    def __init__(self):
        self.rooms = [Room([0, 0], "desert", 1)]
        self.roomCoordinates = [[0, 0, 0]]
    def coordinateToRoom(self, coordinate):
        for room in self.rooms:
            if room.coordinate == coordinate:
                return (self.rooms.index(room), room)

        return 0
    def sortListOfRooms(self, list):
        copyList = list.copy()
        sortList = []

        while len(sortList) < len(list):
            xList = [room.coordinate[0] for room in copyList]
            potentialNextItems = [room for room in copyList if room.coordinate[0] == max(xList)]
            potentialYList = [room.coordinate[1] for room in potentialNextItems]
            potentialNextItems = [room for room in potentialNextItems if room.coordinate[1] == max(potentialYList)]
            potentialZList = [room.coordinate[2] for room in potentialNextItems]
            potentialNextItems = [room for room in potentialNextItems if room.coordinate[2] == max(potentialZList)]
            roomAdded = potentialNextItems[0]
            copyList.remove(roomAdded)
            sortList.append(roomAdded)
            print(len(list), len(sortList))
        print(len(sortList))
        return sortList
    def makeRooms(self, qty, biome):
        room = [0, 0, 0]
        self.unfinishedShelterZones = []
        for number in range(qty):
            self.roomCoordinates = [room.coordinate for room in self.rooms]
            if random.randint(1, 2) == 1:
                while room in self.roomCoordinates:
                    adjRoomNum = random.randint(0, len(self.rooms) - 1)
                    adjacentRoom = [
                        self.roomCoordinates[adjRoomNum][0],
                        self.roomCoordinates[adjRoomNum][1],
                        0
                    ]
                    room = [adjacentRoom[0] + negativeOrPositive(), adjacentRoom[1], 0]
            else:
                while room in self.roomCoordinates:
                    adjRoomNum = random.randint(0, len(self.rooms) - 1)
                    adjacentRoom = [
                        self.roomCoordinates[adjRoomNum][0],
                        self.roomCoordinates[adjRoomNum][1],
                        0
                    ]
                    room = [adjacentRoom[0], adjacentRoom[1] + negativeOrPositive(), 0]

            self.rooms.append(Room(room, biome, number))
            self.roomCoordinates.append(room)
        for room in self.rooms:
            if room.coordinate[2] == 0 and int(room.num / 6) == room.num / 6:
                newShelter = Room(room.coordinate[0: 2], 'desert', 6, depth=1)
                self.rooms.append(newShelter)
                self.shelters = [area for area in self.rooms if area.coordinate[2] == 1]
                self.roomCoordinates.append(self.rooms[-1].coordinate)
                for shelter in self.shelters:
                    if shelter.coordinate[0] == newShelter.coordinate[0] and abs(shelter.coordinate[1] - newShelter.coordinate[1]) == 1:
                        for thing in shelter.shelterZone:
                            if not thing in newShelter.shelterZone:
                                newShelter.shelterZone.append(thing)
                    elif shelter.coordinate[1] == newShelter.coordinate[1] and abs(shelter.coordinate[0] - newShelter.coordinate[0]) == 1:
                        for thing in shelter.shelterZone:
                            if not thing in newShelter.shelterZone:
                                newShelter.shelterZone.append(thing)
                    for place in newShelter.shelterZone:
                        place.shelterZone = newShelter.shelterZone
                self.unfinishedShelterZones.append(newShelter.shelterZone)
        Liszt = []
        for zone in self.unfinishedShelterZones:
            if not self.sortListOfRooms(zone) in Liszt:
                Liszt.append(self.sortListOfRooms(zone))
        Liszt = Liszt.copy()
        for zone in Liszt:
                shelterYCoords = [loaction.coordinate[1] for loaction in zone]
                print(shelterYCoords)
                topShelter = max(shelterYCoords)
                topShelter = zone[shelterYCoords.index(topShelter)]
                topShelter.background = 'images/shelterBackgroundBMP.bmp'
                print(topShelter.coordinate)
                topShelter.teleporters.append(teleporter(topShelter.coordinate, 800, 50, topShelter.coordinate[0: 2] + [0], 805,
                                                  750, str('images/invisibleTeleporter35X80.png')))

                topShelter.foes = []
                topShelter.traps = []
                topShelter.destructibleMaterialSources = []
                for location in zone:
                    if location != topShelter:
                        location.background = 'images/altShelterBackgroundBMP.bmp'
                        location.teleporters = []
        for zone in self.unfinishedShelterZones:
            for room in zone:
                print(room.coordinate)
        for room in self.shelters:
            if room.background == 'images/shelterBackgroundBMP.bmp':
                self.coordinateToRoom(room.coordinate[0: 2] + [0])[1].teleporters.append(teleporter(room.coordinate[0: 2] + [0],
                                    800, 450, room.coordinate, 800, 750, str('images/shelterEntrance.png')))

    def addDoors(self):
        for room in self.roomCoordinates:
            coordinateToRoom(room)[1].doors = []
            if [room[0], room[1] + 1, room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(800, 20))

            if [room[0], room[1] - 1, room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(800, 880))

            if [room[0] - 1, room[1], room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(20, 450))

            if [room[0] + 1, room[1], room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(1580, 450))
        rooms.roomCoordinates = [room.coordinate for room in rooms.rooms]
    def readdFoes(self):
        for room in self.rooms:
            room.spawnFoes()
class Door:
    def __init__(self, centerx, centery):
        self.sprite = IMAGES['images/door.png']

        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery

class destructibleMaterialSource:
    def __init__(self, centerx, centery, type):
        self.type = type
        self.dr = 0
        self.hp = 2000
        self.dropStackSize = 99
        self.qty = random.randint(2, 3)
        if type == 'fossilFuel':
            self.sprite = IMAGES['images/fossilFuel2.png']
            self.drop = 'fossilFuel'
        elif type == 'shellPile':
            self.sprite = IMAGES['images/shellPile2.png']
            self.drop = 'shell'
        elif type == 'sandstone':
            self.sprite = IMAGES['images/sandstone3.png']
            self.drop = 'sandstone'
        elif type == 'desertTree':
            self.sprite = IMAGES['images/desertTree2.png']
            self.drop = 'desertWood'
        elif type == 'skeleton':
            self.sprite = IMAGES['images/skeleton2.png']
            self.drop = 'bone'
        elif type == 'cactus':
            self.sprite = IMAGES['images/destructibleCactus3.png']
            self.drop = 'chunkOfCactus'
        elif type == 'amethyst':
            self.sprite = IMAGES['images/amethyst2.png']
            self.drop = 'amethyst'

        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.saveCode = f'room.destructibleMaterialSources.append(destructibleMaterialSource({self.place.centerx}, {self.place.centery}, "{self.type}"))'
    def drop_resources(self):
        for number in range(self.qty):
            coordinateToRoom(p.room)[1].droppedItems.append(
                DroppedItem(self.drop, self.place.centerx, self.place.centery, maxStackSize = self.dropStackSize)
            )

        try:
            coordinateToRoom(p.room)[1].destructibleMaterialSources.remove(self)
        except ValueError:
            pass
# Functions
def play(song):
    try:
        if song != p.song:
            pygame.mixer.init()
            pygame.mixer.music.load(song)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            p.song = song
    except:
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

def getLesser(a, b):
    return a if a < b else b

def returnUnlessNegative(number):
    return number if number > 0 else 0

def negativeOrPositive(num=1):
    return -num if random.randint(0, 1) == 0 else num

def semirandomPathWithoutPlace(a, b):
    return [
        pathWithoutPlaceAttribute(a, b)[0] * 3 + random.randint(-200, 200) / 1000,
        pathWithoutPlaceAttribute(a, b)[1] * 3 + random.randint(-200, 200) / 1000
    ]

def pathWithoutPlaceAttribute(a, b):
    disx = b[0] - a[0]
    disy = b[1] - a[1]
    path = []

    try:
        disyoverdisx = disy / disx
        path.append(sign(disx) / sqrt(1 + disyoverdisx ** 2))
    except ZeroDivisionError:
        path.append(0)

    try:
        disxoverdisy = disx / disy
        path.append(sign(disy) / sqrt(1 + disxoverdisy ** 2))
    except ZeroDivisionError:
        path.append(0)

    return path

def floorIfPositive(num):
    return num // 1 if num > 0 else 0

def sign(a):
    return 1 if a > 0 else -1 if a < 0 else 0

def predictivePathToPlayer(attacker, speed):
    hr = p.hr
    vr = p.vr

    a = (hr ** 2 + vr ** 2 - speed ** 2) / speed ** 2
    b = ((p.place.centerx - attacker.place.centerx) * hr + vr * (p.place.centery - attacker.place.centery)) * 2 / speed
    c = p.place.centerx ** 2 - 2 * attacker.place.centerx * p.place.centerx - attacker.place.centerx ** 2 \
      + p.place.centery ** 2 - 2 * attacker.place.centery * p.place.centery - attacker.place.centery ** 2

    try:
        time = (-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a * speed)
    except ZeroDivisionError:
        try:
            time = -c / (b * speed)
        except ZeroDivisionError:
            time = 1 / speed
    time = abs(time)

    nx = time * hr + p.place.centerx
    ny = time * vr + p.place.centery

    if nx > 1600:
        nx = 1600
    elif nx < 0:
        nx = 0

    if ny > 900:
        ny = 900
    elif ny < 0:
        ny = 0

    thePath = pathWithoutPlaceAttribute([attacker.place.centerx, attacker.place.centery], [nx, ny])

    if abs(hr) < abs(speed * thePath[0]) and sign(hr) == sign(thePath[0]):
        thePath[0] = path(attacker, p)[0] / 21 + sign(p.hr)
        thePath[1] -= sign(attacker.place.centery - p.place.centery) / 3

    if abs(vr) < abs(speed * thePath[1]) and sign(vr) == sign(thePath[1]):
        thePath[1] = path(attacker, p)[1] / 21 + sign(p.vr)
        thePath[0] -= sign(attacker.place.centerx - p.place.centerx) / 3
    return [speed * thePath[0], speed * thePath[1]]

def coordinateToRoom(coordinate):
    for room in rooms.rooms:
        if room.coordinate == coordinate:
            return (rooms.rooms.index(room), room)
def getGreater(a, b):
    return a if a > b else b
def checkCollision(a, b):
    if abs(a.place.centerx - b.place.centerx) < (a.place.width  + b.place.width)  / 2 and \
       abs(a.place.centery - b.place.centery) < (a.place.height + b.place.height) / 2:
            if type(a) == Foe:
                if a.attack == 0 and type(b) == destructibleMaterialSource:
                    b.hp -= 100
            elif type(a) == Player and type(b) == destructibleMaterialSource:
                b.hp = 0
            if type(a) == Bullet:
                if type(b) == Foe:
                    if a.mark is not None:
                        b.recentElementDamages += [element for element in a.elements]
                        b.updateStats()
                        b.markEffect = a.markEffect
                        b.markSprite = a.markSprite
                        b.markShatterCondition = a.markShatterCondition
                        b.markShatterEffect = a.markShatterEffect
                if a.delay < 1:
                    if not type(b) == destructibleMaterialSource:
                        b.knockbackAfflictions.append([a.knockback[0], a.knockback[1], a.knockback[2]])
                    elif a.firer == p:
                        b.hp -= 10 * a.damage
                    if a.melee == 0 and not b in a.hurtTargets:
                        print(a.splash)
                        if a.splash > 0:
                            for foe in [enemy for enemy in coordinateToRoom(p.room)[1].foes if getDistance(a, enemy) < a.splash * 75]:
                                foe.hp -= a.splash - getDistance(a, foe) / 75
                        try:
                            a.piercing -= 1

                            if a.piercing < 0:
                                try:
                                    a.firer.bullets.remove(a)
                                except ValueError:
                                    pass

                                try:
                                    coordinateToRoom(p.room)[1].enemyBullets.remove(a)
                                except ValueError:
                                    pass
                                exec(a.specialEndEffect)
                            a.hurtTargets.append(b)

                            if type(b) == Player and p.invincibility < 1:
                                if not a.damage == 0:
                                    b.invincibility = 40
                                    b.hp -= getGreater(1, a.damage - b.dr)
                                return 1

                            if not type(b) == Player:
                                if a.melee == 1:
                                    if not b in a.hurtTargets:
                                        b.hp -= getGreater(1, a.damage - b.dr)
                                        return 1

                                b.hp -= getGreater(1, a.damage - b.dr)
                                return 1

                        except ValueError:
                            pass
            elif type(b) == Player and p.invincibility < 1:
                if b.invincibility < 1:
                    if not a.attack == 0:
                        b.invincibility = 40
                        b.hp -= getGreater(1, a.attack - b.dr)
                    return 1
            elif type(b) == destructibleMaterialSource and type(a) == Foe:
                b.hp -= a.attack

    return 0

def checkNotDamageCollision(a, b):
    if abs(a.place.centerx - b.place.centerx) < (a.place.width + b.place.width) / 2 and abs(a.place.centery - b.place.centery) < (a.place.height + b.place.height) / 2:
        if type(a) == Foe:
            if a.attack == 0 and type(b) == destructibleMaterialSource:
                b.hp -= 10
        if type(b) == destructibleMaterialSource and b.hp < 1:
            try:
                coordinateToRoom(p.room)[1].destructibleMaterialSources.remove(b)
            except ValueError:
                pass
        return 1
def getDistance(a, b):
    return sqrt((a.place.centerx - b.place.centerx) ** 2 + (a.place.centery - b.place.centery) ** 2)
def detectMouseCollision(a):
    try:
        if abs(a.place.centery - pygame.mouse.get_pos()[1]) < a.place.height / 2 and abs(a.place.centerx - pygame.mouse.get_pos()[0]) < a.place.width / 2:
            return 1
    except AttributeError:
        pass
    return 0

def path(a, b):
    disx = b.place.centerx - a.place.centerx
    disy = b.place.centery - a.place.centery
    path = []

    try:
        disyoverdisx = disy / disx
        path.append(21 * sign(disx) / sqrt(1 + disyoverdisx ** 2))
    except ZeroDivisionError:
        path.append(0)

    try:
        disxoverdisy = disx / disy
        path.append(21 * sign(disy) / sqrt(1 + disxoverdisy ** 2))
    except ZeroDivisionError:
        path.append(0)

    return path

def semirandomPath(a, b):
    return [
        path(a, b)[0] / 6 + random.randint(-3200, 3200) / 1000,
        path(a, b)[1] / 6 + random.randint(-3200, 3200) / 1000
    ]
def blitEverything():
    p.display.blit(IMAGES[coordinateToRoom(p.room)[1].background], coordinateToRoom(p.room)[1].backgroundLocation)
    for door in coordinateToRoom(p.room)[1].doors:
        p.display.blit(door.sprite, door.place)

    for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
        p.display.blit(resource.sprite, resource.place)

    p.display.blit(p.sprite, p.place)

    for item in coordinateToRoom(p.room)[1].droppedItems:
        p.display.blit(item.sprite, item.place)
    for i in coordinateToRoom(p.room)[1].teleporters:
        p.display.blit(i.sprite, i.place)
    for trap in coordinateToRoom(p.room)[1].traps:
        p.display.blit(trap.sprite, trap.place)

    for foe in coordinateToRoom(p.room)[1].foes:
        p.display.blit(foe.sprite, foe.place)
        if foe.markSprite != None:
            foe.markPlace = foe.markSprite.get_rect()
            foe.markPlace.bottom = foe.place.top - 25
            foe.markPlace.centerx = foe.place.centerx
            p.display.blit(foe.markSprite, foe.markPlace)
    for i in coordinateToRoom(p.room)[1].enemyBullets:
        if i.delay < 1:
            p.display.blit(i.sprite, i.place)
    for i in p.bullets:
        if i.delay < 1:
            p.display.blit(i.sprite, i.place)
    for anim in coordinateToRoom(p.room)[1].plainAnimations:
        anim.showAndUpdate()
    mouseMarker.place.centerx = pygame.mouse.get_pos()[0]
    mouseMarker.place.centery = pygame.mouse.get_pos()[1]
    mouseMarker.sprite = IMAGES['images/mouseMarkerTarget2.png']
    #if p.room[2] == 0:
    #    if p.time < 45 or p.time >= 315:
    #        p.display.blit(IMAGES['images/nightFilterBMP2.bmp'], pygame.Rect(0, 0, 1600, 900))
    #    elif 45 <= p.time < 135:
    #        p.display.blit(IMAGES['images/earlyMorningFilterBMP.bmp'], pygame.Rect(0, 0, 1600, 900))
    #    elif 135 <= p.time < 225:
     #       p.display.blit(IMAGES['images/midDayFilterBMP.bmp'], pygame.Rect(0, 0, 1600, 900))
     #   else:
     #       p.display.blit(IMAGES['images/eveningFilterBMP.bmp'], pygame.Rect(0, 0, 1600, 900))
    if p.inventoryShown == 1:
        p.showInventory()
    p.showHealthAndStaminaAndHeatAndCharge()
    p.display.blit(mouseMarker.sprite, mouseMarker.place)
    if p.mapShown:
        p.display.fill((0, 0, 0), pygame.Rect(0, 0, 1600, 900))
        for room in [zone for zone in rooms.rooms if zone.coordinate[2] == p.room[2] and zone.found]:
            p.display.blit(room.mapImage, pygame.Rect(778 + 50 * room.coordinate[0], 434 - 37 * room.coordinate[1], 45, 32))
            if room.coordinate == p.room:
                p.display.blit(IMAGES['images/playerRoomMapImage.png'], pygame.Rect(778 + 50 * room.coordinate[0], 434 - 37 * room.coordinate[1], 45, 34))

    for number in range(7):
        pygame.display.flip()

play('music/desertCalm.mp3')
def checkCollisionWithAllPlayerBullets(a):
    for bullet in p.bullets:
        if checkNotDamageCollision(bullet, a) and bullet != a:
            return 1

    return 0
def checkCollisionWithElementalPlayerBullets(elememt, a):
    for bullet in p.bullets:
        if checkNotDamageCollision(bullet, a) and bullet != a and elememt in bullet.elements:
            return 1
deleted = input("Type 'delete' and then a number to delete the save of the cooresponding number: ").lower()
spritesForInventoryItems = {
    'NanotechRevolver'     : IMAGES['images/pistolInInventory.png'],
    'FerroSandShotgun'    : IMAGES['images/basicSpreadInInventory.png'],
    'Mandible'       : IMAGES['images/mandibleInInventory.png'],
    'chunkOfCactus'  : IMAGES['images/chunkOfCactus.png'],
    'wobbegongCloak' : IMAGES['images/wobbegongCloak.png'],
    'bagOfSand'      : IMAGES['images/bagOfSand.png'],
    'sandstone'      : IMAGES['images/sandstoneInInventory.png'],
    'desertWood'     : IMAGES['images/desertWoodInInventory.png'],
    'fossilFuel'     : IMAGES['images/fossilFuelInInventory.png'],
    'amethyst'       : IMAGES['images/amethystInInventory.png'],
    'bone'           : IMAGES['images/boneInInventory.png'],
    'shell'          : IMAGES['images/shellInInventory.png'],
    'ferroSand'      : IMAGES['images/ferroSand.png'],
    'ferroSteel'     : IMAGES['images/ferroSteel.png'],
    'desertWoodHelmet': IMAGES['images/desertWoodHelmetInInventory.png'],
    'desertWoodChestplate': IMAGES['images/desertWoodChestplateInInventory.png'],
    'desertWoodLeggings': IMAGES['images/desertWoodLeggingsInInventory.png'],
    'TheSpark': IMAGES['images/ferroSteel.png'],
}
deletedSave = False
for i in range(3):
    if f'delete{i + 1}' == deleted:
        saveDeleted = i + 1
        deletedSave = True
        try:
            with open(f'inventory{i + 1}.json', 'w') as inv:
                json.dump([['empty', 1, 1, 0, 0, None]] * 100, inv)
        except FileNotFoundError:
            pass
        try:
            with open(f'roomInfo{i + 1}', 'w') as roomInf:
                json.dump({}, roomInf)
        except FileNotFoundError:
            pass
        try:
            with open(f'biomes{i + 1}.json', 'w') as biomes:
                json.dump({}, biomes)
        except FileNotFoundError:
            pass

file = 0


theCraftingBox = CraftingBox()
mouseMarker = mouseMarker()

rooms = Rooms()
if deletedSave:
    rooms.rooms = [Room([0, 0], 'desert', 1)]
    rooms.roomCoordinates = [[0, 0]]
    rooms.makeRooms(16, 'desert')
    for room in rooms.rooms:
        room.saveCode = []
        for foe in room.foes:
            foe.saveCode = ''
        for teleporter in room.teleporters:
            teleporter.saveCode = ''
        for resource in room.destructibleMaterialSources:
            resource.saveCode = ''
p = Player()
if deletedSave:
    file = saveDeleted
    p.room = [0, 0, 0]
    p.saveCode = []
    p.inventory = []
    p.saveCode = []
    for number in range(100):
        p.inventory.append(Item(1, "empty"))
        p.emptySlots.append(Item(1, "empty"))
    p.save()
file = 0
p.startGame = 0
class menuButton:
    def __init__(self, image, left, top):
        self.image = image
        self.place = self.image.get_rect()
        self.place.left = left
        self.place.top = top
    def checkClick(self):
        if detectMouseCollision(self):
            return 1
        return 0
    def show(self):
        p.display.blit(self.image, self.place)
startButton = menuButton(IMAGES['images/startButton.png'], 767, 400)
exitButton = menuButton(IMAGES['images/exitButton.png'], 767, 600)
backButton = menuButton(IMAGES['images/backButton.png'], 767, 800)
for i in range(1, 4):
    exec(f'save{i}Button = menuButton(IMAGES["images/save{i}Button.png"], 767, {400 + 100 * i})')
file = 0
titleBackground = pygame.transform.scale(IMAGES['images/titleScreenBackground.png'], (1600, 900))
titleBackgroundPlace = titleBackground.get_rect()
titleBackgroundPlace.top = 0
titleBackgroundPlace.left = 0
p.menuScreen = 'titleScreen'
quit = 0
pygame.mouse.set_visible(False)

rooms.addDoors()
while not p.startGame:
    p.display.blit(titleBackground, titleBackgroundPlace)
    mouseMarker.update_position()
    p.display.blit(mouseMarker.sprite, mouseMarker.place)
    print(p.menuScreen)
    if p.menuScreen == 'titleScreen':
        startButton.show()
        exitButton.show()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.checkClick():
                    p.menuScreen = 'saveSelect'
                elif exitButton.checkClick():
                    sys.exit(1)
    elif p.menuScreen == 'saveSelect':
        for i in range(1, 4):
            exec(f'save{i}Button.show()')
        backButton.show()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(1, 4):
                    if eval(f'save{i}Button.checkClick()'):
                        file = i
                        p.startGame = 1
                if backButton.checkClick():
                    p.menuScreen = 'titleScreen'
    pygame.display.flip()
p.load(file)
while True:
    while p.hp > 1:

        if p.pause == 0 and p.inventoryShown == 0 and not p.mapShown:
            p.move()
            p.checkDroppedItemCollision()

            for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                if resource.hp < 1:
                    resource.drop_resources()

                    try:
                        coordinateToRoom(p.room)[1].destructibleMaterialSources.remove(resource)
                    except ValueError:
                        pass

            p.showHealthAndStaminaAndHeatAndCharge()
            p.useActiveItem()

            coordinateToRoom(p.room)[1].updateBullets()
            if len(coordinateToRoom(p.room)[1].foes) == 0:
                for i in coordinateToRoom(p.room)[1].teleporters:
                    if checkNotDamageCollision(i, p):
                        p.room = i.destinationCoordinate.copy()
                        p.center[0] = int(i.destinationCenterx)
                        p.center[1] = int(i.destinationCentery)
                        p.bullets = []
                        p.switchSong()
            for trap in coordinateToRoom(p.room)[1].traps:
                if checkNotDamageCollision(trap, p) == 1 and p.dashFramesRemaining <= 1:
                    coordinateToRoom(p.room)[1].traps.remove(trap)

                    if len(coordinateToRoom(p.room)[1].foes) == 0:
                        play('music/desertFight.mp3')

                    coordinateToRoom(p.room)[1].foes.append(Foe("antlion", trap.place.centerx, trap.place.centery))
                    coordinateToRoom(p.room)[1].antlions.append(coordinateToRoom(p.room)[1].foes[-1])
            for foe in coordinateToRoom(p.room)[1].ironAngels:
                foe.spreadShotAsIronAngel()

            for enemy in coordinateToRoom(p.room)[1].antlions:
                enemy.attackAsAntlion()
            for enemy in coordinateToRoom(p.room)[1].blobSummoners:
                enemy.summonAsBlobSummoner()
            for enemy in coordinateToRoom(p.room)[1].meleeBlobs:
                enemy.swingAsMeleeBlob()
            for bullet in p.bullets.copy():
                bullet.move()

                for material in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                    checkCollision(bullet, material)

                for foe in coordinateToRoom(p.room)[1].foes:
                    if foe.vulnerable == 1 and foe.hp > -5:
                        checkCollision(bullet, foe)
            for adversary in coordinateToRoom(p.room)[1].foes:
                if adversary.hp <= 0:
                    coordinateToRoom(p.room)[1].foes.remove(adversary)
                    for list in coordinateToRoom(p.room)[1].classlist:
                        try:
                            list.remove(adversary)
                        except ValueError:
                            pass
                    if len(coordinateToRoom(p.room)[1].foes) == 0:
                        p.switchSong()
                        coordinateToRoom(p.room)[1].cleared = 1
                    if adversary.healsOnKill:
                        p.healByKill()
                    p.loot(adversary.drops, adversary.place.centerx, adversary.place.centery)

                checkCollision(adversary, p)


                adversary.move()

            for adversary in coordinateToRoom(p.room)[1].foes:
                for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                    checkCollision(adversary, resource)

            for projectile in coordinateToRoom(p.room)[1].enemyBullets.copy():
                projectile.move()
                checkCollision(projectile, p)
            for projectile in coordinateToRoom(p.room)[1].enemyBullets:
                for material in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                    checkCollision(projectile, material)

            coordinateToRoom(p.room)[1].updateFoes()

            p.updateStats()
            p.hr = (keyboard.is_pressed('d') - keyboard.is_pressed('a')) * 10
            p.vr = (keyboard.is_pressed('s') - keyboard.is_pressed('w')) * 10
            p.animationFrame += 1
            p.invincibility -= 1

        if p.inventoryShown == 1:
            p.showInventory()
        p.detectInput()
        rooms.addDoors()
        blitEverything()
    p.hr = (keyboard.is_pressed('d') - keyboard.is_pressed('a')) * 10
    p.vr = (keyboard.is_pressed('s') - keyboard.is_pressed('w')) * 10
    p.hp = 130
    p.room = [0, 0, 0]
    rooms.addDoors()
    p.dashFramesRemaining = 0
    p.hp = 130
    p.place.centerx = 805
    p.place.centery = 450
    p.bullets = []
    p.animation = p.idleAnimation['s']
    p.undirectedAnimation = p.idleAnimation
    p.heatHarm = 0
    p.heat = 0
    p.dashFramesRemaining = 0
    p.slideFramesRemaning = 0
    p.song = None
    rooms.addDoors()
    play('music/desertCalm.mp3')
    for room in rooms.rooms:
        room.foes = []
        room.enemyBullets = []
        if not room.cleared:
            for code in room.deathLoadCode:
                print(code)
                exec(code)
        else:
            room.foes = []
    for i in range(16):
        for j in range(10):
            p.detectInput()
            p.display.fill((returnUnlessNegative(225 - 30 * i), returnUnlessNegative(225 - 30 * i), returnUnlessNegative(225 - 30 * i)))
            dthimg = IMAGES[f'images/newDeathAnim{i + 1}.png']
            dthimgplc = dthimg.get_rect()
            dthimgplc.centery = 450
            dthimgplc.centerx = 800
            p.display.blit(dthimg, dthimgplc)
            pygame.display.flip()
    for i in range(750):
        p.detectInput()
        pygame.display.flip()
    p.hr = (keyboard.is_pressed('d') - keyboard.is_pressed('a')) * 10
    p.vr = (keyboard.is_pressed('s') - keyboard.is_pressed('w')) * 10
