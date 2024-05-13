import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Feature from './feature';


export default function AboutJiangFeng() {
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
          imgUrl={siteConfig.customFields.imgUrlLihao}
          title={<Translate id="about.lihao">Hao Li</Translate>}
          description={
            <>
              <p>
                <Translate>
                  { 'Ph.D. candidate in Environmental Science. Email: ' }
                </Translate>

                <a href="mailto: lihao97@mail2.sysu.edu.cn">lihao97@mail2.sysu.edu.cn</a>
                <Translate>.</Translate>
              </p>

            </>
          }
        />
      </div>
    </div>
  );
}
