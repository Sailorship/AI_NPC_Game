import pygame
import math


class NPC:
    def __init__(self, x, y):
        # NPC Properties
        self.width = 50
        self.height = 50
        self.color = (133, 29, 40)
        self.speed = 1

        # Store original patrol position
        self.ori_posx = x
        self.ori_posy = y

        # Rectangle used for position and collision
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Weapon properties
        self.weapon_width = 50
        self.weapon_height = 12
        self.weapon_color = (180, 50, 50)  # Dark red
        self.weapon_rect = None  # Created during attack
        self.facing_right = False  # NPC starts facing left

        # Patrol boundaries (horizontal patrol)
        self.direction = 1
        self.left_limit = x - 100
        self.right_limit = x + 100

        # FSM state tracking
        self.state = "PATROL"
        self.prev_state = None

        # Detection and combat
        self.detection_radius = 150
        self.attack_range = 80  # Range to trigger attack
        self.attack_damage = 5
        self.attack_cooldown = 0
        self.attack_cooldown_time = 60
        self.attacking = False
        self.attack_duration = 15  # How long weapon stays out
        self.attack_timer = 0

        # Return threshold
        self.return_threshold = 5

        # Health system
        self.max_health = 100
        self.current_health = self.max_health
        self.alive = True

    def update(self, player):
        """Main update loop"""
        # Decrease cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.attacking = False
                self.weapon_rect = None

        # Only update AI if alive
        if self.alive:
            # Update facing direction based on player position
            if player.rect.centerx > self.rect.centerx:
                self.facing_right = True
            else:
                self.facing_right = False

            self.decide_state(player)

            # Log state changes
            if self.state != self.prev_state:
                print(f"NPC State: {self.state}")
                self.prev_state = self.state

            # Execute behavior
            if self.state == "PATROL":
                self.patrol()
            elif self.state == "CHASE":
                self.chase(player)
            elif self.state == "RETURN":
                self.return_to_patrol()
            elif self.state == "ATTACK":
                self.attack(player)

    def decide_state(self, player):
        """Determine state based on distance"""
        distance = math.dist(self.rect.center, player.rect.center)

        # Lock in ATTACK during cooldown
        if self.state == "ATTACK" and self.attack_cooldown > 0:
            return

        # State transitions
        if distance <= self.attack_range:
            self.state = "ATTACK"
        elif distance <= self.detection_radius:
            self.state = "CHASE"
        else:
            if self.state in ["CHASE", "ATTACK"]:
                self.state = "RETURN"
            elif self.state == "RETURN":
                if self.is_at_original_position():
                    self.state = "PATROL"

    def patrol(self):
        """Move back and forth horizontally"""
        self.rect.x += self.speed * self.direction

        # Reverse at limits
        if self.rect.x >= self.right_limit:
            self.direction = -1
            self.facing_right = False
        elif self.rect.x <= self.left_limit:
            self.direction = 1
            self.facing_right = True

    def chase(self, player):
        """Chase player in both directions but stop before touching"""
        distance = math.dist(self.rect.center, player.rect.center)
        min_distance = 30  # Minimum distance to maintain

        # Only move if not in attack range AND not too close
        if distance > self.attack_range and distance > min_distance:
            # Store original position
            original_x = self.rect.x
            original_y = self.rect.y

            # Move horizontally
            if player.rect.centerx > self.rect.centerx:
                self.rect.x += self.speed
            elif player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed

            # Move vertically
            if player.rect.centery > self.rect.centery:
                self.rect.y += self.speed
            elif player.rect.centery < self.rect.centery:
                self.rect.y -= self.speed

            # Check if movement caused collision with player
            if self.rect.colliderect(player.rect):
                # Revert movement - don't allow touching
                self.rect.x = original_x
                self.rect.y = original_y

    def attack(self, player):
        """Attack player with weapon hitbox"""
        distance = math.dist(self.rect.center, player.rect.center)
        min_attack_distance = 30  # Minimum distance to show weapon

        if self.attack_cooldown == 0 and not self.attacking:
            # Only attack if not too close (weapon won't show if too close)
            if distance > min_attack_distance:
                print("NPC attacks!")
                self.attacking = True
                self.attack_cooldown = self.attack_cooldown_time
                self.attack_timer = self.attack_duration

                # Create weapon hitbox
                self.create_weapon_hitbox()

        # Hide weapon if player gets too close during attack
        if self.attacking and distance <= min_attack_distance:
            self.attacking = False
            self.attack_timer = 0
            self.weapon_rect = None

        # Check if weapon hits player
        if self.attacking and self.weapon_rect:
            if self.weapon_rect.colliderect(player.rect):
                # Deal damage to player
                player.take_damage(self.attack_damage)
                # End attack immediately after hit
                self.attacking = False
                self.attack_timer = 0
                self.weapon_rect = None

    def create_weapon_hitbox(self):
        """Create weapon rectangle in front of NPC"""
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

    def return_to_patrol(self):
        """Return to original position"""
        # Move horizontally
        if self.rect.x < self.ori_posx - self.return_threshold:
            self.rect.x += self.speed
        elif self.rect.x > self.ori_posx + self.return_threshold:
            self.rect.x -= self.speed

        # Move vertically
        if self.rect.y < self.ori_posy - self.return_threshold:
            self.rect.y += self.speed
        elif self.rect.y > self.ori_posy + self.return_threshold:
            self.rect.y -= self.speed

    def is_at_original_position(self):
        """Check if at original position"""
        return (abs(self.rect.x - self.ori_posx) <= self.return_threshold and
                abs(self.rect.y - self.ori_posy) <= self.return_threshold)

    def take_damage(self, damage):
        """Reduce health when hit"""
        if self.alive:
            self.current_health -= damage
            print(f"NPC hit! Health: {self.current_health}/{self.max_health}")

            if self.current_health <= 0:
                self.current_health = 0
                self.alive = False
                print("NPC defeated!")

    def draw(self, screen):
        """Draw NPC and weapon"""
        # Draw NPC body
        color = (80, 80, 80) if not self.alive else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Draw weapon when attacking
        if self.attacking and self.weapon_rect:
            pygame.draw.rect(screen, self.weapon_color, self.weapon_rect)
            # Draw weapon border
            pygame.draw.rect(screen, (255, 255, 255), self.weapon_rect, 2)

        # Draw health bar above NPC
        self.draw_healthbar(screen)

    def draw_healthbar(self, screen):
        """Draw health bar that hovers above NPC"""
        bar_width = 50
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y - 12  # 12 pixels above NPC

        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Health (green)
        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

        # Border (white)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)