"""
User Interface Management Layer.
Responsible for rendering the Control Panel, Buttons, and Result Pop-ups.
"""

import pygame

import utils.config as configuration_settings


class Button:
    def __init__(self, x, y, width, height, text, action_payload):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_payload = action_payload
        self.base_color = configuration_settings.COLOR_EMPTY
        self.hover_color = configuration_settings.COLOR_EXPLORED
        self.text_color = pygame.Color("white")
        self.font = pygame.font.SysFont("JetBrainsMono Nerd Font", 18, bold=True)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = (
            self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        )

        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(
            surface, configuration_settings.COLOR_GRID, self.rect, 2, border_radius=5
        )

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class InterfaceRenderer:
    def __init__(self, display_surface):
        self.target_surface = display_surface
        self.standard_text_font = pygame.font.SysFont("JetBrainsMono Nerd Font", 16)
        self.header_font = pygame.font.SysFont("JetBrainsMono Nerd Font", 32, bold=True)
        self.popup_font = pygame.font.SysFont("JetBrainsMono Nerd Font", 40, bold=True)

        self.buttons = []
        algos = ["BFS", "DFS", "UCS", "DLS", "IDDFS", "BIDIRECTIONAL"]
        start_y = 200
        for i, algo in enumerate(algos):
            btn = Button(820, start_y + (i * 45), 160, 35, algo, algo)
            self.buttons.append(btn)

    def render_control_panel(self, active_algorithm_name, execution_status):
        """
        Draws the sidebar, buttons, and status text.
        """
        # Clear sidebar
        sidebar_rect = pygame.Rect(
            800,
            0,
            configuration_settings.WINDOW_WIDTH - 800,
            configuration_settings.WINDOW_HEIGHT,
        )
        pygame.draw.rect(
            self.target_surface, configuration_settings.COLOR_BG, sidebar_rect
        )

        # Separator Line
        pygame.draw.line(
            self.target_surface,
            configuration_settings.COLOR_GRID,
            (800, 0),
            (800, configuration_settings.WINDOW_HEIGHT),
            2,
        )

        # Title
        title_visual = self.header_font.render(
            "PATHFINDER", True, configuration_settings.COLOR_PATH
        )
        self.target_surface.blit(title_visual, (815, 30))

        # Status Text
        if execution_status == "RUNNING":
            status_color = configuration_settings.COLOR_DYNAMIC
            status_text = "RUNNING..."
        elif execution_status == "FINISHED":
            status_color = configuration_settings.COLOR_TARGET
            status_text = "DONE"
        else:
            status_color = configuration_settings.COLOR_EXPLORED
            status_text = "IDLE"

        status_visual = self.standard_text_font.render(
            f"Status: {status_text}", True, status_color
        )
        self.target_surface.blit(status_visual, (815, 80))

        algo_visual = self.standard_text_font.render(
            f"Algo: {active_algorithm_name}", True, configuration_settings.COLOR_START
        )
        self.target_surface.blit(algo_visual, (815, 110))

        # Buttons
        for btn in self.buttons:
            btn.draw(self.target_surface)

        # Instructions
        instr_y = 650
        instructions = [
            "SPACE: Start",
            "C: Reset Grid",
            "L-CLICK: Place",
            "R-CLICK: Erase",
        ]
        for line in instructions:
            v = self.standard_text_font.render(
                line, True, configuration_settings.COLOR_EMPTY
            )
            self.target_surface.blit(v, (815, instr_y))
            instr_y += 25

    def render_result_popup(self, success):
        overlay = pygame.Surface(
            (configuration_settings.WINDOW_WIDTH, configuration_settings.WINDOW_HEIGHT),
            pygame.SRCALPHA,
        )
        overlay.fill((0, 0, 0, 180))
        self.target_surface.blit(overlay, (0, 0))

        center_x, center_y = self.target_surface.get_rect().center
        box_rect = pygame.Rect(0, 0, 400, 200)
        box_rect.center = (center_x, center_y)

        pygame.draw.rect(
            self.target_surface,
            configuration_settings.COLOR_BG,
            box_rect,
            border_radius=10,
        )
        pygame.draw.rect(
            self.target_surface,
            configuration_settings.COLOR_PATH,
            box_rect,
            3,
            border_radius=10,
        )

        msg = "PATH FOUND!" if success else "NO PATH POSSIBLE"
        color = (
            configuration_settings.COLOR_START
            if success
            else configuration_settings.COLOR_DYNAMIC
        )

        text_surf = self.popup_font.render(msg, True, color)
        text_rect = text_surf.get_rect(center=(center_x, center_y - 20))
        self.target_surface.blit(text_surf, text_rect)

        sub_surf = self.standard_text_font.render(
            "Press 'C' to Reset", True, configuration_settings.COLOR_EXPLORED
        )
        sub_rect = sub_surf.get_rect(center=(center_x, center_y + 40))
        self.target_surface.blit(sub_surf, sub_rect)

    def check_button_clicks(self, pos):
        for btn in self.buttons:
            if btn.is_clicked(pos):
                return btn.action_payload
        return None
