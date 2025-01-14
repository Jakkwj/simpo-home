const sidebars = {

  docs: [
    'Introduction',

    {
      type: 'category',
      label: 'SIMPO Dash',
      collapsible: true,
      collapsed: false, // 默认展开, 后续多了在折叠
      items: [
        'SIMPO Dash/2025',

        {
          type: 'category',
          label: 'Earlier',
          collapsible: true,
          collapsed: true, // 默认折叠
          items: [
            'SIMPO Dash/Earlier/2024',
            'SIMPO Dash/Earlier/2023',
            'SIMPO Dash/Earlier/2022',
            'SIMPO Dash/Earlier/2021',
          ],
        },

        // 'SIMPO Dash/Earlier/2023',
        // 'SIMPO Dash/Earlier/2022',
        // 'SIMPO Dash/Earlier/2021',
      ],


    },

    {
      type: 'category',
      label: 'SIMPO Backend',
      collapsible: true,
      collapsed: false, // 默认展开, 后续多了在折叠
      items: [
        'SIMPO Backend/2025',

        {
          type: 'category',
          label: 'Earlier',
          collapsible: true,
          collapsed: true, // 默认折叠
          items: [
            'SIMPO Backend/Earlier/2024',
          ],
        },

        // 'SIMPO/2023',
        // 'SIMPO/2022',
        // 'SIMPO/2021',
      ],

    },

    {
      type: 'category',
      label: 'SIMPO',
      collapsible: true,
      collapsed: false, // 默认展开, 后续多了在折叠
      items: [
        'SIMPO/2025',

        {
          type: 'category',
          label: 'Earlier',
          collapsible: true,
          collapsed: true, // 默认折叠
          items: [
            'SIMPO/Earlier/2024',
            'SIMPO/Earlier/2023',
            'SIMPO/Earlier/2022',
            'SIMPO/Earlier/2021',
          ],
        },

        // 'SIMPO/2023',
        // 'SIMPO/2022',
        // 'SIMPO/2021',
      ],

    },

    {
      type: 'category',
      label: 'SIMPO Pro',
      collapsible: true,
      collapsed: false, // 默认展开, 后续多了在折叠
      items: [
        'SIMPO Pro/2025',

        {
          type: 'category',
          label: 'Earlier',
          collapsible: true,
          collapsed: true, // 默认折叠
          items: [
            'SIMPO Pro/Earlier/2024',
            'SIMPO Pro/Earlier/2023',
            'SIMPO Pro/Earlier/2022',
          ],
        },

        // 'SIMPO Pro/2023',
        // 'SIMPO Pro/2022',
      ],


    },

    {
      type: 'category',
      label: 'SIMPO Client',
      collapsible: true,
      collapsed: false, // 默认展开, 后续多了在折叠
      // "link": {
      //   "type": "generated-index",
      //   "description": "Changelog of the core source code of SIMPO."
      //   // type: 'doc',
      //   // id: 'Changelog/index',
      //  },

      items: [
        'SIMPO Client/2025',
        {
          type: 'category',
          label: 'Earlier',
          collapsible: true,
          collapsed: true, // 默认折叠
          items: [
            'SIMPO Client/Earlier/2024',
            'SIMPO Client/Earlier/2023',
          ],
        },

        // {
        //   type: 'category',
        //   label: 'SIMPO Client',
        //   items: [
        //     'SIMPO Client/2023',
        //   ]
        // },



      ],
    },


  ],

};

module.exports = sidebars;
