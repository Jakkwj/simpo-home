// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx,md,mdx}",
    "./docs/**/*.{md,mdx}",
    // 根据你的项目结构添加其他路径
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  // 重要: 插件 docusaurus-tailwindcss 会处理 preflight 以避免与 Infima 冲突
  // 通常不需要手动设置 corePlugins: { preflight: false }，除非插件行为有变
  // 确保 Tailwind 的暗黑模式与 Docusaurus 兼容
  darkMode: ['class', '[data-theme="dark"]'],

  // 为所有 Tailwind 类添加前缀（可选）
  prefix: 'tw-',
};
