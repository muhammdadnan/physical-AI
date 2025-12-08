# Nodes, Topics, and Services

Understanding the fundamental communication patterns in ROS 2 is crucial for building robust humanoid robot applications. This section covers the three primary communication mechanisms: nodes, topics, and services.

## Nodes

Nodes are the fundamental building blocks of a ROS 2 system. Each node is a process that performs a specific task and communicates with other nodes through topics, services, and actions.

### Creating a Node

In ROS 2, nodes are created using client libraries such as `rclpy` (Python) or `rclcpp` (C++). A node typically contains:

- Publishers and subscribers for topic-based communication
- Service clients and servers for request/response communication
- Action clients and servers for goal-oriented communication
- Parameters for configuration
- Timers for periodic tasks

### Node Lifecycle

ROS 2 nodes follow a well-defined lifecycle with states including:
- Unconfigured
- Inactive
- Active
- Finalized

This lifecycle management allows for better resource management and system reliability.

## Topics and Message Passing

Topics enable asynchronous, many-to-many communication between nodes through a publish-subscribe pattern.

### Characteristics of Topics:
- **Decoupled**: Publishers and subscribers don't need to know about each other
- **Asynchronous**: Publishers send messages without waiting for responses
- **Broadcast**: One publisher can send to multiple subscribers
- **Typed**: All messages have defined types

### Common Message Types for Humanoid Robots:
- `sensor_msgs/JointState` - Joint positions, velocities, and efforts
- `geometry_msgs/Twist` - Velocity commands
- `sensor_msgs/Image` - Camera images
- `nav_msgs/Odometry` - Robot pose and velocity information

## Services

Services provide synchronous, request-response communication between nodes.

### Characteristics of Services:
- **Synchronous**: Client waits for server response
- **One-to-one**: One client communicates with one server
- **Request/Response**: Defined request and response message types
- **Blocking**: Client blocks until response is received

### Common Service Types for Humanoid Robots:
- `std_srvs/Trigger` - Simple on/off commands
- `nav_msgs/GetMap` - Retrieve map data
- Custom services for robot-specific operations

## Practical Example: Humanoid Robot Control

Let's examine a typical communication pattern for humanoid robot control:

```
[Joint State Publisher] -> (joint_states topic) -> [Robot State Publisher]
[IMU Sensor Node] -> (imu_data topic) -> [Balance Controller]
[Path Planner] -> (cmd_vel topic) -> [Walking Controller]
[UI Interface] -> [Set Walking Goal Service] -> [Navigation Server]
```

This architecture demonstrates how different components communicate to achieve coordinated humanoid robot behavior.

## Best Practices

1. **Use appropriate QoS settings** for your application requirements
2. **Keep messages small** to reduce network overhead
3. **Use services for infrequent operations** and topics for continuous data
4. **Implement proper error handling** for communication failures
5. **Design for fault tolerance** in distributed systems