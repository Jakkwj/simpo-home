import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Feature from '@site/src/components/Home/Features/feature';
import Feature from './feature';


export default function AboutJiangFeng() {
  const {siteConfig} = useDocusaurusContext();
  return (


    // className="hero"
    <div
      style={{marginTop: '-4vh', marginBottom: '0vh'}}
      // style={{background: '#3b3b62', color: '#eee'}}
      // style={{background: 'linear-gradient(to right, #5e72e4, #3b3b62)', color: '#eee'}}
    >

      <div className="container" >


        <Feature
          reverse={true}
          width='70%'
          marginTop='0vh'
          // imgUrl="img/about/team/Jakk2b.jpg"
          // imgUrl="https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/about/team/Jakk2b.jpg"
          imgUrl={siteConfig.customFields.imgUrlWangjun}

          title={<Translate id="about.wangjun">Jun Wang</Translate>}
          description={
            <>
              <p>
                <Translate
                >
                  {/* { `${siteConfig.title} provides various calculation engines and functions:` } */}
                  {/* { 'Ph.D. in Environmental Science from Sun Yat-sen University, focusing on wastewater treatment simulation algorithm research.' }
                  { 'Ph.D. in Environmental Science of Sun Yat-sen University, is now a researcher of Guangdong Institute of Standardization, specializing in numerical simulation and algorithm research of wastewater treatment, artificial intelligence and big data, etc. He is the co-founder of SIMO, a cloud computing platform for mathematical modeling of water environment. He has published 4 SCI papers, 1 soft book, 4 standards and 3 patents.' } */}

                  {/* { 'Co-founder of SIMPO. Ph.D. in Environmental Science of Sun Yat-sen University, specializing in numerical simulation and algorithm research of wastewater treatment, artificial intelligence and big data, etc. Published 4 SCI papers, 1 software copyright, 4 standards and 3 patents.' } */}

                  { 'Ph.D. in Environmental Science. Email: ' }


                </Translate>

                <a href="mailto: support@simpowater.org">support@simpowater.org</a>
                <Translate>.</Translate>
              </p>
              {/* <ul>
                <li>
                    <Translate
                    >
                      Calculation engines includes: simulation, sensitivity analysis, uncertainty analysis and parameter estimation.
                    </Translate>
                  </li>
                <li>
                  <Translate
                  >
                  { `Models and data can be combined in any way users see fit, so it's very easy to identify the optimal model for a given dataset and evaluate a model's robustness and generalizability.` }
                  </Translate>
                </li>
                <li>
                  <Translate
                  >
                  Models and data can be released in multiple versions, making it easy to determine the optimal model structure and parameter.
                  </Translate>
                </li>
              </ul> */}
            </>
          }
        />
      </div>
    </div>
  );
}
