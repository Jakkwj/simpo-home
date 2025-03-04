// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

// const lightCodeTheme = require('prism-react-renderer/themes/github');
// const darkCodeTheme = require('prism-react-renderer/themes/dracula');
const {themes} = require('prism-react-renderer');
const lightTheme = themes.github;
const darkTheme = themes.dracula;

const title = 'SIMPO'
// const urlConsole = 'https://dashboard.simpowater.org/dashboard/home'

const urlHome = 'https://www.simpowater.org'
const urlConsole = 'https://dash.simpowater.org/dashboard/home'
const urlLogo = 'https://i.postimg.cc/rsPqvJNJ/logo3.png'

/**
 * 登录后台显示 Dashboard, 未登录时显示 Sign In 的功能实现参看: https://github.com/facebook/docusaurus/discussions/5307
 * 1.手动 swizzle Root 组件
 * 2.在其中添加 addEventListener 监听 iframe 加载的后台是否有 accessToken, 有则登录了
 * 3.swizzle NavbarNavLink: yarn swizzle @docusaurus/theme-classic NavbarNavLink --wrap
 * 4.在后台设一个专门的 ifsign 页面, postMessage 传递 accessToken
 * 5.据此判断是否登录
 * 6.注意 nginx 需要打开 X-Frame-Options
 *
 */

const fs = require('fs');
// const resourcesHTML = fs.readFileSync('./src/snippets/resources.html', 'utf-8');

/** @type {import('@docusaurus/types').Config} */



const config = {

  customFields: {
    // global variable
    imgUrlBanner: 'https://i.postimg.cc/3w15s1Kv/banner3.png',
    // imgUrlPowerful: 'https://i.postimg.cc/8CRPjLTp/Powerful.png',
    // imgUrlPowerful: 'https://i.postimg.cc/XY3TRNyp/Powerful2.png',
    imgUrlPowerful: 'https://i.postimg.cc/XqTqxG2H/Powerful2b.png',
    // imgUrlOpen: 'https://i.postimg.cc/dthsGbJS/Fig6.png',
    imgUrlOpen: 'https://i.postimg.cc/NfHhGfvg/Fig5-LHS-Density.png',
    imgUrlTrackable: 'https://i.postimg.cc/85TkWsCh/matrix2.png',
    // imgUrlResource: 'https://i.postimg.cc/FHPRnBnk/resource.png',
    imgUrlResource: 'https://i.postimg.cc/HL2FXpF6/resource.png',

    imgUrlIntroduction_1: 'https://i.postimg.cc/kgNkSsRp/Fig5-Sim-Targets.png',
    imgUrlIntroduction_2: 'https://i.postimg.cc/8zg2s9cv/Project-Eva-Uncertainty-PCDF-59.png',

    imgUrlJiangfeng: 'https://i.postimg.cc/CKmXPKNC/jiangfeng.jpg',
    imgUrlWangjun: 'https://i.postimg.cc/sXx8tR6k/Jakk2b.jpg',
    imgUrlLihao: 'https://i.postimg.cc/YSpTzF1q/lihao.jpg',

    imgUrlTheEasiestWay: 'https://i.postimg.cc/bvV8GgKj/The-Easiest-Way.gif',

    imgUrlASM3_1: 'https://i.postimg.cc/mkJGdrTp/ASM3-1.gif',
    imgUrlASM3_2: "https://i.postimg.cc/DfMFfx1Q/ASM3-2.gif",
    imgUrlASM3_3: 'https://i.postimg.cc/SRJh79bz/ASM3-3.gif',
    imgUrlASM3_4: 'https://i.postimg.cc/xCsQzRh2/ASM3-4.gif',

    imgUrlBioModel_1: 'https://i.postimg.cc/ZRq8Hb7d/biomodel-1.gif',
    imgUrlBioModel_2: 'https://i.postimg.cc/25GdnbwY/biomodel-2.gif',
    imgUrlBioModel_3: 'https://i.postimg.cc/pLDJX15p/biomodel-3.gif',
    imgUrlBioModel_4: 'https://i.postimg.cc/TPfqyqnQ/biomodel-4.gif',

    imgUrlDataSet_1: 'https://i.postimg.cc/KY2QPyhP/dataset-1.gif',
    imgUrlDataSet_2: 'https://i.postimg.cc/4xtBHxq4/dataset-2.gif',
    imgUrlDataSet_3: 'https://i.postimg.cc/fT18b9Hg/dataset-3.gif',
    imgUrlDataSet_4: 'https://i.postimg.cc/WpW9QK0V/dataset-4.gif',
    imgUrlDataSet_5: 'https://i.postimg.cc/7Y5BDVN2/dataset-5.gif',

    imgUrlProject_1: 'https://i.postimg.cc/RVYDn80d/project-1.gif',
    imgUrlProject_2: 'https://i.postimg.cc/SxztLr2h/project-2.gif',
    imgUrlProject_3: 'https://i.postimg.cc/MKHLHxzX/project-3.gif',
    imgUrlProject_4: 'https://i.postimg.cc/FK5CTL3J/project-4.gif',


    imgUrlCaseStudyAQUASIMT2P17_1: 'https://i.postimg.cc/8k48stWX/T2P17-1.jpg',
    imgUrlCaseStudyAQUASIMT2P17_2: 'https://i.postimg.cc/BQnrFHBS/T2P17-2.jpg',
    imgUrlCaseStudyAQUASIMT2P17_3: 'https://i.postimg.cc/QxYRJCfp/T2P17-3.jpg',
    imgUrlCaseStudyAQUASIMT2P17_4: 'https://i.postimg.cc/3xPVz65N/T2P17-4.jpg',
    imgUrlCaseStudyAQUASIMT2P17_5: 'https://i.postimg.cc/RZ32smY2/T2P17-5.jpg',

    imgUrlCaseStudyBWTEE2_3_4Batch: 'https://i.postimg.cc/YSYZ73M3/2-3-4-Batch-1.jpg',

    imgUrlCaseStudyBWTEE2_3_4Chemostat: 'https://i.postimg.cc/7hYWgr7s/2-3-4-Chemostat-1.jpg',
    imgUrlCaseStudyBWTEE2_3_4O2: 'https://i.postimg.cc/76NRGZCJ/2-3-4-Chemostat-2.jpg',
    imgUrlCaseStudyBWTEE2_3_4DHO: 'https://i.postimg.cc/zBNMGgf1/2-3-4-Chemostat-3.jpg',


    urlDashHome: 'https://dash.simpowater.org/dashboard/home',

    urlDashASM3: 'https://dash.simpowater.org/dashboard/biomodels/public/name/ASM3/id/45/did/41',


    // urlDownloadClientWindows: 'https://github.com/Jakkwj/simpo-home/releases/download/v0.11.2/SimpoClient_installer.exe',
    // urlDownloalClientUbuntu: 'https://github.com/Jakkwj/simpo-home/releases/download/v0.11.2/SimpoClient_installer.sh',

    urlDownloadClientWindows: 'https://github.com/Jakkwj/simpo-home/releases/download/v0.11.2/SimpoClient_0.11.2.exe',
    urlDownloalClientUbuntu: 'https://github.com/Jakkwj/simpo-home/releases/download/v0.11.2/SimpoClient_0.11.2_amd64.deb',

    // urlDownloalBaidu: 'https://pan.baidu.com/s/1N89lx1xbCvoIwvbc-Qdl8g?pwd=spwt',
    // urlDownloalNetdisk: 'https://pan.baidu.com/s/1oVqOzanzFKDnSHHkkH_v3g?pwd=simp',
    urlDownloalNetdisk: 'https://pan.baidu.com/s/1dV37ANzonYqQKorJkyX5Ig?pwd=simp',
    // urlDownloalNetdisk: 'https://pan.baidu.com/s/1oVqOzanzFKDnSHHkkH_v3g?pwd=simp#list/path=%2Fsharelink1245391030-65267744155022%2Fwindows&parentPath=%2Fsharelink1245391030-65267744155022',

    // urlDownloadClientWindows: 'https://github.com/Jakkwj/simpo-home/releases/download/v0.6.0/SimpoClient_installer.exe',
    // urlDownloalClientUbuntu: 'https://github.com/Jakkwj/simpo-home/releases/download/v0.6.0/SimpoClient_installer.sh',

    // urlDownloadUrlplateBioModel: 'https://sludge.readthedocs.io/en/latest/_downloads/fe952779792f1eab732422dd1492e15f/BioModel.xlsx',
    // urlDownloadUrlplateDataSet: 'https://sludge.readthedocs.io/en/latest/_downloads/ce5b40856b1e6d339bc3e8055a65ed80/DataSet.xlsx',
    // urlDownloadUrlplateProject: 'https://sludge.readthedocs.io/en/latest/_downloads/cdbae577b8f73a4be69004f393d76da6/Solution.xlsx',
    urlDownloadUrlplateBioModel: 'https://github.com/Jakkwj/simpo-home/releases/download/template/BioModel.xlsx',
    urlDownloadUrlplateDataSet: 'https://github.com/Jakkwj/simpo-home/releases/download/template/DataSet.xlsx',
    urlDownloadUrlplateProject: 'https://github.com/Jakkwj/simpo-home/releases/download/template/Solution.xlsx',

    iframeIfSignSrc: 'https://dash.simpowater.org/ifsign',

  },

  // urlDownloadClientWindows: 'https://sludge.readthedocs.io/en/latest/_downloads/4269e5ad1fd14053bd80f03977e51dad/SimpoClient_installer.exe',
  // urlDownloalClientUbuntu: 'https://sludge.readthedocs.io/en/latest/_downloads/4fffe0f55f67f1c6b7eb94ec4fb6013f/SimpoClient_installer.sh',
  //

  title: title,
  // tagline: 'A Scientific Computing SaaS Platform',
  // tagline: 'A Simulation SaaS Platform for Water and Wastewater Treatment Process Modeling',
  tagline: 'A Scientific Computing SaaS Platform for Water and Wastewater Treatment Process Modeling',
  // tagline: 'A SaaS platform for wastewater treatment modeling',


  favicon: 'img/logo3.ico',
  // favicon: 'https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/ico/logo3.ico',

  // Set the production url of your site here
  // url: 'https://your-docusaurus-test-site.com',
  // url: 'https://jakkwj.github.io',
  url: urlHome,
  // 'https://www.simpowater.org',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  // organizationName: title, // Usually your GitHub org/user name.
  // projectName: 'Sludge', // Usually your repo name.
  organizationName: 'Jakkwj', // Usually your GitHub org/user name.
  // projectName: 'jakkwj.github.io', // Usually your repo name.
  // projectName: 'simpo_home', // Usually your repo name.
  projectName: 'simpo-home', // Usually your repo name.
  trailingSlash: false,
  deploymentBranch: 'gh-pages',

  // onBrokenLinks: 'throw', // 检测到无效链接时的行为, 抛出错误, v3 升级后 build 时会报错
  onBrokenLinks: 'ignore',

  onBrokenMarkdownLinks: 'warn', // 检测到无效 Markdown 链接时的行为 警告



  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh'], // zh-Hans 简体中文
    // locales: ['en'],
    // locales: ['en', 'zh-Hans'], // zh-Hans 简体中文


    // locales: ['en', 'zh-Hans', 'fa'],
    // localeConfigs: {
    //   en: {
    //     htmlLang: 'en-GB',
    //   },
    //   // 如果你不需要覆盖默认值，你可以忽略这个语言（比如 zh-Hans）
    //   fa: {
    //     direction: 'rtl',
    //   },
    // },

  },

  presets: [
    [
      // 'classic',
      '@docusaurus/preset-classic',
      // '@docusaurus/preset-live-codeblock',





      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebarsDocs.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: false,
        // blog: {
        //   showReadingTime: true,
        //   // Please change this to your repo.
        //   // Remove this to remove the "edit this page" links.
        //   editUrl:
        //     'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        // },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
          // customCss: require.resolve('./src/css/custom.scss'),
        },

        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          ignorePatterns: ['/tags/**'],
          filename: 'sitemap.xml',
        },

      }),
    ],
  ],

  plugins: [
    // '@docusaurus/theme-live-codeblock',
    // 'docusaurus-plugin-sass'
    require.resolve("docusaurus-plugin-image-zoom"),

    // [
    //   '@docusaurus/plugin-content-docs',
    //   {
    //     id: 'library',
    //     path: 'library',
    //     routeBasePath: 'library',
    //     // sidebarPath: './sidebarsLibrary.js',
    //     sidebarPath: require.resolve('./sidebarsLibrary.js'),
    //     // ... other options
    //   },
    // ],
    [
      '@docusaurus/plugin-content-docs',
      // {
      //   id: 'library',
      //   path: 'library',
      //   routeBasePath: 'library',
      //   sidebarPath: require.resolve('./sidebarsLibrary.js'),
      // },
       {
        id: 'resource',
        path: 'resource',
        routeBasePath: 'resource',
        sidebarPath: require.resolve('./sidebarsResource.js'),
      },
    ],

    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'changelog',
        path: 'changelog',
        routeBasePath: 'changelog',
        sidebarPath: require.resolve('./sidebarsChangelog.js'),
      },
    ],


  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({

      metadata: [
        {name: 'keywords', content: 'water, wastewater, treatment, modeling'},
      ],

      zoom: {
        selector: '.markdown :not(em) > img', // 仅限 marddown 中的 img 点击放大
        // selector: 'img', // 所有 img
        background: {
            // light: 'rgb(255, 255, 255)',
            // light: "#ebedf0",
            light: "#F5F5F5",
            // light: "#EEEEEE",
            // light: "#E0E0E0",
            // light: "#BDBDBD",
            dark: 'rgb(50, 50, 50)'
          },

        config: {
          // options you can specify via https://github.com/francoischalifour/medium-zoom#usage
          // background: {
          //   // light: 'rgb(255, 255, 255)',
          //   light: "#00a400",
          //   dark: 'rgb(50, 50, 50)'
          // },
          // background: "#00a400",
          scrollOffset: 0, // The number of pixels to scroll to close the zoom
          margin: 65,
        }
      },

      colorMode: {
        disableSwitch: true,
        defaultMode: 'light',
        // respectPrefersColorScheme: true,
      },


      liveCodeBlock: {
        /**
         * 实时效果显示的位置，在编辑器上方还是下方。
         * 可为："top" | "bottom"
         */
        playgroundPosition: 'bottom',
      },

      // Replace with your project's social card
      // image: 'img/docusaurus-social-card.jpg',
      image: urlLogo,
      // 'https://i.postimg.cc/rsPqvJNJ/logo3.png',

      announcementBar: {
        id: 'announcementBar',
        content:
          '<strong>🎉 <a target="_blank" rel="noopener noreferrer" href="http://www.simpowater.org/changelog/SIMPO%20Client/2025">Simpo Client v0.11.2</a> has been released!</strong>',
        isCloseable: true,
        // backgroundColor: '#5e72e4',
        // textColor: '#ffffff',
        backgroundColor: '#eee',
        textColor: '#5e72e4',
        // backgroundColor: '#ffffff',
        // textColor: '#5e72e4',
      },

      algolia: {
        // If Algolia did not provide you any appId, use 'BH4D9OD16A'
        appId: '11LZNE9YBJ',
        // Public API key: it is safe to commit it
        apiKey: '841fa2f7f6ced4b0b5f3743465da2ff8', // Search-Only API Key
        // apiKey: '641c7fdb7f7c5cbc823ca21c58f155d0', // email key
        indexName: 'simpowater',  // must the same as Algolia index name
        // Optional: see doc section below
        contextualSearch: false, // 必须为false, 否则无法访问
        // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
        // externalUrlRegex: 'external\\.com|domain\\.com',
        // Optional: Algolia search parameters
        // searchParameters: {},
      },

      navbar: {
        hideOnScroll: true,
        title: title,
        logo: {
          alt: 'Logo',
          // src: 'img/logo.svg',
          // src: 'img/logo.png',
          // src: 'img/logo3.png',
          src: 'https://i.postimg.cc/rsPqvJNJ/logo3.png',
        },
        items: [
          // {
          //   type: 'docsVersionDropdown',
          //   dropdownItemsAfter: [
          //     {
          //       type: 'html',
          //       value: '<hr style="margin: .5em 0;" />',
          //     },
          //     { to: '/versions', label: 'All Versions' },
          //     { to: '/supported-releases', label: 'Supported Releases' },
          //   ],
          // },

          {
            type: 'localeDropdown',
            position: 'right',
          },
          {
            // label: 'Tutorials',
            // label: 'Documentation',
            label: 'Docs',
            type: 'doc',
            // docId: 'Introduction',
            docId: 'QucikStart',
            // to: 'docs',
            position: 'left',
            // label: 'Guides',

          },
          // {
          //   label: 'Library',
          //   to: 'library',
          //   position: 'left',
          //   // label: 'Guides',
          // },
          {
            label: 'Resource',
            to: 'resource',
            position: 'left',
            // label: 'Guides',
          },
          {
            label: 'Changelog',
            to: 'changelog',
            position: 'left',
            // label: 'Guides',
          },
          {
            // to: 'https://hasura.io/changelog',
            label: "About",
            to: '/about',
            position: 'left',
          },


          // {
          //   label: 'Client',
          //   type: 'dropdown',
          //   position: 'left',
          //   items: [
          //     {
          //       type: 'html',
          //       value: resourcesHTML,
          //       className: 'dyte-dropdown',
          //     },
          //   ],
          // },

          // {
          //   // to: 'https://hasura.io/changelog',
          //   to: '/docs/changelog/intro',
          //   label: "ChangeLog",
          //   position: 'left',
          // },
          // {
          //   label: 'Support',
          //   to: 'https://dyte.io/contact',
          // },
          {
            type: 'search',
            position: 'right',
          },


          // {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://github.com/jakkwj/simpo_home',
            position: 'right',
            className: 'header-github-link',
            'aria-label': 'GitHub repository',
            docspluginid: 'GitHub'
          },

          // { href: `${urlConsole}`, label: true ? 'Dashboard' : 'Login', position: 'right'},
          // { href: `${urlConsole}`, label: true ? 'Sign In' : 'Dashboard', position: 'right'},
          // { href: `${urlConsole}`, label: !!global.localStorage.getItem('accessToken') ? 'Dashboard' : 'Sign In', position: 'right'},

          // { href: `${urlConsole}`, label: 'Dashboard', position: 'right', docspluginid: 'Dashboard'},
          // { href: `${urlConsole}`, label: 'Sign In', position: 'right', docspluginid: 'SignIn'},
          { href: `${urlConsole}`, label: 'Dashboard', position: 'right', docspluginid: 'Dashboard'},
          { href: `${urlConsole}`, label: 'Sign In', position: 'right', docspluginid: 'SignIn'},

          // {
          //   href: 'https://github.com/facebook/docusaurus',
          //   label: 'GitHub',
          //   position: 'right',
          // },
        ],
      },



      footer: {
        style: 'dark',
        // style: 'light',

        // logo: {
        //   // alt: 'Meta 开源图标',
        //   src: 'img/logo3.png',
        //   width: 30,
        //   height: 30,
        // },


        links: [

          {
              // title: 'SIMPO',
              items: [
                // {
                //   label: 'Tutorial',
                //   to: '/docs/intro',
                // },
                // {
                //   html: `
                //       <a href="https://www.netlify.com" target="_blank" rel="noreferrer noopener" aria-label="Deploys by Netlify">
                //         <img src="https://www.netlify.com/img/global/badges/netlify-color-accent.svg" alt="Deploys by Netlify" width="114" height="51" />
                //       </a>
                //     `,
                // },
                {
                  html: `
                      <a href="${urlHome}">
                        <img src="${urlLogo}" alt="SIMPO" width="40" height="40" />
                      </a>
                    `,
                },

              ],
            },

             {
              title: 'Learn',
              items: [
                // {
                //   label: 'Introduction',
                //   to: '/docs/intro',
                // },
                {
                  label: 'Installation',
                  to: '/docs/Tutorials/Installtion',
                },

                {
                  label: 'Case Study',
                  to: '/docs/category/case-study',
                },

              ],
            },



            {
              title: 'Legal',
              items: [
                {
                  // label: 'Terms of Service',
                  label: 'Terms',
                  to: '/legal/terms',
                },
                {
                  // label: 'Privacy Policy',
                  label: 'Privacy',
                  to: '/legal/privacy',
                },

              ],
            },


          // {
          //   title: 'Docs',
          //   items: [
          //     {
          //       label: 'Tutorial',
          //       to: '/docs/intro',
          //     },

          //   ],
          // },
          // {
          //   title: 'Community',
          //   items: [
          //     {
          //       label: 'Stack Overflow',
          //       href: 'https://stackoverflow.com/questions/tagged/docusaurus',
          //     },
          //     {
          //       label: 'Discord',
          //       href: 'https://discordapp.com/invite/docusaurus',
          //     },
          //     {
          //       label: 'Twitter',
          //       href: 'https://twitter.com/docusaurus',
          //     },
          //   ],
          // },

          {
            title: 'Support',
            items: [
              {
                // label: 'Contact Us',
                label: 'Contact',
                to: '/support/contact',
              },

            ],
          },
          {
            title: 'More',
            items: [
              // {
              //   label: 'Blog',
              //   to: '/blog',
              // },
              {
                label: 'Changelog',
                // to: '/docs/category/changelog',
                to: '/changelog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/jakkwj/simpo_home',
              },
            ],
          },
        ],

        //  logo: {
        //   // alt: 'Meta 开源图标',
        //   src: 'img/logo3.png',
        //   width: 30,
        //   height: 30,
        // },


        // copyright: `Copyright © ${new Date().getFullYear()} ${title}, Inc. All rights reserved.`,
        copyright: `Copyright © ${new Date().getFullYear()} ${title}. All rights reserved.`,
        // Built with Docusaurus.
      },
      prism: {
        theme: lightTheme,
        darkTheme: darkTheme,
      },
    }),

  markdown: { // 加入 mermaid https://docusaurus.io/zh-CN/docs/markdown-features/diagrams
    // yarn add @docusaurus/theme-mermaid@next  # 通过 @ next 选择正确的版本 2.4.0
    // yarn add mdx-mermaid mermaid  # mermaid in mdx
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

};

module.exports = config;
