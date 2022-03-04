from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from sims import *

window.borderless = False

app = Ursina()

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

punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1

window.fps_counter.enabled = True
window.exit_button.visible = True

debug = False


def update():
    global block_pick
    global debug

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5
    if held_keys['6']: block_pick = 6
 
    if held_keys['escape']: quit()


    # disable the player FirstPersonController(), to regain control of mouse cursor
    # uhmmm yyyes?... kinda works?
    # but there's like a 1 frame flash of black screen? kinda jarring
    # and when you switch back to enabled, the camera jump cuts to where the mouse is
    # ^add to journal^ Feb 18 [12:08am]
    if held_keys['c']: player.enabled = False
    if held_keys['v']: player.enabled = True

    # [] TODO:  make statechanges thingy for 'paused'
    # turn off ability to interact with the world
    # move arm visually on top of menu, to act like it's a phone(?)
    

    if debug == True:
        print(player.position.y)

    
    # if player falls through the map, return to starting point.
    if player.position.y < -10:

        if debug == True:
            print("falling!")
        
        player.y = 1
        player.x = 1
        player.z = 1


class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (.5, .8),
            origin = (-.5, .5),
            position = (-.3,.4),
            texture = 'white_cube',
            texture_scale = (5,8),
            color = color.dark_gray
        )

        self.item_parent = Entity(parent=self, scale=(1/5,1/8))

    def find_free_spot(self):
        taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]
        for y in range(8):
            for x in range(5):
                if not (x,-y) in taken_spots:
                    return (x,-y)

    def append(self, item):
        icon = Button(
            parent = inventory.item_parent,
            model = 'quad',
            texture = item,
            color = color.white,
            origin = (-.5,.5),
            position = self.find_free_spot(),
            z = -.1
        )
        name = item.replace('_', ' ').title()
        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.color(0,0,0,.8)


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
        if self.hovered:
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
            position = Vec2(0.4,-0.6))

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



def terrainGen():
    for z in range(20):
        for x in range(20):
            voxel = Voxel(position = (x,0,z))



terrainGen()

player = FirstPersonController()
sky = Sky()
hand = Hand()

inventory = Inventory()
#item = Button(parent=inventory.item_parent, origin=(0,.5), color=color.red, position=(0,0))
#inventory.append('test item1')
#inventory.append('test item2')

def add_item():
    inventory.append(random.choice(('bag', 'bow_arrow', 'gem', 'orb', 'sword')))

for i in range(7):
    add_item()

add_item_button = Button(
    scale = (.1,.1),
    x = -.5,
    color = color.lime.tint(-.25),
    text = '+',
    tooltip = Tooltip('Add radnom item'),
    on_click = add_item
    )


app.run()