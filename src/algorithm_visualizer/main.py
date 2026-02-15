import pygame
import pygame_gui
import sys

# Configuration
WIDTH, HEIGHT = 800, 600
FPS = 60

def main():
    pygame.init()
    pygame.display.set_caption("Algorithm Visualizer")
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Create a simple "Hello" button to prove it works
    hello_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (100, 50)),
        text='Hello!',
        manager=manager
    )

    is_running = True
    while is_running:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)

        manager.update(time_delta)
        window_surface.fill((0, 0, 0))
        manager.draw_ui(window_surface)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
