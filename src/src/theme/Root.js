import React, {useEffect, useRef} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function Root({children}) {
  const {siteConfig} = useDocusaurusContext();
  const frame = useRef(null);
  const iframeUrl = siteConfig.customFields.iframeIfSignSrc;
  const dashOrigin = new URL(iframeUrl).origin;

  useEffect(() => {
    localStorage.removeItem('ifSign');
    const receive = event => {
      if (event.origin !== dashOrigin || event.source !== frame.current?.contentWindow ||
          event.data?.type !== 'simpo-auth-status' || typeof event.data.authenticated !== 'boolean') return;
      window.__simpoAuthenticated = event.data.authenticated;
      window.dispatchEvent(new CustomEvent('simpo-auth-changed', {detail: event.data.authenticated}));
    };
    const refresh = () => frame.current?.contentWindow?.postMessage({type: 'simpo-auth-request'}, dashOrigin);
    window.addEventListener('message', receive);
    window.addEventListener('focus', refresh);
    window.addEventListener('pageshow', refresh);
    refresh();
    return () => {
      window.removeEventListener('message', receive);
      window.removeEventListener('focus', refresh);
      window.removeEventListener('pageshow', refresh);
    };
  }, [dashOrigin]);

  return <>
    {children}
    <iframe ref={frame} id="iframeIfSign" title="Dashboard sign-in status" src={iframeUrl} hidden />
  </>;
}
