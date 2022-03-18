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
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
osc_texture   = load_texture('assets/osc_block.png')
earth_texture = load_texture('assets/earth_block.png')
mc_brick      = load_texture('assets/mc_brick.png')
sun_texture   = load_texture('assets/sun.png')
pendulum_texture = load_texture('assets/mc_brick.png')

# inventory menu icon textures
grass_icon_texture = load_texture('assets/grass_icon.png')

punch_sound   = Audio('assets/punch_sound', loop = False, autoplay = False)
block_pick = 1

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
        #inventory.enabled = False

        # animate the hand to move back and forth when clicked
        if held_keys['left mouse'] or held_keys['right mouse']:
            hand.active()
        else:
            hand.passive()
    
    if game_state == 2: # view inventory state
        player.enabled = False
        #inventory.enabled = True
    

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5
    if held_keys['6']: block_pick = 6

    if held_keys['escape']: 
        quit()



    


    """ 
    if debug == True:
        print(player.position.y) 
    """
    
    # if player falls through the map, return to starting point.
    if player.position.y < -10:

        if debug == True:
            print("falling!")
        
        player.y = 1
        player.x = 1
        player.z = 1

    #inventory.get_position()


# === Class Declarations ===

class MenuBG(Entity):
    def __init__(self, rows, cols):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            
            # Divide rows/cols by 10, e.g. 10 cols => 1.00, 8 rows => 0.8
            # The extra 0.06 is used for the padding of the menu grid
            scale = ((rows / 10) + 0.06, (cols / 10) + 0.06), 
            #texture = load_texture(),
            color = color.color(0,0,0,.8) # (hue, saturation, value, alpha)
        )

class InvItem(Draggable):
    def __init__(self, container, iconTexture):
        super().__init__(
            parent = container,
            model = 'quad',
            color = color.white,
            texture = iconTexture,

            # The grid has 10 columns, so each item should be 1/10 of the size of the grid
            # and we multiply it by a small amount to make the item slightly smaller 
            # than the inventory slot to give it a padding.
            # And similarly with the scale_y, there's 8 rows so each is 1/8 of the size
            scale_x = 1 / (container.texture_scale[0] * 1.2), 
            scale_y = 1 / (container.texture_scale[1] * 1.2),
            
            # Change origin to top left, but account for padding by
            # taking what you multiplied above for the scale, and divide by 2
            # e.g. 1.2 / 2 = 0.6
            origin = (-0.6, 0.6) 
        )

    def drag(self):
        self.xy_pos = (self.x, self.y) # store current position

    def drop(self):
        print(f'x: {self.x}')
        print(f'y: {self.y}')

        # Calculation explanation:
        #
        # "(self.x + self.scale_x/2)" 
        # Take the current item's x position (origin: top left), and add half of its width, 
        # so you get the coordinate of its center.
        #
        # "self.parent.texture_scale[0]"
        # This is basically the number of rows that were passed in as arguments for its container
        # (e.g. the grid has 10 rows). And then, "self.parent.texture_scale[1]"" would just be the num of cols.
        # 
        # "int((...) * self.parent.texture_scale[0])"
        # Ursina gives coordinates from 0 (left edge) to 1 (right edge)
        # so we temporarily make the coordinate larger, multiplying by the number of rows 
        # for the x coord (and cols for the y coord) so we can use truncate extra digits
        # and get a nice, clean number using the int().
        #
        # "(...) / self.parent.texture_scale[0]"
        # Then, we turn it back into a usuable Ursina coordinate by
        # dividing what we multiplied from the earlier step.
        self.x = int((self.x + self.scale_x/2) * self.parent.texture_scale[0]) / self.parent.texture_scale[0]

        # Ursina coordinate system has an inverted y-axis so we subtract in this case
        self.y = int((self.y - self.scale_y/2) * self.parent.texture_scale[1]) / self.parent.texture_scale[1]

        # check if outside of boundaries
        self.menu_constraint()

    def menu_constraint(self):
        if self.x < 0 or self.x > 0.95 or self.y > 0 or self.y < -0.95:
            
            # go back to stored position in self.xy_pos
            self.x = self.xy_pos[0]
            self.y = self.xy_pos[1]



class Grid(Entity):
    def __init__(self, rows, cols):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            origin = (-0.5, 0.5), # change origin of grid to top left
            scale = (rows / 10, cols / 10), # must divide num of rows/cols by 10, e.g. 10 rows / 10 = 1.0, 8 cols / 10 = 0.8
            
            # Must be exactly half of the scale's (x, y) from above
            # e.g. scale: (1.0, 0.8), position: (-0.5, 0.4)
            # x coord is negative because-
            position = (-((rows / 10) / 2), (cols / 10) / 2),
            
            texture = 'white_cube', #load_texture(),
            texture_scale = (rows, cols),
            color = color.color(0,0,0.25,.6),
        )
        self.add_new_item() # add items to inventory on grid instantiation
    
    def add_new_item(self):
        InvItem(self, grass_icon_texture)

""" 
class Hotbar(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (10/10, 1/10),
            origin = (-.5, .5),
            position = (-.5, -.4),
            texture = 'white_cube',
            texture_scale = (10, 1),
            color = color.dark_gray
        )

        self.item_parent = Entity(
            parent = self,
            scale = (1/10, 1/1)
        ) 
"""

"""
class Inventory(Entity):
    def __init__(self, grid_x, grid_y, x, y):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (grid_x/10, grid_y/10), # e.g. 5 x 8 grid will have scale = (.5, .8)
            origin = (-.5, .5), 
            position = (x, y),
            texture = 'white_cube',
            texture_scale = (grid_x, grid_y),
            color = color.dark_gray
        )
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.item_parent = Entity(
            parent = self, 
            scale = (1/self.grid_x, 1/self.grid_y)
        )

    def find_free_spot(self):
        taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                if not (x,-y) in taken_spots:
                    return (x,-y)

    def append(self, item):
        icon = Draggable(
            parent = inventory.item_parent,
            model = 'quad',
            texture = grass_icon_texture,
            #texture_scale = (.25, .25),
            #texture_offset = (.37,.25),
            color = color.white,
            origin = (-.5,.5),
            position = self.find_free_spot(),
            z = -.1
        )
        name = item.replace('_', ' ').title()
        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.color(0,0,0,.8)

        def drag():
            icon.org_pos = (icon.x, icon.y)
            #icon.z -= .01

        def drop():
            # from center origin of icon, round to nearest int
            # so that it drops/snaps the icon to the nearest grid space
            icon.x = int(icon.x + 0.5)
            icon.y = int(icon.y - 0.5)
            #icon.z += .01

            '''if outside, return to original position'''
            if icon.x < 0 or icon.x >= self.grid_x or icon.y > 0 or icon.y <= -self.grid_y:
                icon.position = (icon.org_pos)
                return

            '''if the spot is taken, swap positions'''
            for c in self.children:
                if c == icon:
                    continue
                
                if c.x == icon.x and c.y == icon.y:
                    print('swap positions')
                    c.position = icon.org_pos

        icon.drag = drag
        icon.drop = drop
"""

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
        if self.hovered and game_state == 1: 
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

inventoryBG = MenuBG(10, 8)
inventoryGrid = Grid(10, 8)
#testItem = InvItem()

"""
#hotbar = Hotbar()
inventory = Inventory(10, 8, -.5, .4)#, hotbar)

def add_item():
    inventory.append('grass_texture')

for i in range(7):
    add_item()

if debug:
    add_item_button = Button(
        scale = (.1,.1),
        x = -.5,
        color = color.lime.tint(-.25),
        text = '+',
        tooltip = Tooltip('Add random item'),
        on_click = add_item
        )
"""

app.run()