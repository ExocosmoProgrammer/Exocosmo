import pygame
import random
import json
import os
import  math
def sqrt(a):
    return a ** .5
# Import images
IMAGES = {}
for i in os.listdir("images"):
    if i not in ["font"]:
        IMAGES[f"images/{i}"] = pygame.image.load(f'images/{i}')

FONT = {}
for i in os.listdir("images/font"):
    FONT[i[-5].lower()] = pygame.image.load(f'images/font/{i}')
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
def getAngle(x, y):
    try:
        return math.acos(x / sqrt(x ** 2 + y ** 2)) * - sign(y) * 180 / math.pi
    except ZeroDivisionError:
        return random.randint(0, 360)
class Bullet:
    def __init__(self, hr, vr, damage, firer, melee=0, linger=400, sprite=None, piercing=0, centerx=None, centery=None, knockback=(0, 0, 0), delay=0, positionCalculatedOnFire=1, showWhileDelayed = 1):
        self.piercing = piercing
        self.hurtTargets = []
        self.damage = damage
        self.linger = linger
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
            elif p.inventory[p.activeItem].type == "BasicRange":
                self.sprite = IMAGES['images/playerProjectile.png']
            elif p.inventory[p.activeItem].type == "BasicSpread":
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

        self.center = [self.place.centerx, self.place.centery]
        self.sprite = pygame.transform.rotate(self.sprite, getAngle(self.hr, self.vr))
    def move(self):
        if self.delay < 1:
            self.linger -= 1

            if self.linger < 1:
                try:
                    self.firer.bullets.remove(self)
                    if type(self.firer) == Foe:
                        coordinateToRoom(p.room)[1].enemyBullets.remove(self)
                except ValueError:
                    pass

            else:
                self.center[0] += self.hr
                self.center[1] += self.vr

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
            p.display.blit(self.sprite, self.place)

        else:
            self.delay -= 1
            if self.positionCalculatedOnFire:
                self.center[0] += self.firer.hr * self.firer.speed
                self.center[1] += self.firer.vr * self.firer.speed
            if self.showWhileDelayed:
                p.display.blit(self.sprite, self.place)
class Item:
    def __init__(self, dropChance, type, qty=1, maxStackSize=1, dr=0):
        self.dropChance = dropChance
        self.type = type
        self.dragged = 0
        self.qty = qty
        self.stackSize = maxStackSize
        self.dr = dr
        try:
            self.sprite = spritesForInventoryItems[self.type]
        except KeyError:
            self.sprite = IMAGES['images/playerProjectile.png']
        self.place = self.sprite.get_rect()

class DroppedItem:
    def __init__(self, item, centerx, centery, maxStackSize=1):
        self.item = item
        self.stackSize = maxStackSize

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
                self.totalWidth += FONT[letter].get_rect().width

        def write(self):
            left = self.place.left
            for letter in self.word:
                self.recipient.display.blit(FONT[letter], pygame.Rect(left, self.place.top, FONT[letter].get_rect().width, FONT[letter].get_rect().height))
                left += FONT[letter].get_rect().width

        def checkMouseCollision(self):
            if abs(self.centerx - pygame.mouse.get_pos()[0]) < self.totalWidth / 2 and abs(self.centery - pygame.mouse.get_pos()[1]) < 7:
                return 1
            else:
                return 0
class teleporter:
    def __init__(self, coordinate, centerx, centery, destinationCoordinate, destinationCenterx, destinationCentery, sprite):
        self.coordinate = coordinate
        self.sprite = sprite
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.destinationCoordinate = destinationCoordinate
        self.destinationCenterx = destinationCenterx
        self.destinationCentery = destinationCentery
        self.initialDestinationCenterx = self.destinationCenterx
        self.initialDestinationCentery = self.destinationCentery
        self.initialDestinationCoordinate = self.destinationCoordinate
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
        self.place.bottom = 450
        self.place.left   = 805
        self.heatGain = 3
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
        self.recipes = {
            ('sandstone',): (Item(0, 'bagOfSand'),),
            tuple(['desertWood'] * 10): (Item(0, 'desertWoodHelmet', dr=5),),
            tuple(['desertWood'] * 20): (Item(0, 'desertWoodChestplate', dr=15),),
            tuple(['desertWood'] * 15): (Item(0, 'desertWoodLeggings', dr=10),),
        }
        self.walkingAnimation    = {'w': [], 'a': [], 's': [], 'd': []}
        self.craftButton         = Word('craft', 1355, 650, self)
        self.display             = pygame.display.set_mode((1600, 900))

        self.idleAnimation = {
            'd': [IMAGES['images/walkingAnimation_d1.png']],
            'w': [IMAGES['images/walkingAnimation_w1.png']],
            'a': [IMAGES['images/walkingAnimation_a1.png']],
            's': [IMAGES['images/walkingAnimation_s1.png']]
        }

        # Load walking animation sprites
        for i in range(1, 5):
            for o in range(20):
                self.walkingAnimation['w'].append(pygame.image.load(f'images/walkingAnimation_w{i}.png'))
                self.walkingAnimation['a'].append(pygame.image.load(f'images/walkingAnimation_a{i}.png'))
                self.walkingAnimation['s'].append(pygame.image.load(f'images/walkingAnimation_s{i}.png'))
                self.walkingAnimation['d'].append(pygame.image.load(f'images/walkingAnimation_d{i}.png'))

        try:
            self.load(file)
        except:
            self.inventory = []
            for number in range(100):
                self.inventory.append(Item(1, "empty"))
                self.emptySlots.append(Item(1, "empty"))

        self.animation = self.idleAnimation[self.direction]
        self.undirectedAnimation = self.idleAnimation

        for i in range(8):
            self.hotbar[i + 1] = "empty"
        self.updateStats()

    def dropItem(self, item):
        for i in range(item.qty):
            coordinateToRoom(self.room)[1].droppedItems.append(DroppedItem(item.type, self.place.centerx, self.place.centery, maxStackSize=item.stackSize))
    def getQtyOfFoeTypeInRoom(self, type):
        qty = 0
        for foe in coordinateToRoom(self.room)[1].foes:
            if foe.type == type:
                qty += 1
        return qty
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
            try:
                self.inventory[self.inventory.index(item)] = Item(0, 'empty')
            except ValueError:
                pass
            if item.type != 'empty':
                try:
                    self.inventory[self.inventory.index(self.emptySlots[0])] = item
                except IndexError:
                    self.dropItem(item)
            self.updateStats()

    def save(self, file):
        try:
            inventory = open(f'inventory{file}.json', "x")
        except FileExistsError:
            inventory = open(f'inventory{file}.json', "w")

        items = []
        for item in self.inventory:
            items.append([item.type, item.qty, item.stackSize])

        json.dump(items, inventory)
        inventory.close()

    def load(self, file):
        with open(f'inventory{file}.json', "r") as inventory:
            storage = json.load(inventory)
            self.inventory = [Item(100, i[0], qty=i[1], maxStackSize=i[2]) for i in storage]

        self.dashFramesRemaining  = 0
        self.hp                    = 130
        self.place.centerx         = 805
        self.place.centery         = 450
        self.bullets               = []
        self.room                  = [0, 0, 0]
        self.animation             = self.idleAnimation['s']
        self.undirectedAnimation   = self.idleAnimation
        self.heatHarm = 0
        self.heat = 0

        play('music/desertCalm.mp3')

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
                self.inventory[self.inventory.index(self.emptySlots[0])] = Item(item.dropChance, item.type, qty=item.qty, maxStackSize=item.stackSize)
                item.qty = 0
                self.emptySlots.pop(0)
            else:
                self.updateStats()
                coordinateToRoom(self.room)[1].droppedItems.append(DroppedItem(item.type, centerx, centery, maxStackSize=item.stackSize))
                item.qty -= 1

        self.updateStats()

    def loot(self, items, centerx, centery):
        for item in items:
            if not type(item) == None:
                if random.randint(1, 100) <= item.dropChance:
                    self.addItemToInventory(item, centerx, centery)
                    self.updateStats()

    def animationSwap(self, animation, direction):
        self.animation = animation[direction]
        self.undirectedAnimation = animation
        self.animationFrame = 0

    def turn(self, direction):
        self.animation = self.undirectedAnimation[direction]

    def checkDroppedItemCollision(self):
        for item in coordinateToRoom(self.room)[1].droppedItems:
            if checkNotDamageCollision(self, item):
                self.addItemToInventory(Item(0, item.item, maxStackSize=item.stackSize), item.place.centerx, item.place.centery)

                try:
                    coordinateToRoom(self.room)[1].droppedItems.remove(item)
                except ValueError:
                    pass

    def updateStats(self):
        self.dr = 0
        try:
            try:
                exec(coordinateToRoom(self.room)[1].defaultHeatEffect)
            except NameError:
                self.heatGain = 0
        except TypeError:
            pass
        self.heat += self.heatGain
        self.heat = 0
        self.speed               = 0.46
        self.dashFramesRemaining -= 1
        self.staminaRegenRate    = 1.5
        if abs(self.heat) < 300:
            if self.heatHarm > 0.3:
                self.heatHarm -= 0.3
            else:
                self.heatHarm = 0
        if 1200 < abs(self.heat):
            self.heatHarm += 0.1
        if 1800 < abs(self.heat):
            self.hp -= 0.03
            self.heatHarm += 0.1
        if 2400 < abs(self.heat):
            self.hp -= 0.06
            self.heatHarm += 0.3
        if self.heatHarm > 600:
            self.hp = 0
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
            self.inventory[0] = Item(0, 'BasicRange')
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
        for i in range(3):
            self.dr += self.inventory[i + 37].dr
        self.save(file)

    def detectInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS and self.inventoryShown:
                    for item in self.inventory:
                        if item.dragged:
                            coordinateToRoom(p.room)[1].droppedItems.append(DroppedItem(item.type, 800, 450, maxStackSize=item.stackSize))
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

                if event.key == pygame.K_l:
                    self.inventoryShown = not self.inventoryShown

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.dash()

                if event.key == pygame.K_TAB or pygame.key.get_mods() & pygame.KMOD_CTRL or pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.slide()

                for i in range(10):
                    exec(f"if event.key == pygame.K_{i}: self.activeItem = {i}")

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
                self.firing = 1
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
                            for item in self.inventory:
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
            if event.type == pygame.MOUSEBUTTONUP:
                self.firing = 0

    def switchSong(self):
        if coordinateToRoom(self.room)[1].biome == "desert" and self.room[2] == 0:
            if len(coordinateToRoom(self.room)[1].foes) > 0:
                play('music/desertFight.mp3')
            else:
                play('music/desertCalm.mp3')
        elif self.room[2] == 100:
            play('music/shelter.mp3')
    def checkForAccessory(self, item_type):
        return item_type in [i.type for i in self.accessories]

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
        self.display.blit(armorSlotMarker.sprite, armorSlotMarker.place)
        self.display.blit(helmetSlotMarker.sprite, helmetSlotMarker.place)
        self.display.blit(leggingsSlotMarker.sprite, leggingsSlotMarker.place)
        for item in self.inventory:
            if item.type != 'empty':
                self.display.blit(item.sprite, item.place)
                if item.qty > 1:
                    word = Word(str(item.qty), item.place.centerx, item.place.centery, self)
                    word.write()

    def showHealthAndStamina(self):
        # Display bar
        hpBarSprite = IMAGES['images/healthBar.png'].get_rect()
        hpBarSprite.x += 10
        p.display.blit(
            IMAGES['images/healthBar.png'],
            hpBarSprite
        )

        # HP
        self.display.fill("#cd300e", pygame.Rect(41, 30, self.hp * 130 / self.maxHP, 18))

        # Stamina
        self.display.fill("#351c75", pygame.Rect(41, 89, 96 - 96 * returnUnlessNegative(self.stamina) / 315, 14))

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
                    if self.dashFramesRemaining < 1:
                        self.center[0] -= self.hr * 0.14
                    else:
                        self.center[0] -= self.hrWhileDashing * 0.14
                    self.place.centerx = self.center[0]
                if self.place.left < material.place.right and self.place.right > material.place.left:
                    if self.dashFramesRemaining < 1:
                            self.center[1] -= self.vr * 0.14
                    else:
                        self.center[1] -= self.vrWhileDashing * 0.14
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
                self.center[1] = self.place.height / 2
                self.center[0] = 800
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
            else:
                self.center[1] = 900 - self.place.height / 2

        if self.center[0] - self.place.width / 2 < 0:
            if [self.room[0] - 1, self.room[1], self.room[2]] in rooms.roomCoordinates and coordinateToRoom(self.room)[1].foes == [] and 400 < self.center[1] < 500:
                coordinateToRoom(self.room)[1].enemyBullets = []
                self.room[0] -= 1
                self.center[0] = 1600 - self.place.width / 2
                self.bullets = []
                self.center[1] = 450
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
            else:
                self.center[0] = self.place.width / 2

        if self.center[1] - self.place.height / 2 < 0:
            if [self.room[0], self.room[1] + 1, self.room[2]] in rooms.roomCoordinates and coordinateToRoom(self.room)[1].foes == [] and 750 < self.center[0] < 850:
                coordinateToRoom(self.room)[1].enemyBullets = []
                self.room[1] += 1
                self.center[1] = 900 - self.place.height / 2
                self.center[0] = 800
                self.bullets = []
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
            else:
                self.center[1] = self.place.height / 2

        if self.place.center[0] + self.place.width / 2 > 1600:
            if [self.room[0] + 1, self.room[1], self.room[2]] in rooms.roomCoordinates and coordinateToRoom(self.room)[1].foes == [] and 400 < self.center[1] < 500:
                coordinateToRoom(self.room)[1].enemyBullets = []
                self.room[0] += 1
                self.center[0] = self.place.width / 2
                self.center[1] = 450
                self.bullets = []
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
            else:
                self.center[0] = 1600 - self.place.width / 2

        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]
    def useBasicRange(self):
        if self.inventory[self.activeItem].type == "BasicRange":
            if self.fireCooldown < 1 and self.firing == 1:
                pathx = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0] * 3
                pathy = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1] * 3
                self.fireCooldown = 20

                self.bullets.append(Bullet(
                    pathx * 10,
                    pathy * 10,
                    2, self,
                    sprite=IMAGES['images/basicRangeProjectile_d.png']))
    def useBasicSpread(self):
        if self.fireCooldown < 1:
            for number in range(7):
                self.fireSemirandomNoAttack(1.2)
            self.fireCooldown = 30
    def useActiveItem(self):
        if self.firing == 1 and self.fireCooldown < 1 and self.dashFramesRemaining < 1 and self.slideFramesRemaning < 1:
            try:
                exec(f'self.use{self.inventory[self.activeItem].type}()')
            except AttributeError:
                pass
        self.fireCooldown -= 1

    def fireSemirandomNoAttack(self, damage):
        player_pos = [self.place.centerx, self.place.centery]
        mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        pathx = semirandomPathWithoutPlace(player_pos, mouse_pos)[0] * 8
        pathy = semirandomPathWithoutPlace(player_pos, mouse_pos)[1] * 8
        self.bullets.append(Bullet(
            pathx, pathy,damage, self, sprite=IMAGES['images/basicSpreadProjectile_d.png']))

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
    def __init__(self, kind, centerx, centery):
        self.fireCooldown          = 0
        self.knockbackAfflictions  = []
        self.hr                    = 0
        self.dr = 0
        self.healsOnKill = 1
        self.multifaced            = 0
        self.vr                    = 0
        self.vulnerable            = 1
        self.wobbegongDashCooldown = 120
        self.wobbegongDashing      = 0
        self.type                  = kind
        self.bullets               = []
        self.drops                 = []

        if self.type == "antlion":
            self.attack       = 0
            self.hp           = 100
            self.speed        = 0
            self.vulnerable   = 0
            self.antlionPause = random.randint(15, 70)
            self.drops        = [Item(3, "Mandible")]
            self.sprites      = [IMAGES['images/antlion.png'], IMAGES['images/activeLionPit.png']]
            self.sprite       = IMAGES['images/activeLionPit.png']
            self.dr = 0

        elif self.type == "ironAngel":
            self.sprite = IMAGES['images/ironAngel.png']
            self.hp = 100
            self.attack = 40
            self.speed = 0
            self.drops = [Item(1, "BasicSpread"), Item(100, 'ferroSand', qty=random.randint(1, 2), maxStackSize=99),
                          Item(100, 'ferroSteel', qty=random.randint(1, 2), maxStackSize=99)]
            self.dr = 0

        elif self.type == "wobbegong":
            self.sprite = IMAGES['images/wobbegong_a.png']
            self.hp = 100
            self.attack = 50
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
    def move(self):
        if self.type != 'antlion':
            if self.type == "wobbegong":
                if not self.wobbegongDashing:
                    self.hr = path(self, p)[0] * 0.2
                    self.vr = path(self, p)[1] * 0.2
                    if self.wobbegongDashCooldown < 1:
                        self.hr = path(self, p)[0] * 0.5
                        self.vr = path(self, p)[1] * 0.5
                        self.wobbegongDashing = 1
                        self.wobbegongDashCooldown = random.randint(120, 240)
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
            self.center[0] += self.hr
            self.center[1] += self.vr
            self.place.centerx = self.center[0]
            self.place.centery = self.center[1]

            for material in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                while checkCollision(self, material) == 1:
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
                    self.place.x += i[0]
                    self.place.y += i[1]
                    i[2] -= 1
        p.display.blit(self.sprite, self.place)

    def fireStraight(self, target): # Not used in this class
        self.bullets.append(Bullet(path(self, target)[0], path(self, target)[1], 34, self))
    def swingAsMeleeBlob(self):
        if self.fireCooldown < 1:
            self.bullets.append(Bullet(path(self, p)[0] / 3, path(self, p)[1] / 3, 75, self, linger=60, sprite=IMAGES['images/playerMelee.png']))
            self.fireCooldown = random.randint(100, 150)
        self.fireCooldown -= 1
    def summonAsBlobSummoner(self):
        if self.fireCooldown < 1:
            if p.getQtyOfFoeTypeInRoom('blobSummon') < 40:
                for number in range(15):
                    coordinateToRoom(p.room)[1].foes.append(Foe('blobSummon', p.place.centerx + random.randint(-400, 400), p.place.centery + random.randint(-400, 400)))
                self.fireCooldown = random.randint(300, 350)
            else:
                for number in range(15):
                    newBulletCenter = [p.place.centerx + random.randint(-400, 400), p.place.centery + random.randint(-400, 400)]
                    self.bullets.append(Bullet(pathWithoutPlaceAttribute(newBulletCenter, p.center)[0] * 5,
                                               pathWithoutPlaceAttribute(newBulletCenter, p.center)[1] * 5,
                                               65, self, sprite=IMAGES['images/IAP.png'],
                                               centerx=newBulletCenter[0], centery=newBulletCenter[1],
                                               delay=random.randint(200, 250), positionCalculatedOnFire=0))
                self.fireCooldown = random.randint(200, 250)
        self.fireCooldown -= 1

    def fireStraightToPoint(self, point): # Not used in this class
        self.bullets.append(Bullet(
            pathWithoutPlaceAttribute(self.center, point)[0],
            pathWithoutPlaceAttribute(self.center, point)[1], 34, self
        ))

    def spreadShotAsWobbegong(self):
        if self.type == 'wobbegong':
            for number in range(7):
                self.fireSemirandom(p, 0)

    def attackAsAntlion(self):
        self.antlionPause -= 1

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

                self.bullets.append(Bullet(0, 0, 40, self, melee=1, linger = 65, centery=self.place.centery + 30))

                for i in range(2):
                    self.bullets.append(
                        Bullet(semirandomPath(self, p)[0],
                        semirandomPath(self, p)[1],
                        40, self, linger=150
                    ))

    def firePredictivelyAsLobster(self): # Not used in this class
        self.fireCooldown -= 1

        if -100 <self.fireCooldown < 1:
            self.firePredictivelyToPlayer(12)

        if self.fireCooldown < -100:
            self.fireCooldown = 60

    def firePredictivelyToPlayer(self, speed):
        self.bullets.append(Bullet(
            predictivePathToPlayer(self, speed)[0],
            predictivePathToPlayer(self, speed)[1],
            35, self, sprite=IMAGES['images/ironAngelProjectile.png']
        ))

    def fireSemirandom(self, target, delay):
        self.bullets.append(Bullet(
            semirandomPath(self, target)[0] * 1.5,
            semirandomPath(self, target)[1] * 1.5,
            34, self, delay=delay
        ))

    def spreadShotAsIronAngel(self):
        if self.fireCooldown < 1:
            self.fireCooldown = 130
            for i in range(9):
                self.fireSemirandom(p, 0)
        else:
            self.fireCooldown -= 1

class MouseMarkerTarget:
    def __init__(self):
        self.sprite = IMAGES['images/mouseMarkerTarget.png']
        self.place = self.sprite.get_rect()

    def update_position(self):
        self.place.centerx, self.place.centery = pygame.mouse.get_pos()[:2]

class Room:
    def __init__(self, coordinate, biome, num, depth=0):
        self.biome = biome
        if depth == 100:
            self.shelterZone = [self]
        self.teleporters = []
        self.coordinate = [coordinate[0], coordinate[1], depth]
        if self.biome == 'desert' and self.coordinate[2] == 0:
            self.defaultHeatEffect = 'self.heat += 3'
            self.layout = random.randint(1, 4)
            self.foe_types = ['ironAngel', 'wobbegong', 'antlion']
            self.background = IMAGES['images/desertBackground.bmp']
            self.potentialMaterialSources = [DestructableMaterialSource(80, 450, 'sandstone', IMAGES['images/sandstone3.png'], 2000, random.randint(2, 3)),
                                            DestructableMaterialSource(80, 450, 'desertWood', IMAGES['images/desertTree2.png'], 2000, random.randint(2, 3)),
                                             DestructableMaterialSource(80, 450, 'fossilFuel', IMAGES['images/fossilFuel2.png'], 2000, random.randint(2, 3)),
                                             DestructableMaterialSource(80, 450, 'bone', IMAGES['images/skeleton2.png'], 2000, random.randint(2, 3)),
                                             DestructableMaterialSource(80, 450, 'amethyst', IMAGES['images/amethyst2.png'], 2000, random.randint(2, 3)),
                                             DestructableMaterialSource(80, 450, 'shell', IMAGES['images/shellPile2.png'], 2000, random.randint(2, 3)),
                                             DestructableMaterialSource(80, 450, 'chunkOfCactus', IMAGES['images/destructibleCactus3.png'], 200, random.randint(2, 3)),
                                             ]
        if self.coordinate[2] == 100:
            self.background = IMAGES['images/altShelterBackground.png']
            self.defaultHeatEffect = 'self.heat = 0'
            self.layout = 7
            self.foe_types = ['blobSummoner', 'meleeBlob', 'blobSummon']
        self.destructibleMaterialSources = []
        self.difficulty = random.randint(0, 5)
        self.resources = random.randint(0, 3 + floorIfPositive(self.difficulty / 2))
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

        self.potentialPitsX = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
        self.potentialPitsY = [50, 850, 450, 300, 600, 600, 300, 50, 850]

        try:
            if type(coordinateToRoom([coordinate[0], coordinate[1], 0])) == tuple and depth:
                self.biome = coordinateToRoom([coordinate[0], coordinate[1], 0])[1].biome
        except NameError:
            pass



        self.background_location = self.background.get_rect()
        self.background_location.centerx = 800
        self.background_location.centery = 450


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
        if self.coordinate != [0, 0, 0] and self.coordinate[2] != 100:
            for number in range(self.resources):
                for i in range(1000):
                    newMaterialSourceLocation = [random.randint(200, 1400), random.randint(200, 700)]
                    newMaterialSourceType = self.potentialMaterialSources[random.randint(0, len(self.potentialMaterialSources) - 1)]
                    self.destructibleMaterialSources.append(DestructableMaterialSource(newMaterialSourceLocation[0], newMaterialSourceLocation[1],
                                                                                       newMaterialSourceType.drop, newMaterialSourceType.sprite,
                                                                                       newMaterialSourceType.hp, newMaterialSourceType.qty,
                                                                                       newMaterialSourceType.dropStackSize))
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
        adjacentRoom = [0, 0, 0]
        self.unfinishedShelterZones = []
        for number in range(qty):
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
                newShelter = Room(room.coordinate[0: 2], 'desert', 6, depth=100)
                self.rooms.append(newShelter)
                self.shelters = [area for area in self.rooms if area.coordinate[2] == 100]
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

        for zone in Liszt:
                shelterYCoords = [loaction.coordinate[1] for loaction in zone]
                print(shelterYCoords)
                topShelter = max(shelterYCoords)
                topShelter = zone[shelterYCoords.index(topShelter)]
                topShelter.background = IMAGES['images/shelterBackground.png']
                print(topShelter.coordinate)
                topShelter.teleporters.append(teleporter(topShelter.coordinate, 800, 50, topShelter.coordinate[0: 2] + [0], 805,
                                                  750, IMAGES['images/invisibleTeleporter35X80.png']))

                topShelter.foes = []
                topShelter.traps = []
                topShelter.destructibleMaterialSources = []
                for location in zone:
                    if location != topShelter:
                        location.background = IMAGES['images/altShelterBackground.png']
                        location.teleporters = []
        for zone in self.unfinishedShelterZones:
            for room in zone:
                print(room.coordinate)
        for room in self.shelters:
            if room.background == IMAGES['images/shelterBackground.png']:
                self.coordinateToRoom(room.coordinate[0: 2] + [0])[1].teleporters.append(teleporter(room.coordinate[0: 2] + [0],
                                    800, 450, room.coordinate, 800, 750, IMAGES['images/shelterEntrance.png']))

    def addDoors(self):
        for room in self.roomCoordinates:
            if [room[0], room[1] + 1, room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(800, 20))

            if [room[0], room[1] - 1, room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(800, 880))

            if [room[0] - 1, room[1], room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(20, 450))

            if [room[0] + 1, room[1], room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(1580, 450))

    def readdFoes(self):
        for room in self.rooms:
            room.spawnFoes()

class Door:
    def __init__(self, centerx, centery):
        self.sprite = IMAGES['images/door.png']

        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery

class MaterialPickup:
    def __init__(self, sprite, centerx, centery, kind):
        self.sprite = sprite

        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery

        self.type = kind

class DestructableMaterialSource:
    def __init__(self, centerx, centery, drop, sprite, hp, dropsNumber, maxStackSize=99):
        self.sprite = sprite

        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.dr = 0
        self.drop = drop
        self.hp = hp
        self.dropStackSize = maxStackSize
        self.qty = dropsNumber

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
            pygame.mixer.music.set_volume(2)
            pygame.mixer.music.play(-1)
            p.song = song
    except NameError:
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(2)
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

def checkCollision(a, b):
    if abs(a.place.centerx - b.place.centerx) < (a.place.width  + b.place.width)  / 2 and \
       abs(a.place.centery - b.place.centery) < (a.place.height + b.place.height) / 2:
            if type(a) == Foe:
                if a.attack == 0 and type(b) == DestructableMaterialSource:
                    b.hp = 0
            if type(a) == Bullet:
                if a.delay < 1:
                    if not type(b) == DestructableMaterialSource:
                        b.knockbackAfflictions.append([a.knockback[0], a.knockback[1], a.knockback[2]])
                    elif a.firer == p:
                        b.hp -= 10 * a.damage
                    if a.melee == 0 and not b in a.hurtTargets:
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

                            a.hurtTargets.append(b)

                            if type(b) == Player and p.invincibility < 1:
                                if not a.damage == 0:
                                    b.invincibility = 40
                                    b.hp -= a.damage * (1 - b.dr / 100)
                                return 1

                            if not type(b) == Player:
                                if a.melee == 1:
                                    if not b in a.hurtTargets:
                                        b.hp -= a.damage * (1 - b.dr / 100)
                                        return 1

                                b.hp -= a.damage * (1 - b.dr / 100)
                                return 1

                        except ValueError:
                            pass

            elif type(b) == Player and p.invincibility < 1:
                if b.invincibility < 1:
                    if not a.attack == 0:
                        b.invincibility = 40
                        b.hp -= a.attack * (1 - b.dr / 100)
                    return 1
            elif type(b) == DestructableMaterialSource and type(a) == Foe:
                b.hp -= a.attack

    return 0

def checkNotDamageCollision(a, b):
    if abs(a.place.centerx - b.place.centerx) < (a.place.width + b.place.width) / 2 and abs(a.place.centery - b.place.centery) < (a.place.height + b.place.height) / 2:
        if type(a) == Foe:
            if a.attack == 0 and type(b) == DestructableMaterialSource:
                b.hp = 0
        return 1

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
    p.display.blit(coordinateToRoom(p.room)[1].background, coordinateToRoom(p.room)[1].background_location)

    for door in coordinateToRoom(p.room)[1].doors:
        p.display.blit(door.sprite, door.place)

    for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
        p.display.blit(resource.sprite, resource.place)

    p.display.blit(p.sprite, p.place)
    p.showHealthAndStamina()

    for item in coordinateToRoom(p.room)[1].droppedItems:
        p.display.blit(item.sprite, item.place)
    for i in coordinateToRoom(p.room)[1].teleporters:
        p.display.blit(i.sprite, i.place)
    for trap in coordinateToRoom(p.room)[1].traps:
        p.display.blit(trap.sprite, trap.place)

    for foe in coordinateToRoom(p.room)[1].foes:
        p.display.blit(foe.sprite, foe.place)
    for i in coordinateToRoom(p.room)[1].enemyBullets:
        if i.delay < 1:
            p.display.blit(i.sprite, i.place)
    for i in p.bullets:
        if i.delay < 1:
            p.display.blit(i.sprite, i.place)
    if p.inventoryShown == 1:
        p.showInventory()

    for number in range(7):
        pygame.display.flip()

play('music/desertCalm.mp3')

deleted = input("Type 'delete' and then a number to delete the save of the cooresponding number: ").lower()
for i in range(4):
    if f'delete{i + 1}' == deleted:
        try:
            inv = open(f"inventory{i + 1}.json", 'x')
        except FileExistsError:
            inv = open(f"inventory{i + 1}.json", 'w')

        json.dump(['BasicRange', 1, 1] + ["empty", 1, 1] * 99, inv)
        inv.close()

file = 0
while file not in [1, 2, 3, 4]:
    try:
        file = int(input('Choose a file (1-4): '))
    except ValueError:
        print("That was improper.")

spritesForInventoryItems = {
    'BasicRange'     : IMAGES['images/pistolInInventory.png'],
    'BasicSpread'    : IMAGES['images/basicSpreadInInventory.png'],
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
}

theCraftingBox = CraftingBox()
mouseMarkerTarget = MouseMarkerTarget()

p = Player()
p.place.centerx = 100
p.place.centery = 100
p.save(file)
p.hp = 0
p.updateStats()

rooms = Rooms()

rooms.makeRooms(16, 'desert')

rooms.addDoors()

while True:
    while p.hp > 1:
        if p.pause == 0 and p.inventoryShown == 0:
            p.move()
            p.checkDroppedItemCollision()

            for resource in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                if resource.hp < 1:
                    resource.drop_resources()

                    try:
                        coordinateToRoom(p.room)[1].destructibleMaterialSources.remove(resource)
                    except ValueError:
                        pass

            p.showHealthAndStamina()
            p.useActiveItem()

            coordinateToRoom(p.room)[1].updateBullets()
            if len(coordinateToRoom(p.room)[1].foes) == 0:
                for i in coordinateToRoom(p.room)[1].teleporters:
                    if checkNotDamageCollision(i, p):
                        p.room = i.destinationCoordinate
                        p.center[0] = int(i.destinationCenterx)
                        p.center[1] = int(i.destinationCentery)
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

            for bullet in p.bullets.copy():
                bullet.move()

                for material in coordinateToRoom(p.room)[1].destructibleMaterialSources:
                    checkCollision(bullet, material)

                for foe in coordinateToRoom(p.room)[1].foes:
                    if foe.vulnerable == 1 and foe.hp > 0:
                        checkCollision(bullet, foe)
            coordinateToRoom(p.room)[1].updateFoes()

            p.updateStats()
            p.animationFrame += 1
            p.invincibility -= 1

        if p.inventoryShown == 1:
            p.showInventory()
        p.detectInput()
        blitEverything()

    p.load(file)
    rooms.rooms = []
    rooms.roomCoordinates = []
    rooms.makeRooms(16, "desert")
    rooms.addDoors()
    for i in range(16):
        for j in range(10):
            p.display.fill((0, 0, 0))
            dthimg = IMAGES[f'images/newDeathAnim{i + 1}.png']
            dthimgplc = dthimg.get_rect()
            dthimgplc.centery = 450
            dthimgplc.centerx = 800
            p.display.blit(dthimg, dthimgplc)
            pygame.display.flip()
    for i in range(750):
        pygame.display.flip()
