import React from 'react';

export default function Root({children}) {

  window.addEventListener(
    'message',
    (iframeMessage) => {
      // console.log('@19', iframeMessage.data.accessToken, !iframeMessage.data.accessToken, !!iframeMessage.data.accessToken)
      localStorage.setItem('ifSign', !!iframeMessage.data.accessToken);
    }
  ); // 添加监听 iframe 的事件, 判断是否登录

  let iframe = document.createElement("iframe");
  // iframe.src = "http://localhost:9000/sign/ifsign";
  // iframe.src = "http://111.230.245.215/dashboard/home";
  // iframe.src = "http://localhost:9000/ifsign";
  iframe.src = "http://111.230.245.215/ifsign";
  iframe.style="display: none;" // 隐藏本 iframe
  document.body.appendChild(iframe);

  return (
    <>
      {children}
    </>
  );
}
