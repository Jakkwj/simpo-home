import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Feature from '@site/src/components/Home/Features/feature';
import Feature from './feature';


export default function AboutHuangzhaowei() {
  const {siteConfig} = useDocusaurusContext();
  return (


    <div
      style={{marginTop: '3vh', marginBottom: '0vh'}}
    >

      <div className="container" >



        <Feature
          reverse={true}
          width='70%'
          marginTop='0vh'
          imgUrl={siteConfig.customFields.imgUrlHuangzhaowei}
          title={<Translate id="about.huangzhaowei">Zhaowei Huang</Translate>}
          description={
            <>
              <p>
                <Translate
                >
                  {/* { 'Master in Environmental and Standardizaiton Engineer. Email: ' } */}
                   { 'Master in Environmental Engineering. Standardizaiton Engineer. Email: ' }

                </Translate>
                <a href="mailto: superjoehuang@163.com">superjoehuang@163.com</a>
                <Translate>.</Translate>
              </p>

            </>
          }
        />
      </div>
    </div>
  );
}
