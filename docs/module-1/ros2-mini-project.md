# ROS 2 Mini Project: Simple Humanoid Robot Controller

In this mini-project, you'll build a simple humanoid robot controller using ROS 2 and rclpy. This project will integrate the concepts learned in this module to create a functional robot control system.

## Project Overview

You'll create a basic humanoid robot controller that:
- Publishes joint commands to move the robot
- Subscribes to sensor data to monitor the robot's state
- Provides services for high-level commands
- Implements a simple walking gait pattern

## Prerequisites

Before starting this project, ensure you have:
- ROS 2 installed and sourced
- Basic understanding of URDF
- Knowledge of rclpy basics
- A simulated or real humanoid robot (or just the URDF model)

## Project Structure

```
ros2_humanoid_controller/
├── launch/
│   └── humanoid_controller.launch.py
├── config/
│   └── controller_params.yaml
├── src/
│   ├── joint_command_publisher.py
│   ├── sensor_subscriber.py
│   ├── walking_controller.py
│   └── humanoid_services.py
└── CMakeLists.txt
```

## Step 1: Basic Joint Command Publisher

First, let's create a node that publishes joint commands:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__('joint_command_publisher')
        self.publisher = self.create_publisher(JointState, 'joint_commands', 10)

        # Define joint names for a simple humanoid
        self.joint_names = [
            'left_hip_joint', 'left_knee_joint', 'left_ankle_joint',
            'right_hip_joint', 'right_knee_joint', 'right_ankle_joint',
            'left_shoulder_joint', 'left_elbow_joint',
            'right_shoulder_joint', 'right_elbow_joint'
        ]

        # Timer for publishing commands
        timer_period = 0.05  # 20 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = JointState()
        msg.name = self.joint_names
        msg.position = self.calculate_joint_positions()
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)

    def calculate_joint_positions(self):
        # Simple oscillating pattern for demonstration
        time = self.i * 0.05  # Convert to time
        positions = []

        for idx, joint_name in enumerate(self.joint_names):
            if 'hip' in joint_name:
                # Hip joints move in opposition for walking
                phase = math.pi if 'right' in joint_name else 0
                pos = 0.2 * math.sin(time * 2 + phase)
            elif 'knee' in joint_name:
                # Knee joints follow hip with offset
                phase = math.pi * 0.5 if 'right' in joint_name else 0
                pos = 0.3 * math.sin(time * 2 + phase)
            elif 'ankle' in joint_name:
                # Ankle joints for balance
                pos = 0.1 * math.sin(time * 2)
            elif 'shoulder' in joint_name:
                # Arm movement for balance
                pos = 0.5 * math.sin(time * 1.5)
            elif 'elbow' in joint_name:
                # Elbow movement synchronized with shoulders
                pos = 0.3 * math.sin(time * 1.5 + math.pi)
            else:
                pos = 0.0
            positions.append(pos)

        self.i += 1
        return positions

def main(args=None):
    rclpy.init(args=args)
    node = JointCommandPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 2: Sensor Subscriber Node

Create a node to subscribe to sensor data:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32MultiArray

class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')

        # Subscribe to joint states
        self.joint_subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10)

        # Subscribe to IMU data for balance
        self.imu_subscription = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_callback,
            10)

        # Publisher for balance corrections
        self.balance_pub = self.create_publisher(Float32MultiArray, 'balance_corrections', 10)

        self.joint_states = None
        self.imu_data = None

    def joint_state_callback(self, msg):
        self.joint_states = msg
        self.get_logger().info(f'Received {len(msg.name)} joints')

    def imu_callback(self, msg):
        self.imu_data = msg
        # Simple balance check - if tilt is too high, publish correction
        if abs(msg.orientation.z) > 0.1:  # Threshold for tilt
            correction_msg = Float32MultiArray()
            correction_msg.data = [msg.orientation.z * 0.5]  # Simple proportional correction
            self.balance_pub.publish(correction_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SensorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## Step 3: Walking Controller Node

Create a node that implements a simple walking pattern:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger
import time

class WalkingController(Node):
    def __init__(self):
        super().__init__('walking_controller')

        # Service to start/stop walking
        self.srv = self.create_service(Trigger, 'start_walking', self.start_walking_callback)
        self.srv2 = self.create_service(Trigger, 'stop_walking', self.stop_walking_callback)

        # Publisher for walking commands
        self.cmd_pub = self.create_publisher(String, 'walking_commands', 10)

        self.is_walking = False
        self.step_phase = 0

    def start_walking_callback(self, request, response):
        if not self.is_walking:
            self.is_walking = True
            self.get_logger().info('Starting walking sequence')
            response.success = True
            response.message = 'Walking started'

            # Start walking timer
            self.walk_timer = self.create_timer(0.5, self.walk_step)
        else:
            response.success = False
            response.message = 'Already walking'
        return response

    def stop_walking_callback(self, request, response):
        self.is_walking = False
        self.get_logger().info('Stopping walking sequence')
        response.success = True
        response.message = 'Walking stopped'
        return response

    def walk_step(self):
        if self.is_walking:
            # Simple walking gait pattern
            if self.step_phase == 0:
                cmd_msg = String()
                cmd_msg.data = 'lift_left_leg'
                self.cmd_pub.publish(cmd_msg)
                self.step_phase = 1
            elif self.step_phase == 1:
                cmd_msg = String()
                cmd_msg.data = 'move_left_leg_forward'
                self.cmd_pub.publish(cmd_msg)
                self.step_phase = 2
            elif self.step_phase == 2:
                cmd_msg = String()
                cmd_msg.data = 'place_left_leg'
                self.cmd_pub.publish(cmd_msg)
                self.step_phase = 3
            elif self.step_phase == 3:
                cmd_msg = String()
                cmd_msg.data = 'lift_right_leg'
                self.cmd_pub.publish(cmd_msg)
                self.step_phase = 4
            elif self.step_phase == 4:
                cmd_msg = String()
                cmd_msg.data = 'move_right_leg_forward'
                self.cmd_pub.publish(cmd_msg)
                self.step_phase = 5
            elif self.step_phase == 5:
                cmd_msg = String()
                cmd_msg.data = 'place_right_leg'
                self.cmd_pub.publish(cmd_msg)
                self.step_phase = 0

def main(args=None):
    rclpy.init(args=args)
    node = WalkingController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## Step 4: Launch File

Create a launch file to start all nodes together:

```python
# launch/humanoid_controller.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='your_package_name',
            executable='joint_command_publisher',
            name='joint_command_publisher',
            output='screen'
        ),
        Node(
            package='your_package_name',
            executable='sensor_subscriber',
            name='sensor_subscriber',
            output='screen'
        ),
        Node(
            package='your_package_name',
            executable='walking_controller',
            name='walking_controller',
            output='screen'
        ),
    ])
```

## Running the Project

1. Make sure all Python files are executable:
```bash
chmod +x src/*.py
```

2. Build the package:
```bash
colcon build
source install/setup.bash
```

3. Run the launch file:
```bash
ros2 launch your_package humanoid_controller.launch.py
```

4. Test the walking service:
```bash
ros2 service call /start_walking std_srvs/srv/Trigger
```

## Extending the Project

Consider these enhancements:
- Add more sophisticated gait patterns
- Implement balance control using IMU feedback
- Add obstacle avoidance
- Create a state machine for different walking modes
- Integrate with a real humanoid robot or simulation

## Key Learning Outcomes

This project demonstrates:
- Integration of multiple ROS 2 nodes
- Publisher-subscriber pattern for real-time control
- Service-based command interface
- Parameter management
- Launch file configuration

This simple controller forms the foundation for more complex humanoid robot control systems.