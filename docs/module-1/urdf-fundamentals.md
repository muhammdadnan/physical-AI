# URDF Fundamentals

Unified Robot Description Format (URDF) is an XML format for representing a robot model. It's essential for humanoid robotics as it defines the physical and visual properties of robots, enabling simulation, visualization, and control.

## What is URDF?

URDF (Unified Robot Description Format) is an XML-based format that describes robot models including:

- **Kinematic structure**: Joint connections and transformations
- **Visual representation**: How the robot appears in simulation
- **Collision properties**: Shapes for collision detection
- **Inertial properties**: Mass, center of mass, and inertia tensors
- **Physical properties**: Friction, damping, and other physical characteristics

## URDF Structure

A typical URDF file consists of:

### Links
Links represent rigid bodies of the robot. Each link has:
- Visual elements (how it looks)
- Collision elements (for collision detection)
- Inertial properties (mass, center of mass, inertia)

### Joints
Joints connect links together and define their motion relationship:
- **Fixed joints**: No movement between links
- **Revolute joints**: Single-axis rotation (like hinges)
- **Continuous joints**: Unlimited rotation around axis
- **Prismatic joints**: Single-axis translation
- **Floating joints**: 6-DOF motion

### Materials
Define colors and visual appearance properties for visualization.

## URDF for Humanoid Robots

Humanoid robots have complex kinematic structures requiring careful URDF design:

### Common Humanoid Joints:
- **Hip joints**: 3-DOF for leg movement
- **Knee joints**: 1-DOF for flexion/extension
- **Ankle joints**: 2-DOF for foot orientation
- **Shoulder joints**: 3-DOF for arm positioning
- **Elbow joints**: 1-DOF for arm flexion
- **Wrist joints**: 2-DOF for hand orientation

### Kinematic Chains:
- Left and right leg chains
- Left and right arm chains
- Torso and head chain
- Possible tail or additional DOFs

## Example URDF Structure

```xml
<robot name="humanoid_robot">
  <!-- Base/Pelvis link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Hip joint connecting leg -->
  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_thigh"/>
    <origin xyz="0 -0.1 -0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Thigh link -->
  <link name="left_thigh">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>
</robot>
```

## URDF Best Practices for Humanoid Robots

1. **Start Simple**: Begin with basic shapes and add complexity gradually
2. **Validate Kinematics**: Ensure the kinematic chain matches the physical robot
3. **Accurate Inertial Properties**: Use proper mass and inertia values for simulation
4. **Consistent Naming**: Use clear, consistent joint and link names
5. **Proper Joint Limits**: Set realistic joint limits based on physical constraints
6. **Collision vs Visual**: Separate collision and visual geometries appropriately

## Tools for URDF

- **RViz**: Visualize URDF models in ROS
- **Gazebo**: Simulate robots with URDF descriptions
- **xacro**: Macro language for URDF to reduce redundancy
- **URDF parsers**: Various libraries for processing URDF in different languages

## Integration with ROS 2

URDF integrates with ROS 2 through:
- **robot_state_publisher**: Publishes joint states to tf2 transforms
- **joint_state_publisher**: Publishes joint state messages
- **Gazebo ROS packages**: For simulation integration
- **MoveIt!**: For motion planning with URDF models

URDF is the foundation for all humanoid robot simulation and visualization in ROS 2 ecosystems.