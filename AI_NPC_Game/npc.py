import pygame
import math

class NPC:
    def __init__(self, x, y):
        # NPC Properties
        self.width = 30
        self.height = 30
        self.color = (133, 29, 40)    # Temporary color. Add sprite later
        self.speed = 3
        self.direction = 1

        # Rectangle used for position and collision
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.speed = 1
        self.direction = 1
        self.left_limit = x - 100
        self.right_limit = x + 100

        # To track previous state
        self.prev_state = None

        # FSM: current NPC state
        self.state = "PATROL"    # Initial state for now

        # Radius within which NPC detects player
        self.detection_radius = 150

    def update(self, player):
        self.decide_state(player)

        if self.state != self.prev_state:
            print(f"State changed to {self.state}")
            self.prev_state = self.state

        # Execute behavior based on current state
        if self.state == "PATROL":
            self.patrol()


   # Decides NPC state based on distance to player
    def decide_state(self, player):

        # Get center points of NPC and Player
        npc_center = self.rect.center
        player_center = player.rect.center

        # Calculate distance between NPC and Player
        distance = math.dist(npc_center, player_center)

        if distance <= self.detection_radius:
            self.state = "CHASE"
        else:
            self.state = "PATROL"


    def patrol(self):
        # Move NPC horizontally
        self.rect.x += self.speed * self.direction

        # Change the direction at limits
        if self.rect.x >= self.right_limit:
            self.direction = -1
        elif self.rect.x <= self.left_limit:
            self.direction = 1


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

