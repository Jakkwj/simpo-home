import React, {useEffect} from 'react';

// Default implementation, that you can customize
export default function Root({children}) {

  useEffect(() => {
    window.addEventListener(
      'message',
      (iframeMessage) => {
        localStorage.setItem('ifSign', !!iframeMessage.data.accessToken);
      }
    );
    let iframe = document.createElement("iframe");
    iframe.src = "http://111.230.245.215/ifsign";
    iframe.style="display: none;"
    document.body.appendChild(iframe);
  });


  return <>{children}</>;
}
