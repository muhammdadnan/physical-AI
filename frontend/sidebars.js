// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1 - ROS 2',
      items: [
        'module-1/ros2-intro',
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - Digital Twin',
      items: [
        'module-2/gazebo-physics',  // Placeholder - create this file if needed
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-3/isaac-sim-intro',  // Placeholder - create this file if needed
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
        'module-4/whisper-examples',
        'module-4/planning-examples',
        'module-4/vision-examples',
        'module-4/action-examples',
        'module-4/task-runner-example',
        'module-4/task-runner-code',
        'module-4/capstone-workflow',
        'module-4/quickstart',
      ],
    },
  ],
};

export default sidebars;