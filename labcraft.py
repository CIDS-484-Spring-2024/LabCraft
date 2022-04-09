from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from sims import *

window.borderless = False

app = Ursina()

# block textures
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sun_texture   = load_texture('assets/sun.png')
pendulum_texture = load_texture('assets/mc_brick.png')

# inventory menu icon textures
grass_icon_texture = load_texture('assets/grass_icon.png')
stone_icon_texture = load_texture('assets/stone_icon.png')
brick_icon_texture = load_texture('assets/brick_icon.png')
dirt_icon_texture = load_texture('assets/dirt_icon.png')
sun_icon_texture = load_texture('assets/sun_icon.png')
pendulum_icon_texture = load_texture('assets/mc_brick_icon.png')

# other textures
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
osc_texture   = load_texture('assets/osc_block.png')
earth_texture = load_texture('assets/earth_block.png')
mc_brick      = load_texture('assets/mc_brick.png')
hotbar_cursor_texture = load_texture('assets/hotbar_cursor.png')

punch_sound   = Audio('assets/punch_sound', loop = False, autoplay = False)

""" 
# Block ID Legend:
0: empty hand
1: grass
2: stone
3: brick
4: dirt
5: sun
6: pendulum
 """
block_pick = 0 # default empty hand

# {1: active gameplay}
# {2: inventory menu screen}
game_state = 1 

window.fps_counter.enabled = True
window.exit_button.visible = True

debug = True

def update():
    global block_pick
    global game_state
    global debug


    # === Game States ===

    if held_keys['e']:
        game_state = 2

    if held_keys['q']:
        game_state = 1

    # move arm visually on top of menu, to act like it's a phone(?)
    if game_state == 1: # main game state
        player.enabled = True
        inventory_BG.enabled = False
        inventory.enabled = False

        # animate the hand to move back and forth when clicked
        if held_keys['left mouse'] or held_keys['right mouse']:
            hand.active()
        else:
            hand.passive()
    
    if game_state == 2: # view inventory state
        player.enabled = False
        inventory_BG.enabled = True
        inventory.enabled = True
    

    """ if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5
    if held_keys['6']: block_pick = 6 """

    # if a number key is pressed, 
        # set the hotbar to highlight the corresponding slot number pressed
    #if held_keys['1']:
       #hotbar.set_current_slot(0)



    if held_keys['escape']: 
        quit()
    
    # if player falls through the map, return to starting point.
    if player.position.y < -10:

        if debug == True:
            print("falling!")
        
        player.y = 1
        player.x = 1
        player.z = 1

""" 
# input handler?
def input(key):
    if key == '1': block_pick = 1
    if key == '2': block_pick = 2
    if key == '3': block_pick = 3
    if key == '4': block_pick = 4
    if key == '5': block_pick = 5
    if key == '6': block_pick = 6 
"""



# === Class Declarations ===

class MenuBG(Entity):
    def __init__(self, rows, cols, pos):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            
            # Divide rows/cols by 10, e.g. 10 cols => 1.00, 8 rows => 0.8
            # The extra 0.06 is used for the padding of the menu grid
            scale = ((rows / 10) + 0.06, (cols / 10) + 0.06), 
            color = color.color(0,0,0,.8) # (hue, saturation, value, alpha)
        )
        if not pos:
            self.x = 0
            self.y = 0
        else:
            self.x = pos[0]
            self.y = pos[1]

class InvItem(Draggable):
    def __init__(self, inventory, hotbar, ID, pos):
        super().__init__(
            parent = inventory,
            model = 'quad',
            color = color.white,
            #texture = type,

            # The grid has 10 columns, so each item should be 1/10 of the size of the grid
            # and we multiply it by a small amount to make the item slightly smaller 
            # than the inventory slot to give it a padding.
            # And similarly with the scale_y, there's 8 rows so each is 1/8 of the size
            scale_x = 1 / (inventory.texture_scale[0] * 1.2), 
            scale_y = 1 / (inventory.texture_scale[1] * 1.2),
            
            # Change origin to top left, but account for padding by
            # taking what you multiplied above for the scale, and divide by 2
            # e.g. 1.2 / 2 = 0.6
            origin = (-0.6, 0.6), 

            x = pos[0] * 1 / inventory.texture_scale[0],
            y = pos[1] * 1 / inventory.texture_scale[1]
        )
        self.inventory = inventory
        self.hotbar = hotbar
        self.ID = ID

        # 1: grass
        # 2: stone
        # 3: brick
        # 4: dirt
        # 5: sun
        # 6: pendulum
        if self.ID == 1: self.texture = grass_icon_texture
        if self.ID == 2: self.texture = stone_icon_texture
        if self.ID == 3: self.texture = brick_icon_texture
        if self.ID == 4: self.texture = dirt_icon_texture
        if self.ID == 5: self.texture = sun_icon_texture
        if self.ID == 6: self.texture = pendulum_icon_texture

    def drag(self):
        self.xy_pos = (self.x, self.y) # store current position

    def drop(self):
        print('before snap:')
        print(f'x: {self.x}')
        print(f'y: {self.y}')

        """ Calculation explanation:
        
        "(self.x + self.scale_x/2)" 
        Take the current item's x position (origin: top left), and add half of its width, 
        so you get the coordinate of its center.
        
        "self.parent.texture_scale[0]"
        This is basically the number of rows that were passed in as arguments for its container
        (e.g. the grid has 10 rows). And then, "self.parent.texture_scale[1]"" would just be the num of cols.
        
        "int((...) * self.parent.texture_scale[0])"
        Ursina gives coordinates from 0 (left edge) to 1 (right edge)
        so we temporarily make the coordinate larger, multiplying by the number of rows 
        for the x coord (and cols for the y coord) so we can use truncate extra digits
        and get a nice, clean number using the int().
        
        "(...) / self.parent.texture_scale[0]"
        Then, we turn it back into a usuable Ursina coordinate by
        dividing what we multiplied from the earlier step. """
        self.x = int((self.x + self.scale_x/2) * self.parent.texture_scale[0]) / self.parent.texture_scale[0]

        # Ursina coordinate system has an inverted y-axis so we subtract in this case
        self.y = int((self.y - self.scale_y/2) * self.parent.texture_scale[1]) / self.parent.texture_scale[1]

        # check to swap containers
        if self.parent == self.inventory:
            # if the item gets past a certain y value??
            if self.y < -0.9:
                self.swap_container(self.hotbar)
        else:
            if self.y > 0:
                self.swap_container(self.inventory)

        # check for swapping items
        self.overlap_check()

        # check if outside of boundaries
        self.menu_constraint()

        # check for changes in the current slot of the hotbar
        self.hotbar.update_block_pick()

        print('after snap')
        print(f'x: {self.x}')
        print(f'y: {self.y}')
        print('======')

    def swap_container(self, container):

        # more general/flexible
        self.parent = container
            
        # [ ] TODO: instead of finding a free cell, drop it onto the position being hovered over
        self.xy_pos = container.find_free_cell()
        
        self.x = self.xy_pos[0]
        self.y = self.xy_pos[1]
        
        self.scale_x = 1 / (container.texture_scale[0] * 1.2)
        self.scale_y = 1 / (container.texture_scale[1] * 1.2)

        # 
        self.xy_pos = (self.x, self.y)

    def overlap_check(self):
        # check for overlap with another item
        for child in self.parent.children:
            if child.x == self.x and child.y == self.y:
                if child == self:
                    continue
                # if child.ID == -1:
                #     continue 
                else:
                    child.x = self.xy_pos[0]
                    child.y = self.xy_pos[1]
                    print('swap!')

    def menu_constraint(self):

        if self.x < 0 or self.x > 0.95 or self.y > 0 or self.y < -0.95:
            
            # go back to stored position in self.xy_pos
            self.x = self.xy_pos[0]
            self.y = self.xy_pos[1]
            print('out of bounds!')

    def get_cell_pos(self):
        # ... https://youtu.be/hAl7oVJi7r0?t=2904 [48:24]
        x = int(self.x * self.parent.texture_scale[0])
        y = int(self.y * self.parent.texture_scale[1])
        return Vec2(x,y)

class Grid(Entity):
    def __init__(self, rows, cols, pos):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            origin = (-0.5, 0.5), # change origin of grid to top left
            scale = (rows / 10, cols / 10), # must divide num of rows/cols by 10, e.g. 10 rows / 10 = 1.0, 8 cols / 10 = 0.8
            texture = 'white_cube', #load_texture(),
            texture_scale = (rows, cols),
            color = color.color(0,0,0.25,.6),
        )
        self.rows = rows
        self.cols = cols

        if not pos:
            # Must be exactly half of the scale's (x, y) from above
            # e.g. scale: (1.0, 0.8), position: (-0.5, 0.4)
            # x coord is negative because-
            self.position = (-((rows / 10) / 2), (cols / 10) / 2)
        else:
            self.x = pos[0]
            self.y = pos[1]
    
    def get_all_cells(self):
        all_cells = [Vec2(x,y) for y in range(0,-(self.cols),-1) for x in range(0,self.rows)]
        return all_cells
    
    def get_taken_cells(self):
        taken_cells = [child.get_cell_pos() for child in self.children]
        return taken_cells

    def find_free_cell(self):
        all_cells = self.get_all_cells()
        taken_cells = self.get_taken_cells()

        for cell in all_cells:
            if cell not in taken_cells:
                return cell

class Inventory(Grid):
    def __init__(self, rows, cols):
        super().__init__(
            rows = rows,
            cols = cols,
            pos = False
        )

class Hotbar(Grid):    
    def __init__(self, rows, cols, pos, cursor):
        super().__init__(
            rows = rows,
            cols = cols,
            pos = pos
        )
        self.current_slot = 0 # index 0 to 9, of the 10 slots in the hotbar
        self.cursor = cursor

        # print(self.get_all_cells()) # debug

    def update_block_pick(self):
        global block_pick

        # approach1
        # [ ] add this algorithm to the Journal
        # put all cells in a list
        all_cells = self.get_all_cells()

        # use the slot number to reference the corresponding cell in the list
        target_cell = all_cells[self.current_slot]

        # set the block_pick as the ID of the child that overlaps that cell
        if self.children: # if the hotbar has any children, aka if it's not NULL
            for child in self.children:

                print(int(target_cell.x))
                print(int(child.x * 10))

                # (child.x * 10)
                # the item icon's x values are: 0, 0.1, 0.2, ... 1.0
                # but the target_cell's x values are: 0, 1, 2, ... 10
                # so we just multiply the child.x values by 10 so that they are able to match
                # and then truncate the decimal places by using int()
                if int(target_cell.x) == int(child.x * 10):
                    # debug
                    print('pick this block!') 
                    print(block_pick)
                    print(child.ID)

                    block_pick = child.ID

                    print(block_pick)
                    print('======')
                    break
                else:
                    block_pick = 0
        else:
            block_pick = 0


        # approach2
        # if the hotbar cursor overlaps with a child of the hotbar
            # set block_pick to the ID of that child
        #
        # hmmmmm this doesnt work because the coordinates of the crusor are in relation to
        # the camera.ui, but the children of the hotbar are in relation to the hotbar
        # [ ] add this to Journal

    def input(self, key):
        # move the cursor using a left and right key, the number keys, or the scroll wheel
        # position is updated based on user input, and then the hotbar.current_slot is updated after that
        if key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6' or key == '7' or key == '8' or key == '9':
            self.current_slot = (int(key) - 1)
            self.update_block_pick()
            self.cursor.updatePos(self.current_slot)
        
        if key == '0':
            self.current_slot = 9
            self.update_block_pick()
            self.cursor.updatePos(self.current_slot)     

# used for highlighting the current slot of the hotbar that is equipped
class HotbarCursor(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (0.1, 0.1),
            position = ((-.45,-.45)), # (-.5 + (scale_x / 2), -.4 - (scale_y / 2))
            texture = hotbar_cursor_texture
        )

        # debug
        print(f'x: {self.x}')
        print(f'y: {self.y}')

    def updatePos(self, slot):
        # the position is updated based on a hotbar.current_slot check
        # position = starting position + (hotbar.current_slot * cell width)
        self.x = -.45 + (slot * self.scale_x)


class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = 0.5)

    def input(self,key):
        # if the current block is being hovered on by the mouse
        # and the game state is the active gameplay
        # then build/destroy blocks
        if self.hovered and game_state == 1 and block_pick > 0: 
            if key == 'left mouse down':
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                if block_pick == 5: voxel = solarSystem(position = self.position + mouse.normal, texture = sun_texture)
                if block_pick == 6: voxel = pendulum(position = self.position+mouse.normal, texture = pendulum_texture)
            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True)


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4,-0.6)),

    def active(self):
        self.position = Vec2(0.3,-0.5)

    def passive(self):
        self.position = Vec2(0.4,-0.6)


class pendulum(Button):
    def __init__(self,position=(0,0,0), texture = pendulum_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            texture = pendulum_texture,
            color = color.gray,
            origin_y = 0.5,
            scale = 0.5)

        self.pendulum = Entity(model = "pendulum", collider = "mesh", texture = "mc_brick.png", scale = 0.1)


    def update(self):
        simple_pendulum(self)

        if self.hovered and held_keys['right mouse']:
            destroy(self.pendulum)        
            destroy(self)
          
    
class solarSystem(Button):
    def __init__(self, position = (0,0,0), texture = sun_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = 0.5)

        self.planet = Entity(model="assets/block", scale= 0.1, texture = earth_texture)
        self.t = 0.0

    def update(self):
        oscSim(self)
        if self.hovered and held_keys['right mouse']:
            destroy(self.planet)
            destroy(self)



# === Instantiation ===

def terrainGen():
    for z in range(20):
        for x in range(20):
            voxel = Voxel(position = (x,0,z))


terrainGen()

player = FirstPersonController()
sky = Sky()
hand = Hand()

inventory_BG = MenuBG(10, 7, False)
inventory = Inventory(10, 7)
hotbar_BG = MenuBG(10,1, (0,-.46))
hotbar_cursor = HotbarCursor() #hotbar, -1)
hotbar = Hotbar(10,1, (-.5,-.4), hotbar_cursor)


test_item1 = InvItem(inventory, hotbar, 1, inventory.find_free_cell())
test_item2 = InvItem(inventory, hotbar, 2, inventory.find_free_cell())
test_item3 = InvItem(inventory, hotbar, 3, inventory.find_free_cell())
test_item4 = InvItem(inventory, hotbar, 4, inventory.find_free_cell())
test_item5 = InvItem(inventory, hotbar, 5, inventory.find_free_cell())
test_item6 = InvItem(inventory, hotbar, 6, inventory.find_free_cell())

app.run()