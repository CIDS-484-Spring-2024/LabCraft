from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from sims import *

window.borderless = True


#d is the csv file object that is used for the save system
d = open("placed", "a")
d.close()

app = Ursina()
global player
player = FirstPersonController()
mouse.locked = True
window.fullscreen = False

# block textures
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sun_texture   = load_texture('assets/sun.png')
pendulum_texture = load_texture('assets/mc_brick.png')
#apple texture loaded from the assets folder
apple_texture  = load_texture('assets/apple_block.png')
invisible_texture=load_texture('assets/invisible_block.png')
# inventory menu icon textures
grass_icon_texture = load_texture('assets/grass_icon.png')
stone_icon_texture = load_texture('assets/stone_icon.png')
brick_icon_texture = load_texture('assets/brick_icon.png')
dirt_icon_texture = load_texture('assets/dirt_icon.png')
sun_icon_texture = load_texture('assets/sun_icon.png')
pendulum_icon_texture = load_texture('assets/mc_brick_icon.png')
#apple icon loaded from the assets folder
apple_icon_texture = load_texture('assets/apple_icon.png')
cannon_icon_texture = load_texture('assets/cannon_icon.png')
while_icon_texture = load_texture('assets/while_icon')
# other textures
space_texture=load_texture('assets/space_block.png')
sky_texture   = load_texture('assets/skybox.png')
night_sky_texture = load_texture('assets/nightskybox')
arm_texture   = load_texture('assets/arm_texture.png')
osc_texture   = load_texture('assets/osc_block.png')
earth_texture = load_texture('assets/earth_block.png')
jupiter_texture = load_texture('assets/jupiter_block.png')
mercury_texture = load_texture('assets/mercury_block.png')
venus_texture = load_texture('assets/venus_block.png')
mars_texture = load_texture('assets/mars_block.png')
neptune_texture = load_texture('assets/neptune_block.png')
uranus_texture = load_texture('assets/uranus_block.png')
pluto_texture = load_texture('assets/pluto_block.png')
force_vector_icon_texture = load_texture('assets/FV_icon.png')
Friction_icon_texture = load_texture('assets/Friction_icon.png')
For_icon_texture = load_texture('assets/For_Loop_Icon.png')
mc_brick      = load_texture('assets/mc_brick.png')
hotbar_cursor_texture = load_texture('assets/hotbar_cursor.png')
#picture ratios are 1.9 to 1
Slidetexture1=load_texture('assets/Slide1.png')
Slidetexture2=load_texture('assets/Slide 2.png')
Slidetexture3=load_texture('assets/Slide 3.png')

# sound effects
punch_sound   = Audio('assets/punch_sound', loop = False, autoplay = False)
boom_sound = Audio('assets/BOOM', loop= False, autoplay=False)
global Night
Night=1




""" 
# Block ID Legend:
 0: empty hand
 1: grass
 2: stone
 3: brick
 4: dirt
 5: sun
 6: pendulum
 7: apple
 """
block_pick = 0 # default empty hand

"""
# Game States Legend:
 1: active gameplay
 2: inventory menu screen
 """
global game_state
game_state = 5

window.fps_counter.enabled = True
window.exit_button.visible = True

debug = True


Bob=Sprite(model="quad", texture="assets/Slide1.png", position=(0,1.25,8))
CoBoo = Button(scale=(.5,.1), x=-.6,y=-.2,color=color.rgb(189,0,255),text="Start Game")

BooCo = Button(scale=(.3,.1),x=-.7,y=-.3,color=color.rgb(1,255,31),text="Exit Game")
global slideint
slideint=0
app.frameRateMeter=True
app.frame_rate=60
def update():
    if held_keys['v']:
        print(player.y)
        player.y+=3
    global game_state
    global block_pick
    def gamestart():
        global game_state
        global ground
        game_state=1
        ground==1
    global debug
    global Night
    tray = raycast(player.position, player.forward, ignore=[player])
    
    
 
    # === Game States ===
  
    if held_keys['e'] and game_state == 1 :
        global x
        x=0
        game_state = 2
        
    
    if held_keys['q'] and game_state == 2 :
        
        x=2
        game_state = 1
    
    if game_state == 1: # main game state
        player.enabled = True
        inventory_BG.enabled = False
        inventory.enabled = False
        hand.enabled=True
        sky.enabled=True
        hotbar.enabled=True
        hotbar_BG.enabled=True
        hotbar_cursor.enabled=True
        Bob.enabled=False
        CoBoo.enabled=False
        BooCo.enabled=False

        # animate the hand to move back and forth when clicked
        if held_keys['left mouse'] or held_keys['right mouse']:
            hand.active()
        else:
            hand.passive()
    
    if game_state == 2: # view inventory state
        player.enabled = False
        inventory_BG.enabled = True
        inventory.enabled = True


    #game_state 3 is used for the in game pedulumn Amp/Freq changes
    #this is needed as it frees the cursor from the camera
    #so the player can click the buttons and input field
    if game_state == 3: 
        player.enabled = False
        inventory_BG.enabled = False
        inventory.enabled = False
    if game_state == 4:
        player.enabled = True
        inventory_BG.enabled = False
        inventory.enabled = False
        Sky.texture=night_sky_texture
    if game_state == 5:
        global ground
        global slideint
        player.enabled = False
        inventory_BG.enabled = False
        inventory.enabled = False
        hand.enabled=False
        sky.enabled=False
        hotbar.enabled=False
        hotbar_BG.enabled=False
        hotbar_cursor.enabled=False
        if int(slideint%3)==0:
         Bob.texture=Slidetexture1
        if int(slideint%3)==1:
         Bob.texture=Slidetexture2
        if int(slideint%3)==2:
         Bob.texture=Slidetexture3
        slideint+=(.5*time.dt)
        CoBoo.on_click=(gamestart)
        BooCo.on_click=application.quit
    if game_state == 6:
        
        CoBoo.text="Resume Game"
        player.enabled = False
        inventory_BG.enabled = False
        inventory.enabled = False
        hand.enabled=False
        sky.enabled=True
        hotbar.enabled=False
        hotbar_BG.enabled=False
        hotbar_cursor.enabled=False
        
        CoBoo.on_click=(gamestart)
        BooCo.on_click=application.quit
    if held_keys['escape'] and game_state!=5:
          
             BooCo.enabled = True
             CoBoo.enabled = True
             player.enabled = False
             game_state=6
    # if player falls through the map, return to starting point.
    if player.position.y < -100:

        if debug == True:
            print("falling!")
        
        player.y = 1
        player.x = 1
        player.z = 1
    
    #if player goes to high return to starting point.
   # if player.position.y > 20:

        #if debug == True:
            #print("reverse falling!")
        
        #player.y =1
        #player.x =1
        #player.z =1


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

            # The grid has 10 columns, so each item should be 1/10 of the size of the grid
            # and we multiply it by a small amount to make the item slightly smaller 
            # than the inventory slot to give it a padding.
            # this increases the denominator in the equation, which will equal a smaller number.
            # And similarly with the scale_y, there's 8 rows so each is 1/8 of the size
            scale_x = 1 / (inventory.texture_scale[0] * 1.2), 
            scale_y = 1 / (inventory.texture_scale[1] * 1.2),
            
            # Change origin to top left, but account for padding by
            # taking what you multiplied above for the scale, and divide by 2
            # e.g. 1.2 / 2 = 0.6
            origin = (-0.6, 0.6), 

            # set position in relation to however many cells there are in the inventory
            x = pos[0] * 1 / inventory.texture_scale[0],
            y = pos[1] * 1 / inventory.texture_scale[1]
        )
        self.inventory = inventory
        self.hotbar = hotbar
        self.ID = ID
        # set icon's texture based on ID
        if self.ID == 1: self.texture = grass_icon_texture 
        if self.ID == 2: self.texture = stone_icon_texture
        if self.ID == 3: self.texture = brick_icon_texture
        if self.ID == 4: self.texture = dirt_icon_texture
        if self.ID == 5: self.texture = sun_icon_texture
        if self.ID == 6: self.texture = pendulum_icon_texture
        #tells the hotbar/inventory to load the apple icon
        if self.ID == 7: self.texture = apple_icon_texture
        if self.ID == 8: self.texture = cannon_icon_texture
        if self.ID == 9: self.texture = while_icon_texture
        if self.ID == 10: self.texture = force_vector_icon_texture
        if self.ID == 11: self.texture = Friction_icon_texture
        if self.ID == 12: self.texture = For_icon_texture

    def drag(self):
        self.xy_pos = (self.x, self.y) # store current position

    def drop(self):
        print('before snap:')
        print(f'x: {self.x}')
        print(f'y: {self.y}')

        """ 
        # Calculation explanation:

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
        dividing what we multiplied from the earlier step. 
        """
        self.x = int((self.x + self.scale_x/2) * self.parent.texture_scale[0]) / self.parent.texture_scale[0]

        # Ursina coordinate system has an inverted y-axis so we subtract in this case
        self.y = int((self.y - self.scale_y/2) * self.parent.texture_scale[1]) / self.parent.texture_scale[1]
        self.z=-1
        # check to swap containers
        if self.parent == self.inventory:
            # if the item gets past a certain y value, swap containers
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
        

        # resive item to be in relation to the new container
        self.scale_x = 1 / (container.texture_scale[0] * 1.2)
        self.scale_y = 1 / (container.texture_scale[1] * 1.2)

        # i honestly forgot what this does or why i included it here
        #commenting this out, seemed to fix part of the issues with the inventory as now 
        # I can place the inv items in any slot they still dissapear if overlapped with eachother
       # self.xy_pos = (self.x, self.y)

    def overlap_check(self):
        # check for overlap with another item
        for child in self.parent.children:
            if child.x == self.x and child.y == self.y:
                if child == self:
                    continue
                else:
                    child.x = self.xy_pos[0]
                    child.y = self.xy_pos[1]
                    child.z = -1
                    print('swap!')

    def menu_constraint(self):

        if self.x < 0 or self.x > 0.95 or self.y > 0 or self.y < -0.95:
            
            # go back to stored position in self.xy_pos
            self.x = self.xy_pos[0]/ (inventory.texture_scale[0])
            self.y = self.xy_pos[1]/ (inventory.texture_scale[1])
            print('out of bounds!')

    def get_cell_pos(self):

        # This code block is taken from: https://youtu.be/hAl7oVJi7r0?t=2904 [48:24]
        # pls watch for explanation
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
                print(int(child.x * 9))

                if int(target_cell.x) == int(child.x * 9):
                    if debug == True:
                        print('pick this block!') 
                        print(block_pick)
                        print(child.ID)

                    block_pick = child.ID

                    if debug == True:
                        print(block_pick)
                        print('======')
                    
                    break
                else:
                    block_pick = 0
        else:
            block_pick = 0

    def input(self, key):
        # move the cursor using a left and right key, the number keys, or the scroll wheel
        # position is updated based on user input, and then the hotbar.current_slot is updated after that
        if key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6' or key == '7' or key == '8' or key == '9':
            self.current_slot = (int(key) - 1)
            self.update_block_pick()
            self.cursor.updatePos(self.current_slot)
        if key == '0':
            self.current_slot = 8
            self.update_block_pick()
            self.cursor.updatePos(self.current_slot)     

# used for highlighting the current slot of the hotbar that is equipped
class HotbarCursor(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (0.1, 0.1),
            position = ((-.4,-.45)),
            texture = hotbar_cursor_texture
        )

        if debug == True:
            print(f'x: {self.x}')
            print(f'y: {self.y}')

    def updatePos(self, slot):
        # the position is updated based on a hotbar.current_slot check
        # position = starting position + (hotbar.current_slot * cell width)
        self.x = -.45 + (slot * self.scale_x)


class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture or space_texture or invisible_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
          
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = 0.5)
        global ground
        ground=0
      
    def update(self):

        if game_state==1 and block_pick==0:
            self.texture=grass_texture
        if game_state==4:
            self.texture=space_texture
        if game_state==5:
            self.texture=invisible_texture
    

        

    def input(self,key):
        # if the current block is being hovered on by the mouse
        # and the game state is the active gameplay
        # then build/destroy blocks
        #writes to placed file, and to destroyed file for save data
        if self.hovered and game_state == 1 and block_pick > 0: 
            if key == 'left mouse down':
                global place
                global typea
                punch_sound.play()
                if block_pick == 1: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture) 
            
                    voxel.texture=grass_texture
                   
                    #this next bit is for the save system
                    #first the position of the voxel is set to the variable place
                    place=self.position+mouse.normal
                    #place is then cacacanated to a string
                    place1=str(place)
                    #the position is then stripped of the Vec3 leaving just (tuple)
                    place2=place1.replace("Vec3","")
                    #it's then stripped of one bracket
                    place3=place2.replace("(","")
                    #then the next
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    #place4 is the position stripped just to a tupple
                    #the middle digit is the block type which is used in the match case statement in the terrain instantiation
                    #the final digit is just used as a boolean for placed, or destroyed
                    d.write(place4+","+"1"+","+"1"+'\n')
                    d.close
                    
                   
                if block_pick == 2:
                    voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                        #exact same logic as the grass block
                    
                    voxel.texture=stone_texture
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    d.write(place4+","+"2"+","+"1"+'\n')
                    d.close
                if block_pick == 3:
                    voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                    #exact same logic as the grass block
                    voxel.texture=brick_texture
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    d.write(place4+","+"3"+","+"1"+'\n')
                    d.close
                if block_pick == 4 and game_state!=5: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                    #exact same logic as the grass block
                    voxel.texture=dirt_texture
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    d.write(place4+","+"4"+","+"1"+'\n')
                    d.close
                if block_pick == 5: 
                    voxel = solarSystem(position = self.position + mouse.normal, texture = sun_texture)
                    #exact same logic as the grass block
                
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    d.write(place4+","+"5"+","+"1"+'\n')
                    d.close
                if block_pick == 6: 
                    voxel = pendulum(position = self.position+mouse.normal, texture = pendulum_texture)
                    #exact same logic as the grass block
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    d.write(place4+","+"6"+","+"1"+'\n')
                    d.close
                #tells the game to load the apple block
                if block_pick == 7:
                    voxel = apple(position = self.position+mouse.normal)
                if block_pick==8:
                    voxel = cannon(position =self.position+mouse.normal)
                if block_pick==9:
                    voxel = whileloop(position = self.position + mouse.normal)
                  

                if block_pick==10:
                    voxel = FVSim(position=self.position + mouse.normal)
                if block_pick==11:
                    voxel = FrictionSim(position=self.position+mouse.normal)
                if block_pick==12:
                    voxel = ForLoop(position=self.position+mouse.normal)
               

            if key == 'right mouse down':
                global typea
                punch_sound.play()
                #self.texture is cacatenated to string and then set to typeb
                typeb=str(self.texture)
                #typea is an int that is used with a matchcase to set typeb to a number
                #using the match case below this is used later in the code with the placing/destroying logic
                typea=0
               
                match typeb:
                    case "grass_block.png":
                        typea=1
                    case "stone_block.png":
                        typea=2
                    case "brick_block.png":
                        typea=3
                    case "dirt_block.png":
                        typea=4
                    case "sun.png":
                        typea=5
                    case "pend_block.png":
                        typea=6

                #exact same as the logic used for stripping the position of the placed blocks to a tuple
                place=self.position
                place1=str(place)
                place2=place1.replace("Vec3","")
                place3=place2.replace("(","")
                place4=place3.replace(")","")
                d = open("placed","a")  
                d.write(place4+","+str(typea)+","+"0"+'\n')
                d.close
                destroy(self)
                


class Sky(Entity):
    global Night
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
           
            texture=sky_texture or night_sky_texture,
            scale = 1500,
            double_sided = True)
        if game_state==1:
            self.texture=sky_texture
        if game_state==4:
            self.texture=night_sky_texture
    def update(self):
        global Night
        
        if Night == 0:
            self.texture=night_sky_texture
        if Night == 1:
            self.texture=sky_texture
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
class whileloop(Button):
    def __init__(self, position = (0,0,0),collider="none"):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            scale = .5
        
            )
        self.block=Entity(model='assets/block', scale=.5, color = color.red)
        self.block.x=self.x 
        self.block.y=self.y+.5
        self.block.z=self.z 
        self.y=-2
        self.player=player
        self.t=0
        
        self.Night=1
    def update(self):
        while_sim(self)
        if self.block.hovered and held_keys['right mouse']:
            destroy(self)
            destroy(self.block)
        
        global Night
        Night = self.Night
class ForLoop(Button):
    def __init__(self, position = (0,0,0),collider="none"):
         super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            scale = .5
        
            )
         self.block=Entity(model='assets/block', scale=.5, color = color.red)
         
         self.block.x=self.x 
         self.block.y=self.y+.5
         self.block.z=self.z 
         self.y=-2
         self.player=player
         self.t=0
         self.Night=1
    def update(self):
         Loop_sim(self)
         if self.hovered and held_keys['right mouse']:
            destroy(self)
            destroy(self.block)
         
         global Night
         Night = self.Night
class FrictionSim(Button):    
     def __init__(self,position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'sphere',
            color=color.turquoise,
            origin_y=0.5,
            scale = 1
            
            
        )
        self.b=10
     def update(self):
        Friction_sim(self)
        if self.hovered and held_keys['right mouse']:
            destroy(self)
class FVSim(Button):
    
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            color=color.red,
            origin_y=0.5,
            scale = 0.5
            
            
        )
        self.t=0.0
        self.b=10
        #self.block=Entity(model='assets/block', scale=.5, color = color.red)
    def update(self):
        FV_sim(self)
        if self.hovered and held_keys['right mouse']:
            destroy(self)
class cannon(Button):
    #q is used as a boolean, I would use a regular Boolean but Ursina
    #is weird in it's update function
    global q
    q = 0
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            #the Cannon is a basic model I designed in blender and imported as a .obj file
            model = 'assets/Cannon',
            color = color.gray,
            origin_y = 0.5,
            scale = 0.5,
            rotation=Vec3(45,0,0))
        #this is the prompt for the user to fire, it has to be a boolean other wise
        #once it's hovered over it'll never stop being enabled, that lil tidbit was provided
        #through ChatGPT thanks AI!
        cannon.tooltip=Tooltip("press F to fire", enabled=False)
        self.apple = Entity(model="assets/block", scale=0.1,texture=apple_texture,Collider="mesh")
        self.apple.x=self.position.x
        self.apple.z=self.position.z-2.3
        self.apple.y=self.position.y
        self.t=0.0
        self.velocity=0.0
    def update(self):
        global q
        
        if self.hovered:
            cannon.tooltip.enabled=True
        if not self.hovered:
            cannon.tooltip.enabled=False
       
        if self.hovered and held_keys['f']:
            #global q
            #the reason q is needed is because Ursina doesn't handle single key presses
            #in the update function very well so pressing f makes q = to 1
            q=1
            boom_sound.play()
        #which triggers the update function
        if q !=0:
            cannon_sim(self)
            
        #global q
        #then when the apple is more than 10 blocks away in the z axis
        #q is reset to 0 the apple is moved back and you can fire again
        if self.velocity <= .009:
            self.apple.z=self.position.z-2.3
            self.apple.y=self.position.y
            self.velocity=0.0
            self.t=0.0
            q=0
        if self.hovered and held_keys['right mouse']:
            destroy(self)
            destroy(self.apple)
            q=0
    
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
        
        self.t = 0.0
        self.pendulum = Entity(model = "pendulum", collider = "mesh", texture = "mc_brick.png", scale = 0.1)
        #Start of the logic for the amplitude change
        global AmpInput
        global FreqInput
        #These are input fields for the Amplitude and Frequency Changes in game
        AmpInput = InputField()
        FreqInput = InputField(y=.1)
        global AmpButt
        global FreqButt
        #These are the Buttons used for confirming Amplitude and Frequency
        AmpButt = Button(scale=.05, x=-.4)
        FreqButt = Button(scale=.05, x=-.4, y=.1)
        AmpButt.tooltip = Tooltip("Enter an Amplitude, then click me")
        FreqButt.tooltip = Tooltip("Enter a Frequency, then click me")
      
       
        #The game state changes so the cursor is free to move
        global game_state
        game_state = 3
        #x is used as an incrementing value, once the buttons are clicked x increments by one
        #once it reaches 2 the gamestate is set back to 1 and the game continues
        global x
        x=0
        global Amp
        global amp
        global Freq
        global freq
        freq=0
        self.Freq = .5
        amp=0
        #self.Amp is a universal variable touches all the files
        self.Amp=20
      


    def update(self):
        global amp
        global Amp
        global AmpButt
        global FreqButt
        global Freq
        global freq
        global AmpInput
        simple_pendulum(self)
        
        Amp=20
        if self.hovered and held_keys['right mouse']:
            destroy(self.pendulum)        
            destroy(self)
        #This method does all the heavy lifting for converting the user input   
        #Rtrn is used for the Amplitude
        def Rtrn():
            global AmpButt
            global FreqButt
            global game_state
            global amp
            global AmpInput
            global x
            #it sets whatever is in the inputfield to amp which is an int
            try:
                amp=int(float(AmpInput.text))
            #it then sets Amp which is an object which is then used in the sims file to set the Amplitude
            #to the user input
                self.Amp=amp
                x=x+1
                destroy(AmpInput)
                destroy(AmpButt)
            except:
                ValueError
                print("Has to be a number Dawg")
            
            

        def Retrn():
            #the exact same as the method above but for the frequency

            global FreqButt
            global FreqInput
            global freq
            global x
            try:
                freq=int(float(FreqInput.text))
                self.Freq=freq
                destroy(FreqInput)
                destroy(FreqButt)
                x=x+1
            except:
                print("Has to be a number Dawg")
                ValueError

        global AmpButt
        #calls method above
        AmpButt.on_click = Rtrn
        FreqButt.on_click = Retrn
        global x
        if x>=2:
            global game_state
            game_state=1    
        
#here is the class for the apple sim   
class apple(Button):
    def __init__(self, position = (0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            #because the button class position is unchangeable, you have to create a child
            #so I just changed the size of the button and that seemed to work, as you can't see the apple
            #button but you can see the child apple
            scale = .00000000000000001,
            )
        self.apple = Entity(model="assets/block", scale=0.1,texture=apple_texture)
        #this variable is used in the sims file for time
        self.t=0.0
        
            
    def update(self):
        apple_sim(self)
        
        #this destroys the block to prevent memory overflow
        if self.apple.y <= -10:
                destroy(self)
                destroy(self.apple)
class solarSystem(Button):
    def __init__(self, position = (0,0,0), texture = uranus_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = 1)
            
        self.mercury = Entity(model="assets/block", scale= 0.08, texture=mercury_texture)
        self.venus = Entity(model="assets/block", scale= 0.09, texture=venus_texture)
        self.earth = Entity(model="assets/block", scale= 0.1, texture=earth_texture)
        self.mars = Entity(model="assets/block", scale= 0.095, texture=mars_texture)
        self.jupiter = Entity(model="assets/block", scale= 0.4, collider="mesh", texture=jupiter_texture)
        self.saturn = Entity(model="assets/saturn", scale= 0.15)
        self.uranus = Entity(model="assets/block", scale= 0.2, texture=uranus_texture)
        self.neptune = Entity(model="assets/block", scale= 0.3, texture=neptune_texture)
        self.pluto = Entity(model="assets/block", scale= 0.05, texture=pluto_texture)
        #here's my moon I like it it's a nice moon
        self.moon = Entity(model="assets/block", scale=.01, texture = stone_texture)
        self.t = 0.0

    def update(self):
        oscSim(self)
        self.y=4
        if self.hovered and held_keys['right mouse']:
            destroy(self.mercury)
            destroy(self.venus)
            destroy(self.earth)
            destroy(self.moon)
            destroy(self.mars)
            destroy(self.jupiter)
            destroy(self.saturn)
            destroy(self.uranus)
            destroy(self.neptune)
            destroy(self.pluto)
            destroy(self)




# === Instantiation ===
terrainy= [[0]*30 for _ in range(30)]
for x in range(30):
    for z in range(30):
        terrainy[x][z]="*"

#Lrow=0
Lrow=random.randint(0,15)
#Lcol=0
Lcol=random.randint(0,15)
#Hrow=10
Hrow=random.randint(15,30)
#Hcol=10
Hcol=random.randint(15,30)
#Hpoint=10
Hpoint=random.randint(-15,0)
#Lpoint=0
Lpoint=random.randint(-30,-15)
mid=(Hpoint+Lpoint)/2
def ClosestTo(Lrow,Lcol,Hrow,Hcol,Mrow,Mcol):
  dmtL=math.sqrt(abs((Lrow-Mrow)*(Lrow-Mrow))+abs((Lcol-Mcol)*(Lcol-Mcol))) 
  dmtH=math.sqrt(abs((Hrow-Mrow)*(Hrow-Mrow))+abs((Hcol-Mcol)*(Hcol-Mcol))) 
 # print(dmtH,"<dmtH   dmtL>",dmtL)
  if dmtL>dmtH:
      if dmtL:
          return "is Low"
      else:
        return "Closest to Low"
  elif dmtH>dmtL:
      if dmtH==0:
          return "is High"
      else:
        return "Closest to High"
  else:
    return "Equidistant"
def OnBoard(row, col):
    if 0 <= row < 30 and 0 <= col < 30:
        return True
    else:
        return False
def RandomHeight(list, row, col, mid):
    if not OnBoard(row, col):
        return
    print(Hpoint,"<Hpoint-----Lpoint>",Lpoint)
    if list[row][col] == "*":
       # print(ClosestTo(Lrow, Lcol, Hrow, Hcol, row, col))
        if ClosestTo(Lrow, Lcol, Hrow, Hcol, row, col) == "Closest to Low":
            list[row][col] = mid - 1
            Npoint=mid-1
        elif ClosestTo(Lrow, Lcol, Hrow, Hcol, row, col) == "Closest to High":
            list[row][col] = mid + 1
            Npoint=mid+1
        elif ClosestTo(Lrow, Lcol, Hrow, Hcol, row, col) == "is High":
            list[row][col]=Hpoint
            Npoint=Hpoint
        elif ClosestTo(Lrow, Lcol, Hrow, Hcol, row, col) == "is Low":
            list[row][col]=Lpoint
            Npoint=Lpoint
        else:
            list[row][col] = mid
            Npoint=mid
    else:
        return
    
   
  
    for x in range(row - 1, row + 1):
        for z in range(col - 1, col + 1):
           # print(mid," ",Npoint)
            RandomHeight(list, x, z, Npoint)
    

RandomHeight(terrainy,29,29,mid)

    


def terrainGen():
 for z in range(30):
        for x in range(30):
            #voxel = Voxel(position = (x,0,z),texture=grass_texture)
            #uncomment this for the random terrain gen
            voxel = Voxel(position = (x,terrainy[x][z],z),texture=grass_texture)
            
 
 
    #here is the start of the save system logic
    #first the placed file is opened and read
 with open("placed","r") as file:
        #then a default texture is defined with 
        global Text
        #then a blank list is declared
        placeList=[]
        #Can't just declare Text as a variable so Text has a default texture
        Text=grass_texture
        for line in file:
            #the blank list is then appended with the lines in the file
            placeList.append(line.rstrip())
        #a is used to step through the list
        a=0
        #another blank list is then declared as the previous list was read in as
        #strings
        saveList=[]
        for x in placeList:
         if not placeList[a]=='':
          #and the new List is appended with tupples mapped from the string and split with the , delimiter
          res=tuple(map(int, placeList[a].split(',')))
          saveList.append(res)
          #the position of the block is then based off the first 3 numbers of each tupple
          savePOS=res[:3]
          #the texture is the 4th number
          textre=res[3]
          #and the status is the 5th number
          PlaceOrDes=res[4]
          a=a+1
          #This changes the texture of the block based off of the 4th digit of the tuples in the save file
          match textre:
              case 1:
                  Text=grass_texture
                  Greg=Voxel
              case 2:
                  Text=stone_texture
                  Greg=Voxel
              case 3:
                  Text=brick_texture
                  Greg=Voxel
              case 4:
                  Text=dirt_texture
                  Greg=Voxel
              case 5:
                  Text=sun_texture
                  Greg=solarSystem
              case 6:
                  Text=pendulum_texture
                  Greg=pendulum
          #as long as PlaceOrDes is 1 the block is placed
          if PlaceOrDes==1:
           voxel=Greg(position=Vec3(savePOS),texture=Text)
           #there is more to come with this
terrainGen()

sky = Sky()
hand = Hand()


inventory_BG = MenuBG(9, 7, False)
inventory = Inventory(9, 7)
hotbar_BG = MenuBG(9,1, (0,-.46,-1))
hotbar_cursor = HotbarCursor()
hotbar = Hotbar(9,1, (inventory.x,-.4,100), hotbar_cursor)


test_item1 = InvItem(inventory, hotbar, 1, inventory.find_free_cell())
test_item2 = InvItem(inventory, hotbar, 2, inventory.find_free_cell())
test_item3 = InvItem(inventory, hotbar, 3, inventory.find_free_cell())
test_item4 = InvItem(inventory, hotbar, 4, inventory.find_free_cell())
test_item5 = InvItem(inventory, hotbar, 5, inventory.find_free_cell())
test_item6 = InvItem(inventory, hotbar, 6, inventory.find_free_cell())
#this fills the inventory with a blank slot so the apple can be placed in there
test_item7 = InvItem(inventory, hotbar, 7, inventory.find_free_cell())
#here's the cannon sim blank slot
test_item8 = InvItem(inventory, hotbar, 8, inventory.find_free_cell())
test_item9 = InvItem(inventory, hotbar, 9, inventory.find_free_cell())
test_item10 = InvItem(inventory, hotbar, 10, inventory.find_free_cell())
test_item11 = InvItem(inventory, hotbar, 11, inventory.find_free_cell())
test_item12 = InvItem(inventory, hotbar, 12, inventory.find_free_cell())
app.run()