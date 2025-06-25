import React from "react";
import clsx from "clsx";
// import styles from './styles.module.css';
import Link from "@docusaurus/Link";
import ThemedImage from "@theme/ThemedImage";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Translate, { translate } from "@docusaurus/Translate";
import type { MenuProps } from "antd";
import { Button, Dropdown, Space } from "antd";

// const {siteConfig} = useDocusaurusContext();
const items: MenuProps["items"] = [
  {
    key: "1",
    label: (
      <a
        target="_blank"
        rel="noopener noreferrer"
        href="https://www.antgroup.com"
      >
        1st menu item
      </a>
    ),
  },
  {
    key: "2",
    label: (
      <a
        target="_blank"
        rel="noopener noreferrer"
        href="https://www.aliyun.com"
      >
        2nd menu item
      </a>
    ),
  },
  {
    key: "3",
    label: (
      <a
        target="_blank"
        rel="noopener noreferrer"
        href="https://www.luohanacademy.com"
      >
        3rd menu item
      </a>
    ),
  },
];

export default function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={clsx("hero noise-bg")}>
      {/* <div className="col col--1 text-center" style={{marginRight: '-2.2vw'}}>
      </div> */}
      {/* <div className="col col--1 text-center" style={{marginRight: '1.5vw'}}>
      </div> */}
      <div
        className="col col--1 text-center"
        style={{ marginRight: "1.2vw" }}
      ></div>

      <div className="col col--6 text-center">
        {/* banner */}
        <div className="container">
          <div className="row" style={{ marginTop: "-1.5vh", color: "#eee" }}>
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
                marginBottom: "0.8vh",
                color: "#eee",
              }}
              className="hero__subtitle"
            >
              <Translate id="tagline">
                {/* {siteConfig.tagline} */}A Scientific Computing SaaS Platform
                for Water and Wastewater Treatment Process Modeling
              </Translate>
              {/* {siteConfig.customFields.superman} */}
            </p>
          </div>

          <div className="row" style={{ marginTop: "0vh", color: "#eee" }}>
            <p style={{ color: "#eee" }} className="">
              {siteConfig.title}{" "}
              <Translate>
                combines user-friendliness with power and flexibility, it is an
                open-minded modern cloud-based platform for water and wastewater
                treatment process modeling.
              </Translate>{" "}
              {siteConfig.title}{" "}
              <Translate>
                aims to lower the learning and research barriers for modelling,
                improve development efficiency, provide scientific algorithms
                and evaluation methods, and ultimately achieve a sustainable
                intelligent big data platform for co-creation, sharing and
                providing Open Educational Resources (OER) for all.
              </Translate>
            </p>
          </div>
        </div>

        {/* bottom */}

        <div className="" style={{ marginTop: "1vh" }}>
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
          >
            <strong>
              <Translate>Quick Start</Translate>
            </strong>
          </Button>
          <Link> &nbsp; </Link>

          <Dropdown
            // className="refine-button"
            menu={{ items }}
            placement="bottomLeft"
          >
            <Button className="refine-button" size="large">
              <Translate>Client</Translate> &nbsp; →
            </Button>
          </Dropdown>

          {/* <Link */}
          <div className="dropdown">
            <button
              // href="/getting-started"
              // className="button button--secondary dropdown"
              // className="refine-button dropdown"
              className="dropbtn"
              // onclick="myFunction()"
            >
              {/* <div className="dropdown"> */}
              {/* <button class="dropbtn">Dropdown</button> */}
              {/* <Translate>Client</Translate> &nbsp; &gt; → */}
              <Translate>Client</Translate> &nbsp; →{/* ▼ */}
              {/* <div class="dropdown-content"> */}
              {/* <div className="dropdown-content"> */}
              <div className="dropdown-content">
                {/* <a href="/client/sludge_client_setup_0.2.0.exe" download>Windows</a>
              <a href="/client/sludge_client_setup_0.2.0.sh" download>Ubuntu</a> */}

                {/* <a href="https://sludge.readthedocs.io/en/latest/_downloads/49e51d71c1843e69a4bcf2ab74ddf3b1/sludge_client_setup.exe" download>Windows</a> */}
                {/* <a href="https://sludge.readthedocs.io/en/latest/_downloads/defdf270ddacd4bb59b05d72e2c5ed66/sludge_client_setup.sh" download>Ubuntu</a> */}

                {/* <a href="https://sludge.readthedocs.io/en/latest/_downloads/23620dc7572483958d72baa3ecbf35aa/SimpoClient_installer_0.2.1.sh" download>Ubuntu</a> */}
                {/* <a href="https://sludge.readthedocs.io/en/latest/_downloads/0ee7356b0a3ca65e90da9de1aa9f60f7/SimpoClient_installer_0.2.1.exe" download>Windows</a>
              <a href="https://sludge.readthedocs.io/en/latest/_downloads/79be8a991d9deced657e2678f6c9bf3a/SimpoClient_installer_0.2.2.sh" download>Ubuntu</a> */}
                <a
                  href={
                    siteConfig.customFields.urlDownloadClientWindows as string
                  }
                  download
                >
                  Windows
                </a>
                {/* <hr /> */}
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
                  {/* Windows/Ubuntu (Netdisk) */}
                  Netdisk
                </a>

                {/* <a href="#" style={{pointerEvents: 'none', cursor: 'default', color: 'gray'}} >Mac (pending...)</a> */}
                <a href="#" style={{ cursor: "default", color: "gray" }}>
                  Mac (pending...)
                </a>
              </div>
            </button>
          </div>
          {/* </Link> */}
        </div>
      </div>

      <div className="col hero-image" style={{ marginRight: "0vw" }}>
        {/* 手机端将隐藏 */}
        {/* <div className="col hero-image" style={{marginRight: '-10vw'}}> */}
        <ThemedImage
          sources={{
            // light: '/img/banner3.png',
            // dark: '/img/hero-dark.png',
            // dark: '/img/banner3.png',
            // light: 'https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/banner/banner3.png',
            // dark: 'https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/banner/banner3.png',
            light: siteConfig.customFields.imgUrlBanner,
            dark: siteConfig.customFields.imgUrlBanner,
          }}
          alt="Preview of using SIMPO"
          width="75%"
        />
        {/* width='60%' */}
      </div>

      {/* <div className="col  text-center" style={{ backgroundColor: 'white', marginTop: '10vw'}}>1      </div> */}
    </header>
  );
}
