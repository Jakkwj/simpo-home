# 部署

- 每次部署都会clone一次，非常的慢，需要[设置npm和yarn的代理和registry](https://zhuanlan.zhihu.com/p/272474048)
  - 查看``lanter``的代理端口，设置为：``yarn config set proxy 127.0.0.1:33137``
  - 如果需要删除代理：``yarn config delete proxy ``

- 使用这个命令进行部署：``USE_SSH=true yarn deploy``

- 注意在``docusaurus.config.就是``中指明了部署的分支是``deploymentBranch: 'gh-pages'``

  - 即在``github``上的分支
  - 在``xxx.github.io/settings/pages``中``Branch``设置为``gh-pages``，并设置``Custom domain``为: www.simpowater.org

- 每次部署后, 都需要在``settings/pages``中重新设置``Custom domain``: www.simpowater.org

  





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