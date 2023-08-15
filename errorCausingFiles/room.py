import random
import os
import pygame
importing = 1
IMAGES = {}
for i in os.listdir("images"):
    if i not in ["font"]:
        IMAGES[f"images/{i}"] = pygame.image.load(f'images/{i}')
FONT = {}
for i in os.listdir("images/font"):
    FONT[i[-5].lower()] = pygame.image.load(f'images/font/{i}')
try:
    class Room:
        def __init__(self, coordinate, biome, num, depth=0):
            try:
                self.biome = biome
                if depth == 1:
                    self.shelterZone = [self]
                    self.blobSpawnTimerAsShelter = 300
                self.teleporters = []
                self.mapImage = IMAGES[f'images/mapImage{random.randint(1, 6)}.png']
                self.found = 0
                self.coordinate = [coordinate[0], coordinate[1], depth]
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
                self.deathLoadCode = []
                for foe in self.foes:
                    self.deathLoadCode.append(f'room.foes.append(Foe("{foe.type}", {foe.place.centerx}, {foe.place.centery}))')
            except NameError:
                pass
        def prepareToSave(self):
            try:
                for foe in self.foes:
                    foe.prepareToSave()
                self.saveCode = ['room.foes = []', 'room.destructibleMaterialSources = []']
                self.saveCode += [foe.saveCode for foe in self.foes] + [resource.saveCode for resource in self.destructibleMaterialSources] + [teleport.saveCode for teleport in self.teleporters]
                self.saveCode.append(f'room.found = {self.found}')
                self.saveCode.append(f'room.cleared = {self.cleared}')
                self.saveCode.append(f'room.background = "{self.background}"')
                self.saveCode.append(f'room.deathLoadCode = {self.deathLoadCode}')
                self.saveCode = tuple(self.saveCode)
            except NameError:
                pass
        def updateBullets(self):
            for enemy in self.foes:
                for bullet in enemy.bullets:
                    if not bullet in self.enemyBullets:
                        self.enemyBullets.append(bullet)

            for attack in self.enemyBullets:
                if attack.melee == 1 and not attack.firer in self.foes:
                    self.enemyBullets.remove(attack)
        def updateFoes(self):
            try:
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
            except NameError:
                pass
        def spawnFoes(self):
            try:
                if not self.coordinate == [0, 0, 0]:
                    if random.randint(1, 3) == 2 and len(self.foes) < 2 and not self.layout == 4:
                        self.foes.append(Foe(self.foe_types[random.randint(0, len(self.foe_types) - 1)], random.randint(500, 1100), random.randint(300, 600)))
                    self.updateFoes()

                    if random.randint(1, 4) == 1 and len(self.traps) < 4 and self.biome == 'desert' and self.coordinate[2] == 0:
                        self.traps.append(PitTrap(random.randint(500, 1100), random.randint(300, 600)))
            except NameError:
                pass
except NameError:
    pass
