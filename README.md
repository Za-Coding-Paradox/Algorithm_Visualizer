# AI Pathfinder Visualizer

A modular Python application designed to visualize classic AI search algorithms on a 2D grid using a **Catppuccin Mocha** color palette. This project focuses on high-level abstraction and strict separation of concerns between UI, Logic, and Algorithms.

## 🛠️ Features
* **6 Search Algorithms**: Includes BFS, DFS, UCS, DLS, IDDFS, and Bidirectional Search.
* **Real-time Visualization**: Generators are used to visualize the frontier expansion and path discovery step-by-step.
* **Interactive UI**: A custom-built control panel and grid interaction system using Pygame.
* **Clean Architecture**: Deeply abstracted layers for easier maintenance and testing.

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.10+**
* **Poetry** (Python package manager)
* **JetBrainsMono Nerd Font** (Recommended for UI rendering)

### Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repo-link>
   cd ai_pathfinder
   ```
2. **Install Dependencies**:
   ```bash
   poetry install
   ```
### 🎮 Controls

The application utilizes a state-driven interaction model to manage the grid environment and algorithm execution.

#### **Mouse Interactions**
* **Left Click**: Context-aware placement.
    * **1st Click**: Sets the **Start Node** (Green).
    * **2nd Click**: Sets the **Target Node** (Orange).
    * **3rd+ Clicks**: Places **Walls** (Dark) to create obstacles.
* **Right Click**: **Erase Mode**. Resets any individual node back to its **Empty** state.

#### **Keyboard Commands**
* **Keys 1 - 6**: **Algorithm Selection**. Quickly switch between the following search methods:
    1. Breadth-First Search (BFS)
    2. Depth-First Search (DFS)
    3. Uniform Cost Search (UCS)
    4. Depth-Limited Search (DLS)
    5. Iterative Deepening DFS (IDDFS)
    6. Bidirectional Search
* **SPACE**: **Execute**. Begins the search visualization for the currently selected algorithm.
* **C Key**: **Full Reset**. Completely wipes the grid, clearing all walls, explored nodes, and paths to start fresh.

---

### 👥 Project Owners & Contact

This project is a collaborative effort developed for the AI Pathfinder project.

**Primary Developers:**
* **za-coding-paradox**
    * Role: Lead Logic Architect & Algorithm Implementation
    * GitHub: [github.com/za-coding-paradox](https://github.com/za-coding-paradox)
* **Mtz00**
    * Role: UI/UX Designer & Grid Systems Engineering
    * GitHub: [github.com/Mtz00](https://github.com/Mtz00)

**Project Information:**
* **Deadline**: February 16, 2026
* **Location**: Faisalabad, Punjab, Pakistan
* **Stack**: Python, Pygame, Poetry, Neovim 0.11

---

### 🛠️ Technical Details

* **Visual Palette**: Inspired by [Catppuccin Mocha](https://github.com/catppuccin/catppuccin).
* **Environment**: Configured via **Poetry** for dependency management.
* **Architecture**: Implements a strict Model-View-Controller (MVC) style abstraction.
