#!/bin/bash

# 自动部署到 github page
git config --global http.proxy 'http://127.0.0.1:37799'  # 设置 git 代理
git config --global https.proxy 'http://127.0.0.1:37799'
yarn config set proxy "http://127.0.0.1:37799"  # 设置 yarn 代理
yarn config set https-proxy "http://127.0.0.1:37799"

git add -A && git commit -m "updated" && git push -u origin master

USE_SSH=true yarn deploy  # 部署到 github page

git config --global --unset http.proxy  # 取消 git 代理
git config --global --unset https.proxy
yarn config delete proxy  # 取消 yarn 代理
yarn config delete https-proxy
