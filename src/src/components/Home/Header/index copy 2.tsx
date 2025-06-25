import React from "react";
import clsx from "clsx";
// import styles from './styles.module.css';
import Link from "@docusaurus/Link";
import ThemedImage from "@theme/ThemedImage";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Translate, { translate } from "@docusaurus/Translate";
import type { MenuProps } from "antd";
import { Button, Dropdown, Tooltip, Space } from "antd";
import { DownOutlined, UserOutlined } from "@ant-design/icons";

export default function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  const items: MenuProps["items"] = [
    {
      key: "1",
      label: (
        <a
          href={siteConfig.customFields.urlDownloadClientWindows as string}
          style={{ textDecoration: "none" }}
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
          style={{ textDecoration: "none" }}
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
          style={{ cursor: "default", color: "gray", textDecoration: "none" }}
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
              style={{ textDecoration: "none" }}
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
              style={{ textDecoration: "none" }}
            >
              Ubuntu &nbsp;&nbsp;
            </a>
          ),
        },
      ],
      label: "Netdisk",
    },
  ];

  return (
    <header className={clsx("hero noise-bg")}>
      {/* <div className="col col--1 text-center" style={{marginRight: '-2.2vw'}}>
      </div> */}
      {/* <div className="col col--1 text-center" style={{marginRight: '1.5vw'}}>
      </div> */}
      <div
        className="col col--1 text-center"
        // style={{ marginRight: "1.2vw" }}
        style={{ marginRight: "5.5vw" }}
      ></div>

      <div className="col col--5 text-center">
        {/* banner */}
        <div className="container">
          <div
            className="row"
            style={{
              marginTop: "-5.5vh",
              marginBottom: "2.0vh",
              color: "#eee",
            }}
          >
            {/* <img src="/img/SIMPO_logo.png" width='15%'/> */}

            <h1
              style={{ marginBottom: "0vh", color: "#eee" }}
              className="hero__title"
            >
              {siteConfig.title}
            </h1>

            {/* </font> */}
            {/* <h1 className="mb-6 font-jakarta text-4xl font-bold lg:text-6xl">
              Build with Dyte
            </h1>
            <p className="text-sm text-text-400 lg:max-w-lg lg:text-base">
              At Dyte, we&apos;re building the future of real-time communication.
              Integrate high-quality, programmable, and customizable live video
              and voice into your web, mobile, and desktop applications with just
              a few lines of code.
            </p> */}
          </div>

          <div className="row" style={{ marginTop: "0vh", color: "#eee" }}>
            <p
              style={{
                marginRight: "10vw",
                marginTop: "1.8vh",
                marginBottom: "1.8vh",
                color: "#eee",
              }}
              className="hero__subtitle"
            >
              <Translate id="tagline">
                {/* {siteConfig.tagline} */}A Scientific Computing SaaS Platform
                for Water and Wastewater Treatment Process Modelling
                {/* A next-generation platform aimed at simplifying and promoting wastewater treatment modelling */}
              </Translate>
              {/* {siteConfig.customFields.superman} */}
            </p>
          </div>

          {/* <div className="row" style={{ marginTop: "0vh", color: "#eee" }}> */}
          {/* <p style={{ color: "#eee" }} className=""> */}
          {/* {siteConfig.title}{" "} */}
          {/* <Translate> */}
          {/* A Scientific Computing SaaS Platform for Water and Wastewater */}
          {/* Treatment Process Modelling. */}
          {/* SIMPO bridges the gap between advanced modelling capabilities
                and actual availability. It enables users to handle the
                complexity of modern models, whether based on legacy ASM
                frameworks or other cutting-edge expansions, through intuitive
                drag-and-drop interfaces, adaptive algorithms, and collaborative
                tools. */}
          {/* combines user-friendliness with power and flexibility, it
                is an open-minded modern cloud-based platform for water and
                wastewater treatment process modeling. */}
          {/* </Translate>{" "} */}
          {/* {siteConfig.title}{" "} */}
          {/* <Translate> */}
          {/* aims to lower the learning and research barriers for modelling,
                improve development efficiency, provide scientific algorithms
                and evaluation methods, and ultimately achieve a sustainable
                intelligent big data platform for co-creation, sharing and
                providing Open Educational Resources (OER) for all. */}
          {/* </Translate> */}
          {/* </p> */}
          {/* </div> */}
        </div>

        {/* bottom */}

        <div className="" style={{ marginTop: "1.5vh" }}>
          {/* <Link href="docs" className="button button--secondary"> */}
          {/* <Translate>Quick Start</Translate> */}
          {/* Get Started */}
          {/* </Link> */}
          {/* <Link href="docs" className="refine-button">
            <strong>
              <Translate>Quick Start</Translate>
            </strong>
          </Link>
          <Link> &nbsp; </Link> */}
          {/* <Link
            href="/getting-started"
            className="button button--secondary rounded-sm border border-solid border-primary bg-primary/10 px-12 py-2.5 text-center font-semibold text-primary hover:text-primary dark:border-primary-100 dark:text-primary-100"
          >
            Client
          </Link>
          */}
          <Button
            href="docs"
            className="refine-button"
            // type="primary"
            size="large"
            style={{
              padding: "1.4rem",
            }}
          >
            <strong
              style={{
                fontSize: "1.0rem",
              }}
            >
              <Translate>Quick Start</Translate>
            </strong>
          </Button>
          <Link> &nbsp; &nbsp; </Link>

          <Dropdown
            // className="dropdown-content"
            menu={{ items }}
            placement="bottomLeft"
            trigger={["click"]}
          >
            <Button
              className="refine-button"
              size="large"
              style={{
                width: "15%",
                padding: "1.4rem",
              }}
            >
              {/* <a onClick={(e) => e.preventDefault()}> */}
              {/* &nbsp; */}
              {/* <Space> */}
              <span
                style={{
                  fontSize: "1.0rem",
                }}
              >
                <Translate>Client</Translate>
              </span>
              {/* </Space> */}
              {/* → */}
              {/* ▼ */}
              {/* &nbsp; */}
              <DownOutlined />
              {/* &nbsp; */}
              {/* </a> */}
            </Button>
          </Dropdown>

          {/* <div className="dropdown">
            <button className="dropbtn">
              <Translate>Client</Translate> &nbsp; →
              <div className="dropdown-content">
                <a
                  href={
                    siteConfig.customFields.urlDownloadClientWindows as string
                  }
                  download
                >
                  Windows
                </a>
                <a
                  href={
                    siteConfig.customFields.urlDownloalClientUbuntu as string
                  }
                  download
                >
                  Ubuntu
                </a>
                <a
                  href={siteConfig.customFields.urlDownloalNetdisk as string}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Windows/Ubuntu (Netdisk)
                </a>

                <a href="#" style={{ cursor: "default", color: "gray" }}>
                  Mac (pending...)
                </a>
              </div>
            </button>
          </div> */}
        </div>
      </div>

      <div
        className="col hero-image"
        style={{ marginRight: "0vw", marginLeft: "-2.5vw", marginTop: "-2vh" }}
      >
        {/* 手机端将隐藏 */}
        {/* <div className="col hero-image" style={{marginRight: '-10vw'}}> */}
        <ThemedImage
          sources={{
            // light: '/img/banner3.png',
            // dark: '/img/hero-dark.png',
            // dark: '/img/banner3.png',
            // light: 'https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/banner/banner3.png',
            // dark: 'https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/banner/banner3.png',
            light: siteConfig.customFields.imgUrlBanner as string,
            dark: siteConfig.customFields.imgUrlBanner as string,
          }}
          alt="Preview of using SIMPO"
          width="75%"
          // width="70%"
        />
        {/* width='60%' */}
      </div>

      {/* <div className="col  text-center" style={{ backgroundColor: 'white', marginTop: '10vw'}}>1      </div> */}
    </header>
  );
}
