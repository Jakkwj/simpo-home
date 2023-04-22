import React from 'react';
import clsx from 'clsx';
// import styles from './styles.module.css';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Link from '@docusaurus/Link';
import ThemedImage from '@theme/ThemedImage';


export default function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    // <header className={clsx('hero hero--primary', styles.heroBanner)}>
    <header className={clsx('hero noise-bg')}>
    {/* // <header className="row noise-bg"> */}
    {/* <div className="row noise-bg"> */}

      <div className="col col--1 text-center"></div>

      <div className="col col--6 text-center">

        {/* banner */}
        <div className="container">

          <div className="row" style={{marginTop: '-1vh', color: '#eee'}}>
            {/* <img src="/img/SIMPO_logo.png" width='15%'/> */}
            <h1 style={{marginBottom: '0vh', color: '#eee'}} className="hero__title">{siteConfig.title}</h1>

            <p style={{marginRight: '4vw', marginBottom: '0.8vh', color: '#eee'}} className="hero__subtitle">
              {siteConfig.tagline}
            </p>

            {/* {siteConfig.title} focuses on simulating biochemical processes. Only 3 excel files and you are good to go. */}
            {/* <font color='white'> */}
            <p style={{color: '#eee'}} className="">
              {/* {siteConfig.title} is a simulation platform online for water and wastewater treatment process modeling. */}
              {/* {siteConfig.title} is a cloud computing platform that uses software as a service (SaaS) */}
              {/* to ease mechanistic learning and model development. */}
              {/* {siteConfig.title} offers a user-friendly experience without compromising power and flexibility, making it a modern, cloud-based platform for information-sharing and co-creation. */}
              {siteConfig.title} combines user-friendliness with power and flexibility, it is an open-minded modern cloud-based platform for water and wastewater treatment process modeling. {siteConfig.title} aims to lower the learning and research barriers for modelling, improve development efficiency, provide scientific algorithms and evaluation methods, and ultimately achieve a sustainable intelligent big data platform for co-creation, sharing and providing Open Educational Resources (OER) for all.

              {/* Its aim is to create a lower threshold for study and research of modelling, enhance development efficiency, provide scientific evaluation algorithm for models, and ultimately achieve an intelligent big data platform. */}

              {/* Additionally, this platform provides Open Educational Resources (OER) to all researchers and students, particularly in areas with scarce educational resources, such as third-world countries. This endeavor aligns with the United Nations&apos; Sustainable Development Goal 4: Quality  Education. */}

              {/* SaaS computing platform for calculating the matrix like biochemical models (such as activated sludge models 1, 2 and 3). The aim of {siteConfig.title} is to help people to build and calculate their own model easily. */}

              {/* Lets build model together. */}
              {/* The input of the whole process are only 3 excel xlsx files. By this way, you can check and make your own biological model conveniently. */}
            </p>
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

        </div>

        {/* <Link
          className="button button--secondary button--xl"
          to="/docs/intro"
        //  className="dev-portal-signup dev-portal-link"
        >
          Client123
        </Link> */}

        {/* bottom */}
        <div className="" style={{marginTop: '1vh'}}>
          <Link
            href="docs/qucik_start"
            className="button button--secondary"
          >
            Quick Start
            {/* Get Started */}
          </Link>
          <Link> &nbsp; </Link>
          {/* <Link
            href="/getting-started"
            className="button button--secondary rounded-sm border border-solid border-primary bg-primary/10 px-12 py-2.5 text-center font-semibold text-primary hover:text-primary dark:border-primary-100 dark:text-primary-100"
          >
            Client
          </Link>
          */}
          <Link
              // href="/getting-started"
              className="button button--secondary dropdown"
              // onclick="myFunction()"
            >
          {/* <div className="dropdown"> */}
            {/* <button class="dropbtn">Dropdown</button> */}
            Client &nbsp; &gt;
            {/* ▼ */}

            {/* <div class="dropdown-content"> */}
            <div className="dropdown-content">
              <a href="/client/sludge_client_setup_0.2.0.exe" download>Windows</a>
              <a href="/client/sludge_client_setup_0.2.0.sh" download>Ubuntu</a>
              {/* <a href="#" style={{pointerEvents: 'none', cursor: 'default', color: 'gray'}} >Mac (pending...)</a> */}
              <a href="#" style={{cursor: 'default', color: 'gray'}} >Mac (pending...)</a>
            </div>

          {/* </div> */}
          </Link>
        </div>


      </div>

      <div className="col">
      {/* <img src="/img/Xu2.jpg" width='55%'/> */}
      <ThemedImage
          sources={{
            // light: '/img/hero-light.png',
            // light: '/img/banner.png',
            // light: 'img/gif/import_biomodel.gif',
            light: '/img/banner2.png',
            dark: '/img/hero-dark.png',
          }}
          alt="Preview of using SIMPO"
          // width='55%'
          width='60%'
          // className="max-w-[420px] lg:max-w-[560px]"
        />
      </div>

      {/* <div className="col col--4">
      3
      </div> */}

    {/* </div> */}
    </header>
  );
}
