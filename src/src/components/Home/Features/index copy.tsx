import React, { JSX, useState } from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Link from "@docusaurus/Link";
import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";
import { isMobile, isDesktop } from "react-device-detect";
import FeaturesEasyToUse from "@site/src/components/Home/Features/easyToUse";
import FeaturesPowerful from "@site/src/components/Home/Features/powerful";
import FeaturesOpen from "@site/src/components/Home/Features/open";
import FeaturesTrackable from "@site/src/components/Home/Features/trackable";

export default function FeaturesTest() {
  const { siteConfig } = useDocusaurusContext();
  const [activeTab, setActiveTab] = useState("features1");
  const className = isMobile ? "custom-tabs" : "custom-tabs tw-justify-center";
  return (
    <div
      // className="hero"
      className="features-section"
      style={{ width: "100%" }}
      // style={{ marginTop: "0vh", paddingBottom: "0vh" }}
    >
      123
      <div
        className="container text-center"
        // className="text-center"
        style={{ width: "100%" }}
      >
        <h1 className="text-center">
          <Translate>Key Features1</Translate>
        </h1>
        <p>
          <Translate>SIMPO is a supre.</Translate>
        </p>

        <div
          className="custom-tabs-container"
          // style={{ paddingBottom: "0vh", paddingTop: "0vh" }}
        >
          <Tabs
            className={className}
            // className="custom-tabs tw-justify-center"
            // className="tw-justify-center"
            // className="custom-tabs"
            defaultValue="feature1"
            values={[
              { label: "EASY", value: "feature1" },
              { label: "POWERFUL", value: "feature2" },
              { label: "OPEN", value: "feature3" },
              { label: "TRACKABLE", value: "feature4" },
            ]}
            onTabChange={(value) => setActiveTab(value)}
          >
            <TabItem value="feature1" label="feature1">
              <div className="tab-content">
                <div className="content-wrapper">
                  <FeaturesEasyToUse />
                </div>
              </div>
            </TabItem>

            <TabItem value="feature2" label="Powerful">
              <div className="tab-content">
                <div className="content-wrapper">
                  <FeaturesPowerful />
                </div>
              </div>
            </TabItem>

            <TabItem value="feature3" label="Open">
              <div className="tab-content">
                <div className="content-wrapper">
                  <FeaturesOpen />
                </div>
              </div>
            </TabItem>

            <TabItem value="feature4" label="Trackable">
              <div className="tab-content">
                <div className="content-wrapper">
                  <FeaturesTrackable />
                </div>
              </div>
            </TabItem>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
