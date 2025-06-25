import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import ThemedImage from "@theme/ThemedImage";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Translate from "@docusaurus/Translate";
import useBaseUrl from "@docusaurus/useBaseUrl";
import Layout from "@theme/Layout";
import HomepageHeader from "@site/src/components/Home/Header";
import Roadmap from "@site/src/components/Home/Roadmap";
import Features from "@site/src/components/Home/Features";
import FeaturesEasyToUse from "@site/src/components/Home/Features/easyToUse";
import FeaturesPowerful from "@site/src/components/Home/Features/powerful";
import FeaturesOpen from "@site/src/components/Home/Features/open";
import FeaturesTrackable from "@site/src/components/Home/Features/trackable";
import { isMobile, isDesktop } from "react-device-detect";
import Algorithms from "@site/src/components/Home/algorithms";
import Resourses from "@site/src/components/Home/resourses";
// src/components/Home/Roadmap/index.mdx
// import TeamJiangFeng from '@site/src/components/Home/Team/jiangfeng';
import { Tabs } from "antd";
import type { TabsProps } from "antd";

import styles from "./index.module.css";

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  const onChange = (key: string) => {
    console.log(key);
  };

  const items: TabsProps["items"] = [
    {
      key: "1",
      label: "Tab 1",
      children: "Content of Tab Pane 1",
    },
    {
      key: "2",
      label: "Tab 2",
      children: "Content of Tab Pane 2",
    },
    {
      key: "3",
      label: "Tab 3",
      children: "Content of Tab Pane 3",
    },
  ];

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
      title={"Home"}
      description="Description will go into a meta tag in <head />"
    >
      {/* noFooter */}
      {/* wrapperClassName="homepage flex flex-col" */}

      <HomepageHeader />

      <main>
        {/* <Tabs defaultActiveKey="1" centered items={items} /> */}
        <Features />
        <Algorithms />
        {/* <FeaturesEasyToUse /> */}
        {/* <FeaturesPowerful /> */}
        {/* <FeaturesOpen /> */}
        {/* <FeaturesTrackable /> */}
        <Resourses />
        {/* <Roadmap /> */}
        {isDesktop ? <Roadmap /> : <span></span>}

        {/* <TeamJiangFeng /> */}
        {/* <iframe width="100%" height="100%" style={{ position: 'absolute', border: 'none' }} src="https://tgik6tfkz3.jiandaoyun.com/dash/67147701ef6ecbb6ab15c12b?embed=true"></iframe> */}
      </main>
    </Layout>
  );
}
