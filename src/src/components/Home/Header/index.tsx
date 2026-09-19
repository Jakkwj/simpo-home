import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Translate from "@docusaurus/Translate";
import { Dropdown } from "antd";
import { FaLinux, FaWindows } from "react-icons/fa";
import {
  FiChevronDown,
  FiDownload,
  FiMonitor,
  FiTerminal,
} from "react-icons/fi";

import styles from "./styles.module.css";

export default function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  const [downloadOpen, setDownloadOpen] = React.useState(false);

  // 每个产品使用一个紧凑区块，区块内横向排列 Windows 和 Linux 下载项。
  const downloadPanel = (
    <div className={styles.downloadPanel} role="menu">
      <section className={styles.productSection} aria-labelledby="simpoclient-title">
        <div className={styles.productHeader}>
          <span className={styles.productIcon} aria-hidden="true">
            <FiMonitor />
          </span>
          <span>
            <strong id="simpoclient-title" className={styles.productTitle}>
              SimpoClient
            </strong>
            <span className={styles.productDescription}>
              <Translate id="home.client.calculationDescription">
                Calculation client
              </Translate>
            </span>
          </span>
        </div>
        <div className={styles.platformGrid}>
          <a
            className={styles.platformLink}
            href={siteConfig.customFields.urlDownloadClientWindows as string}
            target="_self"
            rel="noopener noreferrer"
            role="menuitem"
            download
            onClick={() => setDownloadOpen(false)}
          >
            <FaWindows className={styles.windowsIcon} aria-hidden="true" />
            <span className={styles.platformText}>
              <strong>Windows</strong>
              <small>.exe · x64</small>
            </span>
            <FiDownload className={styles.linkDownloadIcon} aria-hidden="true" />
          </a>
          <a
            className={styles.platformLink}
            href={siteConfig.customFields.urlDownloalClientUbuntu as string}
            target="_self"
            rel="noopener noreferrer"
            role="menuitem"
            download
            onClick={() => setDownloadOpen(false)}
          >
            <FaLinux className={styles.linuxIcon} aria-hidden="true" />
            <span className={styles.platformText}>
              <strong>Linux</strong>
              <small>.deb · amd64</small>
            </span>
            <FiDownload className={styles.linkDownloadIcon} aria-hidden="true" />
          </a>
        </div>
      </section>

      <section className={styles.productSection} aria-labelledby="simpo-cli-title">
        <div className={styles.productHeader}>
          <span className={styles.productIcon} aria-hidden="true">
            <FiTerminal />
          </span>
          <span>
            <strong id="simpo-cli-title" className={styles.productTitle}>
              SimpoCLI
            </strong>
            <span className={styles.productDescription}>
              <Translate id="home.client.cliDescription">
                Command-line application
              </Translate>
            </span>
          </span>
        </div>
        <div className={styles.platformGrid}>
          <a
            className={styles.platformLink}
            href={siteConfig.customFields.urlDownloadCLIWindows as string}
            target="_self"
            rel="noopener noreferrer"
            role="menuitem"
            download
            onClick={() => setDownloadOpen(false)}
          >
            <FaWindows className={styles.windowsIcon} aria-hidden="true" />
            <span className={styles.platformText}>
              <strong>Windows</strong>
              <small>.exe · x64</small>
            </span>
            <FiDownload className={styles.linkDownloadIcon} aria-hidden="true" />
          </a>
          <a
            className={styles.platformLink}
            href={siteConfig.customFields.urlDownloadCLILinux as string}
            target="_self"
            rel="noopener noreferrer"
            role="menuitem"
            download
            onClick={() => setDownloadOpen(false)}
          >
            <FaLinux className={styles.linuxIcon} aria-hidden="true" />
            <span className={styles.platformText}>
              <strong>Linux</strong>
              <small>.deb · amd64</small>
            </span>
            <FiDownload className={styles.linkDownloadIcon} aria-hidden="true" />
          </a>
        </div>
      </section>
    </div>
  );

  return (
    <div>
      <div className="hero tw-bg-white tw-py-16">
        <div className="tw-container tw-mx-auto tw-px-4">
          <div className="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-8 tw-items-center">
            <div
              className="tw-text-left"
              style={{
                // marginTop: "1rem",
                marginLeft: "10%",
                // background: "transparent",
              }}
            >
              <div style={{ display: "flex", alignItems: "center" }}>
                <img
                  // src="/img/hero.png" // 替换为您的图片路径
                  src={siteConfig.customFields.imgUrlLogo as string}
                  alt="Preview of using SIMPO"
                  width="9%"
                  // style={{
                  //   // borderRadius: "10px",
                  //   // boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                  //   // marginTop: "2rem",
                  //   marginLeft: "21%",
                  // }}
                />
                <Link> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </Link>
                <h1
                  className="hero__title fade-in-up"
                  style={{
                    marginTop: "1.8rem",
                    marginBottom: "2.2rem",
                    // color: "transparent",
                  }}
                >
                  {siteConfig.title}
                </h1>
              </div>
              {/* <p className="hero__title_2 fade-in-up">
                <Translate id="tagline">{siteConfig.tagline}</Translate>
              </p> */}
              <p
                className="hero__subtitle fade-in-up"
                style={{ marginBottom: "2.2rem" }}
              >
                <Translate id="tagline">
                  {siteConfig.tagline}
                  {/* A Scientific Computing SaaS */}
                  {/* Platform for Water and Wastewater Treatment Process Modelling */}
                  {/* A next-generation platform aimed at simplifying and promoting wastewater treatment modelling */}
                </Translate>
              </p>

              <div className="tw-flex tw-flex-wrap tw-items-center tw-gap-4">
                <div
                // style={{
                //   display: "flex",
                //   gap: "1rem",
                //   justifyContent: "center",
                //   flexWrap: "wrap",
                // }}
                >
                  <Link className="refine-button" to="/docs">
                    <Translate>Quick Start</Translate>
                  </Link>
                </div>

                {/* <CaretRightOutlined
                    style={{ fontSize: "16px", color: "#08c" }}
                  /> */}
                {/* <Button
                href="docs"
                className="refine-button"
                size="large"
                style={{
                  padding: "1.6rem",
                }}
              >
                <strong
                  style={{
                    fontSize: "1.0rem",
                  }}
                >
                  <Translate>Quick Start</Translate>
                </strong>
              </Button> */}
                {/* <Link> &nbsp; &nbsp; </Link> */}
                {/*
              <Link
                className="refine-button refine-button--secondary"
                to="/contact"
              >
                client
              </Link> */}

                <Dropdown
                  menu={{ items: [] }}
                  popupRender={() => downloadPanel}
                  placement="bottomLeft"
                  trigger={["click"]}
                  open={downloadOpen}
                  onOpenChange={setDownloadOpen}
                  rootClassName={styles.downloadDropdown}
                >
                  <button
                    type="button"
                    className={clsx(
                      styles.downloadButton,
                      downloadOpen && styles.downloadButtonOpen,
                    )}
                    aria-haspopup="menu"
                    aria-expanded={downloadOpen}
                  >
                    <span
                      className={styles.downloadButtonIcon}
                      aria-hidden="true"
                    >
                      <FiDownload />
                    </span>
                    <span>
                      <Translate id="home.client.download">
                        Download clients
                      </Translate>
                    </span>
                    <FiChevronDown
                      className={styles.downloadChevron}
                      aria-hidden="true"
                    />
                  </button>
                </Dropdown>
              </div>
            </div>

            {/* 右侧：图片 */}
            <div className="tw-flex tw-justify-left">
              <img
                // src="/img/hero.png" // 替换为您的图片路径
                src={siteConfig.customFields.imgUrlBanner as string}
                alt="Preview of using SIMPO"
                width="80%"
                style={{
                  borderRadius: "10px",
                  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                  marginTop: "2.8rem",
                  marginLeft: "10%",
                }}
              />
              {/* className="tw-rounded-lg tw-shadow-lg" */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
