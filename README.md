# Turtle Treasure Hunt (ROS 1 Noetic)

An interactive educational game built using **ROS 1 (Noetic)**, **`rospy`**, and **`turtlesim`**.

---

## 🎮 Overview
The objective of the game is to drive `turtle1` around the arena to collect randomly spawned treasure turtles. Once 5 treasures are collected, you win!

### Key ROS Concepts Demonstrated
* **Service Calls**: Uses `/spawn` and `/kill` turtlesim services to dynamically create and despawn treasure targets.
* **Topic Subscription**: Subscribes to `/turtle1/pose` to monitor the player's real-time coordinates.
* **Collision Detection**: Computes Euclidean distance between the player and the treasure:
  $$\text{distance} = \sqrt{(x_{\text{player}} - x_{\text{treasure}})^2 + (y_{\text{player}} - y_{\text{treasure}})^2}$$
  A collision is triggered whenever $\text{distance} < 0.5$ units.
* **Game State Management**: Manages arena coordinate bounds (1.5 to 9.5), score tracking, and victory conditions.

---

## 📂 Repository Structure

The repository contains a complete catkin workspace (`turtle_tresure`) holding the `turtle_treasure` ROS package under `src/`:

```
turtle_treasure/                        # Repository Root
├── README.md                           # Documentation
├── .gitignore                          # Git ignore rules
├── .gitattributes                      # Git attributes configuration
└── turtle_tresure/                     # Catkin Workspace folder
    └── src/
        └── turtle_treasure/            # ROS Package
            ├── CMakeLists.txt          # Catkin build configuration
            ├── package.xml             # Package dependencies (rospy, turtlesim)
            └── scripts/
                └── game.py             # Game loop & ROS node script
```

---

## 🚀 How to Run

### 1. Build the Catkin Workspace
From the repository root, enter the workspace folder and build:
```bash
cd turtle_tresure
catkin_make
source devel/setup.bash
```

### 2. Make the Script Executable
```bash
chmod +x src/turtle_treasure/scripts/game.py
```

### 3. Launch the Game
Open separate terminals:

**Terminal 1: Start ROS Master**
```bash
roscore
```

**Terminal 2: Launch Turtlesim GUI**
```bash
rosrun turtlesim turtlesim_node
```

**Terminal 3: Start Teleoperation (to drive turtle1)**
```bash
rosrun turtlesim turtle_teleop_key
```

**Terminal 4: Start the Treasure Game Node**
```bash
rosrun turtle_treasure game.py
```

Drive `turtle1` using the arrow keys to collect 5 treasures to win!
