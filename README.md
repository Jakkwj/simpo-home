# 部署

- 每次部署都会 clone 一次，非常的慢，需要[设置 npm 和 yarn 的代理和 registry](https://zhuanlan.zhihu.com/p/272474048)

  - 查看`lanter`的代理端口，设置为：`yarn config set proxy 127.0.0.1:33137`
  - 如果需要删除代理：`yarn config delete proxy `

- 使用这个命令进行部署：`USE_SSH=true yarn deploy`

- 注意在`docusaurus.config.就是`中指明了部署的分支是`deploymentBranch: 'gh-pages'`

  - 即在`github`上的分支
  - 在`xxx.github.io/settings/pages`中`Branch`设置为`gh-pages`，并设置`Custom domain`为: www.simpowater.org

# CNAME

- 每次部署后, 都需要在`settings/pages`中重新设置`Custom domain`: www.simpowater.org
- 为了解决这个问题, 需要在`static/`文件夹下新建一个`CNAME`文件: www.simpowater.org
- https://github.com/facebook/docusaurus/issues/3889

- 

# 图片点击放大

- https://gabrielcsapo.github.io/docusaurus-plugin-image-zoom/docs/getting-started/
- `npm install docusaurus-plugin-image-zoom --save`

# Mermaid

- 加入 mermaid https://docusaurus.io/zh-CN/docs/markdown-features/diagrams
  - yarn add @docusaurus/theme-mermaid@next # 通过 @ next 选择正确的版本 2.4.0
- [mermaid in mdx](https://github.com/sjwall/mdx-mermaid): yarn add mdx-mermaid mermaid #

# Algolia docsearch

- https://docusaurus.io/docs/search
- 申请后, 需要等待审核
- https://zhuanlan.zhihu.com/p/625637978
- -

## Github Action 自动在 push 后爬取

- https://oreo.life/en/blog/2023-02-12-crawl-website-using-github-actions/
  - https://crawler.algolia.com/admin/user/settings/ 获取`Crawler User ID`和`Crawler API Key`.
  - `algolia-api-key`用的是`SEARCH_API_KEY`
- `.github/workflows/docsearch-scraper.yml`:

```bash
name: Crawl

on:
  push:
    branches: [ "master" ]
  workflow_dispatch:

jobs:
  crawl:
    runs-on: ubuntu-latest
    steps:
      - name: Algolia Crawler Automatic Crawl
        uses: algolia/algoliasearch-crawler-github-actions@v1.1.10
        with:
          crawler-user-id: ${{ secrets.CRAWLER_USER_ID }}
          crawler-api-key: ${{ secrets.CRAWLER_API_KEY }}
          github-token: ${{ github.token }}
          crawler-name: 'simpowater'
          algolia-app-id: ${{ secrets.ALGOLIA_APP_ID }}
          algolia-api-key: ${{ secrets.ALGOLIA_SEARCH_API_KEY }}
          site-url: 'https://www.simpowater.org/docs'

```

- 注意: `algoliasearch-crawler-github-actions`版本升级：
  - 这里查询新版：https://github.com/algolia/algoliasearch-crawler-github-actions/releases

- 
- 以下方式作废：
- ~~在根目录中添加`docsearch-config.json`: https://github.com/algolia/docsearch-configs/blob/master/configs/docusaurus-2.json~~
- ~~在根目录中`.github/workflows/algolia-docsearch-scraper.yml`~~
  - ~~`ALGOLIA_APP_ID`和`ALGOLIA_API_KEY`在`https://crawler.algolia.com`后台获取~~
  - ~~具体内容见下:~~

```bash
# 以下 action 脚本作废
name: algolia-docsearch-scraper

on:
  push:
    branches: [master]


jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - name: Sleep for 10 seconds
        run: sleep 10s
        shell: bash

      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Run scraper
        env:
          APPLICATION_ID: ${{ secrets.ALGOLIA_APP_ID }}
          API_KEY: ${{ secrets.ALGOLIA_API_KEY }}
        run: |
          CONFIG="$(cat docsearch-config.json)"
          docker run -i --rm \
                  -e APPLICATION_ID=$APPLICATION_ID \
                  -e API_KEY=$API_KEY \
                  -e CONFIG="${CONFIG}" \
                  algolia/docsearch-scraper
```

## 问题：

- DocSearch Error: 400: Bad Request {"code":"invalid_action","message":"This action cannot be executed on a blocked crawler"}
  - https://support.algolia.com/hc/en-us/articles/12151775552017-DocSearch-Error-400-Bad-Request-code-invalid-action-message-This-action-cannot-be-executed-on-a-blocked-crawler#:~:text=When%20using%20the%20API%20of%20the%20Crawler%20and,and%20then%20the%20API%20will%20accept%20requests%20again.
  - When using the API of the Crawler and you find the Crawler is blocked, you can take a look at the frontend for more information: [Crawler Admin Console](https://crawler.algolia.com/admin/users/login)
  - To fix the issue, you need to unblock the Crawler by clicking the `Cancel` button from the UI, and then the API will accept requests again.

 

# 多语言

- https://docusaurus.io/docs/i18n/tutorial
- 生成翻译文档: `yarn write-translations --locale zh`
- 生成`md`:
  ```bash
  mkdir -p i18n/zh/docusaurus-plugin-content-docs/current
  cp -r docs/** i18n/zh/docusaurus-plugin-content-docs/current
  ```
- 启动语言服务器: `yarn start --locale zh`

# 强制删除某次`github`提交

- https://stackoverflow.com/questions/448919/how-can-i-remove-a-commit-on-github

```bash
# 获取某次提交的 hash
git log
# 删除这之前的提交
git reset --hard 71c27777543ccfcb0376dcdd8f6777df055ef479
# 强制推送一次
git push --force
```

---

# Website

This website is built using [Docusaurus 2](https://docusaurus.io/), a modern static website generator.

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

如果失败, 重新运行`yarn install`一次

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Using SSH:

```
$ USE_SSH=true yarn deploy
```

Not using SSH:

```
$ GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
