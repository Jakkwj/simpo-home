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
import Simple from "@site/src/components/Home/Features/simple";
import Efficiency from "@site/src/components/Home/Features/efficiency";
import Prevention from "@site/src/components/Home/Features/prevention";
import Advanced from "@site/src/components/Home/Features/advanced";
import Collaboration from "@site/src/components/Home/Features/collaboration";

export default function Features() {
  const { siteConfig } = useDocusaurusContext();
  const [activeTab, setActiveTab] = useState("features1");
  const className = isMobile ? "custom-tabs" : "custom-tabs tw-justify-center";
  return (
    <div
      className="hero"
      // className="features-section"
      // style={{ width: "80%" }}
      // style={{
      //   background:
      //     "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%)",
      // }}
      // style={{ marginTop: "0vh", paddingBottom: "0vh" }}
    >
      {/* <div className="hero" style={{ marginTop: "-8vh" }}> */}
      {/* <div className="container-features" style={{ width: "80%" }}></div> */}

      {/* <div className="tw-grid tw-place-items-center tw-w-screen">
        <div className="tw-bg-green-500 p-4 text-white">Width 12</div>
      </div> */}

      <div
        // className="container text-center"
        // className="container-features text-center"
        className="tw-container tw-mx-auto tw-px-14"
        // className="tw-grid tw-place-items-center tw-w-screen tw-p-5"
        style={{ width: "100%" }}
      >
        {/* <div>1</div> */}
        <div className="text-white">
          <h1 className="text-center">
            <Translate>Features</Translate>
          </h1>
          {/* <p> */}
          <ul>
            <li style={{ marginBottom: "0.5rem" }}>
              <strong>SIMPO </strong>
              <Translate>
                is initiated by JiangLab (a research team in the School of
                Environmental Science and Engineering, Sun Yat-sen University,
                China). It is an intelligent SaaS platform specifically designed
                for wastewater treatment modelling.
              </Translate>
            </li>

            <li style={{ marginBottom: "0.5rem" }}>
              <strong>SIMPO </strong>
              <Translate>
                integrates advanced algorithms with robust error-proofing
                mechanisms, offering a powerful, user-friendly, free-of-charge
                and collaborative tool for model development, simulation and
                evaluation. It significantly reduced the learning threshold,
                enabling researchers to efficiently construct, simulate, and
                validate models. Its open nature and collaborative features
                further enhanced accessibility and innovation, making SIMPO a
                transformative tool for advancing environmental engineering
                research.
              </Translate>
            </li>

            <li style={{ marginBottom: "0.5rem" }}>
              <strong>SIMPO</strong>
              <Translate>
                's innovations address critical limitations of traditional
                platforms:
              </Translate>
            </li>
          </ul>
          {/* </p> */}
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
                { label: "SIMPLE", value: "feature1" },
                { label: "EFFICIENCY", value: "feature2" },
                { label: "PREVENTION", value: "feature3" },
                { label: "ADVANCED", value: "feature4" },
                { label: "COLLABORATION", value: "feature5" },
              ]}
              onTabChange={(value) => setActiveTab(value)}
            >
              <TabItem value="feature1" label="Simple">
                <div className="tab-content">
                  <div className="content-wrapper">
                    {/* <FeaturesEasyToUse /> */}
                    <Simple />
                  </div>
                </div>
              </TabItem>
              <TabItem value="feature2" label="Efficiency">
                <div className="tab-content">
                  <div className="content-wrapper">
                    {/* <FeaturesPowerful /> */}
                    <Efficiency />
                  </div>
                </div>
              </TabItem>
              <TabItem value="feature3" label="Prevention">
                <div className="tab-content">
                  <div className="content-wrapper">
                    {/* <FeaturesOpen /> */}
                    <Prevention />
                  </div>
                </div>
              </TabItem>
              <TabItem value="feature4" label="Advanced">
                <div className="tab-content">
                  <div className="content-wrapper">
                    {/* <FeaturesTrackable /> */}
                    <Advanced />
                  </div>
                </div>
              </TabItem>
              <TabItem value="feature5" label="Collaboration">
                <div className="tab-content">
                  <div className="content-wrapper">
                    <Collaboration />
                  </div>
                </div>
              </TabItem>
            </Tabs>
          </div>
        </div>
        {/* <div>3</div> */}
      </div>
    </div>
  );
}
