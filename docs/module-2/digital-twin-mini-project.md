# Digital Twin Mini Project: Humanoid Robot Simulation Environment

In this mini-project, you'll create a comprehensive digital twin environment for a humanoid robot using Gazebo and Unity, integrating multiple sensors and physics simulation.

## Project Overview

Create a complete digital twin environment that includes:
- Physics simulation with realistic humanoid robot model
- Multiple sensor systems (cameras, LIDAR, IMU)
- ROS 2 integration for control and data flow
- Unity rendering for high-fidelity visualization
- Synthetic data generation capabilities

## Prerequisites

Before starting this project, ensure you have:
- ROS 2 installed and configured
- Gazebo Classic or Garden installed
- Unity Hub and Editor (optional for high-fidelity rendering)
- Basic understanding of URDF and sensor integration

## Project Structure

```
digital_twin_project/
├── robot_description/
│   ├── urdf/
│   │   └── humanoid_robot.urdf
│   └── meshes/
├── gazebo_worlds/
│   └── humanoid_lab.world
├── launch/
│   └── digital_twin.launch.py
├── config/
│   ├── sensors.yaml
│   └── controllers.yaml
└── scripts/
    ├── sensor_data_processor.py
    └── unity_bridge.py
```

## Step 1: Create the Robot URDF with Sensors

Create a comprehensive URDF model with integrated sensors:

```xml
<!-- robot_description/urdf/humanoid_robot.urdf -->
<?xml version="1.0"?>
<robot name="humanoid_robot"
       xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Base link -->
  <link name="base_link">
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
    </collision>
  </link>

  <!-- Head with RGB-D camera -->
  <joint name="head_joint" type="fixed">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
  </joint>

  <link name="head">
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
    <visual>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
    </collision>
  </link>

  <!-- RGB-D Camera -->
  <joint name="camera_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 0" rpy="0 0 0"/>
  </joint>

  <link name="camera_link">
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Gazebo plugin for RGB-D camera -->
  <gazebo reference="camera_link">
    <sensor type="depth" name="camera">
      <always_on>true</always_on>
      <update_rate>30.0</update_rate>
      <camera name="head">
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>10.0</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
        <baseline>0.2</baseline>
        <alwaysOn>true</alwaysOn>
        <updateRate>30.0</updateRate>
        <cameraName>camera</cameraName>
        <imageTopicName>rgb/image_raw</imageTopicName>
        <depthImageTopicName>depth/image_raw</depthImageTopicName>
        <pointCloudTopicName>depth/points</pointCloudTopicName>
        <cameraInfoTopicName>rgb/camera_info</cameraInfoTopicName>
        <depthImageCameraInfoTopicName>depth/camera_info</depthImageCameraInfoTopicName>
        <frameName>camera_link</frameName>
        <pointCloudCutoff>0.1</pointCloudCutoff>
        <pointCloudCutoffMax>3.0</pointCloudCutoffMax>
        <distortion_k1>0.0</distortion_k1>
        <distortion_k2>0.0</distortion_k2>
        <distortion_k3>0.0</distortion_k3>
        <distortion_t1>0.0</distortion_t1>
        <distortion_t2>0.0</distortion_t2>
        <CxPrime>0.0</CxPrime>
        <Cx>320.5</Cx>
        <Cy>240.5</Cy>
        <focalLength>320.0</focalLength>
      </plugin>
    </sensor>
  </gazebo>

  <!-- IMU Sensor -->
  <joint name="imu_joint" type="fixed">
    <parent link="base_link"/>
    <child link="imu_link"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>

  <link name="imu_link"/>

  <gazebo reference="imu_link">
    <sensor type="imu" name="imu_sensor">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <imu>
        <angular_velocity>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </z>
        </angular_velocity>
        <linear_acceleration>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </z>
        </linear_acceleration>
      </imu>
      <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
        <frame_name>imu_link</frame_name>
        <topic>imu/data</topic>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

## Step 2: Create a Gazebo World

Create a world file with obstacles and environment features:

```xml
<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="humanoid_lab">
    <!-- Physics engine -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000.0</real_time_update_rate>
    </physics>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Lighting -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Lab environment with obstacles -->
    <model name="table">
      <pose>2 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 0.8 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 0.8 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.8 0.8 0.8 1</specular>
          </material>
        </visual>
        <inertial>
          <mass>10</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertial>
        </inertial>
      </link>
    </model>

    <!-- Boxes for navigation testing -->
    <model name="box1">
      <pose>3 1 0.2 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.4 0.4 0.4</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.4 0.4 0.4</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.5 1 1</ambient>
            <diffuse>0.5 0.5 1 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1</mass>
          <inertia>
            <ixx>0.01</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>0.01</iyy>
            <iyz>0</iyz>
            <izz>0.01</izz>
          </inertial>
        </inertial>
      </link>
    </model>

    <!-- Add more objects as needed -->
  </world>
</sdf>
```

## Step 3: Create Launch File

Create a launch file to start the complete simulation:

```python
# launch/digital_twin.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world = LaunchConfiguration('world', default='humanoid_lab.world')

    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_world = DeclareLaunchArgument(
        'world',
        default_value='humanoid_lab.world',
        description='Choose one of the world files from `/digital_twin_project/gazebo_worlds`'
    )

    # Start Gazebo server
    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([
                FindPackageShare('digital_twin_project'),
                'gazebo_worlds',
                world
            ])
        }.items()
    )

    # Start Gazebo client
    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )

    # Spawn the robot
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'humanoid_robot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5'
        ],
        output='screen'
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': PathJoinSubstitution([
                FindPackageShare('digital_twin_project'),
                'robot_description',
                'urdf',
                'humanoid_robot.urdf'
            ])
        }],
        output='screen'
    )

    # Joint state publisher (for simulation)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # RViz2 for visualization
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', PathJoinSubstitution([
            FindPackageShare('digital_twin_project'),
            'rviz',
            'digital_twin.rviz'
        ])],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_world,
        start_gazebo_server,
        start_gazebo_client,
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
        # rviz  # Uncomment if you want RViz
    ])
```

## Step 4: Sensor Data Processing Node

Create a node to process and analyze sensor data:

```python
#!/usr/bin/env python3
# scripts/sensor_data_processor.py

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, Imu, PointCloud2
from cv_bridge import CvBridge
import cv2
import numpy as np

class SensorDataProcessor(Node):
    def __init__(self):
        super().__init__('sensor_data_processor')

        # Create CvBridge for image processing
        self.bridge = CvBridge()

        # Subscribe to sensor topics
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/rgb/image_raw',
            self.image_callback,
            10
        )

        self.imu_subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        self.pointcloud_subscription = self.create_subscription(
            PointCloud2,
            '/camera/depth/points',
            self.pointcloud_callback,
            10
        )

        # Publishers for processed data
        self.processed_image_pub = self.create_publisher(
            Image,
            '/processed/rgb/image_filtered',
            10
        )

        # Data storage
        self.latest_image = None
        self.latest_imu = None

        # Processing parameters
        self.image_counter = 0
        self.processing_rate = 10  # Hz
        self.timer = self.create_timer(1.0/self.processing_rate, self.process_callback)

    def image_callback(self, msg):
        self.latest_image = msg
        self.get_logger().info(f'Received image: {msg.width}x{msg.height}')

    def imu_callback(self, msg):
        self.latest_imu = msg
        # Extract orientation and angular velocity
        orientation = msg.orientation
        angular_velocity = msg.angular_velocity
        linear_acceleration = msg.linear_acceleration

        # Log IMU data
        self.get_logger().info(
            f'IMU - Orientation: ({orientation.x:.2f}, {orientation.y:.2f}, {orientation.z:.2f}, {orientation.w:.2f})'
        )

    def pointcloud_callback(self, msg):
        self.get_logger().info(f'Received point cloud with {msg.height * msg.width} points')

    def process_callback(self):
        if self.latest_image is not None:
            # Convert ROS image to OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(self.latest_image, 'bgr8')

            # Apply some basic image processing
            # Example: Convert to grayscale and apply Gaussian blur
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Convert back to ROS image
            processed_msg = self.bridge.cv2_to_imgmsg(blurred, 'mono8')
            processed_msg.header = self.latest_image.header

            # Publish processed image
            self.processed_image_pub.publish(processed_msg)

            # Save image for synthetic data generation
            cv2.imwrite(f'/tmp/processed_image_{self.image_counter:05d}.png', blurred)
            self.image_counter += 1

def main(args=None):
    rclpy.init(args=args)
    processor = SensorDataProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 5: Unity Integration Script (Optional)

If using Unity for high-fidelity rendering, create a ROS bridge script:

```csharp
// scripts/UnityBridge.cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using RosMessageTypes.Geometry;

public class UnityBridge : MonoBehaviour
{
    ROSConnection ros;

    // Topics
    string cameraTopic = "/camera/rgb/image_raw";
    string imuTopic = "/imu/data";
    string jointStatesTopic = "/joint_states";

    // Robot components
    public GameObject robotModel;
    public List<GameObject> jointObjects = new List<GameObject>();

    // Start is called before the first frame update
    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.RegisterPublisher<JointStateMsg>(jointStatesTopic);

        // Subscribe to sensor data
        ros.Subscribe<ImageMsg>(cameraTopic, CameraCallback);
        ros.Subscribe<ImuMsg>(imuTopic, ImuCallback);
    }

    void CameraCallback(ImageMsg imageMsg)
    {
        // Process camera image data
        Debug.Log($"Received camera image: {imageMsg.width}x{imageMsg.height}");
    }

    void ImuCallback(ImuMsg imuMsg)
    {
        // Process IMU data
        Debug.Log($"Received IMU data: {imuMsg.orientation.x}, {imuMsg.orientation.y}, {imuMsg.orientation.z}");
    }

    void Update()
    {
        // Publish joint states periodically
        if (Time.frameCount % 60 == 0) // Every 60 frames
        {
            PublishJointStates();
        }
    }

    void PublishJointStates()
    {
        JointStateMsg jointState = new JointStateMsg();
        jointState.header = new std_msgs.HeaderMsg();
        jointState.header.stamp = new builtin_interfaces.TimeMsg(ROSConnection.GetNodeTime());
        jointState.header.frame_id = "base_link";

        // Set joint names and positions (example)
        jointState.name = new string[] { "head_joint", "camera_joint" };
        jointState.position = new double[] { 0.0, 0.0 };
        jointState.velocity = new double[] { 0.0, 0.0 };
        jointState.effort = new double[] { 0.0, 0.0 };

        ros.Publish(jointStatesTopic, jointState);
    }
}
```

## Running the Project

1. Build the ROS 2 package:
```bash
cd digital_twin_project
colcon build
source install/setup.bash
```

2. Launch the complete simulation:
```bash
ros2 launch digital_twin_project digital_twin.launch.py
```

3. In another terminal, run the sensor processor:
```bash
ros2 run digital_twin_project sensor_data_processor
```

4. Visualize the data:
```bash
# Check available topics
ros2 topic list

# View camera data
ros2 run image_view image_view _image:=/camera/rgb/image_raw

# View IMU data
ros2 topic echo /imu/data
```

## Extending the Project

Consider these enhancements:
- Add more complex environments with dynamic objects
- Implement synthetic data generation pipelines
- Add Unity visualization for high-fidelity rendering
- Create perception algorithms that process the sensor data
- Add machine learning components for sensor fusion
- Implement navigation and path planning in the simulation

## Key Learning Outcomes

This project demonstrates:
- Complete digital twin setup with physics simulation
- Multi-sensor integration in a humanoid robot model
- ROS 2 communication between simulation and processing nodes
- Data processing and analysis for sensor streams
- Realistic environment modeling for robot testing

The digital twin environment provides a safe, repeatable, and controllable platform for humanoid robot development and testing.