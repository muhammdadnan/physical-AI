# rclpy Basics

rclpy is the Python client library for ROS 2, providing Python bindings for the ROS 2 ecosystem. This module covers the fundamentals of using rclpy for humanoid robot development.

## What is rclpy?

rclpy is the official Python client library for ROS 2, built on top of the ROS Client Library (rcl) and the Common Client Library Interface (rclcpp). It provides:

- **Node creation and management**
- **Publisher and subscriber functionality**
- **Service client and server implementation**
- **Action client and server support**
- **Parameter handling**
- **Timer and callback management**
- **TF2 transformation utilities**

## Setting Up rclpy

### Installation
rclpy is typically installed as part of the ROS 2 Python development packages:
```bash
pip install rclpy
# Or as part of ROS 2 distribution
```

### Basic Node Structure
```python
import rclpy
from rclpy.node import Node

class HumanoidController(Node):
    def __init__(self):
        super().__init__('humanoid_controller')
        # Node initialization code here

def main(args=None):
    rclpy.init(args=args)
    node = HumanoidController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating Publishers and Subscribers

### Publishers
Publishers send messages to topics:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState

class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__('joint_command_publisher')
        self.publisher = self.create_publisher(JointState, 'joint_commands', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = JointState()
        msg.name = ['joint1', 'joint2', 'joint3']
        msg.position = [1.0, 2.0, 3.0]
        self.publisher.publish(msg)
        self.get_logger().info('Publishing joint states: "%s"' % msg.position)
```

### Subscribers
Subscribers receive messages from topics:

```python
class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Received joint states: "%s"' % msg.position)
```

## Services in rclpy

Services provide request-response communication:

### Service Server
```python
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response
```

### Service Client
```python
class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
```

## Actions in rclpy

Actions are for long-running tasks with feedback:

### Action Server
```python
from rclpy.action import ActionServer
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import threading

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup())
```

## Parameters

Parameters allow runtime configuration:

```python
class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'humanoid_robot')
        self.declare_parameter('max_velocity', 1.0)

        # Get parameter values
        robot_name = self.get_parameter('robot_name').value
        max_velocity = self.get_parameter('max_velocity').value
```

## Timers and Callbacks

Timers allow periodic execution:

```python
class TimerNode(Node):
    def __init__(self):
        super().__init__('timer_node')
        self.timer = self.create_timer(0.5, self.timer_callback)  # 0.5 second period
        self.counter = 0

    def timer_callback(self):
        self.get_logger().info(f'Timer callback executed {self.counter} times')
        self.counter += 1
```

## TF2 with rclpy

Transformations for coordinate systems:

```python
import tf2_ros
from geometry_msgs.msg import TransformStamped

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_transform)

    def broadcast_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser_frame'
        # Set transform values...
        self.tf_broadcaster.sendTransform(t)
```

## Best Practices for Humanoid Robotics

1. **Use appropriate QoS profiles** for real-time requirements
2. **Handle exceptions** in callbacks to prevent node crashes
3. **Use threading** appropriately for blocking operations
4. **Implement proper shutdown** procedures
5. **Use logging** for debugging and monitoring
6. **Design for real-time performance** where needed

rclpy provides the essential Python interface for developing humanoid robot applications in ROS 2.