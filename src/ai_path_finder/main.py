"""
AI Pathfinder Entry Point.
This is a minimalist launcher that abstracts all implementation details,
simply initializing the application orchestrator.
"""

from logic.app import PathfinderApp


def main():
    """
    Initializes the high-level application controller and starts
    the execution heartbeat.
    """
    pathfinder_application = PathfinderApp()
    pathfinder_application.run()


if __name__ == "__main__":
    main()
