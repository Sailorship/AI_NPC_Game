import pygame
import sys
from player import Player
from npc import NPC

# Initialize all pygame modules
pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A_ Game")

# Clock to control FPS
clock = pygame.time.Clock()

# Colors
BACKGROUND_COLOR = (130, 124, 108)
White = (255, 255, 255)
Red = (255, 0, 0)

# Font
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# Create player and NPC objects
player = Player(WIDTH // 2, HEIGHT // 2)  # Player starts at center
npc = NPC(650, 200)  # NPC starts upper right (above player horizontal line)

# Game state
game_over = False


def draw_ui():
    """Draw game UI"""
    # Player health text (top left)
    player_text = small_font.render(f"Player HP: {player.current_health}/100", True, White)
    screen.blit(player_text, (20, 20))

    # Controls (bottom)
    controls = small_font.render("WASD: Move | SPACE: Attack", True, White)
    screen.blit(controls, (WIDTH // 2 - 130, HEIGHT - 30))


def draw_game_over():
    """Draw game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Game over text
    game_over_text = font.render("GAME OVER", True, Red)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(game_over_text, text_rect)

    # Restart instruction
    restart_text = small_font.render("ESC to quit", True, White)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(restart_text, restart_rect)


def reset_game():
    """Reset game to initial state"""
    global player, npc, game_over
    player = Player(WIDTH // 2, HEIGHT // 2)
    npc = NPC(650, 200)
    game_over = False
    print("Game reset!")


# Main game loop
running = True
while running:
    clock.tick(60)  # Run game at 60 frames per second

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Restart on R key
            if event.key == pygame.K_r and game_over:
                reset_game()

    # Get keyboard input
    keys = pygame.key.get_pressed()

    # Update game if not over
    if not game_over:
        player.move(keys, npc)  # Pass npc for collision prevention
        player.attack(keys, npc)

        # Update NPC logic (FSM + movement)
        npc.update(player)

        # Check if player is dead
        if not player.alive:
            game_over = True
            print("Game Over!")

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    
    draw_ui()

    # Draw game objects
    player.draw(screen)
    npc.draw(screen)

    # Draw game over screen
    if game_over:
        draw_game_over()

    # Update display
    pygame.display.update()

pygame.quit()
sys.exit()