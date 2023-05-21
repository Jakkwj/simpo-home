import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Feature from '@site/src/components/Home/Features/feature';
import Feature from './feature';


export default function AboutWuKe() {
  const {siteConfig} = useDocusaurusContext();
  return (


    // className="hero"
    <div
      style={{marginTop: '-6vh', marginBottom: '0vh'}}
      // style={{background: '#3b3b62', color: '#eee'}}
      // style={{background: 'linear-gradient(to right, #5e72e4, #3b3b62)', color: '#eee'}}
    >

      <div className="container" >


        <Feature
          reverse={true}
          width='70%'
          marginTop='0vh'
          imgUrl="img/about/team/logo3.png"
          title={<Translate id="about.wuke">Ke Wu</Translate>}
          description={
            <>
              <p>
                <Translate
                >
                  {/* { `${siteConfig.title} provides various calculation engines and functions:` } */}
                  { 'Ph.D. in Environmental Engineering from Sun Yat-sen University, focusing on standard research, business intelligence and enterprise information system development.' }
                </Translate>
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
