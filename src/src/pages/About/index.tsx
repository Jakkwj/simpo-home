import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import ThemedImage from '@theme/ThemedImage';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Translate from '@docusaurus/Translate'
import useBaseUrl from '@docusaurus/useBaseUrl'
import Layout from '@theme/Layout';
import HomepageHeader from '@site/src/components/Home/Header';
// import FeaturesEasyToUse from '@site/src/components/Home/Features/easyToUse';
// import FeaturesPowerful from '@site/src/components/Home/Features/powerful';
// import FeaturesOpen from '@site/src/components/Home/Features/open';
// import FeaturesTrackable from '@site/src/components/Home/Features/trackable';
import AboutJiangFeng from '@site/src/pages/About/jiangfeng';
import AboutWangJun from '@site/src/pages/About/wangjun';
import AboutLiHao from '@site/src/pages/About/lihao';
// import AboutWuKe from '@site/src/pages/About/wuke';
// import AboutHuangZhaoWei from './huangzhaowei';
// import AboutShiYongFeng from './shiyongfeng';

import styles from './index.module.css';


export default function About(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    // <Layout
    //   title={`Hello from ${siteConfig.title}`}
    //   description="Description will go into a meta tag in <head />">
    //   <HomepageHeader />
    //   <main>
    //     <HomepageFeatures />
    //   </main>
    // </Layout>

    <Layout
    // title={`Hello from ${siteConfig.title}`}
    // title={`${siteConfig.title}`}
    title={'Home'}
    description="Description will go into a meta tag in <head />"
    >
      {/* noFooter */}
      {/* wrapperClassName="homepage flex flex-col" */}

      {/* <HomepageHeader /> */}


      <main>

        <h1 style={{ marginTop: '3vh', marginBottom: '-3vh', textAlign: 'center' }} className="hero__title">
          <Translate>
            {'About The Team'}
          </Translate>
        </h1>

        <h1 style={{ marginTop: '3vh', marginBottom: '-4vh', marginLeft: '15vw', textAlign: 'left' }}>
          <Translate>
            {'Developer Team'}
          </Translate>
        </h1>

        <AboutJiangFeng />

        <AboutWangJun />

        <h1 style={{ marginTop: '3vh', marginBottom: '-4vh', marginLeft: '15vw', textAlign: 'left' }}>
          <Translate>
            {'Supporter Team'}
          </Translate>
        </h1>

        <AboutLiHao />
        {/* <AboutWuKe />
        <AboutHuangZhaoWei />
        <AboutShiYongFeng /> */}

      </main>

    </Layout>
  );
}
