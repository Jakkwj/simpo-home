# Hugo



[Hugo + GitHub Pages 搭建自己的网站](https://blog.csdn.net/azl397985856/article/details/110848517)

[Hugo官网](https://gohugo.io/getting-started/quick-start/)

# Theme

## [Academic](https://sourcethemes.com/academic/)

[Edit on your PC with Hugo Extended](https://wowchemy.com/docs/getting-started/install-hugo-extended/)

```
# 安装 Go 依赖
sudo snap install --classic go
# 下载 Academic 主题
git clone https://github.com/wowchemy/starter-academic.git
cd starter-academic
hugo server

# 通过 Hugo 生成静态页面时，指定目标目录为 docs：
hugo -d docs


```


# Github

- 数据源默认使用主分支下的根目录，我个人建议改为 docs 目录；
  - Github pages 的 Source 中，Branch：main/docs
- 小细节：避免 Jekyll 起作用，可以在仓库根目录放一个空文件，文件名：.nojekyll





