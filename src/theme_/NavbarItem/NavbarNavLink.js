// import axios from "axios";
import React from 'react';
import NavbarNavLink from '@theme-original/NavbarItem/NavbarNavLink';

export default function NavbarNavLinkWrapper(props) {

  const { docsPluginId } = props;
  // console.log(docsPluginId)
  // console.log(localStorage.getItem('accs'))

  // <iframe src="http://localhost:9000/sign/ifsign"></iframe>;

  // let ifSign = false;

  // window.addEventListener(
  //   'message',
  //   (iframeMessage) => {
  //     console.log('@19', iframeMessage.data.accessToken, !iframeMessage.data.accessToken, !!iframeMessage.data.accessToken)
  //     // ifSign = !!iframeMessage.data.accessToken;
  //     // localStorage.getItem('ifSign')
  //     // localStorage.setItem('ifSign', !!iframeMessage.data.accessToken);
  //     localStorage.setItem('ifSign', !!iframeMessage.data.accessToken);

  //     // if (docsPluginId === 'Dashboard' && !iframeMessage.data.accessToken) {
  //     //   return null;
  //     // }

  //     // if (docsPluginId === 'SignIn' && !!iframeMessage.data.accessToken) {
  //     //   return null;
  //     // }

  //   }
  // ); // 添加监听 iframe 的事件


  // console.log('@32', docsPluginId, ifSign)

  // const baseURL = "https://jsonplaceholder.typicode.com/posts/1";
  // const baseURL = "http://localhost:9000/sign/ifsign";

  // axios.get(baseURL).then((response) => {
  //   console.log(response.data)
  //   // setPost(response.data);
  // });

  // document.getElementById("Iframe").contentWindow.postMessage('get', '*');

  // if (docsPluginId === 'Iframe') {
  //   // return  <iframe src="http://localhost:9000/sign/ifsign" style="display: none;"></iframe>;

  //   // return <iframe id="iframeConsole" src="http://localhost:9000/sign/ifsign" style={{display: 'none'}} οnlοad={document.getElementById("iframeConsole").contentWindow.postMessage(JSON.stringify('data'), "*")}></iframe>;

  //   // var iframe = document.createElement("iframe");
  //   // iframe.src = "http://localhost:9000/sign/ifsign";
  //   // // if (iframe.attachEvent){
  //   // //     iframe.attachEvent("onload", function(){
  //   // //         alert("Local iframe is now loaded.");
  //   // //         // document.getElementById("iframeConsole").contentWindow.postMessage(JSON.stringify('data'), "*")
  //   // //     });
  //   // // } else {
  //   // //     iframe.onload = function(){
  //   // //         alert("Local iframe is now loaded.");
  //   // //         // document.getElementById("iframeConsole").contentWindow.postMessage(JSON.stringify('data'), "*")
  //   // //     };
  //   // // }
  //   // // console.log(iframe)
  //   // document.body.appendChild(iframe);
  //   return null


  // }

  // var iframe = document.createElement("iframe");
  // iframe.src = "http://localhost:9000/sign/ifsign";
  // if (iframe.attachEvent){
  //       iframe.attachEvent("onload", function(){
  //           alert("Local iframe is now loaded.");
  //           // document.getElementById("iframeConsole").contentWindow.postMessage(JSON.stringify('data'), "*")
  //       });
  //   } else {
  //       iframe.onload = function(){
  //           alert("Local iframe is now loaded.");
  //           // document.getElementById("iframeConsole").contentWindow.postMessage(JSON.stringify('data'), "*")
  //       };
  //   }
  //   console.log(iframe)
  // document.body.appendChild(iframe);

  // if (docsPluginId === 'Dashboard' && !!ifSign) {
  if (docsPluginId === 'Dashboard' && localStorage.getItem('ifSign') !== 'true') {

    // console.log('@97', localStorage.getItem('ifSign'))
    // if (localStorage.getItem('ifSign') !== 'true') {
      return null;
    // }
  }

    if (docsPluginId === 'SignIn' && localStorage.getItem('ifSign') === 'true') {
      return null;
    }

  // if (docsPluginId === 'Dashboard') {


  //   // return  <iframe src="http://111.230.245.215/dashboard/home"></iframe>;
  //   return  <iframe src="http://localhost:9000/sign/ifsign"></iframe>;
  //   // <iframe id="iframe" src="http://localhost:9000/dashboard/home"></iframe>;
  //   // console.log(document.getElementById("iframe").contentWindow.document.getElementById("iframe"));

  //   return  <iframe id="iframe" src="http://localhost:9000/dashboard/home"></iframe>;


  //   // return  <iframe src="https://www.simpowater.org"></iframe>;


  // }

  // if (docsPluginId === 'SignIn') {
  //   return null;

  // }

  // return <NavbarNavLink {...props} />
  // const label = '123'
  return (
    <>
      {/* <NavbarNavLink label={label} {...props} /> */}
      <NavbarNavLink {...props} />
    </>
  );

}
