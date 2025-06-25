import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
// import PartialExample from './_markdown-partial-example.mdx';
import { isMobile, isDesktop } from "react-device-detect";
import TimeLine from "./timeline.mdx";
import Gantt from "./gantt.mdx";

export default function FeaturesOpen() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div
      className="hero"
      // style={{ marginTop: "-9vh" }}
    >
      <div
        // className="container-features text-center"
        className="tw-container tw-mx-auto tw-px-14"
        style={{ width: "100%" }}
      >
        {/* <hr
          style={{
            marginTop: "2.8vh",
            marginBottom: "3vh",
            paddingLeft: "18vw",
            paddingRight: "18vw",
          }}
        /> */}
        <h1 className="text-center">Roadmap</h1>
        This is the raodmap of <b>SIMPO</b>. For more details please refer to:{" "}
        <a href="changelog">Changelog</a>.{/* <TimeLine name="TimeLine" /> */}
        <Gantt name="Gantt" />
        {/* {isDesktop ? <Gantt name="Gantt" /> : <span></span>} */}
      </div>
    </div>
  );
}
