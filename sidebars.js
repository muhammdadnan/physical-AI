// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1 - ROS 2',
      items: [
        'module-1/ros2-intro',
        'module-1/nodes-topics-services',
        'module-1/urdf-fundamentals',
        'module-1/rclpy-basics',
        'module-1/ros2-mini-project',
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - Digital Twin',
      items: [
        'module-2/gazebo-physics',
        'module-2/unity-rendering',
        'module-2/sensors',
        'module-2/digital-twin-mini-project',
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-3/isaac-sim-intro',
        'module-3/synthetic-data',
        'module-3/vslam',
        'module-3/nav2-humanoid',
        'module-3/isaac-mini-project',
      ],
    },
    {
      type: 'category',
      label: 'Module 4 - Vision-Language-Action (VLA)',
      items: [
        'module-4/introduction',
        'module-4/whisper-setup',
        'module-4/llm-planning',
        'module-4/ros2-execution',
        'module-4/vision-perception',
        'module-4/mini-project',
        'module-4/capstone-project',
      ],
    },
  ],
};

export default sidebars;