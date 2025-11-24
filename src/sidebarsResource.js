import { readdirSync, statSync } from 'fs';
import { resolve, join } from 'path';
const docsFolder = 'resource';  // 要扫描的文件夹路径 (相对于 Docusaurus 项目根目录)

function generateSidebarItems(folderPath) {
  /**
   * 更加文件夹自动生成 sidebar 项目列表
   *
   * 注意: 文件(不是文件夹)的命名不能带 ()/, 因为文件命名决定了 url 的内容
   * 可以在 mdx 文件内的最上级 title 使用这些特殊字符
   * 所以 url 通过 .mdx 文件内的 slug 字段自定义, 覆盖文件名决定的 url
   * slug 第一个字符为 / 则会跳过子文件夹, 不加则保留
   * () 统一被替换为 _
   *
   */
  const items = [];
  const files = readdirSync(resolve(__dirname, folderPath));

  files.forEach(file => {
    const filePath = join(folderPath, file);
    const stat = statSync(resolve(__dirname, filePath));

    if (stat.isFile() && (file.endsWith('.md') || file.endsWith('.mdx'))) {
      const id = filePath.replace(/\.mdx?$/, '').replace(`${docsFolder}/`, '');  // 假设文件名就是文档 ID (去掉 .md 或 .mdx 后缀)
      // console.log('Generated sidebar item ID:', id);
      items.push(id);
    } else if (stat.isDirectory()) {
      // 递归处理子文件夹
      items.push({
        type: 'category',
        label: file, // 使用文件夹名作为类别标签
        collapsible: true,
        collapsed: false,  // 默认展开
        "link": {
          "type": "generated-index",
          "description": "Catalog."
        },
        items: generateSidebarItems(filePath),
      });
    }
  });

  return items;
}

// console.log(generateSidebarItems(docsFolder).reverse())

// const docsArray= generateSidebarItems(docsFolder)
// for (const item of docsArray) {
//   console.log(item['items']);
// }

// @ts-check
/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
export const docs = generateSidebarItems(docsFolder).reverse();
