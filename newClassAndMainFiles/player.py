from functions import defs
import pygame
import json
from items import Item
from words import Word
from room import Room
for i in defs:
    exec(f'from functions import {i}')
IMAGES = {}
import os
for i in os.listdir("images"):
    if i not in ["font"]:
        IMAGES[f"images/{i}"] = pygame.image.load(f'images/{i}')
IMPORTING = 1
FONT = {}
for i in os.listdir("images/font"):
    FONT[i[-5].lower()] = pygame.image.load(f'images/font/{i}')
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


class Player:
    def __init__(self, isRun=1):
        self.isRun = isRun
        if self.isRun:
            self.sprite = IMAGES['images/walkingAnimation_s1.png']
            self.place = self.sprite.get_rect()
            self.knockbackAfflictions = []
            self.dr = 0
            self.mapShown = 0
            self.attackNum = 1
            self.time = 12
            self.place.bottom = 450
            self.place.left   = 805
            self.activeItem          = 0
            self.animationFrame      = 0
            self.dashFramesRemaining = 0
            self.fireCooldown        = 0
            self.firing              = 0
            self.fullPowerMandibleCooldown = 0
            self.healingByKill       = 65
            self.song = None
            self.hp                  = 130
            self.hr                  = 0
            self.hrWhileDashing      = 0
            self.heat = 0
            self.attackNumResetCooldown = 100
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
            self.animationSwap(self.idleAnimation, self.direction)
            self.animationFrame = 0
            self.save()
            self.hitbox = rectangle(pygame.Rect(self.place.left, self.place.top + 40, self.place.width, self.place.height - 20), 0)
            self.updateStats()

    def dropItem(self, item):
        if self.isRun:
            for i in range(item.qty):
                coordinateToRoom(self.room)[1].droppedItems.append(DroppedItem(item.type, self.place.centerx, self.place.centery, maxStackSize=item.stackSize, dr=item.dr, altAttackCharge=item.altAttackCharge, armorSlot=item.armorSlot))


    def getQtyOfFoeTypeInRoom(self, type):
        if self.isRun:
            qty = 0
            for foe in coordinateToRoom(self.room)[1].foes:
                if foe.type == type:
                    qty += 1
            return qty

    def prepareToSave(self):
        if self.isRun:
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
            self.saveCode.remove(f'self.hr = {self.hr}')
            self.saveCode.remove(f'self.vr = {self.vr}')
            self.saveCode = tuple(self.saveCode)


    def craft(self):
        if self.isRun:
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
        if self.isRun:
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
                roomCoordsInfo[f'[{room.coordinate[0]}, {room.coordinate[1]}, {room.coordinate[2]}]'] = tuple(room.saveCode)
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
        if self.isRun:
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
        if self.isRun:
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
        if self.isRun:
            for item in items:
                if not type(item) == None:
                    if random.randint(1, 100) <= item.dropChance:
                        self.addItemToInventory(item, centerx, centery)
                        self.updateStats()
                        self.save()


    def animationSwap(self, animation, direction):
        self.animation = animation[direction]
        self.undirectedAnimation = animation

    def turn(self, direction):
        self.animationSwap(self.undirectedAnimation, direction)

    def checkDroppedItemCollision(self):
        if self.isRun:
            for item in coordinateToRoom(self.room)[1].droppedItems:
                if checkNotDamageCollision(self, item):
                    self.addItemToInventory(Item(0, item.item, maxStackSize=item.stackSize, dr=item.dr, altAttackCharge=item.altAttackCharge, armorSlot=item.armorSlot), item.place.centerx, item.place.centery)
                    self.save()
                    try:
                        coordinateToRoom(self.room)[1].droppedItems.remove(item)
                    except ValueError:
                        pass


    def updateStats(self):
        if self.isRun:
            self.hr = (keyboard.is_pressed('d') - keyboard.is_pressed('a')) * 10
            self.vr = (keyboard.is_pressed('s') - keyboard.is_pressed('w')) * 10
            self.fullPowerMandibleCooldown -= gameSpeed
            self.time += 0.1 * gameSpeed
            self.attackNumResetCooldown -= gameSpeed
            if self.attackNumResetCooldown <= 0:
                self.attackNum = 1
            if self.time >= 360:
                self.time = 0
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
            self.dashFramesRemaining -= gameSpeed
            self.dr = 0
            self.staminaRegenRate    = 1.5
            if pygame.mouse.get_pressed()[2] and self.inventory[self.activeItem].chargeProgress < self.inventory[
                self.activeItem].altAttackCharge and self.inventory[self.activeItem].altAttackCharge > 0:
                self.inventory[self.activeItem].chargeProgress += gameSpeed
            if 15 < abs(self.heat):
                self.dr -= 25
            if 30 < abs(self.heat):
                self.hp -= 0.01 * gameSpeed
            if 50 < abs(self.heat):
                self.hp -= 0.03 * gameSpeed
            for item in self.inventory:
                if item.qty <= 0:
                    self.inventory[self.inventory.index(item)] = Item(0, 'empty')
            self.accessories         = self.inventory[30:37]
            self.standardInventory  = self.inventory[0:30]
            try:
                self.sprite              = self.animation[self.animationFrame]
            except IndexError:
                self.sprite = self.animation[0]
            self.place = self.sprite.get_rect(center=[self.place.centerx, self.place.centery])
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
            self.slideFramesRemaning -= gameSpeed

            if self.firing:
                self.direction = getDirection(pygame.mouse.get_pos()[0] - self.place.centerx, pygame.mouse.get_pos()[1] - self.place.centery)

            elif self.hr != 0 or self.vr != 0:
                self.direction = getDirection(self.hr, self.vr)

            if self.hr == 0 and self.vr == 0 and self.undirectedAnimation == self.walkingAnimation:
                self.animationSwap(self.idleAnimation, self.direction)
                self.animationFrame = 0
            self.turn(self.direction)
            if self.animationFrame >= len(self.animation):
                self.animationFrame = 0

                if not abs(self.hr) and not abs(self.vr):
                    self.animationSwap(self.idleAnimation, self.direction)
                else:
                    self.animationSwap(self.walkingAnimation, getDirection(self.hr, self.vr))
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


            self.hitbox = rectangle(pygame.Rect(self.place.left, self.place.top + 40, self.place.width, self.place.height - 20), 0)


    def detectInput(self):
        if self.isRun:
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
                        self.pause = 1
                        try:
                            exec(input(':'))
                        except:
                            print('invalid command')
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
                        if self.inventory[self.activeItem].chargeProgress >= self.inventory[self.activeItem].altAttackCharge:
                            exec(f'self.useAlt{self.inventory[self.activeItem].type}()')
                            self.direction = getDirection(pygame.mouse.get_pos()[0] - self.center[0], pygame.mouse.get_pos()[1] - self.center[1])
                            self.turn(self.direction)
                        self.inventory[self.activeItem].chargeProgress = 0

    def switchSong(self):
        if self.isRun:
            if coordinateToRoom(self.room)[1].biome == "desert" and self.room[2] == 0:
                if len(coordinateToRoom(self.room)[1].foes) > 0:
                    play('music/desertFight.mp3')
                else:
                    play('music/Desert overground base.mp3')
            elif self.room[2] == 1:
                play('music/shelter.mp3')


    def checkForAccessory(self, item_type):
        return item_type in [i.type for i in self.accessories]

    def useTheSpark(self):
        if self.isRun:
            self.bullets.append(Bullet(pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0] * 10,
                                       pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1] * 10,
                                       2, self, sprite=IMAGES['images/spark.png'],
                                       elements=["heat"], mark=('for effect in ["self.hp -= .05", "self.totalSpeed *= 1.1"]: exec(effect)', IMAGES['images/fireMarkSprite.png'], '1 == 2', ''),
                                       ))
            self.fireCooldown = 30


    def showInventory(self):
        if self.isRun:
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
        if self.isRun:
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
        if self.isRun:
            self.place.centerx = self.center[0]
            self.place.centery = self.center[1]

            self.detectInput()
            self.updateStats()


            if self.dashFramesRemaining < 1:
                self.center[1] += self.vr * self.speed * gameSpeed
                self.center[0] += self.hr * self.speed * gameSpeed
            else:
                self.center[1] += self.vrWhileDashing * gameSpeed
                self.center[0] += self.hrWhileDashing * gameSpeed

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
                    self.hitbox = rectangle(
                        pygame.Rect(self.place.left, self.place.top + 40, self.place.width, self.place.height - 20), 0)
            for projectile in self.bullets:
                if projectile.melee == 1:
                    projectile.place.x += self.hr * self.speed * gameSpeed
                    projectile.place.y += self.vr * self.speed * gameSpeed

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
        if self.isRun:
            if self.inventory[self.activeItem].type == "NanotechRevolver":
                if self.fireCooldown < 1 and self.firing == 1:
                    pathx = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0]
                    pathy = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1]
                    self.fireCooldown = 30

                    self.bullets.append(Bullet(
                        pathx * 15,
                        pathy * 15,
                        1, self,
                        sprite=IMAGES['images/basicRangeProjectile_d.png'], elements=['metal'],
                        mark=('self.dr -= 0.5', IMAGES['images/nanotechRevolverMark.png'], '"heat" in self.recentElementDamages',
                              'self.hp -= 12')))


    def advanceAttackSequence(self):
        self.attackNum += 1
        self.attackNumResetCooldown = 100

    def useFerroSandShotgun(self):
        if self.isRun:
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
        if self.isRun:
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
                                                            'rotated=0))', hasRotatedHitbox=1))

    def useActiveItem(self):
        if self.isRun:
            if self.firing and self.fireCooldown < 1 and self.dashFramesRemaining < 1 and self.slideFramesRemaning < 1:
                try:
                    exec(f'self.use{self.inventory[self.activeItem].type}()')
                except AttributeError:
                    pass
                self.inventory[self.activeItem].chargeProgress = 0
            self.fireCooldown -= gameSpeed


    def fireSemirandomNoAttack(self, damage):
        if self.isRun:
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
        if self.isRun:
            self.fireCooldown = 40
            theAngle = getAngle(pygame.mouse.get_pos()[0] - self.place.centerx, pygame.mouse.get_pos()[1] - self.place.centery)
            if self.attackNum == 1:
                if self.fullPowerMandibleCooldown <= 0:
                    self.bullets.append(Bullet(0, 0, 5, self, melee=1, linger=20, sprite=IMAGES['images/theMandibleSwing1.png'], angle=theAngle))
                else:
                    self.bullets.append(
                        Bullet(0, 0, 3, self, melee=1, linger=20, sprite=pygame.transform.scale(IMAGES['images/theMandibleSwing1.png'], (66, 75)), angle=theAngle))
                self.advanceAttackSequence()
            elif self.attackNum == 2:
                if self.fullPowerMandibleCooldown <= 0:
                    self.bullets.append(Bullet(0, 0, 10, self, melee=1, linger=20, sprite=IMAGES['images/theMandibleSwing2.png'], angle=theAngle))
                else:
                    self.bullets.append(
                        Bullet(0, 0, 5, self, melee=1, linger=20, sprite=pygame.transform.scale(IMAGES['images/theMandibleSwing2.png'], (66, 75)), angle=theAngle))
                self.advanceAttackSequence()
            elif self.attackNum == 3:
                self.attackNum = 1
                if self.fullPowerMandibleCooldown <= 0:
                    self.bullets.append(Bullet(0, 0, 15, self, melee=1, linger=25, sprite=IMAGES['images/theMandibleSwing3.png'], angle=theAngle, specialEffectConditions=['checkCollisionWithAllFoes(self) and p.inventory[p.activeItem].type == "Mandible"'], specialEffects=['for command in ["p.attackNum = 4", "p.attackNumResetCooldown = 120"]: exec(command)']))
                else:
                    self.bullets.append(
                        Bullet(0, 0, 8, self, melee=1, linger=20, sprite=pygame.transform.scale(IMAGES['images/theMandibleSwing3.png'], (150, 42)),
                               angle=theAngle))
            elif self.attackNum == 4:
                self.bullets.append(Bullet(0, 0, 40, self, melee=1, linger=30, sprite=pygame.transform.scale(IMAGES['images/theMandibleSwing1.png'], (264, 300)), angle=theAngle))
                self.fullPowerMandibleCooldown = 2500
                self.attackNum = 1


    def dash(self):
        if self.isRun:
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
