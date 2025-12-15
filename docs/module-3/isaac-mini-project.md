# Isaac Mini Project: Complete Humanoid AI Brain Implementation

In this comprehensive mini-project, you'll implement a complete AI brain for a humanoid robot using Isaac Sim for simulation, Isaac ROS for perception and navigation, and Nav2 for autonomous navigation. This project integrates all the concepts learned in Module 3.

## Project Overview

Build a complete humanoid robot AI system that includes:
- Photorealistic simulation in Isaac Sim
- Visual SLAM for environment mapping
- Nav2-based navigation for autonomous movement
- Perception systems for object detection and recognition
- Human-aware navigation behaviors
- GPU-accelerated processing throughout

## Prerequisites

Before starting this project, ensure you have:
- NVIDIA RTX GPU (20xx/30xx series or higher)
- Isaac Sim installed via Omniverse
- Isaac ROS packages installed
- ROS 2 Humble Hawksbill
- Nav2 installed and configured
- Basic understanding of all Module 3 concepts

## Project Structure

```
isaac_humanoid_brain/
├── configs/
│   ├── isaac_sim/
│   │   ├── robot_config.yaml
│   │   └── environment_config.yaml
│   ├── perception/
│   │   ├── vslam_config.yaml
│   │   └── object_detection.yaml
│   ├── navigation/
│   │   ├── nav2_params.yaml
│   │   └── costmap_params.yaml
│   └── ai_brain/
│       └── ai_brain_config.yaml
├── launch/
│   ├── simulation.launch.py
│   ├── perception.launch.py
│   ├── navigation.launch.py
│   └── ai_brain.launch.py
├── scripts/
│   ├── ai_brain_node.py
│   ├── perception_manager.py
│   ├── navigation_manager.py
│   └── behavior_manager.py
├── worlds/
│   └── humanoid_office.usd
└── rviz/
    └── humanoid_ai_brain.rviz
```

## Step 1: Isaac Sim Environment Setup

Create a USD environment for humanoid robot testing:

```usd
# worlds/humanoid_office.usd
#usda 1.0

def Xform "World"
{
    def Xform "Robot" (
        prepend references = </Isaac/Robots/HumanoidRobot>
    )
    {
        # Robot configuration
        double3 xformOp:translate = (0, 0, 1.0)
        uniform token[] apiSchemas = ["IsaacRobotConfigurationAPI"]

        # IsaacRobotConfigurationAPI settings
        bool enable_collision = 1
        bool enable_physics = 1
    }

    def Xform "Environment"
    {
        # Office environment elements
        def Xform "Floor"
        {
            def Cube "floor" (
                prepend references = </Isaac/Props/Prismarine/Room/Geometry/Cube>
            )
            {
                double3 xformOp:translate = (0, 0, 0)
                double3 xformOp:scale = (10, 10, 0.1)
            }
        }

        def Xform "Obstacles"
        {
            # Tables, chairs, and other office furniture
            def Cube "table1"
            {
                double3 xformOp:translate = (2, 1, 0.4)
                double3 xformOp:scale = (1.5, 0.8, 0.8)
            }

            def Cube "chair1"
            {
                double3 xformOp:translate = (3, -1, 0.3)
                double3 xformOp:scale = (0.5, 0.5, 0.6)
            }
        }

        def Xform "Lighting"
        {
            # Realistic lighting setup
            def DistantLight "sun"
            {
                float angle = 0.5
                float intensity = 300
                color3f color = (1, 1, 1)
                float exposure = 0
                bool enableColorTemperature = 0
                float colorTemperature = 5500
            }
        }
    }
}
```

## Step 2: Perception System Configuration

Create the perception configuration file:

```yaml
# configs/perception/vslam_config.yaml
/**:
  ros__parameters:
    # Isaac ROS Visual SLAM parameters
    rectified_left_topic: "/camera/rgb/left/image_rect_color"
    rectified_right_topic: "/camera/rgb/right/image_rect_color"
    left_camera_info_topic: "/camera/rgb/left/camera_info"
    right_camera_info_topic: "/camera/rgb/right/camera_info"

    # Output topics
    pose_topic: "/visual_slam/pose"
    odom_topic: "/visual_slam/odometry"
    map_topic: "/visual_slam/map"
    trajectory_topic: "/visual_slam/trajectory"

    # Processing parameters
    enable_rectification: true
    enable_imu_fusion: true
    enable_localization: true
    enable_mapping: true

    # Performance parameters
    tracking_rate: 30.0
    mapping_rate: 10.0
    min_num_features: 100
    max_num_features: 1000

    # GPU parameters
    use_gpu: true
    gpu_device_id: 0

    # Feature parameters
    detector_type: "ORB"
    descriptor_type: "ORB"
    matcher_type: "BF"

    # Optimization parameters
    enable_bundle_adjustment: true
    enable_loop_closure: true
    bundle_adjustment_frequency: 10
    loop_closure_frequency: 5
```

## Step 3: Navigation Configuration

Create the Nav2 configuration for humanoid navigation:

```yaml
# configs/navigation/nav2_params.yaml
bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    default_nav_through_poses_bt_xml: /opt/ros/humble/share/nav2_bt_navigator/behavior_trees/navigate_w_replanning_and_recovery.xml
    default_nav_to_pose_bt_xml: /opt/ros/humble/share/nav2_bt_navigator/behavior_trees/navigate_w_replanning_and_recovery.xml
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_smooth_path_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_assisted_teleop_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_globally_consistent_localization_condition_bt_node
    - nav2_is_path_valid_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_controller_cancel_bt_node
    - nav2_path_longer_on_approach_bt_node
    - nav2_wait_cancel_bt_node
    - nav2_spin_cancel_bt_node
    - nav2_back_up_cancel_bt_node
    - nav2_assisted_teleop_cancel_bt_node
    - nav2_drive_on_heading_cancel_bt_node

bt_navigator_rclcpp_node:
  ros__parameters:
    use_sim_time: True

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.01
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.01
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Humanoid-specific controller
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      time_steps: 50
      model_dt: 0.05
      batch_size: 1000
      vx_std: 0.2
      vy_std: 0.2
      wz_std: 0.3
      vx_max: 0.5
      vx_min: -0.2
      vy_max: 0.3
      wz_max: 0.3
      simulation_time: 2.0
      speed_scaling_factor: 0.2
      control_duration: 0.05
      transform_tolerance: 0.1
      debug_trajectory_details: false

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 10.0
      publish_frequency: 10.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: True
      rolling_window: true
      width: 6
      height: 6
      resolution: 0.05
      robot_radius: 0.3  # Humanoid robot radius
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: False
        origin_z: 0.0
        z_resolution: 0.2
        z_voxels: 10
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
  local_costmap_client:
    ros__parameters:
      use_sim_time: True
  local_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: True
      robot_radius: 0.3
      resolution: 0.05
      track_unknown_space: false
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
  global_costmap_client:
    ros__parameters:
      use_sim_time: True
  global_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner::NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

smoother_server:
  ros__parameters:
    use_sim_time: True
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      do_refinement: True

behavior_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "wait", "assisted_teleop"]
    spin:
      plugin: "nav2_behaviors::Spin"
      spin_dist: 1.57
    backup:
      plugin: "nav2_behaviors::BackUp"
      backup_dist: 0.15
      backup_speed: 0.05
    wait:
      plugin: "nav2_behaviors::Wait"
      wait_duration: 1.0
    assisted_teleop:
      plugin: "nav2_behaviors::AssistedTeleop"
      min_linear_speed: 0.05
      max_linear_speed: 0.3
      min_angular_speed: 0.1
      max_angular_speed: 0.5

waypoint_follower:
  ros__parameters:
    loop_rate: 20
    stop_on_failure: false
    waypoint_task_executor_plugin: "wait_at_waypoint"
    wait_at_waypoint:
      plugin: "nav2_waypoint_follower::WaitAtWaypoint"
      enabled: true
      waypoint_pause_duration: 200
```

## Step 4: AI Brain Node Implementation

Create the main AI brain node:

```python
# scripts/ai_brain_node.py
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, LaserScan
from std_msgs.msg import String
from builtin_interfaces.msg import Duration
import numpy as np
import cv2
from cv_bridge import CvBridge
from typing import Optional, List, Dict, Any
import time

class HumanoidAIBrainNode(Node):
    def __init__(self):
        super().__init__('humanoid_ai_brain')

        # Initialize components
        self.bridge = CvBridge()
        self.current_pose = None
        self.current_odom = None
        self.navigation_goals = []
        self.perception_data = {}
        self.behavior_state = "IDLE"
        self.last_behavior_switch = time.time()

        # QoS profiles
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Subscriptions
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )

        self.pose_sub = self.create_subscription(
            PoseStamped, '/visual_slam/pose', self.pose_callback, 10
        )

        self.image_sub = self.create_subscription(
            Image, '/camera/rgb/image_rect_color', self.image_callback, qos_profile
        )

        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )

        self.navigation_status_sub = self.create_subscription(
            String, '/navigation/status', self.navigation_status_callback, 10
        )

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.behavior_pub = self.create_publisher(String, '/behavior/status', 10)
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # Timer for main AI loop
        self.ai_loop_timer = self.create_timer(0.1, self.ai_loop)

        # Initialize perception and navigation managers
        self.perception_manager = PerceptionManager(self)
        self.navigation_manager = NavigationManager(self)
        self.behavior_manager = BehaviorManager(self)

        self.get_logger().info('Humanoid AI Brain initialized')

    def odom_callback(self, msg: Odometry):
        """Handle odometry messages"""
        self.current_odom = msg

    def pose_callback(self, msg: PoseStamped):
        """Handle pose estimation from VSLAM"""
        self.current_pose = msg.pose

    def image_callback(self, msg: Image):
        """Process camera images for perception"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            self.perception_manager.process_image(cv_image, msg.header.stamp)
        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

    def scan_callback(self, msg: LaserScan):
        """Process LIDAR data for navigation"""
        self.perception_manager.process_lidar(msg)

    def navigation_status_callback(self, msg: String):
        """Handle navigation status updates"""
        self.navigation_manager.update_status(msg.data)

    def ai_loop(self):
        """Main AI decision-making loop"""
        try:
            # Update perception
            self.perception_manager.update()

            # Determine current behavior based on perception and goals
            current_behavior = self.behavior_manager.determine_behavior()

            # Execute navigation if needed
            if current_behavior == "NAVIGATE":
                self.navigation_manager.execute_navigation()
            elif current_behavior == "EXPLORE":
                self.navigation_manager.explore_environment()
            elif current_behavior == "AVOID_OBSTACLE":
                self.navigation_manager.avoid_obstacles()
            elif current_behavior == "INTERACT":
                self.behavior_manager.execute_interaction()

            # Publish current behavior status
            behavior_msg = String()
            behavior_msg.data = current_behavior
            self.behavior_pub.publish(behavior_msg)

        except Exception as e:
            self.get_logger().error(f'Error in AI loop: {e}')

class PerceptionManager:
    def __init__(self, node: Node):
        self.node = node
        self.latest_image = None
        self.latest_lidar = None
        self.detected_objects = []
        self.environment_map = {}

    def process_image(self, image, timestamp):
        """Process camera image for object detection and scene understanding"""
        self.latest_image = image
        # In a real implementation, this would run object detection models
        # For this example, we'll simulate object detection
        self.detected_objects = self.simulate_object_detection(image)

    def process_lidar(self, lidar_msg):
        """Process LIDAR data for obstacle detection and mapping"""
        self.latest_lidar = lidar_msg
        # Process LIDAR ranges for obstacle detection
        obstacles = []
        for i, range_val in enumerate(lidar_msg.ranges):
            if 0 < range_val < lidar_msg.range_max:
                angle = lidar_msg.angle_min + i * lidar_msg.angle_increment
                x = range_val * np.cos(angle)
                y = range_val * np.sin(angle)
                if range_val < 1.0:  # Obstacle within 1m
                    obstacles.append((x, y, range_val))
        self.environment_map['obstacles'] = obstacles

    def simulate_object_detection(self, image):
        """Simulate object detection on image"""
        # This is a simplified simulation - in reality, this would use
        # deep learning models for object detection
        height, width = image.shape[:2]
        objects = []

        # Simulate detecting some objects in the image
        if width > 0 and height > 0:
            # Simulate detecting a person in the center
            objects.append({
                'class': 'person',
                'confidence': 0.8,
                'bbox': [width//2 - 50, height//2 - 100, width//2 + 50, height//2 + 100],
                'center': (width//2, height//2)
            })

        return objects

    def update(self):
        """Update perception data"""
        # This method would run periodic perception updates
        pass

class NavigationManager:
    def __init__(self, node: Node):
        self.node = node
        self.current_status = "IDLE"
        self.current_goal = None
        self.path = []
        self.is_exploring = False

    def update_status(self, status: str):
        """Update navigation status"""
        self.current_status = status

    def execute_navigation(self):
        """Execute navigation to current goal"""
        if self.current_goal and self.current_status != "EXECUTING":
            self.node.get_logger().info(f'Navigating to goal: {self.current_goal}')
            # In a real implementation, this would send goals to Nav2
            # For simulation, we'll just update the status
            self.current_status = "EXECUTING"

    def explore_environment(self):
        """Explore the environment systematically"""
        if not self.is_exploring:
            self.node.get_logger().info('Starting environment exploration')
            self.is_exploring = True
            # In a real implementation, this would implement exploration strategies
            # like frontier-based exploration

    def avoid_obstacles(self):
        """Execute obstacle avoidance behaviors"""
        self.node.get_logger().info('Executing obstacle avoidance')
        # In a real implementation, this would use local planner recovery behaviors
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.0
        cmd_vel.angular.z = 0.5  # Turn to avoid obstacle
        self.node.cmd_vel_pub.publish(cmd_vel)

class BehaviorManager:
    def __init__(self, node: Node):
        self.node = node
        self.behavior_priority = [
            "EMERGENCY_STOP",
            "AVOID_OBSTACLE",
            "INTERACT",
            "NAVIGATE",
            "EXPLORE",
            "IDLE"
        ]

    def determine_behavior(self) -> str:
        """Determine the highest priority behavior based on current state"""
        perception = self.node.perception_manager
        navigation = self.node.navigation_manager

        # Check for emergencies first
        if self.check_emergency_conditions():
            return "EMERGENCY_STOP"

        # Check for obstacles
        if self.check_obstacle_conditions():
            return "AVOID_OBSTACLE"

        # Check for interaction opportunities
        if self.check_interaction_conditions():
            return "INTERACT"

        # Check navigation goals
        if self.check_navigation_conditions():
            return "NAVIGATE"

        # Default to exploration if no specific goals
        return "EXPLORE"

    def check_emergency_conditions(self) -> bool:
        """Check for emergency conditions requiring immediate stop"""
        # Check for collision imminent based on LIDAR
        if hasattr(self.node.perception_manager, 'environment_map'):
            obstacles = self.node.perception_manager.environment_map.get('obstacles', [])
            for _, _, distance in obstacles:
                if distance < 0.3:  # Less than 30cm from obstacle
                    return True
        return False

    def check_obstacle_conditions(self) -> bool:
        """Check if obstacle avoidance is needed"""
        if hasattr(self.node.perception_manager, 'environment_map'):
            obstacles = self.node.perception_manager.environment_map.get('obstacles', [])
            for _, _, distance in obstacles:
                if distance < 0.8:  # Less than 80cm from obstacle
                    return True
        return False

    def check_interaction_conditions(self) -> bool:
        """Check if human interaction is needed"""
        # Check if person is detected in front of robot
        objects = self.node.perception_manager.detected_objects
        for obj in objects:
            if obj['class'] == 'person':
                # Check if person is in front of robot (simplified)
                center_x = obj['center'][0]
                image_width = self.node.perception_manager.latest_image.shape[1] if self.node.perception_manager.latest_image is not None else 640
                if abs(center_x - image_width/2) < image_width/4:  # In center third of image
                    return True
        return False

    def check_navigation_conditions(self) -> bool:
        """Check if navigation to specific goals is needed"""
        # Check if there are specific navigation goals
        return len(self.node.navigation_goals) > 0

    def execute_interaction(self):
        """Execute human interaction behaviors"""
        self.node.get_logger().info('Executing human interaction behavior')
        # In a real implementation, this would include:
        # - Head/eye movement toward detected person
        # - Speech output
        # - Gesture execution
        # - Social navigation patterns

def main(args=None):
    rclpy.init(args=args)

    ai_brain = HumanoidAIBrainNode()

    try:
        rclpy.spin(ai_brain)
    except KeyboardInterrupt:
        pass
    finally:
        ai_brain.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 5: Launch Files

Create the main launch file:

```python
# launch/ai_brain.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, SetParameter
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit
from launch.actions import TimerAction

def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    params_file = LaunchConfiguration('params_file', default=PathJoinSubstitution([
        FindPackageShare('isaac_humanoid_brain'),
        'configs',
        'ai_brain',
        'ai_brain_config.yaml'
    ]))

    # Set parameters
    set_use_sim_time = SetParameter(name='use_sim_time', value=use_sim_time)

    # Launch Isaac Sim (if available)
    # Note: Isaac Sim launch would be more complex in practice
    isaac_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('isaac_ros_examples'),
                'launch',
                'isaac_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'headless': 'False',
            'world': PathJoinSubstitution([
                FindPackageShare('isaac_humanoid_brain'),
                'worlds',
                'humanoid_office.usd'
            ])
        }.items()
    )

    # Launch perception system
    perception_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('isaac_humanoid_brain'),
                'launch',
                'perception.launch.py'
            ])
        ])
    )

    # Launch navigation system
    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('isaac_humanoid_brain'),
                'launch',
                'navigation.launch.py'
            ])
        ])
    )

    # Launch AI brain node
    ai_brain_node = Node(
        package='isaac_humanoid_brain',
        executable='ai_brain_node',
        name='humanoid_ai_brain',
        parameters=[
            params_file,
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    # Launch RViz for visualization
    rviz_config = PathJoinSubstitution([
        FindPackageShare('isaac_humanoid_brain'),
        'rviz',
        'humanoid_ai_brain.rviz'
    ])

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        set_use_sim_time,
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Isaac Sim) clock if true'
        ),
        DeclareLaunchArgument(
            'params_file',
            default_value=params_file,
            description='Full path to the ROS2 parameters file to use for the AI brain node'
        ),
        # isaac_sim_launch,  # Uncomment when Isaac Sim is properly configured
        perception_launch,
        navigation_launch,
        ai_brain_node,
        rviz_node
    ])
```

## Step 6: RViz Configuration

Create an RViz configuration file for visualization:

```yaml
# rviz/humanoid_ai_brain.rviz
Panels:
  - Class: rviz_common/Displays
    Help Height: 78
    Name: Displays
    Property Tree Widget:
      Expanded:
        - /Global Options1
        - /Status1
        - /TF1/Frames1
        - /RobotModel1
        - /LaserScan1
        - /Image1
        - /Path1
        - /PoseArray1
      Splitter Ratio: 0.5
    Tree Height: 694
  - Class: rviz_common/Selection
    Name: Selection
  - Class: rviz_common/Tool Properties
    Expanded:
      - /2D Goal Pose1
      - /Publish Point1
    Name: Tool Properties
    Splitter Ratio: 0.5886790156364441
  - Class: rviz_common/Views
    Expanded:
      - /Current View1
    Name: Views
    Splitter Ratio: 0.5
Visualization Manager:
  Class: ""
  Displays:
    - Alpha: 0.5
      Cell Size: 1
      Class: rviz_default_plugins/Grid
      Color: 160; 160; 164
      Enabled: true
      Line Style:
        Line Width: 0.029999999329447746
        Value: Lines
      Name: Grid
      Normal Cell Count: 0
      Offset:
        X: 0
        Y: 0
        Z: 0
      Plane: XY
      Plane Cell Count: 10
      Reference Frame: <Fixed Frame>
      Value: true
    - Class: rviz_default_plugins/TF
      Enabled: true
      Frame Timeout: 15
      Frames:
        All Enabled: true
      Marker Scale: 1
      Name: TF
      Show Arrows: true
      Show Axes: true
      Show Names: false
      Tree:
        {}
      Update Interval: 0
      Value: true
    - Alpha: 1
      Class: rviz_default_plugins/RobotModel
      Collision Enabled: false
      Description File: ""
      Description Source: Topic
      Description Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /robot_description
      Enabled: true
      Links:
        All Links Enabled: true
        Expand Joint Details: false
        Expand Link Details: false
        Expand Tree: false
        Link Tree Style: Links in Alphabetic Order
      Name: RobotModel
      TF Prefix: ""
      Update Interval: 0
      Value: true
      Visual Enabled: true
    - Alpha: 1
      Autocompute Intensity Bounds: true
      Autocompute Value Bounds:
        Max Value: 10
        Min Value: -10
        Value: true
      Axis: Z
      Channel Name: intensity
      Class: rviz_default_plugins/LaserScan
      Color: 255; 255; 255
      Color Transformer: Intensity
      Decay Time: 0
      Enabled: true
      Invert Rainbow: false
      Max Color: 255; 255; 255
      Max Intensity: 0
      Min Color: 0; 0; 0
      Min Intensity: 0
      Name: LaserScan
      Position Transformer: XYZ
      Queue Size: 10
      Selectable: true
      Size (Pixels): 3
      Size (m): 0.009999999776482582
      Style: Flat Squares
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Best Effort
        Value: /scan
      Use Fixed Frame: true
      Use rainbow: true
      Value: true
    - Class: rviz_default_plugins/Image
      Enabled: true
      Max Value: 1
      Min Value: 0
      Name: Image
      Normalize Range: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Best Effort
        Value: /camera/rgb/image_rect_color
      Value: true
    - Alpha: 0.30000001192092896
      Buffer Length: 1
      Class: rviz_default_plugins/Path
      Color: 25; 255; 0
      Enabled: true
      Head Diameter: 0.30000001192092896
      Head Length: 0.20000000298023224
      Length: 0.30000001192092896
      Line Style: Lines
      Line Width: 0.029999999329447746
      Name: Path
      Offset:
        X: 0
        Y: 0
        Z: 0
      Pose Color: 255; 85; 255
      Pose Style: None
      Radius: 0.029999999329447746
      Shaft Diameter: 0.10000000149011612
      Shaft Length: 0.10000000149011612
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /plan
      Value: true
    - Class: rviz_default_plugins/PoseArray
      Color: 0; 255; 0
      Enabled: true
      Name: PoseArray
      Shaft Length: 0.30000001192092896
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /particlecloud
      Value: true
  Enabled: true
  Global Options:
    Background Color: 48; 48; 48
    Fixed Frame: map
    Frame Rate: 30
  Name: root
  Tools:
    - Class: rviz_default_plugins/Interact
      Hide Inactive Objects: true
    - Class: rviz_default_plugins/MoveCamera
    - Class: rviz_default_plugins/Select
    - Class: rviz_default_plugins/FocusCamera
    - Class: rviz_default_plugins/Measure
      Line color: 128; 128; 0
    - Class: rviz_default_plugins/SetInitialPose
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /initialpose
    - Class: rviz_default_plugins/SetGoal
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /goal_pose
    - Class: rviz_default_plugins/PublishPoint
      Single click: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /clicked_point
  Transformation:
    Current:
      Class: rviz_default_plugins/TF
  Value: true
  Views:
    Current:
      Class: rviz_default_plugins/Orbit
      Distance: 10
      Enable Stereo Rendering:
        Stereo Eye Separation: 0.05999999865889549
        Stereo Focal Distance: 1
        Swap Stereo Eyes: false
        Value: false
      Focal Point:
        X: 0
        Y: 0
        Z: 0
      Focal Shape Fixed Size: true
      Focal Shape Size: 0.05000000074505806
      Invert Z Axis: false
      Name: Current View
      Near Clip Distance: 0.009999999776482582
      Pitch: 0.5
      Target Frame: <Fixed Frame>
      Value: Orbit (rviz)
      Yaw: 0.5
    Saved: ~
Window Geometry:
  Displays:
    collapsed: false
  Height: 1024
  Hide Left Dock: false
  Hide Right Dock: false
  Image:
    collapsed: false
  QMainWindow State: 000000ff00000000fd000000040000000000000156000003a2fc0200000008fb0000001200530065006c0065006300740069006f006e00000001e10000009b0000005c00fffffffb0000001e0054006f006f006c002000500072006f007000650072007400690065007302000001ed000001df00000185000000a3fb000000120056006900650077007300200054006f006f02000001df000002110000018500000122fb000000200054006f006f006c002000500072006f0070006500720074006900650073003203000002880000011d000002210000017afb000000100044006900730070006c006100790073010000003d0000029b000000c900fffffffb0000002000730065006c0065006300740069006f006e00200062007500660066006500720200000138000000aa0000023a00000294fb00000014005700690064006500530074006500720065006f02000000e6000000d2000003ee0000030bfb0000000c004b0069006e0065006300740200000186000001060000030c00000261000000010000010f000003a2fc0200000003fb0000001e0054006f006f006c002000500072006f00700065007200740069006500730100000041000000780000000000000000fb0000000a00560069006500770073010000003d000003a2000000a400fffffffb0000001200530065006c0065006300740069006f006e010000025a000000b200000000000000000000000200000490000000a9fc0100000001fb0000000a00560069006500770073030000004e00000080000002e10000019700000003000004420000003efc0100000002fb0000000800540069006d00650100000000000004420000000000000000fb0000000800540069006d00650100000000000004500000000000000000000003a3000003a200000004000000040000000800000008fc0000000100000002000000010000000a0054006f006f006c00730100000000ffffffff0000000000000000
  Width: 1200
  X: 60
  Y: 60
```

## Running the Project

1. Build the ROS 2 package:
```bash
cd isaac_humanoid_brain
colcon build
source install/setup.bash
```

2. Launch the complete AI brain system:
```bash
ros2 launch isaac_humanoid_brain ai_brain.launch.py
```

3. Send navigation goals:
```bash
# In another terminal
ros2 run turtlesim turtle_teleop_key
# Or use RViz to set 2D Nav Goal
```

## Extending the Project

Consider these enhancements:
- Add Isaac ROS perception packages for more advanced computer vision
- Implement learning-based navigation policies
- Add speech recognition and natural language processing
- Integrate with Isaac Sim for photorealistic training
- Add manipulation capabilities for the humanoid robot
- Implement multi-robot coordination

## Key Learning Outcomes

This project demonstrates:
- Complete AI brain architecture for humanoid robots
- Integration of Isaac Sim, Isaac ROS, and Nav2
- GPU-accelerated perception and navigation
- Real-time decision making and behavior management
- ROS 2 best practices for complex robotic systems

The complete humanoid AI brain provides a foundation for advanced humanoid robot capabilities combining perception, navigation, and intelligent behavior in a unified system.