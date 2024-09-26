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
      style={{marginTop: '3vh', marginBottom: '0vh'}}
      // style={{background: '#3b3b62', color: '#eee'}}
      // style={{background: 'linear-gradient(to right, #5e72e4, #3b3b62)', color: '#eee'}}
    >

      <div className="container" >

      {/* <h1 style={{marginTop: '0vh', marginBottom: '-3vh', textAlign: 'center'}} className="hero__title">About The Team</h1> */}
      {/* <h1 style={{marginTop: '0vh', marginBottom: '-3vh', textAlign: 'center'}} className="hero__title">About The Team</h1> */}
      {/* <h1 style={{marginTop: '0vh', marginBottom: '-3vh', textAlign: 'left'}} className="hero__title">Development Team</h1> */}


        <Feature
          reverse={true}
          width='70%'
          marginTop='0vh'
          // imgUrl="img/about/team/jiangfeng.jpg"
          // imgUrl="https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/about/team/jiangfeng.jpg"
          imgUrl={siteConfig.customFields.imgUrlJiangfeng}
          title={<Translate id="about.jiangfeng">Feng Jiang</Translate>}
          description={
            <>
              <p>
                <Translate
                >
                  {/* { `${siteConfig.title} provides various calculation engines and functions:` } */}
                  {/* { 'Professor of Sun Yat-Sen University. 江峰教授主要从事市政排水、污水处理、重金属污染与废气污染控制技术的教学科研工作，重点关注环境中含硫物质生物化学转化的科学问题及其应用技术。' } */}
                  {/* { 'Co-founder of SIMPO. Professor of Sun Yat-Sen University. 主要从事市政排水、污水处理、重金属污染与废气污染控制技术的教学科研工作，重点关注环境中含硫物质生物化学转化的科学问题及其应用技术。' } */}

                  {/* { 'Co-founder of SIMPO. Professor of Sun Yat-Sen University. Mainly engaged in teaching and research in municipal drainage, wastewater treatment, heavy metal pollution and waste gas pollution control technology, focusing on scientific issues of biochemical transformation of sulfur-containing substances in the environment and its applied technology.' } */}
                  { 'Professor in the School of Environmental Science and Engineering at Sun Yat-sen University. Email: ' }

                </Translate>
                <a href="mailto: Jiangf58@mail.sysu.edu.cn">Jiangf58@mail.sysu.edu.cn</a>
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
