"""
User Interface Management Layer.
Responsible for rendering the Control Panel and translating
application state into visual text on the screen.
"""

import pygame

import utils.config as configuration_settings


class InterfaceRenderer:
    def __init__(self, display_surface):
        self.target_surface = display_surface

        self.standard_text_font = pygame.font.SysFont("JetBrainsMono Nerd Font", 20)
        self.prominent_header_font = pygame.font.SysFont(
            "JetBrainsMono Nerd Font", 32, bold=True
        )

    def render_control_panel(self, active_algorithm_name, execution_status):
        """
        Draws the sidebar UI, separating the grid from the control interface.
        """
        # Draw Section Divider (The line between grid and menu)
        pygame.draw.line(
            self.target_surface,
            configuration_settings.COLOR_GRID,
            (800, 0),
            (800, configuration_settings.WINDOW_HEIGHT),
            2,
        )

        # Render Application Title
        title_visual = self.prominent_header_font.render(
            "GOOD PERFORMANCE TIME APP", True, configuration_settings.COLOR_PATH
        )
        self.target_surface.blit(title_visual, (815, 50))

        # Render Algorithm Selection Status
        algorithm_display_text = f"Algorithm: {active_algorithm_name}"
        algorithm_label_visual = self.standard_text_font.render(
            algorithm_display_text, True, configuration_settings.COLOR_START
        )
        self.target_surface.blit(algorithm_label_visual, (815, 120))

        # Render Dynamic Execution Status (Running vs Idle)
        status_display_color = (
            configuration_settings.COLOR_DYNAMIC
            if execution_status == "RUNNING"
            else configuration_settings.COLOR_EXPLORED
        )
        status_label_visual = self.standard_text_font.render(
            f"Status: {execution_status}", True, status_display_color
        )
        self.target_surface.blit(status_label_visual, (815, 150))

        # Render Interaction Guide (User Manual)
        interaction_instructions = [
            "1-6: Select Algorithm",
            "SPACE: Start Search",
            "C: Clear Full Grid",
            "LEFT-CLICK: Set Start/Target/Wall",
            "RIGHT-CLICK: Erase Node",
        ]

        for line_index, instruction_text in enumerate(interaction_instructions):
            instruction_visual = self.standard_text_font.render(
                instruction_text, True, configuration_settings.COLOR_EMPTY
            )
            # Offset vertically based on line index
            vertical_pixel_position = 300 + (line_index * 35)
            self.target_surface.blit(instruction_visual, (815, vertical_pixel_position))
