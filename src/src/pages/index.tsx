import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import ThemedImage from '@theme/ThemedImage';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Translate from '@docusaurus/Translate'
import useBaseUrl from '@docusaurus/useBaseUrl'
import Layout from '@theme/Layout';
import HomepageHeader from '@site/src/components/Home/Header';
import Roadmap from '@site/src/components/Home/Roadmap';
import FeaturesEasyToUse from '@site/src/components/Home/Features/easyToUse';
import FeaturesPowerful from '@site/src/components/Home/Features/powerful';
import FeaturesOpen from '@site/src/components/Home/Features/open';
import FeaturesTrackable from '@site/src/components/Home/Features/trackable';
import FeaturesCollaboration from '@site/src/components/Home/Features/collaboration';
// src/components/Home/Roadmap/index.mdx
// import TeamJiangFeng from '@site/src/components/Home/Team/jiangfeng';

import styles from './index.module.css';


export default function Home(): JSX.Element {
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

      <HomepageHeader />

      <main>

        <FeaturesEasyToUse />
        <FeaturesPowerful />
        <FeaturesOpen />
        <FeaturesTrackable />
        <FeaturesCollaboration />
        <Roadmap />
        {/* <TeamJiangFeng /> */}

      </main>

    </Layout>
  );
}
