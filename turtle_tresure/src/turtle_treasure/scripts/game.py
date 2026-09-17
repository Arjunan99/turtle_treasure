#!/usr/bin/env python3
"""
ROS 1 Node: Turtle Treasure Hunt Game
Simple educational game using ROS 1 Noetic, rospy, and turtlesim.
"""

import math
import random
import rospy
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill


class TurtleTreasureGame:
    def __init__(self):
        # 1. Initialize ROS 1 node
        rospy.init_node('turtle_treasure_game')

        # 2. Game State Variables
        self.score = 0
        self.max_score = 5
        self.treasure_name = 'treasure'
        self.treasure_x = None
        self.treasure_y = None
        self.player_x = None
        self.player_y = None
        self.is_processing = False
        self.game_over = False

        # 3. Connect to turtlesim Services (/spawn, /kill)
        rospy.loginfo("Connecting to turtlesim services (/spawn, /kill)...")
        rospy.wait_for_service('/spawn')
        rospy.wait_for_service('/kill')
        self.spawn_proxy = rospy.ServiceProxy('/spawn', Spawn)
        self.kill_proxy = rospy.ServiceProxy('/kill', Kill)
        rospy.loginfo("Connected to turtlesim services successfully!")

        # 4. Subscribe to player turtle position
        self.pose_sub = rospy.Subscriber(
            '/turtle1/pose',
            Pose,
            self.pose_callback
        )

        rospy.loginfo("=============================================")
        rospy.loginfo("     WELCOME TO TURTLE TREASURE HUNT!        ")
        rospy.loginfo("  Drive turtle1 to collect 5 treasures to win ")
        rospy.loginfo("=============================================")

        # Clean up any leftover turtle named 'treasure' from a previous game run
        try:
            self.kill_proxy(self.treasure_name)
        except rospy.ServiceException:
            pass

        # Spawn the first treasure
        self.spawn_treasure()

    def spawn_treasure(self):
        """Spawns a new treasure turtle at a random position."""
        if self.game_over:
            return

        self.is_processing = True

        # Random coordinate inside safe turtlesim window bounds (bounds are ~0.0 to ~11.0)
        x = round(random.uniform(1.5, 9.5), 2)
        y = round(random.uniform(1.5, 9.5), 2)
        theta = 0.0

        try:
            self.spawn_proxy(x, y, theta, self.treasure_name)
            self.treasure_x = x
            self.treasure_y = y
            self.is_processing = False
            rospy.loginfo(f"New treasure appeared at ({x:.2f}, {y:.2f})")
        except rospy.ServiceException as e:
            rospy.logerr(f"Failed to spawn treasure: {e}")
            self.is_processing = False

    def pose_callback(self, msg: Pose):
        """Callback for /turtle1/pose to track player and check distance."""
        self.player_x = msg.x
        self.player_y = msg.y

        # Do nothing if game finished, waiting for spawn/kill, or no treasure active
        if self.game_over or self.is_processing or self.treasure_x is None:
            return

        # Euclidean distance: sqrt((x2 - x1)^2 + (y2 - y1)^2)
        dx = self.player_x - self.treasure_x
        dy = self.player_y - self.treasure_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Collision threshold: 0.5 units
        if distance < 0.5:
            self.collect_treasure()

    def collect_treasure(self):
        """Handles collection, updates score, and triggers win or respawn."""
        self.is_processing = True
        self.score += 1

        rospy.loginfo("Treasure collected!")
        rospy.loginfo(f"Score: {self.score}")

        if self.score >= self.max_score:
            self.game_over = True
            self.kill_treasure()
            print("\n" + "=" * 26)
            print("       YOU WIN!")
            print(f"Final Score: {self.score}/{self.max_score}")
            print("=" * 26 + "\n")
        else:
            # Remove current treasure and spawn the next one
            self.kill_treasure()
            self.spawn_treasure()

    def kill_treasure(self):
        """Removes the collected treasure turtle from the simulator."""
        try:
            self.kill_proxy(self.treasure_name)
            self.treasure_x = None
            self.treasure_y = None
        except rospy.ServiceException as e:
            rospy.logerr(f"Failed to remove treasure: {e}")


def main():
    try:
        game = TurtleTreasureGame()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
