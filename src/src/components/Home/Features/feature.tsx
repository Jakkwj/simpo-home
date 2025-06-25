import React from "react";
import clsx from "clsx";
// import Translate from '@docusaurus/Translate'
import styles from "./index.module.css";
// import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Link from '@docusaurus/Link';
import useBaseUrl from "@docusaurus/useBaseUrl";
import { isMobile, isDesktop } from "react-device-detect";
// import ThemedImage from '@theme/ThemedImage';

interface Props {
  imgUrl: string;
  title: JSX.Element | string;
  description: JSX.Element;
  reverse: boolean;
  width?: string;
  marginTopImg?: string;
  marginRightImg?: string;
  objectPosition?: string;
  marginTop?: string;
}

export default function Feature({
  imgUrl,
  title,
  description,
  reverse,
  width = "100%",
  marginTopImg = "0vh",
  marginRightImg = "0vh",
  objectPosition = "50% 0%",
  marginTop = "0vh",
}: Props) {
  return (
    <div
      className={clsx(
        // "tw-row",
        "tw-grid tw-gap-12 lg:tw-grid-cols-2 sm:tw-grid-cols-1",
        isMobile ? styles.featureMobile : styles.feature,
        reverse && styles.featureReverse
      )}
    >
      {/* <div className="tw-col tw-col-6 tw-text--center"> */}
      <div className="">
        {/* <img className={styles.featureImage} src={useBaseUrl(imgUrl)} alt={title}/> */}
        <img
          src={useBaseUrl(imgUrl)}
          alt={title as string}
          width={width}
          style={{
            marginTop: marginTopImg,
            marginRight: marginRightImg,
            // padding: "1.5rem",
            // width: "670px",
            // height: "400px",
            objectPosition: objectPosition,
            // objectFit: "cover",
          }}
        />
      </div>
      {/* <div className={clsx("tw-col tw-col-6", styles.featureContent)}> */}
      <div className={clsx("", styles.featureContent)}>
        <div style={{ marginTop: marginTop }}>
          <h3>{title}</h3>
          <div>{description}</div>
        </div>
      </div>
    </div>
  );
}
