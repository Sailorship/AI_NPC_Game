import pygame
import math


class NPC:
    def __init__(self, x, y):
        # NPC Properties
        self.width = 50
        self.height = 50
        self.color = (133, 29, 40)
        self.speed = 1
        self.TBspeed = 1

        # Store original patrol position
        self.ori_posx = x
        self.ori_posy = y

        # Rectangle used for position and collision
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Patrol boundaries
        self.direction = 1
        self.left_limit = x - 100
        self.right_limit = x + 100

        # FSM state tracking
        self.state = "PATROL"
        self.prev_state = None

        # Detection radius
        self.detection_radius = 150

        # Attack range to
        self.attack_range = 50

        # Threshold for "close enough" when returning
        self.return_threshold = 5

        # Attack cooldown
        self.attack_cooldown = 0
        self.attack_cooldown_time = 60  # 1 second at 60 FPS



    def update(self, player):
        # Decrease cooldown timer every frame
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.decide_state(player)

        # Log state changes
        if self.state != self.prev_state:
            print(f"RED's State switched to {self.state}")
            self.prev_state = self.state

        # Execute behavior based on current state
        if self.state == "PATROL":
            self.patrol()
        elif self.state == "CHASE":
            self.chase(player)
        elif self.state == "RETURN":
            self.return_to_patrol()
        elif self.state == "ATTACK":
            self.attack(player)

    def decide_state(self, player):
        """Determines NPC state based on player distance"""
        distance = math.dist(self.rect.center, player.rect.center)

        if self.state == "ATTACK" and self.attack_cooldown > 0:
            return        # Stay in ATTACK state until cooldown finishes

        # Switch states based on condition
        if distance <= self.attack_range:
            # Only attack if cooldown is ready
            if self.attack_cooldown == 0:
                self.state = "ATTACK"
            else:
                # Wait near player during cooldown
                self.state = "CHASE"
        elif distance <= self.detection_radius:
            self.state = "CHASE"
        else:
            # If the player is not in range, switch to PATROL
            if self.state == "CHASE" or self.state == "ATTACK":
                self.state = "RETURN"
            # If already at patrol position, switch to PATROL
            elif self.state == "RETURN":
                if self.is_at_original_position():
                    self.state = "PATROL"

    def patrol(self):
        """Move NPC back and forth horizontally"""
        self.rect.x += self.speed * self.direction

        # Reverse direction at patrol limits
        if self.rect.x >= self.right_limit:
            self.direction = -1
        elif self.rect.x <= self.left_limit:
            self.direction = 1

    def chase(self, player):
        """Chase player in both horizontal and vertical directions"""
        distance = math.dist(self.rect.center, player.rect.center)

        # Move horizontally toward player
        if distance > self.attack_range:
            # Move horizontally toward player
            if player.rect.centerx > self.rect.centerx:
                self.rect.x += self.speed
            elif player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed

            # Move vertically toward player
            if player.rect.centery > self.rect.centery:
                self.rect.y += self.TBspeed
            elif player.rect.centery < self.rect.centery:
                self.rect.y -= self.TBspeed                


    def attack(self, player):
        # Only attack if cooldown is ready
        if self.attack_cooldown == 0:
            print("NPC attacks!")
            self.attack_cooldown = self.attack_cooldown_time
            # Add damage logic here


    # NPC returns after a chase
    def return_to_patrol(self):
        """Return to the original patrol position"""
        # Move horizontally toward the original position
        if self.rect.x < self.ori_posx - self.return_threshold:
            self.rect.x += self.speed
        elif self.rect.x > self.ori_posx + self.return_threshold:
            self.rect.x -= self.speed

        # Move vertically toward the original position
        if self.rect.y < self.ori_posy - self.return_threshold:
            self.rect.y += self.TBspeed
        elif self.rect.y > self.ori_posy + self.return_threshold:
            self.rect.y -= self.TBspeed

    def is_at_original_position(self):
        """Check if NPC is close enough to the original position"""
        return (
            abs(self.rect.x - self.ori_posx) <= self.return_threshold
            and abs(self.rect.y - self.ori_posy) <= self.return_threshold
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
