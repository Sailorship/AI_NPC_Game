import pygame
import math


class Player:
    def __init__(self, x, y):
        # Player Properties
        self.width = 50
        self.height = 50
        self.color = (123, 171, 128)
        self.speed = 3

        # Rectangle used for position and collision
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Weapon properties
        self.weapon_width = 60
        self.weapon_height = 15
        self.weapon_color = (200, 200, 200)  # Light gray
        self.weapon_rect = None  # Created during attack
        self.facing_right = True  # Direction player is facing

        # Attack properties
        self.attack_damage = 10
        self.attack_cooldown = 0
        self.attack_cooldown_time = 25
        self.attacking = False
        self.attack_duration = 10  # How long weapon stays out (frames)
        self.attack_timer = 0

        # Track if space was pressed last frame
        self.space_was_pressed = False

        # Health system
        self.max_health = 100
        self.current_health = self.max_health
        self.alive = True

        # Track last movement for facing direction
        self.last_dx = 1  # Default facing right

    def move(self, keys, npc=None):
        """Top-down WASD movement with collision prevention"""
        screen_width = 800
        screen_height = 600

        if self.alive:
            # Store original position
            original_x = self.rect.x
            original_y = self.rect.y

            dx = 0
            dy = 0

            # Move up
            if keys[pygame.K_w] and self.rect.top > 0:
                dy = -self.speed
            # Move down
            if keys[pygame.K_s] and self.rect.bottom < screen_height:
                dy = self.speed
            # Move left
            if keys[pygame.K_a] and self.rect.left > 0:
                dx = -self.speed
            # Move right
            if keys[pygame.K_d] and self.rect.right < screen_width:
                dx = self.speed

            # Apply movement
            self.rect.x += dx
            self.rect.y += dy

            # Check collision with NPC and prevent overlap
            if npc and self.rect.colliderect(npc.rect):
                # Revert movement - don't allow touching
                self.rect.x = original_x
                self.rect.y = original_y

            # Update facing direction based on horizontal movement
            if dx > 0:
                self.facing_right = True
                self.last_dx = 1
            elif dx < 0:
                self.facing_right = False
                self.last_dx = -1

        # Decrease attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Decrease attack timer
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.attacking = False
                self.weapon_rect = None

    def attack(self, keys, npc):
        """Attack with SPACE key - creates weapon hitbox"""
        # Check distance to NPC
        distance = math.dist(self.rect.center, npc.rect.center)
        min_attack_distance = 30  # Minimum distance to show weapon

        # Only attack on new key press
        if keys[pygame.K_SPACE] and not self.space_was_pressed:
            if self.attack_cooldown == 0 and self.alive and not self.attacking:
                # Only attack if not too close (weapon won't show if too close)
                if distance > min_attack_distance:
                    print("Player attacks!")
                    self.attacking = True
                    self.attack_cooldown = self.attack_cooldown_time
                    self.attack_timer = self.attack_duration

                    # Create weapon hitbox in front of player
                    self.create_weapon_hitbox()
                else:
                    print("Too close to attack!")

        # Hide weapon if NPC gets too close during attack
        if self.attacking and distance <= min_attack_distance:
            self.attacking = False
            self.attack_timer = 0
            self.weapon_rect = None

        # Check if weapon hits NPC
        if self.attacking and self.weapon_rect:
            if self.weapon_rect.colliderect(npc.rect):
                # Deal damage to NPC
                npc.take_damage(self.attack_damage)
                # End attack immediately after hit
                self.attacking = False
                self.attack_timer = 0
                self.weapon_rect = None

        # Update space key state
        self.space_was_pressed = keys[pygame.K_SPACE]

    def create_weapon_hitbox(self):
        """Create weapon rectangle in front of player"""
        if self.facing_right:
            # Weapon extends to the right
            weapon_x = self.rect.right
            weapon_y = self.rect.centery - self.weapon_height // 2
        else:
            # Weapon extends to the left
            weapon_x = self.rect.left - self.weapon_width
            weapon_y = self.rect.centery - self.weapon_height // 2

        self.weapon_rect = pygame.Rect(weapon_x, weapon_y,
                                       self.weapon_width, self.weapon_height)

    def take_damage(self, damage):
        """Reduce health when hit"""
        if self.alive:
            self.current_health -= damage
            print(f"Player hit! Health: {self.current_health}/{self.max_health}")

            if self.current_health <= 0:
                self.current_health = 0
                self.alive = False
                print("Player defeated!")

    def draw(self, screen):
        """Draw player and weapon"""
        # Draw player body
        color = (80, 80, 80) if not self.alive else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Draw weapon when attacking
        if self.attacking and self.weapon_rect:
            pygame.draw.rect(screen, self.weapon_color, self.weapon_rect)
            # Draw weapon border
            pygame.draw.rect(screen, (255, 255, 255), self.weapon_rect, 2)