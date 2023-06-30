import pygame
import random
import json

def play(song):
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.set_volume(2)
    pygame.mixer.music.play(-1)

def alphabetize_list(list):
    return sorted(list)

def get_lesser(a, b):
    return a if a < b else b

def return_unless_negative(number):
    return number if number > 0 else 0

def negative_or_positive(num=1):
    return -num if random.randint(0, 1) == 0 else num

class Inventory_Box:
    def __init__(self, centerx, centery, sprite=pygame.image.load('images/inventory_box.png')):
        self.sprite = sprite
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery

class Bullet:
    def __init__(self, hr, vr, damage, firer, melee=0, linger=400, sprite=None, piercing=0):
        self.piercing = piercing
        self.hurt_targets = []
        self.damage = damage
        self.linger = linger
        self.melee = melee
        self.firer = firer
        self.hr = hr
        self.vr = vr

        # Set correct sprite based on firer
        if firer == p:
            if p.inventory[p.active_item].type == "mandible":
                self.sprite = pygame.image.load('images/player_meele_w.png')
            elif p.inventory[p.active_item].type == "basic range":
                self.sprite = pygame.image.load('images/PP2.png')
            elif p.inventory[p.active_item].type == "basic spread":
                self.sprite = pygame.image.load('images/PP2.png')
        else:
            self.sprite = pygame.image.load('images/hp3.bmp')
            if self.firer.type == "iron angel" or self.firer.type == "wobbegong":
                self.sprite = pygame.image.load('images/IAP.png')
            elif self.firer.type == "antlion":
                if self.melee == 1:
                    self.sprite = pygame.image.load('images/lionmeleea2.png')
                else:
                    self.sprite = pygame.image.load('images/player_meele_w.png')
            elif self.firer == p and p.inventory[p.active_item].type == "mandible":
                self.sprite = pygame.image.load('images/player_meele_w.png')

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
                    coordinate_to_room(p.room)[1].enemy_bullets.remove(self)
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

play('music/Desert calm.mp3')

file = 0
sprites_for_inventory_items = {
    'basic range'     : pygame.image.load('images/pistol_in_inventory.png'),
    'basic spread'    : pygame.image.load('images/basic_spread_in_inventory.png'),
    'mandible'        : pygame.image.load('images/mandible_in_inventory.png'),
    'chunk of cactus' : pygame.image.load('images/chunk_of_cactus.png'),
    'wobbegong cloak' : pygame.image.load('images/wobbegong_cloak.png'),
    'bag of sand'     : pygame.image.load('images/bag_of_sand.png')
}

font = {}
for i in "abcdefghijklmnopqrstuvwxyz":
    font[i] = pygame.image.load(f'images/letter_{i}.png')

deleted_save_text = input("Type bwhufkwevfguavesfytidsgvweyih wvetfyuh igweqyf 34qerjf breufveuywfeb wejfyuvwe k.f bwe hukaymjbui34wketf e8.ofhgq4yurf3 we,h and then a number to delete the save of the cooresponding number.:").lower()
for number in range(4):
    if f'bwhufkwevfguavesfytidsgvweyih wvetfyuh igweqyf 34qerjf breufveuywfeb wejfyuvwe k.f bwe hukaymjbui34wketf e8.ofhgq4yurf3 we,h{number + 1}' == deleted_save_text:
        save_number_deleted = number
        inventories = ['inventory', 'inventory2', 'inventory3', 'inventory4']
        material_inventories = ['materials', 'materials2', 'materials3', 'materials4']
        save_deleted = inventories[number]
        material_save_deleted = material_inventories[number]
        with open(save_deleted, 'w') as inv:
            cleared_inventory = ['basic range']
            for number in range(99):
                cleared_inventory.append('empty')
            json.dump(cleared_inventory, inv)
        with open(material_save_deleted, 'w') as mtrl:
            json.dump([0, 0], mtrl)
while not file == 1 and not file == 2 and not file == 3 and not file == 4:
    try:
        file = int(input('Choose a file:'))
    except ValueError:
        print("That was improper.")
class Item:
    def __init__(self, drop_chance, type, qty = 1, max_stack_size = 1):
        self.drop_chance = drop_chance
        self.type = type
        self.dragged = 0
        self.qty = qty
        self.stack_size = max_stack_size
        try:
            self.sprite = sprites_for_inventory_items[self.type]
        except KeyError:
            self.sprite = pygame.image.load('images/PP.png')
        self.place = self.sprite.get_rect()
class Dropped_Item:
    def __init__(self, item, centerx, centery, max_stack_size = 1):
        self.item = item
        try:
            self.sprite = sprites_for_inventory_items[self.item]
        except KeyError:
            self.sprite = pygame.image.load('images/PP.png')
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.stack_size = max_stack_size
class Crafting_Box:
    def __init__(self):
        self.sprite = pygame.image.load('images/Crafting_Box3.png')
        self.place = self.sprite.get_rect()
        self.place.centerx = 1390
        self.place.centery = 450
the_crafting_box = Crafting_Box()
class Word:
    def __init__(self, word, left, top, what_will_be_p):
        self.word = word
        self.total_width = 0
        for letter in word:
            self.total_width += font[letter].get_rect().width
        self.place = pygame.Rect(left, top, self.total_width, 14)
        self.recipient = what_will_be_p
        self.centerx = left + self.total_width / 2
        self.centery = top + 7
    def write(self):
        left = self.place.left
        for letter in self.word:
            self.recipient.display.blit(font[letter], pygame.Rect(left, self.place.top, font[letter].get_rect().width, font[letter].get_rect().height))
            left += font[letter].get_rect().width
    def check_collision_with_mouse(self):
        if abs(self.centerx - pygame.mouse.get_pos()[0]) < self.total_width / 2 and abs(self.centery - pygame.mouse.get_pos()[1]) < 7:
            return 1
        else:
            return 0

class Player:
    def __init__(self):
        self.display = pygame.display.set_mode((1600, 900))
        self.bullets = []
        self.craft_button = Word('craft', 1355, 650, self)
        self.fire_rate = 0
        self.slide_frames_remaining = 0
        self.inventory_shown = 0
        self.dash_frames_remaining = 0
        self.active_item = 0
        self.healing_by_kill = 65
        self.max_hp = 130
        self.pause = 0
        self.empty_slots = []
        self.one_hp_save_cooldown = 0
        self.background = (150, 120, 60)
        self.sprite = pygame.image.load('images/PRO.png')
        self.place = self.sprite.get_rect()
        self.place.bottom = 450
        self.place.left = 805
        self.basic_strike_color = (0, 0, 0)
        self.basic_attacking = 0
        self.speed = 1
        self.invincibility = 0
        self.basic_attack_linger = 0
        self.fire_cooldown = 0
        self.vr = 0
        self.firing = 0
        self.room = [0, 0, 0]
        self.hr = 0
        self.hp = 130
        self.hr_while_dashing = 0
        self.vr_while_dashing = 0
        self.death_anim_frames = []
        self.stamina_regen_rate = 1.5
        self.death_anim = []
        for number in range(19):
            self.death_anim_frames.append(pygame.image.load(f'images/death_frame_{number + 1}.png'))
        for death_frame in self.death_anim_frames:
            for number in range(5):
                self.death_anim.append(death_frame)
        self.stamina = 0
        self.direction = 's'
        self.animation_frame = 0
        self.center = [self.place.centerx, self.place.centery]
        self.walking_anim = {'d': [], 's': [], 'a': [], 'w': []}
        self.idle_anim = {'d': [pygame.image.load('images/Walking_Anim_d_1.png')], 'w': [pygame.image.load('images/Walking_Anim_w_1.png')],'a': [pygame.image.load('images/Walking_Anim_a_1.png')],'s': [pygame.image.load('images/Walking_Anim_s_1.png')]}
        self.d_walking_anim = [pygame.image.load('images/Walking_Anim_d_1.png'),
                               pygame.image.load('images/Walking_Anim_d_2.png'),
                               pygame.image.load('images/Walking_Anim_d_3.png'),
                               pygame.image.load('images/Walking_Anim_d_4.png')]
        for image in self.d_walking_anim:
            for number in range(20):
                self.walking_anim['d'].append(image)
        self.s_walking_anim = [pygame.image.load('images/Walking_Anim_s_1.png'),
                               pygame.image.load('images/Walking_Anim_s_2.png'),
                               pygame.image.load('images/Walking_Anim_s_3.png'),
                               pygame.image.load('images/Walking_Anim_s_4.png')]
        for image in self.s_walking_anim:
            for number in range(20):
                self.walking_anim['s'].append(image)
        self.a_walking_anim = [pygame.image.load('images/Walking_Anim_a_1.png'),
                               pygame.image.load('images/Walking_Anim_a_2.png'),
                               pygame.image.load('images/Walking_Anim_a_3.png'),
                               pygame.image.load('images/Walking_Anim_a_4.png')]
        for image in self.a_walking_anim:
            for number in range(20):
                self.walking_anim['a'].append(image)
        self.w_walking_anim = [pygame.image.load('images/Walking_Anim_w_1.png'),
                               pygame.image.load('images/Walking_Anim_w_2.png'),
                               pygame.image.load('images/Walking_Anim_w_3.png'),
                               pygame.image.load('images/Walking_Anim_w_4.png')]
        for image in self.w_walking_anim:
            for number in range(20):
                self.walking_anim['w'].append(image)
        try:
                self.load(file)
        except json.decoder.JSONDecodeError:
            self.inventory = [Item(100, "basic range")]
            for number in range(99):
                self.inventory.append(Item(1, "empty"))
                self.empty_slots.append(Item(1, "empty"))
        self.load_materials(file)
        for number in range(59):
            self.inventory[40 + number] = Item(0, 'empty')
        self.hpmark = pygame.Rect(0, 25, self.hp * 5, 25)
        self.hpcolor = (205, 48, 114)
        self.hotbar = {}
        self.inventory[99] = Item(0, 'empty')
        self.recipes = {('basic spread',): (Item(0, 'bag of sand'),)}
        self.bullet_sprites_for_basic_range = {'d': pygame.image.load('images/basic_range_projectile_d_v2.png'),
                               'w': pygame.image.load('images/basic_range_projectile_w_v2.png'),
                               'a': pygame.image.load('images/basic_range_projectile_a_v2.png'),
                               's': pygame.image.load('images/basic_range_projectile_s_v2.png')}
        self.shell_sprites_for_basic_spread = {'d': pygame.image.load('images/basic_spread_projectile_d.png'),
                                               'w': pygame.image.load('images/basic_spread_projectile_w.png'),
                                               'a': pygame.image.load('images/basic_spread_projectile_a.png'),
                                               's': pygame.image.load('images/basic_spread_projectile_s.png')}
        self.animation = self.idle_anim[self.direction]
        self.undirected_animation = self.idle_anim
        for number in range(8):
            self.hotbar[number + 1] = "empty"
        self.update_stats()
    def drop_item(self, item):
        for number in range(item.qty):
            coordinate_to_room(self.room)[1].items_dropped.append(Dropped_Item(item.type, self.place.centerx, self.place.centery, max_stack_size=item.stack_size))
            self.update_stats()
    def craft(self):
        ingredients = []
        for item in self.inventory:
            if check_collision_not_for_damage(item, the_crafting_box) == 1 and not item.type == 'empty':
                for number in range(item.qty):
                    ingredients.append(item.type)
        ingredients = alphabetize_list(ingredients)
        ingredients = tuple(ingredients)
        print(ingredients)
        print(self.recipes)
        try:
            for item in self.recipes[ingredients]:
                self.update_stats()
                self.add_item_to_inventory(item, self.place.centerx, self.place.centery)
        except KeyError:
            for item in self.inventory[40: 100]:
                if not item.type == 'empty':
                    self.update_stats()
                    self.drop_item(item)
        for number in range(59):
            self.inventory[number + 40].type = 'empty'
        for item in self.inventory:
            print(item.type + str(item.qty))
    def load_materials(self, file):
        self.materials = {'pharaoh sand': 0, 'pharaoh steel': 0}
        try:
            if  file == 1:
                with open('materials', 'r') as materials_list:
                    materials = json.load(materials_list)
                    self.materials['pharaoh sand'] = materials[0]
                    self.materials['pharaoh steel'] = materials[1]
            if file == 2:
                with open('materials2', 'r') as materials_list:
                    materials = json.load(materials_list)
                    self.materials['pharaoh sand'] = materials[0]
                    self.materials['pharaoh steel'] = materials[1]
            if file == 3:
                with open('materials3', 'r') as materials_list:
                    materials = json.load(materials_list)
                    self.materials['pharaoh sand'] = materials[0]
                    self.materials['pharaoh steel'] = materials[1]
            if file == 4:
                with open('materials4', 'r') as materials_list:
                    materials = json.load(materials_list)
                    self.materials['pharaoh sand'] = materials[0]
                    self.materials['pharaoh steel'] = materials[1]
        except json.decoder.JSONDecodeError:
            pass
            self.materials = {'pharaoh sand': 0, 'pharaoh steel': 0}
    def save(self, file):
        if file == 1:
            with open('inventory', "w") as inventory:
                items = []
                for item in self.inventory:
                    items.append(item.type)
                json.dump(items, inventory)
            with open('materials', 'w') as materials:
                json.dump([self.materials['pharaoh sand'], self.materials['pharaoh steel']], materials)
        if file == 2:
            with open('inventory2', "w") as inventory:
                items = []
                for item in self.inventory:
                    items.append(item.type)
                json.dump(items, inventory)
            with open('materials2', 'w') as materials:
                json.dump([self.materials['pharaoh sand'], self.materials['pharaoh steel']], materials)
        if file == 3:
            with open('inventory3', "w") as inventory:
                items = []
                for item in self.inventory:
                    items.append(item.type)
                json.dump(items, inventory)
            with open('materials3', 'w') as materials:
                json.dump([self.materials['pharaoh sand'], self.materials['pharaoh steel']], materials)
        if file == 4:
            with open('inventory4', "w") as inventory:
                items = []
                for item in self.inventory:
                    items.append(item.type)
                json.dump(items, inventory)
            with open('materials4', 'w') as materials:
                json.dump([self.materials['pharaoh sand'], self.materials['pharaoh steel']], materials)
    def load(self, file):
        if file == 1:
            with open('inventory', "r") as inventory:
                storage = json.load(inventory)
                self.inventory = []
                for item in storage:
                    self.inventory.append(Item(0, item))
        if file == 2:
            with open('inventory2', "r") as inventory:
                storage = json.load(inventory)
                self.inventory = []
                for item in storage:
                    self.inventory.append(Item(100, item))
        if file == 3:
            with open('inventory3', "r") as inventory:
                storage = json.load(inventory)
                self.inventory = []
                for item in storage:
                    self.inventory.append(Item(100, item))
        if file == 4:
            with open('inventory4', "r") as inventory:
                storage = json.load(inventory)
                self.inventory = []
                for item in storage:
                    self.inventory.append(Item(100, item))
        self.hp = 130
        self.place.centery = 450
        self.place.centerx = 805
        self.bullets = []
        self.room = [0, 0, 0]
        self.dash_frames_remaining = 0
        self.animation = self.idle_anim['s']
        self.undirected_animation = self.idle_anim
        play('music/Desert calm.mp3')
    def heal_by_kill(self):
        if self.hp < self.max_hp - self.healing_by_kill:
            self.hp += self.healing_by_kill
        else:
            self.hp = self.max_hp
    def add_item_to_inventory(self, item, centerx, centery):
        for thing in self.inventory:
            if thing.type == item.type:
                for number in range(get_lesser(item.stack_size - thing.qty, item.qty)):
                    if thing.qty < thing.stack_size and item.qty > 0:
                        thing.qty += 1
                        item.qty -= 1
                    else:
                        break
        while item.qty > 0:
            if len(self.standard_inventory) - len(self.empty_slots) < 30:
                self.update_stats()
                replaced_slot = self.inventory.index(self.empty_slots[0])
                self.inventory[replaced_slot] = Item(item.drop_chance, item.type, qty=item.qty, max_stack_size=item.stack_size)
                item.qty = 0
                self.empty_slots.pop(0)
                print('wtf is wrong')
                self.update_stats()
            else:
                coordinate_to_room(self.room)[1].items_dropped.append(Dropped_Item(item.type, centerx, centery, max_stack_size=item.stack_size))
                item.qty -= 1
        self.update_stats()
        print('an item was added')
        self.save(file)
        print(str(item.qty) + "add")
    def loot(self, items, centerx, centery):
        for item in items:
            if not type(item) == None:
                if random.randint(1, 100) <= item.drop_chance or item.type == 'wobbegong cloak':
                    self.add_item_to_inventory(item, centerx, centery)
                    self.update_stats()
                    self.save(file)
    def animation_swap(self, animation, direction):
        self.animation = animation[direction]
        self.undirected_animation = animation
        self.animation_frame = 0
    def turn(self, direction):
        self.animation = self.undirected_animation[direction]
    def check_for_collision_with_dropped_items(self):
        for item in coordinate_to_room(self.room)[1].items_dropped:
            if check_collision_not_for_damage(self, item) == 1:
                self.add_item_to_inventory(Item(0, item.item, max_stack_size=item.stack_size), item.place.centerx, item.place.centery)
                try:
                    coordinate_to_room(self.room)[1].items_dropped.remove(item)
                except ValueError:
                    pass
    def get_direction(self, x, y):
        if abs(x) > abs(y):
            if x > 0:
                return 'd'
            else:
                return 'a'
        else:
            if y > 0:
                return 's'
            else:
                return 'w'
    def update_stats(self):
        self.speed = 0.4564567456845764587650486745096845768945678945670
        self.recipes = {('bag of sand',): (Item(0, 'basic spread'),), ('basic spread',): (Item(0, 'bag of sand'),)}
        self.standard_inventory = self.inventory[0: 30]
        self.accessories = self.inventory[30: 37]
        self.stamina_regen_rate = 1.5
        if self.check_for_item_in_accessories('wobbegong cloak') == 1:
            self.stamina_regen_rate += 0.35
        if self.slide_frames_remaining > 0:
            self.speed *= 4
        if abs(self.hr) > 0 or abs(self.vr) > 0:
            self.direction = self.get_direction(self.hr, self.vr)
        self.animation_frame += 1
        if self.hr == 0 and self.vr == 0 and self.undirected_animation == self.walking_anim:
                self.animation = self.idle_anim[self.direction]
                self.undirected_animation = self.idle_anim
        if self.animation_frame >= len(self.animation):
            self.animation_frame = 0
            if self.hr == 0 and self.vr == 0:
                self.animation = self.idle_anim[self.direction]
                self.undirected_animation = self.idle_anim
            else:
                self.animation = self.walking_anim[self.get_direction(self.hr, self.vr)]
                self.undirected_animation = self.walking_anim
        self.sprite = self.animation[self.animation_frame]
        self.stamina -= self.stamina_regen_rate
        if self.stamina < 0:
            self.stamina = 0
        self.dash_frames_remaining -= 1
        self.slide_frames_remaining -= 1
        for number in range(10):
            self.hotbar[number] = self.inventory[number].type
        pathx = path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[0] * 3
        pathy = path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[1] * 3
        if self.firing == 1:
            self.turn(self.get_direction(pathx, pathy))
        else:
            self.turn(self.get_direction(self.hr, self.vr))
        self.empty_slots = []
        for item in self.standard_inventory:
            if item.type == "empty":
                self.empty_slots.append(item)
        if len(self.empty_slots) == 30:
            self.inventory[0] = Item(0, 'basic range')
            for item in self.standard_inventory:
                if item.type == "empty":
                    self.empty_slots.append(item)
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS and self.inventory_shown == 1:
                    for item in self.inventory:
                        if item.dragged == 1:
                            item_dropped_index = self.inventory.index(item)
                            coordinate_to_room(p.room)[1].items_dropped.append(Dropped_Item(item.type, 800, 450, max_stack_size=item.stack_size))
                            self.inventory[item_dropped_index] = Item(0, 'empty')
                            self.update_stats()
                            self.save(file)
                if event.key == pygame.K_ESCAPE:
                    if self.pause == 0:
                        self.pause = 1
                        self.pause = 1
                    else:
                        self.pause = 0
                if event.key == pygame.K_w:
                    self.vr -= 10
                if event.key == pygame.K_a:
                    self.hr -= 10
                if event.key == pygame.K_s:
                    self.vr += 10
                if event.key == pygame.K_d:
                    self.hr += 10
                if event.key == pygame.K_l:
                    if self.inventory_shown == 0:
                        self.inventory_shown = 1
                    else:
                        self.inventory_shown = 0
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.dash()
                if event.key == pygame.K_TAB or pygame.key.get_mods() & pygame.KMOD_CTRL or pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.slide()
                if event.key == pygame.K_0:
                    self.active_item = 0
                if event.key == pygame.K_1:
                    self.active_item = 1
                if event.key == pygame.K_2:
                    self.active_item = 2
                if event.key == pygame.K_3:
                    self.active_item = 3
                if event.key == pygame.K_4:
                    self.active_item = 4
                if event.key == pygame.K_5:
                    self.active_item = 5
                if event.key == pygame.K_6:
                    self.active_item = 6
                if event.key == pygame.K_7:
                    self.active_item = 7
                if event.key == pygame.K_8:
                    self.active_item = 8
                if event.key == pygame.K_9:
                    self.active_item = 9
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
                if self.inventory_shown == 1:
                    if self.craft_button.check_collision_with_mouse() == 1:
                        self.craft()
                    you_are_dragging_an_item = False
                    for item in self.inventory:
                        if item.dragged == 1:
                            you_are_dragging_an_item = True
                            dragged_item = item
                            shall_drop = 1
                            break
                    if you_are_dragging_an_item:
                        if check_collision_not_for_damage(dragged_item, the_crafting_box) == 1:
                            for item in self.inventory[40: 100]:
                                if item.type == 'empty':
                                    dragged_item.dragged = 0
                                    item1 = self.inventory.index(dragged_item)
                                    item2 = self.inventory.index(item)
                                    self.inventory[item1] = item
                                    self.inventory[item2] = dragged_item
                                    shall_drop = 0
                                    break
                        for item in self.inventory:
                            if detect_mouse_collision(item) == 1 and not item == dragged_item:
                                item1 = self.inventory.index(item)
                                item2 = self.inventory.index(dragged_item)
                                self.inventory[item1] = dragged_item
                                self.inventory[item2] = item
                                item.dragged = 1
                                shall_drop = 0
                                dragged_item.dragged = 0
                        if shall_drop == 1:
                            for item in self.inventory:
                                item.dragged = 0
                    else:
                        for item in self.inventory:
                            if detect_mouse_collision(item) == 1:
                                item.dragged = 1
            if event.type == pygame.MOUSEBUTTONUP:
                self.firing = 0
    def switch_song(self):
        if coordinate_to_room(self.room)[1].biome == "desert" and self.room[2] == 0:
            if not len(coordinate_to_room(self.room)[1].foes) == 0:
                play('music/Desert fight.mp3')
    def check_for_item_in_accessories(self, item_type):
        for item in self.accessories:
            if item.type == item_type:
                return 1
        return 0
    def show_inventory(self):
        self.display.blit(the_crafting_box.sprite, the_crafting_box.place)
        self.craft_button.write()
        for numerical_symbol in range(30):
            self.inventory[numerical_symbol].place.left = numerical_symbol * 60 - 600 * floor_when_num_is_positive(numerical_symbol / 10) + 590
            self.inventory[numerical_symbol].place.top = 280 + 130 * floor_when_num_is_positive(numerical_symbol / 10)
            self.display.blit(Inventory_Box(numerical_symbol * 60 - 600 * floor_when_num_is_positive(numerical_symbol / 10) + 610, 305 + 130 * floor_when_num_is_positive(numerical_symbol / 10)).sprite, (Inventory_Box(numerical_symbol * 60 - 600 * floor_when_num_is_positive(numerical_symbol / 10) + 610, 305 + 130 * floor_when_num_is_positive(numerical_symbol / 10)).place))
            if self.inventory[numerical_symbol].dragged == 1:
                self.inventory[numerical_symbol].place.centerx = pygame.mouse.get_pos()[0]
                self.inventory[numerical_symbol].place.centery = pygame.mouse.get_pos()[1]
        for number in range(7):
            self.inventory[number + 30].place.left = number * 60 + 590
            self.inventory[number + 30].place.top = 670
            self.display.blit(
                Inventory_Box(number * 60 + 610, 695, sprite=pygame.image.load('images/accessory_box2.png')).sprite,
                Inventory_Box(number * 60 + 610, 695).place)
            if self.inventory[number + 30].dragged == 1:
                self.inventory[number + 30].place.centerx = pygame.mouse.get_pos()[0]
                self.inventory[number + 30].place.centery = pygame.mouse.get_pos()[1]
        for item in self.inventory:
            if not item.type == 'empty':
                self.display.blit(item.sprite, item.place)
    def show_hp(self):
        hpbarsprite = pygame.image.load('images/HPBAR2.png')
        hpbarspriteplace = hpbarsprite.get_rect()
        hpbarspriteplace.x += 10
        p.display.blit(hpbarsprite, hpbarspriteplace)
        self.hpmark = pygame.Rect(41, 30, self.hp * 130 / self.max_hp, 18)
        self.display.fill(self.hpcolor, self.hpmark)
    def show_stamina(self):
        staminamark = pygame.Rect(41, 89, 96 - 96 * return_unless_negative(self.stamina) / 315, 14)
        self.display.fill((53, 28, 117), staminamark)
    def show_hp_and_stamina(self):
        self.show_hp()
        self.show_stamina()
    def move(self):
        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]
        self.input()
        self.update_stats()
        if not self.animation_frame == 0:
            self.animation_frame -= 1
        if self.dash_frames_remaining < 1:
            self.center[1] += self.vr * self.speed
            self.center[0] += self.hr * self.speed
        else:
            self.center[1] += self.vr_while_dashing
            self.center[0] += self.hr_while_dashing
        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]
        for material in coordinate_to_room(self.room)[1].destructible_environmental_material_sources:
            while check_collision_not_for_damage(self, material) == 1:
                if self.dash_frames_remaining < 1 and self.hr ** 2 + self.vr ** 2 > 0:
                    self.center[0] -= self.hr
                    self.center[1] -= self.vr
                else:
                    self.center[0] -= self.hr_while_dashing
                    self.center[1] -= self.vr_while_dashing
                self.place.centerx = self.center[0]
                self.place.centery = self.center[1]
        for projectile in self.bullets:
            if projectile.melee == 1:
                projectile.place.x += self.hr * self.speed
                projectile.place.y += self.vr * self.speed
        if self.center[1] - self.place.height / 2 < 0:
            if [self.room[0], self.room[1] + 1, self.room[2]] in rooms.room_coordinates and coordinate_to_room(self.room)[1].foes == [] and 750 < self.center[0] < 850:
                coordinate_to_room(self.room)[1].enemy_bullets = []
                self.room[1] += 1
                self.center[1] = 900 - self.place.height / 2
                self.center[0] = 800
                self.bullets = []
                self.pause = 1
                self.dash_frames_remaining = -1
                self.stamina = 0
                rooms.re_add_foes()
                self.switch_song()
            else:
                self.center[1] = self.place.height / 2
        if self.center[1] + self.place.height / 2 > 900:
            if [self.room[0], self.room[1] - 1, self.room[2]] in rooms.room_coordinates and coordinate_to_room(self.room)[1].foes == [] and 750 < self.center[0] < 850:
                coordinate_to_room(self.room)[1].enemy_bullets = []
                self.room[1] -= 1
                self.bullets = []
                self.center[1] = self.place.height / 2
                self.center[0] = 800
                self.pause = 1
                self.dash_frames_remaining = -1
                self.stamina = 0
                rooms.re_add_foes()
                self.switch_song()
            else:
                self.center[1] = 900 - self.place.height / 2
        if self.center[0] - self.place.width / 2 < 0:
            if [self.room[0] - 1, self.room[1], self.room[2]] in rooms.room_coordinates and coordinate_to_room(self.room)[1].foes == [] and 400 < self.center[1] < 500:
                coordinate_to_room(self.room)[1].enemy_bullets = []
                self.room[0] -= 1
                self.center[0] = 1600 - self.place.width / 2
                self.bullets = []
                self.center[1] = 450
                self.pause = 1
                self.dash_frames_remaining = -1
                self.stamina = 0
                rooms.re_add_foes()
                self.switch_song()
            else:
                self.center[0] = self.place.width / 2
        if self.place.center[0] + self.place.width / 2 > 1600:
            if [self.room[0] + 1, self.room[1], self.room[2]] in rooms.room_coordinates and coordinate_to_room(self.room)[1].foes == [] and 400 < self.center[1] < 500:
                coordinate_to_room(self.room)[1].enemy_bullets = []
                self.room[0] += 1
                self.center[0] = self.place.width / 2
                self.bullets = []
                self.center[1] = 450
                self.pause = 1
                self.dash_frames_remaining = -1
                self.stamina = 0
                rooms.re_add_foes()
                self.switch_song()
            else:
                self.center[0] = 1600 - self.place.width / 2
        self.place.centerx = self.center[0]
        self.place.centery = self.center[1]
    def fire_straight(self):
        if self.fire_cooldown < 1 and self.firing == 1:
            pathx = path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[0] * 3
            pathy = path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[1] * 3
            self.bullets.append(Bullet(pathx * 10, pathy * 10, 2, self, sprite=self.bullet_sprites_for_basic_range[self.get_direction(path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[0], path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[1])]))
            self.fire_cooldown = 20
    def use_active_item(self):
        if self.firing == 1 and self.fire_cooldown < 1 and self.dash_frames_remaining < 1 and self.slide_frames_remaining < 1:
            if self.inventory[self.active_item].type == "basic range":
                self.fire_straight()
            if self.inventory[self.active_item].type == "basic spread":
                self.spread_shot_with_basic_spread()
            if self.inventory[self.active_item].type == "mandible":
                self.mandible_attack()
            self.direction = self.get_direction(path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[0], path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[1])
        self.fire_cooldown -= 1
    def fire_semirandomly_not_as_entire_attack(self, damage, linger=300, piercing=0):
        player_pos = [self.place.centerx, self.place.centery]
        mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        self.bullets.append(Bullet(semirandom_path_without_place(player_pos, mouse_pos)[0] * 8, semirandom_path_without_place(player_pos, mouse_pos)[1] * 8, damage, self, sprite=self.shell_sprites_for_basic_spread[self.get_direction(path_without_automatic_place_attribute(p.center, pygame.mouse.get_pos())[0], path_without_automatic_place_attribute(p.center, pygame.mouse.get_pos())[1])], linger=linger, piercing=piercing))
    def spread_shot_with_basic_spread(self):
        if self.fire_cooldown < 1:
            for number in range(7):
                self.fire_semirandomly_not_as_entire_attack(1.3)
            self.fire_cooldown = 30
    def basic_fire_blast(self):
        for number in range(10):
            self.fire_semirandomly_not_as_entire_attack(0.06, linger=20, piercing=100)
    def swing_as_part_of_mandible_attack(self):
        self.bullets.append(Bullet(0, 0, 8, self, melee=1, linger=20, sprite=pygame.image.load('images/lionmeleea2.png')))
    def fire_as_part_of_mandible_attack(self):
        player_pos = [self.place.centerx, self.place.centery]
        mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        self.bullets.append(Bullet(path_without_automatic_place_attribute(player_pos, mouse_pos)[0] * 6, path_without_automatic_place_attribute(player_pos, mouse_pos)[1] * 6, 5, self, piercing=1))
    def mandible_attack(self):
        self.swing_as_part_of_mandible_attack()
        self.fire_as_part_of_mandible_attack()
        self.fire_cooldown = 40
    def dash(self):
        if self.stamina < 1:
            self.dash_frames_remaining = 30
            self.invincibility = 45
            self.hr_while_dashing = 35 * path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[0]
            self.vr_while_dashing = 35 * path_without_automatic_place_attribute(self.center, pygame.mouse.get_pos())[1]
            self.stamina = 315
            for melee_attack in self.bullets:
                if melee_attack.melee == 1:
                    self.bullets.remove(melee_attack)
    def slide(self):
        if self.stamina < 216 and self.dash_frames_remaining < 1 and self.slide_frames_remaining < 1:
            self.slide_frames_remaining = 15
            self.stamina += 100
            for melee_attack in self.bullets:
                if melee_attack.melee == 1:
                    self.bullets.remove(melee_attack)
class Mouse_Marker_Target:
    def __init__(self):
        self.sprite = pygame.image.load('images/mouse_marker_target.png')
        self.place = self.sprite.get_rect()
    def update_position(self):
        self.place.centerx = pygame.mouse.get_pos()[0]
        self.place.centery = pygame.mouse.get_pos()[1]
mouse_marker_target = Mouse_Marker_Target()
def clone_item(item):
    return Item(item.drop_chance, item.type, qty=item.qty, max_stack_size=item.stack_size)
def count_inventory_items(item):
    count = 0
    for thing in p.inventory:
        if thing.type == item:
            count += 1
    return count
class Foe:
    def __init__(self, type, centerx, centery):
        self.type = type
        self.wobbegong_dashing = 0
        self.hr = 0
        self.vulnerable = 1
        self.dash_cooldown_as_wobbegong = 120
        self.multifaced = 0
        self.drops = []
        self.target = p
        self.fire_cooldown = 0
        self.bullets = []

        if self.type == "antlion":
            self.antlion_pause = random.randint(15, 70)
            self.hp = 100
            self.attack = 0
            self.speed = 0
            self.sprite = pygame.image.load('images/active_lionpit.png')
            self.sprites = [pygame.image.load('images/antlion_a.png'), pygame.image.load('images/active_lionpit.png')]
            self.vulnerable = 0
            self.drops = [Item(3, "mandible")]
        else:
            self.does_contact_damage = 1
        self.turret_pause = 20
        self.turret_firing = 0
        self.vr = 0
        if self.type == "iron angel":
            self.sprite = pygame.image.load('images/IAV3.png')
            self.hp = 100
            self.attack = 40
            self.speed = 0
            self.drops = [Item(1, "basic spread")]
        if self.type == "wobbegong":
            self.sprite = pygame.image.load('images/WOBBEGONG.png')
            self.hp = 100
            self.attack = 50
            self.multifaced = 1
            self.dsprite = pygame.image.load('images/WOBBEGONGD.png')
            self.ssprite = pygame.image.load('images/WOBBEGONGS.png')
            self.asprite = pygame.image.load('images/WOBBEGONG.png')
            self.wsprite = pygame.image.load('images/WOBBEGONGW.png')
            self.speed = 2 / sqrt(2)
            self.drops = [Item(1, 'wobbegong cloak')]
        if not self.type == "wobbegong":
            self.wsprite = self.sprite
            self.dsprite = self.sprite
            self.asprite = self.sprite
            self.ssprite = self.sprite
        else:
            self.dsprite = pygame.image.load('images/WOBBEGONGD.png')
            self.ssprite = pygame.image.load('images/WOBBEGONGS.png')
            self.asprite = pygame.image.load('images/WOBBEGONG.png')
            self.wsprite = pygame.image.load('images/WOBBEGONGW.png')
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.center = [self.place.centerx, self.place.centery]
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
        if not self.type == "antlion":
            if self.type == "wobbegong":
                if self.wobbegong_dashing == 0:
                    self.hr = path(self, p)[0] * 0.2
                    self.vr = path(self, p)[1] * 0.2
                self.dash_cooldown_as_wobbegong -= 1
                if self.wobbegong_dashing == 0 and self.dash_cooldown_as_wobbegong < 1:
                    self.dash_as_wobbegong()
            if self.type == "knight":
                self.hr = path(self, p)[0] * 0.2
                self.vr = path(self, p)[1] * 0.2
            if self.type == "iron angel":
                self.vr = 0
                self.hr = 0
            self.center[0] += self.hr
            self.center[1] += self.vr
            self.place.centerx = self.center[0]
            self.place.centery = self.center[1]
            for material in coordinate_to_room(p.room)[1].destructible_environmental_material_sources:
                if not self.type == 'antlion':
                    while check_collision_not_for_damage(self, material) == 1:
                        if self.wobbegong_dashing == 1:
                            self.spread_shot_as_wobbegong()
                            self.wobbegong_dashing = 0
                        check_collision(self, material)
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
                self.accelerate()
                if self.type == "wobbegong" and self.wobbegong_dashing == 1:
                    self.spread_shot_as_wobbegong()
                self.wobbegong_dashing = 0
            if self.place.right >= 1600:
                self.place.right = 1600
                self.accelerate()
                if self.type == "wobbegong" and self.wobbegong_dashing == 1:
                    self.spread_shot_as_wobbegong()
                self.wobbegong_dashing = 0
            if self.place.top <= 0:
                self.place.top = 0
                self.accelerate()
                if self.type == "wobbegong" and self.wobbegong_dashing == 1:
                    self.spread_shot_as_wobbegong()
                self.wobbegong_dashing = 0
            if self.place.bottom >= 900:
                self.place.bottom = 900
                self.accelerate()
                if self.type == "wobbegong" and self.wobbegong_dashing == 1:
                    self.spread_shot_as_wobbegong()
                self.wobbegong_dashing = 0
            if random.randint(1, 100) == 1 and self.wobbegong_dashing == 0:
                self.accelerate()
        else:
            self.speed = 0
            self.hr = 0
            self.vr = 0
        p.display.blit(self.sprite, self.place)
    def fire_straight(self, target):
        self.bullets.append(Bullet(path(self, target)[0], path(self, target)[1], 34, self))
    def fire_straight_to_point(self, point):
        self.bullets.append(Bullet(path_without_automatic_place_attribute(self.center, point)[0], path_without_automatic_place_attribute(self.center, point)[1], 34, self))
    def fire_straight_as_turret(self, target):
        self.bullets.append(Bullet(path(self, target)[0] / 3, path(self, target)[1] / 3, 50, self))
    def spread_shot_as_wobbegong(self):
        for number in range(7):
            self.fire_semirandomly(p)
    def burrow_as_antlion(self):
        self.antlion_pause -= 1
        if self.vulnerable == 1 and self.antlion_pause < 1:
            self.sprite = pygame.image.load('images/active_lionpit.png')
            self.place = self.sprite.get_rect()
            self.place.centerx = p.place.centerx
            self.place.centery = p.place.centery
            self.antlion_pause = 25
            self.vulnerable = 0
    def attack_as_antlion(self):
        self.burrow_as_antlion()
        if self.antlion_pause < 1 and self.vulnerable == 0:
            consistent_place = [self.place.centerx, self.place.centery]
            self.sprite = pygame.image.load('images/antlion_a.png')
            self.place = self.sprite.get_rect()
            self.place.centerx = consistent_place[0]
            self.place.centery = consistent_place[1]
            self.bullets.append(Bullet(0, 0, 40, self, melee=1, linger = 65))
            for number in range(2):
                self.bullets.append(Bullet(semirandom_path(self, p)[0], semirandom_path(self, p)[1], 40, self, linger=150))
            self.antlion_pause = 70
            self.vulnerable = 1
    def fire_predictively_as_lobster(self):
        self.fire_cooldown -= 1
        if -100 <self.fire_cooldown < 1:
            self.fire_predictively_to_p(12)
        if self.fire_cooldown < -100:
            self.fire_cooldown = 60
    def fire_predictively_to_p(self, speed):
        self.bullets.append(Bullet(predictive_path_to_p(self, speed)[0], predictive_path_to_p(self, speed)[1], 35, self, sprite=pygame.image.load('images/IAP.png')))
    def fire_semirandomly(self, target):
        self.bullets.append(Bullet(semirandom_path(self, target)[0] * 1.5, semirandom_path(self, target)[1] * 1.5, 34, self))
    def spread_shot_as_turret(self):
        if self.fire_cooldown < 1:
            for number in range(9):
                self.fire_semirandomly(p)
            self.fire_cooldown = 130
        else:
            self.fire_cooldown -= 1
    def dash_as_wobbegong(self):
        if self.wobbegong_dashing == 0:
            self.hr = path(self, p)[0] * 0.5
            self.vr = path(self, p)[1] * 0.5
            self.wobbegong_dashing = 1
            self.dash_cooldown_as_wobbegong = random.randint(120, 240)
    def update_drops(self):
        if self.type == "wobbegong":
            self.drops = [Item(1, "wobbegong cloak")]
        if self.type == "antlion":
            self.drops = [Item(3, "mandible")]
        if self.type == "iron angel":
            self.drops = [Item(1, "basic spread")]
class Room:
    def __init__(self, coordinate, biome, depth = 0):
        self.coordinate = [coordinate[0], coordinate[1], depth]
        self.biome = biome
        self.destructible_environmental_material_sources = [Destructible_Environmental_Material_Source(1200, 675, 'chunk of cactus', pygame.image.load('images/destructible_cactus.png'), 200, random.randint(2, 3))]
        try:
            if type(coordinate_to_room([coordinate[0], coordinate[1], 0])) == tuple and not depth == 0:
                self.biome = coordinate_to_room([coordinate[0], coordinate[1], 0])[1].biome
        except NameError:
            pass
        self.iron_angels = []
        self.wobbegongs = []
        self.enemy_bullets = []
        self.p_bullets = []
        self.antlions = []
        self.items_dropped = []
        if self.biome == "desert":
            self.background = pygame.image.load('images/DBMN2FIN2.bmp')
        self.background_location = self.background.get_rect()
        self.background_location.centerx = 805
        self.background_location.centery = 450
        self.doors = []
        if self.biome == "desert":
            self.layout = random.randint(1, 4)
            self.foe_types = ['iron angel', 'wobbegong', 'antlion']
        self.difficulty = random.randint(0, 5)
        self.resources = random.randint(0, 3) + self.difficulty
        self.traps = []
        self.foes = []
        self.potential_pits_x = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
        self.potential_pits_y = [50, 850, 450, 300, 600, 600, 300, 50, 850]
        if not self.coordinate == [0, 0, 0] and not self.difficulty == 5:
            if self.layout == 1:
                self.foes = [Foe("iron angel", 50, 50), Foe("iron angel", 50, 850), Foe("iron angel", 1560, 850), Foe("iron angel", 1560, 50)]
                if not self.difficulty > 1:
                    self.foes.pop(random.randint(0, 3))
                    self.foes.pop(random.randint(0, 2))
                if self.difficulty == 1:
                    self.foes.append(Foe("iron angel", 800, 450))
                if self.difficulty == 2:
                    self.traps.append(PitTrap(800, 450))
                    self.foes.pop(random.randint(0, 3))
                if self.difficulty > 2:
                    foe_popped_from_layout_one_with_difficulties_above_two = random.randint(0, 1)
                    self.foes.pop(foe_popped_from_layout_one_with_difficulties_above_two)
                    self.foes.pop(foe_popped_from_layout_one_with_difficulties_above_two + 1)
                    self.foes.append(Foe("wobbegong", 800, 450))
            if self.layout == 2:
                self.foes = [Foe("wobbegong", 800, 450)]
                if self.difficulty == 1:
                    for number in range(5):
                        self.traps.append(PitTrap(800 + random.randint(- number * 40, number * 40), 450 + random.randint(- number * 40, number * 40)))
                if self.difficulty == 2:
                    self.foes = [Foe("wobbegong", 50, 50), Foe("wobbegong", 1560, 850)]
                    self.traps.append(PitTrap(805, 450))
                if self.difficulty > 2:
                    self.foes = [Foe("wobbegong", 50, 50), Foe("wobbegong", 1550, 850), Foe("iron angel", 800, 450)]
            if self.layout == 3:
                self.foes = [Foe("wobbegong", 800, 450), Foe("antlion", 50, 50), Foe("antlion", 1550, 850)]
                if self.difficulty == 0:
                    self.foes.pop(0)
                if self.difficulty == 1 or self.difficulty > 2:
                    self.foes.pop(2)
                if self.difficulty == 2:
                    self.traps = [PitTrap(800, 187), PitTrap(800, 563), PitTrap(400, 450), PitTrap(1200, 450), PitTrap(800, 450)]
                if self.difficulty > 2:
                    for number in range(9):
                        self.traps.append((PitTrap(self.potential_pits_x[number], self.potential_pits_y[number])))
                        self.traps.append(PitTrap(30 + 70 * number, 20 + 50 * number))
            if self.layout == 4:
                for number in range(27):
                    self.traps.append(PitTrap(400, number * 35 + 27))
                for number in range(27):
                    self.traps.append(PitTrap(1200, number * 35 + 27))
                for number in range(9):
                    self.potential_pits_x = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
                    self.potential_pits_y = [50, 850, 450, 300, 600, 600, 300, 50, 850]
                    self.traps.append(PitTrap(self.potential_pits_x[number], self.potential_pits_y[number]))
                self.potential_pits_x = [50, 1550, 800, 685, 925, 685, 925, 1550, 50]
                self.potential_pits_y = [50, 850, 450, 300, 600, 600, 300, 50, 700]
            if self.difficulty > 3:
                for difficulty in range(self.difficulty * 2):
                    self.traps.append(PitTrap(self.potential_pits_x[random.randint(0, 8)] + random.randint(-50, 50), self.potential_pits_y[random.randint(0, 8)] + random.randint(-30, 30)))
            for enemy in self.foes:
                if enemy.type == "iron angel":
                    self.iron_angels.append(enemy)
                if enemy.type == "wobbegong":
                    self.wobbegongs.append(enemy)
                if enemy.type == "antlion":
                    self.antlions.append(enemy)
        self.initial_foes = self.foes
        self.initial_iron_angels = self.iron_angels
        self.initial_wobbegongs = self.wobbegongs
        self.initial_antlions = self.antlions
        self.initial_traps = self.traps
    def update_bullets(self):
        for adversary in self.foes:
            for bullet in adversary.bullets:
                if not bullet in self.enemy_bullets:
                    self.enemy_bullets.append(bullet)
        for range_attack in self.enemy_bullets:
            if range_attack.melee == 1 and not range_attack.firer in self.foes:
                self.enemy_bullets.remove(range_attack)
    def spawn_foes_in_room(self):
        if not self.coordinate == [0, 0, 0]:
            if random.randint(1, 3) == 2 and len(self.foes) < 2 and not self.layout == 4:
                self.foes.append(Foe(self.foe_types[random.randint(0, len(self.foe_types) - 1)], random.randint(500, 1100), random.randint(300, 600)))
            for enemy in self.foes:
                if enemy.type == "iron angel" and not enemy in self.iron_angels:
                    self.iron_angels.append(enemy)
                if enemy.type == "wobbegong" and not enemy in self.wobbegongs:
                    self.wobbegongs.append(enemy)
                if enemy.type == "antlion" and not enemy in self.antlions:
                    self.antlions.append(enemy)
            if random.randint(1, 4) == 1 and len(self.traps) < 4:
                self.traps.append(PitTrap(random.randint(500, 1100), random.randint(300, 600)))
class PitTrap:
    def __init__(self, centerx, centery):
        self.sprite = pygame.image.load('images/LIONPIT.png')
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.attack = 34
class Rooms:
    def __init__(self):
        self.rooms = [Room([0, 0], "desert")]
        self.room_coordinates = [[0, 0, 0]]
    def make_rooms(self, qty, biome, depth=0):
        room = [0, 0, depth]
        for number in range(qty):
            if random.randint(1, 2) == 1:
                while room in self.room_coordinates.copy():
                    adjacent_room = [self.room_coordinates[random.randint(0, len(self.rooms) - 1)][0], self.room_coordinates[random.randint(0, len(self.rooms) - 1)][1], depth]
                    room = [adjacent_room[0] + negative_or_positive(), adjacent_room[1], depth]
            else:
                while room in self.room_coordinates.copy():
                    adjacent_room = [self.room_coordinates[random.randint(0, len(self.rooms) - 1)][0], self.room_coordinates[random.randint(0, len(self.rooms) - 1)][1], depth]
                    room = [adjacent_room[0], adjacent_room[1] + negative_or_positive(), depth]
            self.rooms.append(Room(room, biome))
            self.room_coordinates.append(room)
    def coordinate_to_room(self):
        for room in rooms.rooms:
            if room.coordinate == self:
                return (self.rooms.index(room), room)
        return 0
    def add_doors(self):
        for room in self.room_coordinates:
            if [room[0], room[1] + 1, room[2]] in self.room_coordinates:
                coordinate_to_room(room)[1].doors.append(Door(800, 20))
            if [room[0], room[1] - 1, room[2]] in self.room_coordinates:
                coordinate_to_room(room)[1].doors.append(Door(800, 880))
            if [room[0] - 1, room[1], room[2]] in self.room_coordinates:
                coordinate_to_room(room)[1].doors.append(Door(20, 450))
            if [room[0] + 1, room[1], room[2]] in self.room_coordinates:
                coordinate_to_room(room)[1].doors.append(Door(1580, 450))
    def re_add_foes(self):
        for room in self.rooms:
            room.spawn_foes_in_room()
class Door:
    def __init__(self, centerx, centery):
        self.sprite = pygame.image.load('images/door.bmp')
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
def semirandom_path_without_place(a, b):
    return [path_without_automatic_place_attribute(a, b)[0] * 3 + random.randint(-200, 200) / 1000, path_without_automatic_place_attribute(a, b)[1] * 3 + random.randint(-200, 200) / 1000]
def path_without_automatic_place_attribute(a, b):
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
def floor_when_num_is_positive(num):
    result = 0
    while num >= 1:
        num -= 1
        result += 1
    try:
        return result
    except ZeroDivisionError:
        return 0
def sign(a):
    if a > 0:
        return 1
    if a < 0:
        return -1
    if a == 0:
        return 0
def sqrt(a):
    return a ** (1 / 2)
def root(a, b):
    return b ** (1 / a)
class Material_Pickup:
    def __init__(self, sprite, centerx, centery, type):
        self.sprite = sprite
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.type = type
class Destructible_Environmental_Material_Source:
    def __init__(self, centerx, centery, drop, sprite, hp, drops_number, max_stack_size=99):
        self.sprite = sprite
        self.place = self.sprite.get_rect()
        self.place.centerx = centerx
        self.place.centery = centery
        self.drop = drop
        self.hp = hp
        self.drop_stack_size = max_stack_size
        self.qty = drops_number
    def drop_resources(self):
        for number in range(self.qty):
            coordinate_to_room(p.room)[1].items_dropped.append(Dropped_Item(self.drop, self.place.centerx, self.place.centery, max_stack_size = self.drop_stack_size))
        try:
            coordinate_to_room(p.room)[1].destructible_environmental_material_sources.remove(self)
        except ValueError:
            pass
def predictive_path_to_p(attacker, speed):
    hr = p.hr
    vr = p.vr
    a = (hr ** 2 + vr ** 2 - speed ** 2) / speed ** 2
    b = ((p.place.centerx - attacker.place.centerx) * hr + vr * (p.place.centery - attacker.place.centery)) * 2 / speed
    c = p.place.centerx ** 2 - 2 * attacker.place.centerx * p.place.centerx - attacker.place.centerx ** 2 + p.place.centery ** 2 - 2 * attacker.place.centery * p.place.centery - attacker.place.centery ** 2
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
    if nx < 0:
        nx = 0
    if ny > 900:
        ny = 900
    if ny < 0:
        ny = 0
    the_path = path_without_automatic_place_attribute([attacker.place.centerx, attacker.place.centery], [nx, ny])
    if abs(hr) < abs(speed * the_path[0]) and sign(hr) == sign(the_path[0]):
        the_path[0] = path(attacker, p)[0] / 21 + sign(p.hr)
        the_path[1] -= sign(attacker.place.centery - p.place.centery) / 3
    if abs(vr) < abs(speed * the_path[1]) and sign(vr) == sign(the_path[1]):
        the_path[1] = path(attacker, p)[1] / 21 + sign(p.vr)
        the_path[0] -= sign(attacker.place.centerx - p.place.centerx) / 3
    return [speed * the_path[0], speed * the_path[1]]
def coordinate_to_room(coordinate):
    for room in rooms.rooms:
        if room.coordinate == coordinate:
            return (rooms.rooms.index(room), room)
def check_collision(a, b):
    if abs(a.place.centerx - b.place.centerx) < (a.place.width + b.place.width) / 2 and abs(a.place.centery - b.place.centery) < (a.place.height + b.place.height) / 2:
        if type(a) == Bullet:
            if a.melee == 0 and not b in a.hurt_targets:
                try:
                    a.piercing -= 1
                    if a.piercing < 0:
                        try:
                            a.firer.bullets.remove(a)
                        except ValueError:
                            pass
                        try:
                            coordinate_to_room(p.room)[1].enemy_bullets.remove(a)
                        except ValueError:
                            pass
                    a.hurt_targets.append(b)
                    if type(b) == Player and p.invincibility < 1:
                        if not a.damage == 0:
                            b.invincibility = 40
                            b.hp -= a.damage
                        return 1
                    if not type(b) == Player:
                        if a.melee == 1:
                            if not b in a.hurt_targets:
                                b.hp -= a.damage
                                return 1
                        else:
                            b.hp -= a.damage
                            return 1
                except ValueError:
                    pass
        else:
            if type(b) == Player and p.invincibility < 1:
                if b.invincibility < 1:
                    if not a.attack == 0:
                        b.invincibility = 40
                        b.hp -= a.attack
                    return 1
def check_collision_not_for_damage(a, b):
    if abs(a.place.centerx - b.place.centerx) < (a.place.width + b.place.width) / 2 and abs(a.place.centery - b.place.centery) < (a.place.height + b.place.height) / 2:
        return 1
def detect_mouse_collision(a):
    try:
        if abs(a.place.centery - pygame.mouse.get_pos()[1]) < a.place.height / 2 + 10 and abs(a.place.centerx - pygame.mouse.get_pos()[0]) < a.place.width / 2 + 10:
            return 1
        else:
            return 0
    except AttributeError:
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
def semirandom_path(a, b):
    return [path(a, b)[0] / 6 + random.randint(-3200, 3200) / 1000, path(a, b)[1] / 6 + random.randint(-3200, 3200) / 1000]
p = Player()
rooms = Rooms()
rooms.make_rooms(16, 'desert')
p.save(file)
def blit_everything():
    p.display.blit(coordinate_to_room(p.room)[1].background, coordinate_to_room(p.room)[1].background_location)
    for door in coordinate_to_room(p.room)[1].doors:
        p.display.blit(door.sprite, door.place)
    for resource in coordinate_to_room(p.room)[1].destructible_environmental_material_sources:
        p.display.blit(resource.sprite, resource.place)
    p.display.blit(p.sprite, p.place)
    p.show_hp_and_stamina()
    for item in coordinate_to_room(p.room)[1].items_dropped:
        p.display.blit(item.sprite, item.place)
    for trap in coordinate_to_room(p.room)[1].traps:
        p.display.blit(trap.sprite, trap.place)
    for bullet in coordinate_to_room(p.room)[1].enemy_bullets:
        p.display.blit(bullet.sprite, bullet.place)
    for bullet in p.bullets:
        p.display.blit(bullet.sprite, bullet.place)
    for foe in coordinate_to_room(p.room)[1].foes:
        p.display.blit(foe.sprite, foe.place)
    if p.inventory_shown == 1:
        p.show_inventory()
    for number in range(7):
        pygame.display.flip()
rooms.add_doors()
p.hp = 0
p.update_stats()
for number in range(10):
    p.add_item_to_inventory(Item(0, 'basic spread'), 805, 450)
while 1 == 1:
    while p.hp > 1:
        if p.pause == 0 and p.inventory_shown == 0:
            p.move()
            p.check_for_collision_with_dropped_items()
            for resource in coordinate_to_room(p.room)[1].destructible_environmental_material_sources:
                if resource.hp < 1:
                    resource.drop_resources()
                    try:
                        coordinate_to_room(p.room)[1].destructible_environmental_material_sources.remove(resource)
                    except ValueError:
                        pass
            p.show_hp_and_stamina()
            p.use_active_item()
            coordinate_to_room(p.room)[1].update_bullets()
            for trap in coordinate_to_room(p.room)[1].traps:
                if check_collision_not_for_damage(trap, p) == 1 and p.dash_frames_remaining <= 1:
                    coordinate_to_room(p.room)[1].traps.remove(trap)
                    if len(coordinate_to_room(p.room)[1].foes) == 0:
                        play('music/Desert fight.mp3')
                    coordinate_to_room(p.room)[1].foes.append(Foe("antlion", trap.place.centerx, trap.place.centery))
                    coordinate_to_room(p.room)[1].antlions.append(coordinate_to_room(p.room)[1].foes[-1])
            for foe in coordinate_to_room(p.room)[1].iron_angels:
                foe.spread_shot_as_turret()
            for enemy in coordinate_to_room(p.room)[1].antlions:
                enemy.attack_as_antlion()
            for adversary in coordinate_to_room(p.room)[1].foes:
                if adversary.hp <= 0:
                    coordinate_to_room(p.room)[1].foes.remove(adversary)
                    if adversary in coordinate_to_room(p.room)[1].antlions:
                        coordinate_to_room(p.room)[1].antlions.remove(adversary)
                    if adversary in coordinate_to_room(p.room)[1].wobbegongs:
                        coordinate_to_room(p.room)[1].wobbegongs.remove(adversary)
                    if adversary in coordinate_to_room(p.room)[1].iron_angels:
                        coordinate_to_room(p.room)[1].iron_angels.remove(adversary)
                    if len(coordinate_to_room(p.room)[1].foes) == 0:
                        play('music/Desert calm.mp3')
                    p.heal_by_kill()
                    p.loot(adversary.drops, adversary.place.centerx, adversary.place.centery)
                check_collision(adversary, p)
                for resource in coordinate_to_room(p.room)[1].destructible_environmental_material_sources:
                    check_collision(adversary, resource)
                adversary.move()
                adversary.update_drops()
            for projectile in coordinate_to_room(p.room)[1].enemy_bullets.copy():
                projectile.move()
                check_collision(projectile, p)
                for material in coordinate_to_room(p.room)[1].destructible_environmental_material_sources:
                    check_collision(projectile, material)
            for bullet in p.bullets.copy():
                bullet.move()
                for material in coordinate_to_room(p.room)[1].destructible_environmental_material_sources:
                    check_collision(bullet, material)
                for foe in coordinate_to_room(p.room)[1].foes:
                    if foe.vulnerable == 1:
                        check_collision(bullet, foe)
            p.update_stats()
            p.invincibility -= 1
            if p.inventory_shown == 1:
                p.show_inventory()
        p.input()
        blit_everything()
    p.load(file)
    rooms.rooms = []
    rooms.room_coordinates = []
    rooms.make_rooms(16, "desert")
    rooms.add_doors()
    for number in range(256):
        p.display.fill((255 - number, 255 - number, 255 - number))
        for number in range(5):
            pygame.display.flip()