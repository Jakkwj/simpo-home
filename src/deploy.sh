#!/bin/bash

if [ "$1" == "proxy" ]; then  # ./deploy.sh proxy 运行时
    proxy_ip='http://127.0.0.1:37799'
    git config --global http.proxy $proxy_ip  # 设置 git 代理
    git config --global https.proxy $proxy_ip
    yarn config set proxy $proxy_ip  # 设置 yarn 代理
    yarn config set https-proxy $proxy_ip
fi

git add -A && git commit -m "v0.8.1 released" && git push -u origin master
# git push -u origin master

USE_SSH=true yarn deploy  # 自动部署到 github page

if [ "$1" == "proxy" ]; then
    git config --global --unset http.proxy  # 取消 git 代理
    git config --global --unset https.proxy
    yarn config delete proxy  # 取消 yarn 代理
    yarn config delete https-proxy
fi
