// import React, {useEffect, useState} from 'react';
// import useIsBrowser from '@docusaurus/useIsBrowser';
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';



const addIframeListener = () => {
  /**
   * 加载时, 添加 iframe Listener
   * 监听是否登录了 Dashborad
   */
  window.addEventListener(
    'message',
    (iframeMessage) => {
      localStorage.setItem('ifSign', !!iframeMessage.data.accessToken);
      // console.log('@15', localStorage.getItem('ifSign'));
    }
  );
  // let iframe = document.createElement("iframe");
  // iframe.src = "https://dash.simpowater.org/ifsign";
  // iframe.style="display: none;" // 隐藏
  // document.body.appendChild(iframe);

}


// Default implementation, that you can customize
export default function Root({children}) {
  /**
   * TODO: 2023.05.22
   * Mixed Content: The page at was loaded over HTTPS, but requested an insecure frame. This request has been blocked; the content must be served over HTTPS: https://stackoverflow.com/questions/67765238/mixed-content-the-page-at-was-loaded-over-https-but-requested-an-insecure-resour
   * 搬去 https 后需要移除
   *
   */

  const {siteConfig} = useDocusaurusContext();


  //
    // const isBrowser = useIsBrowser();
    // console.log('@32', isBrowser);


    // const [content, setContent] = useState('初始状态')
    // if (isBrowser) {
      // useEffect(() => {
        // console.log('@38');

      // });
    // } else {
      // console.log('@58');
      // }




  // <BrowserOnly>
  //   {() => { // 编译时必须打开, 否则无法识别 window
  //     addIframe();
  //     // window.addEventListener(
  //     //   'message',
  //     //   (iframeMessage) => {
  //     //     localStorage.setItem('ifSign', !!iframeMessage.data.accessToken);

  //     //     // setContent(!!iframeMessage.data.accessToken);
  //     //     console.log('@15', localStorage.getItem('ifSign'));
  //     //   }
  //     // );
  //     // let iframe = document.createElement("iframe");
  //     // iframe.src = "https://dash.simpowater.org/ifsign";
  //     // iframe.style="display: none;"
  //     // document.body.appendChild(iframe);
  //   }}
  // </BrowserOnly>

  if (ExecutionEnvironment.canUseDOM) {
    addIframeListener(); // 开发时打开
  }

  return <>

    {/* 只是 http 强制变化为 https, 没法解决 Mixed Content */}
    {/* <Head>
      <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests" />
    </Head> */}
    {children}

    {/* <iframe id="iframeIfSign" src="http://dash.simpowater.org/ifsign"></iframe> */}
    {/* <iframe id="iframeIfSign" src="https://dash.simpowater.org/ifsign"></iframe> */}
    <iframe id="iframeIfSign" src={siteConfig.customFields.iframeIfSignSrc}></iframe>

  </>;
}
