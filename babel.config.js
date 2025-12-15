module.exports = {
  presets: [require.resolve('@docusaurus/core/lib/babel/preset')],
  sourceType: 'module', // Changed to module to handle ES modules properly
  plugins: [
    // Add plugin to handle ES modules in generated files
    ['@babel/plugin-transform-modules-commonjs', {
      allowTopLevelThis: true,
    }],
  ],
};