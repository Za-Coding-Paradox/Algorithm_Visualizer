# AI Pathfinder Visualizer

A real-time, interactive pathfinding algorithm visualizer built with Python and Pygame. Watch classical search algorithms explore a grid and find the shortest path — step by step.

---

## Features

- **6 Search Algorithms** visualized in real-time:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Uniform Cost Search (UCS) with random cell weights
  - Depth-Limited Search (DLS)
  - Iterative Deepening DFS (IDDFS)
  - Bidirectional BFS
- Interactive grid — click to place start, target, and walls
- Step-by-step animation with configurable speed
- Visual distinction between frontier, explored, and path nodes
- Elapsed time display on completion
- UCS mode renders per-cell weights directly on the grid

---

## Project Structure
```
.
└── src/
    ├── ai_path_finder/
    │   └── main.py               # Entry point
    ├── algorithms/
    │   ├── bfs.py
    │   ├── dfs.py
    │   ├── ucs.py
    │   ├── dls.py
    │   ├── iddfs.py
    │   └── bidirectional.py
    ├── logic/
    │   ├── app.py                # Application orchestrator
    │   └── simulation_manager.py # Bridges UI and algorithm layer
    ├── ui/
    │   ├── grid.py               # Grid rendering and node logic
    │   └── menu.py               # Sidebar, buttons, and popups
    └── utils/
        └── config.py             # Global constants and color palette
```

---

## Prerequisites

### 1. Python 3.10+

Download from [python.org](https://www.python.org/downloads/).
On Windows, check **"Add Python to PATH"** during setup.

Verify:
```bash
python --version
```

### 2. Poetry

**Linux / macOS / WSL:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Verify:
```bash
poetry --version
```

> On Windows the default install path is `%APPDATA%\Python\Scripts` — ensure it is on your PATH, then restart your terminal.

---

## Getting Started

### Step 1 — Clone the Repository
```bash
git clone https://github.com/your-username/ai-path-finder.git
cd ai-path-finder
```

### Step 2 — Install Dependencies
```bash
poetry install
```

This creates an isolated virtual environment and installs all required packages as defined in `pyproject.toml`.

### Step 3 — Run the Application
```bash
poetry run python src/ai_path_finder/main.py
```

Or activate the environment first, then run directly:
```bash
poetry shell
python src/ai_path_finder/main.py
```

---

## How to Use

Once the application window opens:

| Action | Input |
|---|---|
| Place Start Node | Left-click any empty cell (1st click) |
| Place Target Node | Left-click any empty cell (2nd click) |
| Draw Walls | Hold and drag left-click over cells |
| Erase a Cell | Right-click any node |
| Select Algorithm | Click an algorithm button in the sidebar |
| Start Simulation | Press `SPACE` |
| Reset Grid | Press `C` |

**Tips:**

- Both a start and a target node must be placed before pressing `SPACE`.
- Walls are impassable — use them to build mazes and stress-test each algorithm.
- Switch algorithms via the sidebar buttons to compare their exploration patterns.
- In **UCS** mode, each cell displays a random weight (1–5). The algorithm finds the minimum-cost path, not necessarily the geometrically shortest one.
- After a simulation completes, a popup shows whether a path was found and the total elapsed time. Press `C` to reset and run again.

---

## Color Legend

| Color | Meaning |
|---|---|
| Green | Start node |
| Orange | Target node |
| Yellow | Frontier — nodes queued for exploration |
| Blue | Explored — nodes already visited |
| Pink | Final path |
| Dark / Black | Wall |

---

## Configuration

Edit `src/utils/config.py` to tune the visualizer:
```python
GRID_SIZE   = 25      # Number of rows and columns
CELL_SIZE   = 20      # Pixel size per cell
STEP_DELAY  = 0.05    # Delay in seconds between algorithm steps (lower = faster)
FPS         = 60      # Maximum render frame rate
```

Setting `STEP_DELAY` to `0` runs the simulation at maximum speed.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pygame` | Window rendering, grid drawing, and input handling |

All dependencies are declared in `pyproject.toml` and installed automatically via `poetry install`.

---

## Windows Quick-Start

A `setup_and_run.bat` file is included in the repository root. Double-clicking it will:

1. Verify Python is installed and accessible
2. Check for Poetry and install it if missing
3. Run `poetry install` to configure the environment
4. Launch the application

See [`setup_and_run.bat`](./setup_and_run.bat).

---

## License

See [`LICENSE.md`](./LICENSE.md).

---

## Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss your proposal.
