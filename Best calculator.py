from ursina import *

app = Ursina()

# Define the player-controlled marble
class Marble(Entity):
    def __init__(self):
        super().__init__(
            model='sphere',
            color=color.white,
            scale=0.2,
            collider='box',
        )

    def update(self):
        # Handle keyboard input for movement
     if not Marble.intersects(Obstacle):
        speed = 5
        if held_keys['a']:
            self.x -= speed * time.dt
        if held_keys['d']:
            self.x += speed * time.dt
        if held_keys['w']:
            self.y += speed * time.dt
        if held_keys['s']:
            self.y -= speed * time.dt

# Define the level obstacles
class Obstacle(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            color=color.red,
            scale=(1, 0.1, 1),
            position=position,
            collider='box',
            
        )
    CollisionBox

# Create the player marble
marble = Marble()

# Create some obstacles (you can create more or design your own level)
obstacle1 = Obstacle((2, 2))
obstacle2 = Obstacle((-2, -2))

# Set up the camera to follow the marble
camera.add_script(SmoothFollow(target=marble, offset=(0, 2, -10), speed=4))

app.run()