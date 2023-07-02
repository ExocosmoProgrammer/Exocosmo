import pygame
import random
import json
import os

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

class Bullet:
    def __init__(self, hr, vr, damage, firer, melee=0, linger=400, sprite=None, piercing=0):
        self.piercing = piercing
        self.hurtTargets = []
        self.damage = damage
        self.linger = linger
        self.melee = melee
        self.firer = firer
        self.hr = hr
        self.vr = vr

        # Set correct sprite based on firer
        if firer == p:
            if p.inventory[p.activeItem].type == "mandible":
                self.sprite = IMAGES['images/playerMelee.png']
            elif p.inventory[p.activeItem].type == "basicRange":
                self.sprite = IMAGES['images/playerProjectile.png']
            elif p.inventory[p.activeItem].type == "basicSpread":
                self.sprite = IMAGES['images/playerProjectile.png']
        else:
            if self.firer.type == "ironAngel" or self.firer.type == "wobbegong":
                self.sprite = IMAGES['images/ironAngelProjectile.png']
            elif self.firer.type == "antlion":
                if self.melee == 1:
                    self.sprite = IMAGES['images/lionMelee.png']
                else:
                    self.sprite = IMAGES['images/playerMelee.png']
            elif self.firer == p and p.inventory[p.activeItem].type == "mandible":
                self.sprite = IMAGES['images/playerMelee.png']

        if not sprite == None:
            self.sprite = sprite

        # Gets the coordinates for usage later
        self.place = self.sprite.get_rect()
        self.place.centerx = self.firer.place.centerx
        self.place.centery = self.firer.place.centery

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

        self.center = [self.place.centerx, self.place.centery]

    def move(self):
        self.linger -= 1

        if self.linger < 1:
            try:
                self.firer.bullets.remove(self)
                if type(self.firer) == Foe:
                    coordinateToRoom(p.room)[1].enemyBullets.remove(self)
            except ValueError:
                pass

        self.center[0] += self.hr
        self.center[1] += self.vr

        if self.melee == 1:
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

        try:
            if self.place.top < 0 or self.place.left < 0 or self.place.bottom > 900 or self.place.right > 1600:
                if self.melee == 0 and not self.firer == p:
                    self.firer.bullets.remove(self)
        except ValueError:
            pass

class Item:
    def __init__(self, dropChance, type, qty=1, maxStackSize=1):
        self.dropChance = dropChance
        self.type = type
        self.dragged = 0
        self.qty = qty
        self.stackSize = maxStackSize

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

class CraftingBox:
    def __init__(self):
        self.sprite = IMAGES['images/craftingBox.png']
        self.place = self.sprite.get_rect()
        self.place.centerx = 1390
        self.place.centery = 450

class Player:
    def __init__(self):
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

        self.sprite = IMAGES['images/walkingAnimation_s1.png']
        self.place = self.sprite.get_rect()

        self.place.bottom = 450
        self.place.left   = 805

        self.activeItem          = 0
        self.animationFrame      = 0
        self.dashFramesRemaining = 0
        self.fireCooldown        = 0
        self.firing              = 0
        self.healingByKill       = 65
        self.hp                  = 130
        self.hr                  = 0
        self.hrWhileDashing      = 0
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
        self.recipes             = {('basicSpread',): (Item(0, 'bagOfSand'),)}
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
            self.inventory = [Item(100, "basicRange")]
            for number in range(99):
                self.inventory.append(Item(1, "empty"))
                self.emptySlots.append(Item(1, "empty"))
        self.inventory[99]       = Item(0, 'empty')

        self.bulletSpritesForBasicRange = {
            'w': IMAGES['images/basicRangeProjectile_w.png'],
            'a': IMAGES['images/basicRangeProjectile_a.png'],
            's': IMAGES['images/basicRangeProjectile_s.png'],
            'd': IMAGES['images/basicRangeProjectile_d.png']
        }
        self.shellSpritesForBasicSpread = {
            'w': IMAGES['images/basicSpreadProjectile_w.png'],
            'a': IMAGES['images/basicSpreadProjectile_a.png'],
            's': IMAGES['images/basicSpreadProjectile_s.png'],
            'd': IMAGES['images/basicSpreadProjectile_d.png']
        }

        self.animation = self.idleAnimation[self.direction]
        self.undirectedAnimation = self.idleAnimation

        for i in range(8):
            self.hotbar[i + 1] = "empty"
        self.updateStats()

    def dropItem(self, item):
        for i in range(item.qty):
            coordinateToRoom(self.room)[1].droppedItems.append(DroppedItem(item.type, self.place.centerx, self.place.centery, maxStackSize=item.stackSize))
            self.updateStats()

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
            for item in self.inventory[40:100]:
                if not item.type == 'empty':
                    self.updateStats()
                    self.dropItem(item)

        for i in range(59):
            self.inventory[i + 40].type = 'empty'

    def save(self, file):
        try:
            inventory = open(f'inventory{file}.json', "x")
        except FileExistsError:
            inventory = open(f'inventory{file}.json', "w")

        items = []
        for item in self.inventory:
            items.append(item.type)

        json.dump(items, inventory)
        inventory.close()

    def load(self, file):
        with open(f'inventory{file}.json', "r") as inventory:
            storage = json.load(inventory)
            self.inventory = [Item(100, i) for i in storage]

        self.dashFramesRemaining  = 0
        self.hp                    = 130
        self.place.centerx         = 805
        self.place.centery         = 450
        self.bullets               = []
        self.room                  = [0, 0, 0]
        self.animation             = self.idleAnimation['s']
        self.undirectedAnimation   = self.idleAnimation

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

    def getDirection(self, x, y):
        if abs(x) > abs(y):
            return 'd' if x > 0 else 'a'
        else:
            return 's' if y > 0 else 'w'

    def updateStats(self):
        self.dashFramesRemaining -= 1
        self.staminaRegenRate    = 1.5
        self.speed               = 0.46
        self.accessories         = self.inventory[30:37]
        self.standardInventory  = self.inventory[0:30]
        self.sprite              = self.animation[self.animationFrame]

        self.recipes = {
            ('bagOfSand',)  : (Item(0, 'basicSpread'),),
            ('basicSpread',) : (Item(0, 'bagOfSand'),)
        }

        if self.checkForAccessory('wobbegongCloak'):
            self.staminaRegenRate += 0.35
        self.stamina -= self.staminaRegenRate
        if self.stamina < 0:
            self.stamina = 0

        if self.slideFramesRemaning > 0:
            self.speed *= 4
        self.slideFramesRemaning -= 1

        if self.hr or self.vr:
            self.direction = self.getDirection(self.hr, self.vr)

        if not self.hr and not self.vr and self.undirectedAnimation == self.walkingAnimation:
                self.animation = self.idleAnimation[self.direction]
                self.undirectedAnimation = self.idleAnimation

        if self.animationFrame >= len(self.animation):
            self.animationFrame = 0

            if not self.hr and not self.vr:
                self.animation = self.idleAnimation[self.direction]
                self.undirectedAnimation = self.idleAnimation
            else:
                self.animation = self.walkingAnimation[self.getDirection(self.hr, self.vr)]
                self.undirectedAnimation = self.walkingAnimation

        for i in range(10):
            self.hotbar[i] = self.inventory[i].type

        if self.firing == 1:
            self.turn(self.getDirection(
                pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0] * 3,
                pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1] * 3
            ))
        else:
            self.turn(self.getDirection(self.hr, self.vr))

        self.emptySlots = []
        for item in self.standardInventory:
            if item.type == "empty":
                self.emptySlots.append(item)

        if len(self.emptySlots) == 30:
            self.inventory[0] = Item(0, 'basicRange')
            self.standardInventory[0] = self.inventory[0]
            self.emptySlots.pop(0)

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
                            for item in self.inventory[40:100]:
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
                                item1 = self.inventory.index(item)
                                item2 = self.inventory.index(draggedItem)
                                self.inventory[item1] = draggedItem
                                self.inventory[item2] = item
                                item.dragged = 1
                                shallDrop = 0
                                draggedItem.dragged = 0

                        if shallDrop:
                            for item in self.inventory:
                                item.dragged = 0
                    else:
                        for item in self.inventory:
                            if detectMouseCollision(item) == 1:
                                item.dragged = 1

            if event.type == pygame.MOUSEBUTTONUP:
                self.firing = 0

    def switchSong(self):
        if coordinateToRoom(self.room)[1].biome == "desert" and \
            not self.room[2] and \
            len(coordinateToRoom(self.room)[1].foes):
                play('music/desertFight.mp3')

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

        for item in self.inventory:
            if not item.type == 'empty':
                self.display.blit(item.sprite, item.place)

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

        if self.animationFrame:
            self.animationFrame -= 1

        if self.dashFramesRemaining < 1:
            self.center[1] += self.vr * self.speed
            self.center[0] += self.hr * self.speed
        else:
            self.center[1] += self.vrWhileDashing
            self.center[0] += self.hrWhileDashing

        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]

        for material in coordinateToRoom(self.room)[1].destructibleMaterialSource:
            while checkNotDamageCollision(self, material):
                if self.dashFramesRemaining < 1 and self.hr ** 2 + self.vr ** 2 > 0:
                    self.center[0] -= self.hr
                    self.center[1] -= self.vr
                else:
                    self.center[0] -= self.hrWhileDashing
                    self.center[1] -= self.vrWhileDashing

                self.place.centerx = self.center[0]
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
                self.pause = 1
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
                self.pause = 1
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
                self.pause = 1
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
                self.pause = 1
                self.dashFramesRemaining = -1
                self.stamina = 0
                rooms.readdFoes()
                self.switchSong()
            else:
                self.center[0] = 1600 - self.place.width / 2

        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]

    def useActiveItem(self):
        if self.firing == 1 and self.fireCooldown < 1 and self.dashFramesRemaining < 1 and self.slideFramesRemaning < 1:
            if self.inventory[self.activeItem].type == "basicRange":
                if self.fireCooldown < 1 and self.firing == 1:
                    pathx = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0] * 3
                    pathy = pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1] * 3
                    self.fireCooldown = 20

                    self.bullets.append(Bullet(
                        pathx * 10,
                        pathy * 10,
                        2, self,
                        sprite=self.bulletSpritesForBasicRange[
                            self.getDirection(pathWithoutPlaceAttribute(
                                self.center,
                                pygame.mouse.get_pos())[0],
                                pathWithoutPlaceAttribute(
                                    self.center,
                                    pygame.mouse.get_pos()
                                )[1]
                            )
                        ]
                    ))

            elif self.inventory[self.activeItem].type == "basicSpread":
                if self.fireCooldown < 1:
                    for number in range(7):
                        self.fireSemirandomNoAttack(1.3)
                    self.fireCooldown = 30

            elif self.inventory[self.activeItem].type == "mandible":
                self.mandibleAttack()

            self.direction = self.getDirection(
                pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[0],
                pathWithoutPlaceAttribute(self.center, pygame.mouse.get_pos())[1]
            )
        self.fireCooldown -= 1

    def fireSemirandomNoAttack(self, damage, linger=300, piercing=0):
        player_pos = [self.place.centerx, self.place.centery]
        mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        self.bullets.append(Bullet(
            semirandomPathWithoutPlace(player_pos, mouse_pos)[0] * 8,
            semirandomPathWithoutPlace(player_pos, mouse_pos)[1] * 8,
            damage, self,
            sprite=self.shellSpritesForBasicSpread[
                self.getDirection(pathWithoutPlaceAttribute(p.center, pygame.mouse.get_pos())[0],
                pathWithoutPlaceAttribute(p.center, pygame.mouse.get_pos())[1])
            ],
            linger=linger, piercing=piercing
        ))

    def basicFireBlast(self):
        for number in range(10):
            self.fireSemirandomNoAttack(0.06, linger=20, piercing=100)

    def mandibleAttack(self):
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
        self.hr                    = 0
        self.multifaced            = 0
        self.turretFiring          = 0 # Not used anywhere but here
        self.turretPause           = 20 # Not used anywhere but here
        self.vr                    = 0
        self.vulnerable            = 1
        self.wobbegongDashCooldown = 120
        self.wobbegongDashing      = 0
        self.target                = p # Not used anywhere but here
        self.type                  = kind
        self.bullets               = []
        self.drops                 = []

        if self.type == "antlion":
            self.attack       = 0
            self.hp           = 100
            self.speed        = 0
            self.vulnerable   = 0
            self.antlionPause = random.randint(15, 70)
            self.drops        = [Item(3, "mandible")]
            self.sprites      = [IMAGES['images/antlion.png'], IMAGES['images/activeLionPit.png']]
            self.sprite       = IMAGES['images/activeLionPit.png']

        elif self.type == "ironAngel":
            self.sprite = IMAGES['images/ironAngel.png']
            self.hp = 100
            self.attack = 40
            self.speed = 0
            self.drops = [Item(1, "basicSpread")]

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

        if self.type != "antlion":
            self.doesContactDamage = 1 # Not used anywhere but here

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

    def accelerate(self):
        self.hr = random.randint(-1, 1) * self.speed

        if sign(self.hr) == sign(p.place.centerx - self.place.centerx):
            self.vr = random.randint(-1, 1) * self.speed
        else:
            self.vr = sign(p.place.centery - self.place.centery) * self.speed

        if random.randint(1, 2) == 1:
            self.hr = sign(p.place.centerx - self.place.centerx) * self.speed
        if random.randint(1, 2) == 2:
            self.vr = sign(p.place.centery - self.place.centery) * self.speed

    def move(self):
        if self.type != "antlion":
            if self.type == "wobbegong":
                if self.wobbegongDashing == 0:
                    self.hr = path(self, p)[0] * 0.2
                    self.vr = path(self, p)[1] * 0.2

                self.wobbegongDashCooldown -= 1

                if not self.wobbegongDashing and self.wobbegongDashCooldown < 1:
                    self.hr = path(self, p)[0] * 0.5
                    self.vr = path(self, p)[1] * 0.5
                    self.wobbegongDashing = 1
                    self.wobbegongDashCooldown = random.randint(120, 240)

            if self.type == "knight":
                self.hr = path(self, p)[0] * 0.2
                self.vr = path(self, p)[1] * 0.2

            if self.type == "ironAngel":
                self.vr = 0
                self.hr = 0

            self.center[0] += self.hr
            self.center[1] += self.vr
            self.place.centerx = self.center[0]
            self.place.centery = self.center[1]

            for material in coordinateToRoom(p.room)[1].destructibleMaterialSource:
                if self.type != 'antlion':
                    while checkNotDamageCollision(self, material) == 1:
                        if self.wobbegongDashing == 1:
                            self.spreadShotAsWobbegong()
                            self.wobbegongDashing = 0

                        checkCollision(self, material)

                        self.center[0] -= self.hr * 1.1
                        self.center[1] -= self.vr * 1.1
                        self.place.centery = self.center[1]
                        self.place.centerx = self.center[0]

            if abs(self.hr) > abs(self.vr):
                if self.hr > 0:
                    self.sprite = self.dsprite
                else:
                    self.sprite = self.asprite

            else:
                if self.vr > 0:
                    self.sprite = self.ssprite
                else:
                    self.sprite = self.wsprite

            if self.place.left <= 0:
                self.place.left = 0

            if self.place.right >= 1600:
                self.place.right = 1600

            if self.place.top <= 0:
                self.place.top = 0

            if self.place.bottom >= 900:
                self.place.bottom = 900

            if self.place.left == 0 or self.place.right == 1600 or self.place.top == 0 or self.place.bottom == 900:
                self.accelerate()
                if self.type == "wobbegong" and self.wobbegongDashing == 1:
                    self.spreadShotAsWobbegong()
                self.wobbegongDashing = 0

            if random.randint(1, 100) == 1 and self.wobbegongDashing == 0:
                self.accelerate()

        else:
            self.speed = 0
            self.hr    = 0
            self.vr    = 0

        p.display.blit(self.sprite, self.place)

    def fireStraight(self, target): # Not used in this class
        self.bullets.append(Bullet(path(self, target)[0], path(self, target)[1], 34, self))

    def fireStraightToPoint(self, point): # Not used in this class
        self.bullets.append(Bullet(
            pathWithoutPlaceAttribute(self.center, point)[0],
            pathWithoutPlaceAttribute(self.center, point)[1], 34, self
        ))

    def spreadShotAsWobbegong(self):
        for number in range(7):
            self.fireSemirandom(p)

    def attackAsAntlion(self):
        self.antlionPause -= 1

        if self.antlionPause < 1:
            if self.vulnerable:
                self.sprite       = IMAGES['images/activeLionPit.png']
                self.antlionPause = 25
                self.vulnerable   = 0

                self.place         = self.sprite.get_rect()
                self.place.centerx = p.place.centerx
                self.place.centery = p.place.centery
            else:
                self.sprite       = IMAGES['images/antlion.png']
                self.antlionPause = 70
                self.vulnerable   = 1

                self.place         = self.sprite.get_rect()
                self.place.centerx = self.place.centerx
                self.place.centery = self.place.centery

                self.bullets.append(Bullet(0, 0, 40, self, melee=1, linger = 65))

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

    def fireSemirandom(self, target):
        self.bullets.append(Bullet(
            semirandomPath(self, target)[0] * 1.5,
            semirandomPath(self, target)[1] * 1.5,
            34, self
        ))

    def spreadShotAsIronAngel(self):
        if self.fireCooldown < 1:
            self.fireCooldown = 130
            for i in range(9):
                self.fireSemirandom(p)
        else:
            self.fireCooldown -= 1

class MouseMarkerTarget:
    def __init__(self):
        self.sprite = IMAGES['images/mouseMarkerTarget.png']
        self.place = self.sprite.get_rect()

    def update_position(self):
        self.place.centerx, self.place.centery = pygame.mouse.get_pos()[:2]

class Room:
    def __init__(self, coordinate, biome, depth=0):
        self.biome = biome
        self.coordinate = [coordinate[0], coordinate[1], depth]
        self.destructibleMaterialSource = [DestructableMaterialSource(
            1200, 675, 'chunkOfCactus', IMAGES['images/destructibleCactus.png'], 200, random.randint(2, 3)
        )]

        self.antlions      = []
        self.doors         = []
        self.enemyBullets  = []
        self.foes          = []
        self.ironAngels   = []
        self.droppedItems = []
        self.p_bullets     = []
        self.traps         = []
        self.wobbegongs    = []

        self.potentialPitsX = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
        self.potentialPitsY = [50, 850, 450, 300, 600, 600, 300, 50, 850]

        self.difficulty = random.randint(0, 5)
        self.resources = random.randint(0, 3) + self.difficulty

        try:
            if type(coordinateToRoom([coordinate[0], coordinate[1], 0])) == tuple and depth:
                self.biome = coordinateToRoom([coordinate[0], coordinate[1], 0])[1].biome
        except NameError:
            pass

        if self.biome == "desert":
            self.background = IMAGES['images/desertBackground.bmp']

        self.background_location = self.background.get_rect()
        self.background_location.centerx = 805
        self.background_location.centery = 450

        if self.biome == "desert":
            self.layout = random.randint(1, 4)
            self.foe_types = ['ironAngel', 'wobbegong', 'antlion']

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

            if self.layout == 2:
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

            if self.layout == 3:
                self.foes = [Foe("wobbegong", 800, 450), Foe("antlion", 50, 50), Foe("antlion", 1550, 850)]
                if self.difficulty == 0:
                    self.foes.pop(0)

                if self.difficulty == 1 or self.difficulty > 2:
                    self.foes.pop(2)

                if self.difficulty == 2:
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

            if self.layout == 4:
                for i in range(27):
                    self.traps.append(PitTrap(400, i * 35 + 27))

                for i in range(27):
                    self.traps.append(PitTrap(1200, i * 35 + 27))

                self.potentialPitsX = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
                self.potentialPitsY = [50, 850, 450, 300, 600, 600, 300, 50, 700]

                for i in range(9):
                    self.traps.append(PitTrap(self.potentialPitsX[i], self.potentialPitsY[i]))

            if self.difficulty > 3:
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

        self.initialFoes        = self.foes # Not used anywhere in this class
        self.initialIronAngels  = self.ironAngels # Not used anywhere in this class
        self.initialWobbegongs  = self.wobbegongs # Not used anywhere in this class
        self.initialAntlions    = self.antlions # Not used anywhere in this class
        self.initialTraps       = self.traps # Not used anywhere in this class

    def updateBullets(self):
        for enemy in self.foes:
            for bullet in enemy.bullets:
                if not bullet in self.enemyBullets:
                    self.enemyBullets.append(bullet)

        for attack in self.enemyBullets:
            if attack.melee == 1 and not attack.firer in self.foes:
                self.enemyBullets.remove(attack)

    def spawnFoes(self):
        if not self.coordinate == [0, 0, 0]:
            if random.randint(1, 3) == 2 and len(self.foes) < 2 and not self.layout == 4:
                self.foes.append(Foe(self.foe_types[random.randint(0, len(self.foe_types) - 1)], random.randint(500, 1100), random.randint(300, 600)))

            for enemy in self.foes:
                if enemy.type == "ironAngel" and not enemy in self.ironAngels:
                    self.ironAngels.append(enemy)
                elif enemy.type == "wobbegong" and not enemy in self.wobbegongs:
                    self.wobbegongs.append(enemy)
                elif enemy.type == "antlion" and not enemy in self.antlions:
                    self.antlions.append(enemy)

            if random.randint(1, 4) == 1 and len(self.traps) < 4:
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
        self.rooms = [Room([0, 0], "desert")]
        self.roomCoordinates = [[0, 0, 0]]

    def makeRooms(self, qty, biome, depth=0):
        room = [0, 0, depth]

        for number in range(qty):
            if random.randint(1, 2) == 1:
                while room in self.roomCoordinates:
                    adjacentRoom = [
                        self.roomCoordinates[random.randint(0, len(self.rooms) - 1)][0],
                        self.roomCoordinates[random.randint(0, len(self.rooms) - 1)][1],
                        depth
                    ]
                    room = [adjacentRoom[0] + negativeOrPositive(), adjacentRoom[1], depth]
            else:
                while room in self.roomCoordinates:
                    adjacentRoom = [
                        self.roomCoordinates[random.randint(0, len(self.rooms) - 1)][0],
                        self.roomCoordinates[random.randint(0, len(self.rooms) - 1)][1],
                        depth
                    ]
                    room = [adjacentRoom[0], adjacentRoom[1] + negativeOrPositive(), depth]

            self.rooms.append(Room(room, biome))
            self.roomCoordinates.append(room)

    def coordinateToRoom(self):
        for room in rooms.rooms:
            if room.coordinate == self:
                return (self.rooms.index(room), room)

        return 0

    def addDoors(self):
        for room in self.roomCoordinates:
            if [room[0], room[1] + 1, room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(800, 20))

            elif [room[0], room[1] - 1, room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(800, 880))

            elif [room[0] - 1, room[1], room[2]] in self.roomCoordinates:
                coordinateToRoom(room)[1].doors.append(Door(20, 450))

            elif [room[0] + 1, room[1], room[2]] in self.roomCoordinates:
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
            coordinateToRoom(p.room)[1].destructibleMaterialSource.remove(self)
        except ValueError:
            pass

# Functions
def play(song):
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

def sqrt(a):
    return a ** .5

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
            if type(a) == Bullet:
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
                                b.hp -= a.damage
                            return 1

                        if not type(b) == Player:
                            if a.melee == 1:
                                if not b in a.hurtTargets:
                                    b.hp -= a.damage
                                    return 1

                            b.hp -= a.damage
                            return 1

                    except ValueError:
                        pass

            elif type(b) == Player and p.invincibility < 1:
                if b.invincibility < 1:
                    if not a.attack == 0:
                        b.invincibility = 40
                        b.hp -= a.attack
                    return 1

    return 0

def checkNotDamageCollision(a, b):
    if abs(a.place.centerx - b.place.centerx) < (a.place.width + b.place.width) / 2 and \
       abs(a.place.centery - b.place.centery) < (a.place.height + b.place.height) / 2:
            return 1

def detectMouseCollision(a):
    try:
        if abs(a.place.centery - pygame.mouse.get_pos()[1]) < a.place.height / 2 + 10 and \
           abs(a.place.centerx - pygame.mouse.get_pos()[0]) < a.place.width / 2 + 10:
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

    for resource in coordinateToRoom(p.room)[1].destructibleMaterialSource:
        p.display.blit(resource.sprite, resource.place)

    p.display.blit(p.sprite, p.place)
    p.showHealthAndStamina()

    for item in coordinateToRoom(p.room)[1].droppedItems:
        p.display.blit(item.sprite, item.place)

    for trap in coordinateToRoom(p.room)[1].traps:
        p.display.blit(trap.sprite, trap.place)

    for bullet in coordinateToRoom(p.room)[1].enemyBullets:
        p.display.blit(bullet.sprite, bullet.place)

    for bullet in p.bullets:
        p.display.blit(bullet.sprite, bullet.place)

    for foe in coordinateToRoom(p.room)[1].foes:
        p.display.blit(foe.sprite, foe.place)

    if p.inventoryShown == 1:
        p.showInventory()

    for number in range(7):
        pygame.display.flip()

play('music/desertCalm.mp3')

deleted = input("Type 'delete' and then a number to delete the save of the cooresponding number: ").lower()
for i in range(4):
    if f'delete{i + 1}' == deleted:
        try:
            inv = open(f"inventory{i + 1}", 'x')
        except FileExistsError:
            inv = open(f"inventory{i + 1}", 'w')

        json.dump(['basicRange'] + ["empty"] * 99, inv)
        inv.close()

file = 0
while file not in [1, 2, 3, 4]:
    try:
        file = int(input('Choose a file (1-4): '))
    except ValueError:
        print("That was improper.")

spritesForInventoryItems = {
    'basicRange'     : IMAGES['images/pistolInInventory.png'],
    'basicSpread'    : IMAGES['images/basicSpreadInInventory.png'],
    'mandible'       : IMAGES['images/mandibleInInventory.png'],
    'chunkOfCactus'  : IMAGES['images/chunkOfCactus.png'],
    'wobbegongCloak' : IMAGES['images/wobbegongCloak.png'],
    'bagOfSand'      : IMAGES['images/bagOfSand.png']
}

theCraftingBox = CraftingBox()
mouseMarkerTarget = MouseMarkerTarget()

p = Player()

p.save(file)
p.hp = 0
p.updateStats()

rooms = Rooms()

rooms.makeRooms(16, 'desert')
rooms.addDoors()

for i in range(10):
    p.addItemToInventory(Item(0, 'basicSpread'), 805, 450)

while True:
    while p.hp > 1:
        if p.pause == 0 and p.inventoryShown == 0:
            p.move()
            p.checkDroppedItemCollision()

            for resource in coordinateToRoom(p.room)[1].destructibleMaterialSource:
                if resource.hp < 1:
                    resource.drop_resources()

                    try:
                        coordinateToRoom(p.room)[1].destructibleMaterialSource.remove(resource)
                    except ValueError:
                        pass

            p.showHealthAndStamina()
            p.useActiveItem()

            coordinateToRoom(p.room)[1].updateBullets()

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

            for adversary in coordinateToRoom(p.room)[1].foes:
                if adversary.hp <= 0:
                    coordinateToRoom(p.room)[1].foes.remove(adversary)
                    if adversary in coordinateToRoom(p.room)[1].antlions:
                        coordinateToRoom(p.room)[1].antlions.remove(adversary)

                    elif adversary in coordinateToRoom(p.room)[1].wobbegongs:
                        coordinateToRoom(p.room)[1].wobbegongs.remove(adversary)

                    elif adversary in coordinateToRoom(p.room)[1].ironAngels:
                        coordinateToRoom(p.room)[1].ironAngels.remove(adversary)

                    if len(coordinateToRoom(p.room)[1].foes) == 0:
                        play('music/desertCalm.mp3')

                    p.healByKill()
                    p.loot(adversary.drops, adversary.place.centerx, adversary.place.centery)

                checkCollision(adversary, p)

                for resource in coordinateToRoom(p.room)[1].destructibleMaterialSource:
                    checkCollision(adversary, resource)

                adversary.move()

            for projectile in coordinateToRoom(p.room)[1].enemyBullets.copy():
                projectile.move()
                checkCollision(projectile, p)

                for material in coordinateToRoom(p.room)[1].destructibleMaterialSource:
                    checkCollision(projectile, material)

            for bullet in p.bullets.copy():
                bullet.move()

                for material in coordinateToRoom(p.room)[1].destructibleMaterialSource:
                    checkCollision(bullet, material)

                for foe in coordinateToRoom(p.room)[1].foes:
                    if foe.vulnerable == 1:
                        checkCollision(bullet, foe)

            p.updateStats()
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

    for i in range(256):
        p.display.fill((255 - i, 255 - i, 255 - i))
        for i in range(5):
            pygame.display.flip()