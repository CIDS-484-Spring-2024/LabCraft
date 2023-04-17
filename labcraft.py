from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from sims import *

window.borderless = False

d = open("placed", "a")
d.close()
pl = open("destroyed", "a")
pl.close()
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

# sound effects
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

"""
# Game States Legend:
 1: active gameplay
 2: inventory menu screen
 """
global game_state
game_state = 1 


window.fps_counter.enabled = True
window.exit_button.visible = True

debug = True

#voxel = Voxel(position = Vec3(17,1,10), texture = grass_texture)
def update():
    global block_pick
    global game_state
    global debug

    # === Game States ===

    if held_keys['e']:
        game_state = 2
        
    
    if held_keys['q']:
        game_state = 1
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
    
    if game_state == 3: #This logic is for the pendulum
        player.enabled = False
        inventory_BG.enabled = False
        inventory.enabled = False
    if held_keys['escape']: 
        quit()
    
    # if player falls through the map, return to starting point.
    if player.position.y < -10:

        if debug == True:
            print("falling!")
        
        player.y = 1
        player.x = 1
        player.z = 1
    
    #if player goes to high return to starting point.
    if player.position.y > 20:

        if debug == True:
            print("reverse falling!")
        
        player.y =1
        player.x =1
        player.z =1


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
        self.xy_pos = (self.x, self.y)

    def overlap_check(self):
        # check for overlap with another item
        for child in self.parent.children:
            if child.x == self.x and child.y == self.y:
                if child == self:
                    continue
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
                print(int(child.x * 10))

                if int(target_cell.x) == int(child.x * 10):
                    
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

        if debug == True:
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
        #writes to placed file, and to destroyed file for save data
        if self.hovered and game_state == 1 and block_pick > 0: 
            if key == 'left mouse down':
                global place
                global typea
                punch_sound.play()

                if block_pick == 1: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture) 
                #this is for potential save state idea
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    #place4 is the position stripped just to a tupple
                    #the middle digit is the block type which is used in the match case statement in the terrain instantiation
                    #the final digit is just used as a boolean for placed, or destroyed
                    d.write(place4+","+"1"+","+"1"+'\n')
                    d.close
                    
                   
                if block_pick == 2: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
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
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    d.write(place4+","+"3"+","+"1"+'\n')
                    d.close
                if block_pick == 4: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
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
                    place=self.position+mouse.normal
                    place1=str(place)
                    place2=place1.replace("Vec3","")
                    place3=place2.replace("(","")
                    place4=place3.replace(")","")
                    d = open("placed","a")   
                    d.write(place4+","+"6"+","+"1"+'\n')
                    d.close
            if key == 'right mouse down':
                global typea
                punch_sound.play()
                typeb=self.texture
                typea=0
                print(type(typeb))
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
        
        self.t = 0.0
        self.pendulum = Entity(model = "pendulum", collider = "mesh", texture = "mc_brick.png", scale = 0.1)
        #Start of the logic for the amplitude change
        global Box
        global Rox
        Box = InputField()
        Rox = InputField(y=.1)
        global BOB
        global ROB
        BOB = Button(scale=.05, x=-.4)
        ROB = Button(scale=.05, x=-.4, y=.1)
        BOB.tooltip = Tooltip("Enter an Amplitude, then click me")
        ROB.tooltip = Tooltip("Enter a Frequency, then click me")
      
       
        #The game state changes so the cursor is free to move
        global game_state
        game_state = 3
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
        global BOB
        global ROB
        global Freq
        global freq
        global Box
        simple_pendulum(self)
        
        Amp=20
        if self.hovered and held_keys['right mouse']:
            destroy(self.pendulum)        
            destroy(self)
        #This method does all the heavy lifting for converting the user input   
        def Rtrn():
            global BOB
            global ROB
            global game_state
            global amp
            global Box
            global x
            amp=int(float(Box.text))
            self.Amp=amp
            x=x+1
            print(x)
            destroy(Box)
            destroy(BOB)
            
            

        def Retrn():
            global ROB
            global Rox
            global freq
            global x
            freq=int(float(Rox.text))
            self.Freq=freq
            destroy(Rox)
            destroy(ROB)
            x=x+1
            print(x)
        global BOB
        #calls method above
        BOB.on_click = Rtrn
        ROB.on_click = Retrn
        global x
        if x>=2:
            global game_state
            game_state=1        
            
    
          
    
class solarSystem(Button):
    def __init__(self, position = (0,0,0), texture = sun_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = .5)

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
            voxel = Voxel(position = (x,-1,z))
    #test_string ="1,1,1"
  #  res=tuple(map(int, test_string.split(',')))
   # voxel=Voxel(position = Vec3(res), texture=grass_texture)
    
    with open("placed","r") as file:
        global Blob
        myList=[]
        #Can't just declare Blob as a variable so Blob has a default texture
        Blob=grass_texture
        for line in file:
            myList.append(line.rstrip())
        a=0
        for x in myList:
         if not myList[a]=='':
          res=tuple(map(int, myList[a].split(',')))
          byList=res[:3]
          textre=res[3]
          PLOD=res[4]
          a=a+1
          #This changes the texture of the block based off the save file
          match textre:
              case 1:
                  Blob=grass_texture
                  Greg=Voxel
              case 2:
                  Blob=stone_texture
                  Greg=Voxel
              case 3:
                  Blob=brick_texture
                  Greg=Voxel
              case 4:
                  Blob=dirt_texture
                  Greg=Voxel
              case 5:
                  Blob=sun_texture
                  Greg=solarSystem
              case 6:
                  Blob=pendulum_texture
                  Greg=pendulum
          if PLOD==1:
           voxel=Greg(position=Vec3(byList),texture=Blob)
        #  if PLOD==0:
          #   print("Not Placed")
         
         #"""
     #with open("destroyed","r") as file:
      #  tyList=[]
        #for line in file:
          #  tyList.append(line.rstrip())
            
       # a=0
       # for x in tyList:
        #    if not tyList[a]=='':
         #       res=tuple(map(int, tyList[a].split(',')))
         #       ryList=res[:3]
              
         #       a=a+1
#
      # """
          
        
    


terrainGen()

player = FirstPersonController()
sky = Sky()
hand = Hand()


inventory_BG = MenuBG(10, 7, False)
inventory = Inventory(10, 7)
hotbar_BG = MenuBG(10,1, (0,-.46))
hotbar_cursor = HotbarCursor()
hotbar = Hotbar(10,1, (-.5,-.4), hotbar_cursor)


test_item1 = InvItem(inventory, hotbar, 1, inventory.find_free_cell())
test_item2 = InvItem(inventory, hotbar, 2, inventory.find_free_cell())
test_item3 = InvItem(inventory, hotbar, 3, inventory.find_free_cell())
test_item4 = InvItem(inventory, hotbar, 4, inventory.find_free_cell())
test_item5 = InvItem(inventory, hotbar, 5, inventory.find_free_cell())
test_item6 = InvItem(inventory, hotbar, 6, inventory.find_free_cell())

app.run()