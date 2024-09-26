import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import ThemedImage from '@theme/ThemedImage';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Translate from '@docusaurus/Translate'
import useBaseUrl from '@docusaurus/useBaseUrl'
import Layout from '@theme/Layout';
import HomepageHeader from '@site/src/components/Home/Header';
import AboutJiangFeng from '@site/src/pages/About/jiangfeng';
import AboutWangJun from '@site/src/pages/About/wangjun';

import styles from './index.module.css';


export default function About(): JSX.Element {
  return (
    <Layout
    title={'Contact'}
    description="Contact"
    >

      <main>
        <div
          style={{marginTop: '3vh', marginBottom: '0vh'}}
          // style={{background: '#3b3b62', color: '#eee'}}
          // style={{background: 'linear-gradient(to right, #5e72e4, #3b3b62)', color: '#eee'}}
        >

          {/* <h1 style={{marginTop: '0vh', marginBottom: '-3vh', textAlign: 'center'}} className="hero__title">Contact Us</h1> */}
          <h1 style={{marginTop: '8vh', marginBottom: '-0vh', textAlign: 'center'}} className="hero__title">How Can We Help?</h1>
          <p style={{marginTop: '1vh', marginBottom: '-0vh', textAlign: 'center', fontSize: '105%'}} className="hero__title">Our team here will get back to you in no time.</p>

          <p className="hero__title" style={{marginTop: '2.8vh', marginBottom: '0vh', textAlign: 'center', fontSize: '138%'}}>Academic Cooperation: <a href="mailto: Jiangf58@mail.sysu.edu.cn">Jiangf58@mail.sysu.edu.cn</a></p>
          <p className="hero__title" style={{marginTop: '1vh', marginBottom: '0vh', textAlign: 'center', fontSize: '138%'}}>Technical Support: <a href="mailto: support@simpowater.org">support@simpowater.org</a></p>



          {/* <div className={clsx('row')}>
              <p className={clsx('col col--12 text--center')} style={{marginTop: '5vh', marginBottom: '0vh', textAlign: 'center', fontSize: 'x-large'}}>Email us: Jiangf58@mail.sysu.edu.cn</p>
            </div> */}


         </div>
      </main>

    </Layout>
  );
}
