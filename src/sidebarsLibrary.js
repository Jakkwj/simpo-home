/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  // tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually
  docs: [
    'Introduction',
    // 'QucikStart',
    // 'Tutorials',

    {
      type: 'category',
      label: '2016',
      collapsible: true,
      collapsed: false, // 默认展开, 后续多了在折叠
      items: [

        '2016/WaterResearch',

      ],
    },

    {
      type: 'category',
      label: '2005',
      collapsible: true,
      collapsed: false, // 默认展开

      items: [

        '2005/WaterResearch',

      ],
    },

    {
      type: 'category',
      label: '2001',
      collapsible: true,
      collapsed: false, // 默认展开

      items: [

        '2001/WaterResearch',

      ],
    },



    // {
    //   type: 'category',
    //   label: 'Papers',
    //   // "link": {
    //   //   "type": "generated-index",
    //   //   "description": "Use AGI (such as: Kimi) to understand papers."
    //   //   // type: 'doc',
    //   //   // id: 'Changelog/index',
    //   // },
    //   items: [

    //     '2016/WaterResearch',
    //     '2005/WaterResearch',
    //     '2001/WaterResearch',

    //     // {
    //     //   type: 'category',
    //     //   label: '2017',
    //     //   items: [
    //     //     'Papers/2017/aa',

    //     //   ]
    //     // },
    //     // {
    //     //   type: 'category',
    //     //   label: '2016',
    //     //   items: [
    //     //     'Papers/2016/WaterResearch',

    //     //   ]
    //     // },

    //     // {
    //     //   type: 'category',
    //     //   label: '2005',
    //     //   items: [
    //     //     'Papers/2005/WaterResearch',

    //     //   ]
    //     // },

    //     // {
    //     //   type: 'category',
    //     //   label: '2001',
    //     //   items: [
    //     //     'Papers/2001/WaterResearch',

    //     //   ]
    //     // },







    //   ],
    // },

  ],

};

module.exports = sidebars;