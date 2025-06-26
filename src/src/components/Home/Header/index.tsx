import React from "react";
import clsx from "clsx";
// import styles from './styles.module.css';
import Link from "@docusaurus/Link";
import ThemedImage from "@theme/ThemedImage";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Translate, { translate } from "@docusaurus/Translate";
import type { MenuProps } from "antd";
import { Button, Dropdown, Tooltip, Space } from "antd";
import { AiOutlineDown } from "react-icons/ai";

export default function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  const items: MenuProps["items"] = [
    {
      key: "1",
      label: (
        <a
          href={siteConfig.customFields.urlDownloadClientWindows as string}
          style={{
            textDecoration: "none",
            // color: "var(--ifm-color-primary)",
            fontWeight: 400,
          }}
          download
        >
          Windows
        </a>
      ),
    },
    {
      key: "2",
      label: (
        <a
          href={siteConfig.customFields.urlDownloalClientUbuntu as string}
          style={{
            textDecoration: "none",
            // color: "var(--ifm-color-primary)",
            fontWeight: 400,
          }}
          download
        >
          Ubuntu
        </a>
      ),
    },
    {
      key: "3",
      disabled: true,
      label: (
        <a
          href="#"
          style={{
            cursor: "default",
            color: "gray",
            textDecoration: "none",
            // color: "var(--ifm-color-primary)",
            fontWeight: 400,
          }}
        >
          Mac (pending...)
        </a>
      ),
    },
    {
      key: "4",
      children: [
        {
          key: "4-1",
          label: (
            <a
              target="_blank"
              rel="noopener noreferrer"
              href={siteConfig.customFields.urlDownloalNetdiskWindows as string}
              style={{
                textDecoration: "none",
                // color: "var(--ifm-color-primary)",
                fontWeight: 400,
              }}
            >
              Windows &nbsp;&nbsp;
            </a>
          ),
        },
        {
          key: "4-2",
          label: (
            <a
              target="_blank"
              rel="noopener noreferrer"
              href={siteConfig.customFields.urlDownloalNetdiskUbuntu as string}
              style={{
                textDecoration: "none",
                // color: "var(--ifm-color-primary)",
                fontWeight: 400,
              }}
            >
              Ubuntu &nbsp;&nbsp;
            </a>
          ),
        },
      ],
      label: (
        <a
          target="_blank"
          rel="noopener noreferrer"
          href={siteConfig.customFields.urlDownloalNetdiskUbuntu as string}
          style={{
            textDecoration: "none",
            // color: "var(--ifm-color-primary)",
            fontWeight: 400,
          }}
        >
          Netdisk
        </a>
      ),
    },
  ];

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
              }}
            >
              <div style={{ display: "flex", alignItems: "center" }}>
                <img
                  // src="/img/hero.png" // 替换为您的图片路径
                  src={siteConfig.customFields.imgUrlLogo as string}
                  alt="Preview of using SIMPO"
                  width="9%"
                  // style={{
                  //   borderRadius: "10px",
                  //   boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                  //   marginTop: "2rem",
                  //   marginLeft: "10%",
                  // }}
                />
                <Link> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </Link>
                <h1
                  className="hero__title fade-in-up"
                  style={{ marginTop: "1.8rem", marginBottom: "2.2rem" }}
                >
                  {siteConfig.title}
                </h1>
              </div>
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

              <div className="tw-flex tw-flex-wrap tw-gap-4">
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
                  // className="dropdown-button"
                  menu={{ items }}
                  placement="bottomLeft"
                  trigger={["click"]}
                  // style={{
                  //   padding: "1.3rem",
                  //   color: "var(--ifm-color-primary)",
                  //   borderColor: "var(--ifm-color-primary)",
                  //   fontWeight: 600,
                  //   fontSize: "1.0rem",
                  // }}
                >
                  <button
                    // className="refine-button refine-button--secondary"
                    className="refine-button2"
                    // style={{
                    //   // width: "20%",
                    //   padding: "1.3rem",
                    //   color: "var(--ifm-color-primary)",
                    //   borderColor: "var(--ifm-color-primary)",
                    //   fontWeight: 600,
                    //   border: "none",
                    //   borderRadius: "10px",
                    //   // padding: 0.3rem 1rem;
                    //   // text-decoration: none;
                    //   // align-items: center;
                    //   // gap: 0.5rem;
                    //   transition: "all 0.3s ease";
                    //   // box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
                    // }}
                  >
                    <span>
                      <Translate>Installtion</Translate>
                    </span>
                    {/* <DownOutlined
                      style={{
                        color: "var(--ifm-color-primary)",
                      }}
                    /> */}
                    {/* &nbsp; */}
                    {/* </a> */}
                    {/* <FaHome /> */}
                    {/* <MdHome /> */}
                    <AiOutlineDown />
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
