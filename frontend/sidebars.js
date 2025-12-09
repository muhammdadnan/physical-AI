// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1 - ROS 2',
      items: [
        'module-1/ros2-intro',
        'module-1/ros2-nodes-services',
        'module-1/ros2-topics-actions',
        'module-1/ros2-projects',
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - Digital Twin',
      items: [
        'module-2/gazebo-physics',
        'module-2/unity-rendering',
        'module-2/sensor-integration',
        'module-2/digital-twin-projects',
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-3/isaac-sim-intro',
        'module-3/isaac-perception',
        'module-3/isaac-navigation',
        'module-3/isaac-projects',
      ],
    },
    {
      type: 'category',
      label: 'Module 4 - Vision-Language-Action (VLA)',
      items: [
        'module-4/vla-fundamentals',
        'module-4/llm-integration',
        'module-4/execution-systems',
        'module-4/vla-projects',
      ],
    },
  ],
};

export default sidebars;