import sys
import pygame
import random
import json
import os
import math
import keyboard
gameSpeed = 1.5
IMPORTING = 0
from player import Player
from room import Room
from room import Room
from functions import defs
for i in defs:
    exec(f'from functions import {i}')
from version import VERSION
print(__file__[len(__file__) - (5 + len(str(VERSION))): len(__file__) - 3], 'rg79', VERSION)
# Import images
IMAGES = {}
for i in os.listdir("images"):
    if i not in ["font"]:
        IMAGES[f"images/{i}"] = pygame.image.load(f'images/{i}')

FONT = {}
for i in os.listdir("images/font"):
    FONT[i[-5].lower()] = pygame.image.load(f'images/font/{i}')

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

def getAngle(x, y):
    try:
        return math.acos(x / sqrt(x ** 2 + y ** 2)) * - sign(y) * 180 / math.pi
    except ZeroDivisionError:
        return random.randint(0, 360)
def getRadAngle(x, y):
    try:
        return math.acos(x / sqrt(x ** 2 + y ** 2)) * - sign(y)
    except ZeroDivisionError:
        return random.randint(0, 360)
def dis(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

class Bullet:
    def __init__(self, hr, vr, damage, firer, melee=0, linger=400,
                 sprite=None, piercing=0, centerx=None, centery=None,
                 knockback=(0, 0, 0), delay=0, positionCalculatedOnFire=1,
                 showWhileDelayed=1, elements=(), splash=0, mark=None,  specialEndEffect='',
                 specialEffects=(), specialEffectConditions=(), rotated=1, animation=None,
                 angle=None, hasRotatedHitbox=0, frameBasedScale = None, hitboxIsRotatedOrUnrotatedPlace=1):
        self.piercing = piercing
        self.hurtTargets = []
        self.specialEndEffect = specialEndEffect
        self.damage = damage
        self.elements = elements
        self.hitboxIsRotatedOrUnrotatedPlace = hitboxIsRotatedOrUnrotatedPlace
        self.frameBasedScale = frameBasedScale
        self.initialSprite = sprite
        if self.initialSprite is not None:
            self.initialPlace = self.initialSprite.get_rect()
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
        self.hasRotatedHitbox = hasRotatedHitbox
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
        self.angle = angle
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
        rotation = getAngle(self.hr, self.vr)

        self.center = [self.place.centerx, self.place.centery]
        if angle == None:
            self.hitbox = rectangle(self.place, rotation * math.pi / 180)
            self.sprite = pygame.transform.rotate(self.sprite, rotation)
        else:
            self.hitbox = rectangle(self.place, angle * math.pi / 180)
            self.sprite = pygame.transform.rotate(self.sprite, angle)
        self.currentDuration = 0



    def move(self):
        spearExplosion = []
        for i in range(1, 8):
            for j in range(2):
                spearExplosion.append(IMAGES[f'images/spearExplosion{i}.png'])
        if self.delay < 1:
            if self.melee and type(self.firer) == Foe:
                self.linger -= self.firer.totalSpeed * gameSpeed
            else:
                self.linger -= gameSpeed
            if self.linger <= 0:
                try:
                    self.firer.bullets.remove(self)
                    if type(self.firer) == Foe:
                        coordinateToRoom(p.room)[1].enemyBullets.remove(self)
                except ValueError:
                    pass
                exec(self.specialEndEffect)
            else:
                self.center[0] += self.hr * gameSpeed
                self.center[1] += self.vr * gameSpeed
            self.place.centerx, self.place.centery = self.center[0], self.center[1]
            formerPlace = self.place.copy()
            self.sprite = self.animation[floorIfPositive(self.frame)]
            self.currentDuration += 1
            self.frame += gameSpeed
            self.hitbox = rectangle(self.place.copy(), 0)
            if self.frameBasedScale is not None:
                self.sprite = pygame.transform.scale(self.sprite, (eval(self.frameBasedScale)))
                self.hitbox.scale(eval(self.frameBasedScale)[0], eval(self.frameBasedScale)[1])
            if self.rotated:
                if self.angle is not None:
                    self.sprite = pygame.transform.rotate(self.sprite, self.angle)
                    if self.hasRotatedHitbox:
                        self.hitbox.rotate(self.angle * math.pi / 180)
                else:
                    rotation = getAngle(self.hr, self.vr)
                    self.sprite = pygame.transform.rotate(self.sprite, rotation)
                    if self.hasRotatedHitbox:
                        self.hitbox.rotate(getRadAngle(self.hr, self.vr))
            self.place = self.sprite.get_rect(center=formerPlace.center)
            if self.frame >= len(self.animation):
                self.frame = 0
            if self.melee:
                if self.firer.place.top <= 0 and self.firer.vr < 0:
                    pass
                elif self.firer.place.bottom >= 900 and self.firer.vr > 0:
                    pass
                else:
                    self.center[1] += self.firer.vr * self.firer.speed * gameSpeed
                    self.hitbox.move(0, self.firer.vr * self.firer.speed * gameSpeed)

                if self.firer.place.left <= 0 and self.firer.hr < 0:
                    pass
                elif self.firer.place.right >= 1600 and self.firer.hr > 0:
                    pass
                else:
                    self.center[0] += self.firer.hr * self.firer.speed * gameSpeed
                    self.hitbox.move(self.firer.hr * self.firer.speed * gameSpeed, 0)
            self.place.centerx = self.center[0]
            self.place.centery = self.center[1]
            self.hitbox.move(self.place.centerx - self.hitbox.centerx, self.place.centery - self.hitbox.centery)
            for condition in self.specialEffectConditions:
                if eval(condition):
                    exec(self.specialEffects[self.specialEffectConditions.index(condition)])
            p.display.blit(self.sprite, self.place)
            if self.hitbox.right < 0 or self.hitbox.left > 1600 or self.hitbox.bottom < 0 or self.hitbox.top > 900:
                try:
                    self.firer.bullets.remove(self)
                    coordinateToRoom(p.room)[1].enemyBullets.remove(self)
                except ValueError:
                    pass
            if self.hitboxIsRotatedOrUnrotatedPlace:
                if self.rotated:
                    if self.angle != None:
                        self.hitbox = rectangle(self.place.copy(), self.angle * math.pi / 180)
                    else:
                        self.hitbox = rectangle(self.place, getAngle(self.hr, self.vr) * math.pi / 180)
        else:
            self.delay -= gameSpeed
            if self.positionCalculatedOnFire:
                self.center[0] += self.firer.hr * self.firer.speed * gameSpeed
                self.center[1] += self.firer.vr * self.firer.speed * gameSpeed
                if self.angle != None:
                    self.hitbox = rectangle(self.place.copy(), self.angle)
            if self.showWhileDelayed:
                p.display.blit(self.sprite, self.place)
class Item:
    def __init__(self, dropChance, type, qty=1, maxStackSize=1, dr=0, altAttackCharge=0, armorSlot=None, **kwargs):
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
            self.description = f'{self.type} is a material.'
        self.hitbox = rectangle(self.place, 0)
        for key in[key for key in kwargs.keys()]:
            exec(f'self.{key} = {kwargs[key]}')
class DroppedItem:
    def __init__(self, item, centerx, centery, maxStackSize=1, dr=0, altAttackCharge=0, armorSlot=None, **kwargs):
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
        self.hitbox = rectangle(self.place, 0)
        for key in [key for key in kwargs.keys()]:
            exec(f'self.{key} = {kwargs[key]}')
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
        self.hitbox = rectangle(self.place, 0)
class CraftingBox:
    def __init__(self):
        self.sprite = IMAGES['images/craftingBox.png']
        self.place = self.sprite.get_rect()
        self.place.centerx = 1390
        self.place.centery = 450
        self.hitbox = rectangle(self.place, 0)
frameNum = 0

class Foe:
    def __init__(self, kind, centerx, centery, **extraStats):
        self.fireCooldown          = 0
        self.knockbackAfflictions  = []
        self.hr                    = 0
        self.dr = 0
        self.markShatterCondition = '1 == 2'
        self.markShatterEffect = ''
        self.swingsBeforeWraithDash = 3
        self.healsOnKill = 1
        self.multifaced            = 0
        self.markEffect = ''
        self.vr                    = 0
        self.vulnerable            = 1
        self.hitboxIsPlace = 1
        self.wraithDashFrames = 0
        self.wobbegongDashCooldown = 120
        self.wobbegongDashing      = 0
        self.type                  = kind
        self.recentElementDamages = []
        self.bullets               = []
        self.drops                 = []
        self.markSprite = None
        self.wraithMode = ['range', 'melee'][random.randint(0, 1)]
        self.wraithModeFrames = random.randint(1000, 5000)
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
        elif self.type == 'wraith':
            self.hp = 40
            self.attack = 60
            self.drops = []
            self.sprite = IMAGES['images/wraithS.png']
            self.speed = 1
        if self.multifaced == 0:
            self.wsprite = self.sprite
            self.dsprite = self.sprite
            self.asprite = self.sprite
            self.ssprite = self.sprite
        else:
            if self.type == 'wobbegong':
                self.dsprite = IMAGES['images/wobbegong_d.png']
                self.ssprite = IMAGES['images/wobbegong_s.png']
                self.asprite = IMAGES['images/wobbegong_a.png']
                self.wsprite = IMAGES['images/wobbegong_w.png']
            elif self.type == 'wraith':
                self.dsprite = IMAGES['images/wraithD.png']
                self.ssprite = IMAGES['images/wraithS.png']
                self.asprite = IMAGES['images/wraithA.png']
                self.wsprite = IMAGES['images/wraithW.png']
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
        self.saveCode = f'room[coordinate].foes.append(Foe("{self.type}", {self.place.centerx}, {self.place.centery}))'
        self.deathLoadCode = f'room.foes.append(Foe("{self.type}", {self.place.centerx}, {self.place.centery}))'
        self.hitbox = rectangle(self.place.copy(), 0)
    def prepareToSave(self):
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
    def moveAsWraith(self):
        self.wraithDashFrames -= 1
        self.wraithModeFrames -= 1
        if self.wraithDashFrames <= 0:
            self.fireCooldown -= 1
            if self.wraithModeFrames <= 0:
                self.wraithModeFrames = random.randint(500, 1000)
                if self.wraithMode == 'range':
                    self.wraithMode = 'melee'
                else:
                    self.wraithMode = 'range'
            self.wraithMode = 'range'
            if self.wraithMode == 'melee':
                if getDistance(self, p) > 275:
                    self.hr = path(self, p)[0] * 0.5
                    self.vr = path(self, p)[1] * 0.5
                else:
                    self.hr = path(self, p)[0] * 0.16
                    self.vr = path(self, p)[1] * 0.16
                    if self.fireCooldown <= 0:
                        if self.swingsBeforeWraithDash > 0:
                            self.bullets.append(Bullet(path(self, p)[0] * 0.65, path(self, p)[1] * 0.65, 60, self, linger=100,
                                                       sprite=pygame.transform.scale(IMAGES['images/wraithSwing.png'], (37, 110))))
                            self.fireCooldown = 75
                            self.swingsBeforeWraithDash -= 1
                        else:
                            self.wraithDashFrames = 70
                            self.swingsBeforeWraithDash = 3
            else:
                self.hr = 0
                self.vr = 0
                if self.fireCooldown <= 0:
                    self.bullets.append(Bullet(0, 0, 0, self, linger=10, sprite=pygame.transform.scale(IMAGES['images/wraithShot.png'], (50, 50)), centery=self.place.centery + 40, rotated=0))
                    self.bullets.append(Bullet(0, 0, 75, self, linger=15, sprite=pygame.transform.scale(IMAGES['images/wraithShot.png'], (1836, 5)), delay=25, angle=getAngle(path(self, p)[0], path(self, p)[1]), hasRotatedHitbox=1, centerx=self.place.centerx + 800 * (p.place.centerx - self.place.centerx) / getDistance(self, p), centery=self.place.centery + 800 * (p.place.centery - self.place.centery) / getDistance(self, p)))
                    self.fireCooldown = 50
        elif self.wraithDashFrames > 50:
            self.hr = 0
            self.vr = 0
        elif self.wraithDashFrames > 48:
            self.hr = path(self, p)[0] * (getDistance(self, p) / 400)
            self.vr = path(self, p)[1] * (getDistance(self, p) / 400)

    def updateStats(self):
        self.speed = 1

        self.totalSpeed = 1
        self.dr = 0
        exec(self.markEffect)
        if eval(self.markShatterCondition):
            exec(self.markShatterEffect)
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
                self.wobbegongDashCooldown -=   gameSpeed

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
            elif self.type == 'wraith':
                self.moveAsWraith()
            self.center[0] += self.hr * self.speed * self.totalSpeed * gameSpeed
            self.center[1] += self.vr * self.speed * self.totalSpeed * gameSpeed
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
                    if not self.hitboxIsPlace:
                        self.hitbox = rectangle(self.place.copy(), 0)
                    self.place.centery = self.center[1]
                    self.place.centerx = self.center[0]

            self.sprite = self.directionalSprites[getDirection(self.hr, self.vr)]

            if self.place.left <= 0:
                self.place.left = 0
                self.wraithDashFrames = 0
            elif self.place.right >= 1600:
                self.place.right = 1600
                self.wraithDashFrames = 0
            if self.place.top <= 0:
                self.place.top = 0
                self.wraithDashFrames = 0
            elif self.place.bottom >= 900:
                self.place.bottom = 900
                self.wraithDashFrames = 0
            if self.hitbox.left <= 0:
                self.hitbox.move(-self.hitbox.left, 0)
            elif self.hitbox.right >= 1600:
                self.hitbox.move(1600 - self.hitbox.right, 0)
            if self.hitbox.top <= 0:
                self.hitbox.move(0, -self.hitbox.top)
            elif self.hitbox.bottom >= 900:
                self.hitbox.move(0, 900 - self.hitbox.bottom)
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
                    self.center[0] += i[0] * gameSpeed
                    self.center[1] += i[1] * gameSpeed
                    self.hitbox.move(i[0] * gameSpeed, i[1] * gameSpeed)
                    i[2] -= 1 * gameSpeed
        if self.hitboxIsPlace:
            self.hitbox = rectangle(self.place, 0)
        p.display.blit(self.sprite, self.place)

    def fireStraight(self, target): # Not used in this class
        self.bullets.append(Bullet(path(self, target)[0] * self.totalSpeed, path(self, target)[1] * self.totalSpeed, 34, self))
    def swingAsMeleeBlob(self):
        if self.fireCooldown < 1:
            self.bullets.append(Bullet(path(self, p)[0] * self.totalSpeed / 3, path(self, p)[1] * self.totalSpeed / 3, 75, self, linger=60, sprite=IMAGES['images/playerMelee.png']))
            self.fireCooldown = random.randint(100, 150)
        self.fireCooldown -= self.totalSpeed * gameSpeed
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
        self.fireCooldown -= self.totalSpeed * gameSpeed

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
        self.antlionPause -= self.totalSpeed * gameSpeed
        self.attack = 0
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

                self.bullets.append(Bullet(0, 0, 100, self, melee=1, linger = 65, centery=self.place.centery + 30, angle=getAngle(p.hitbox.centerx - self.hitbox.centerx, p.hitbox.centery - self.hitbox.centery), delay=10))

                for i in range(2):
                    self.bullets.append(
                        Bullet(semirandomPath(self, p)[0] * self.totalSpeed,
                        semirandomPath(self, p)[1] * self.totalSpeed,
                        100, self, linger=150, delay=10
                    ))
        self.hitbox = rectangle(self.place, 0)

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
            self.fireCooldown -= self.totalSpeed * gameSpeed

class mouseMarker:
    def __init__(self):
        self.sprite = IMAGES['images/mouseMarkerTarget2.png']
        self.place = self.sprite.get_rect()

    def update_position(self):
        self.place.centerx, self.place.centery = pygame.mouse.get_pos()[:2]

class PitTrap:
    def __init__(self, centerx, centery):
        self.attack = 34

        self.sprite = IMAGES['images/lionPit.png']

        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.saveCode = f'room.traps.append(PitTrap(self.place.centerx, self.place.centery))'
        self.hitbox = rectangle(self.place, 0)
class Rooms:
    def __init__(self):
        self.rooms = [Room([0, 0], "desert", 1, 1)]
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

            self.rooms.append(Room(room, biome, number, 1))
            self.roomCoordinates.append(room)
        for room in self.rooms:
            if room.coordinate[2] == 0 and int(room.num / 6) == room.num / 6:
                newShelter = Room(room.coordinate[0: 2], 'desert', 6, 1, depth=1)
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
            if len([coolZone for coolZone in zone if coolZone.background == 'images/shelterBackgroundBMP.bmp']) == 0 and not self.sortListOfRooms(zone) in Liszt:
                Liszt.append(self.sortListOfRooms(zone))
        Liszt = Liszt.copy()
        for zone in Liszt:
                shelterYCoords = [loaction.coordinate[1] for loaction in zone]
                topShelter = max(shelterYCoords)
                topShelter = zone[shelterYCoords.index(topShelter)]
                topShelter.background = 'images/shelterBackgroundBMP.bmp'
                topShelter.teleporters.append(teleporter(topShelter.coordinate, 800, 50, topShelter.coordinate[0: 2] + [0], 805,
                                                  750, str('images/invisibleTeleporter35X80.png')))

                topShelter.foes = []
                topShelter.traps = []
                topShelter.destructibleMaterialSources = []
                for location in zone:
                    if location != topShelter:
                        location.background = 'images/altShelterBackgroundBMP.bmp'
                        location.teleporters = []

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
        if abs(self.centerx - pygame.mouse.get_pos()[0]) < self.totalWidth / 2 and abs(
                self.centery - pygame.mouse.get_pos()[1]) < 7:
            return 1
        else:
            return 0
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
        self.hitbox = rectangle(self.place, 0)
        if self.type == 'desertTree':
            self.hitbox = rectangle(pygame.Rect(self.place.left, self.place.top + 151, self.place.width, self.place.height - 151), 0)
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
def getGreater(a, b):
    return a if a > b else b
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
    return int(num // 1) if num > 0 else 0

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
def checkCollision(a, b):
    if a.hitbox.checkCollisionWithRect(b.hitbox):
            if p.invincibility <= 0:
                if type(a) == Bullet and b == p:
                    pass
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
                    if not b in a.hurtTargets:
                        if a.splash > 0:
                            for foe in [enemy for enemy in coordinateToRoom(p.room)[1].foes if getDistance(a, enemy) < a.splash * 75]:
                                foe.hp -= a.splash - getDistance(a, foe) / 75
                        try:
                            if not a.melee:
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
    if a.hitbox.checkCollisionWithRect(b.hitbox):
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
    p.display.blit(p.sprite, p.place)
    for i in coordinateToRoom(p.room)[1].enemyBullets:
        if i.delay < 1:
            p.display.blit(i.sprite, i.place)
    for i in p.bullets:
        if i.delay < 1:
            p.display.blit(i.sprite, i.place)
    for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
        p.display.blit(resource.sprite, resource.place)
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

    pygame.display.flip()
from rectangles import rectangle
play('music/Desert overground base.mp3')
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
    'TheSpark': IMAGES['images/theSparkInInventory.png'],
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
    rooms.rooms = [Room([0, 0], 'desert', 1, 1)]
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
def checkCollisionWithAllFoes(a):
    for foe in coordinateToRoom(p.room)[1].foes:
        if checkNotDamageCollision(a, foe):
            return 1
    return 0
while not p.startGame:
    p.display.blit(titleBackground, titleBackgroundPlace)
    mouseMarker.update_position()
    p.display.blit(mouseMarker.sprite, mouseMarker.place)
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
    try:
        while p.hp > 1:
            frameNum += 1
            if p.pause == 0 and p.inventoryShown == 0 and not p.mapShown:
                p.move()
                p.checkDroppedItemCollision()
                print(vars(coordinateToRoom(p.room)[1]))
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
                if int(frameNum / 1) == frameNum / 1:
                    for bullet in p.bullets.copy():
                        for material in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                            checkCollision(bullet, material)
                        for foe in coordinateToRoom(p.room)[1].foes:
                            if foe.vulnerable == 1 and foe.hp > -5:
                                checkCollision(bullet, foe)
                    for trap in coordinateToRoom(p.room)[1].traps:
                        if checkNotDamageCollision(trap, p) and p.dashFramesRemaining <= 1:
                            coordinateToRoom(p.room)[1].traps.remove(trap)

                            if len(coordinateToRoom(p.room)[1].foes) == 0:
                                play('music/desertFight.mp3')

                            coordinateToRoom(p.room)[1].foes.append(Foe("antlion", trap.place.centerx, trap.place.centery))
                            coordinateToRoom(p.room)[1].antlions.append(coordinateToRoom(p.room)[1].foes[-1])
                    p.checkDroppedItemCollision()

                    for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                        if resource.hp < 1:
                            resource.drop_resources()

                            try:
                                coordinateToRoom(p.room)[1].destructibleMaterialSources.remove(resource)
                            except ValueError:
                                pass
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



                    for adversary in coordinateToRoom(p.room)[1].foes:
                        for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                            checkCollision(adversary, resource)

                    for projectile in coordinateToRoom(p.room)[1].enemyBullets:
                        checkCollision(projectile, p)
                        for material in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                            checkCollision(projectile, material)
                for foe in coordinateToRoom(p.room)[1].foes:
                    foe.move()
                for i in coordinateToRoom(p.room)[1].enemyBullets:
                    i.move()
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
        play('music/Desert overground base.mp3')
        for room in rooms.rooms:
            room.foes = []
            room.enemyBullets = []
            if not room.cleared:
                for code in room.deathLoadCode:
                    try:
                        exec(code)
                    except NameError:
                        print(code)
            else:
                room.foes = []
            room.foes = [Foe('wraith', 100, 100)]
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
        p.save()
    except AttributeError:
        raise AttributeError