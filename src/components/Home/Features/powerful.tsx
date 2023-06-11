import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Feature from './feature';


export default function FeaturesPowerful() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <div
      className="hero"
      style={{marginTop: '-10vh'}}
      // style={{background: '#3b3b62', color: '#eee'}}
      // style={{background: 'linear-gradient(to right, #5e72e4, #3b3b62)', color: '#eee'}}
    >
      <div className="container" >
        <Feature
          reverse={true}
          width='100%'
          marginTop='2vh'
          // imgUrl="img/matrix.png"
          // imgUrl="img/Xu.png"
          // imgUrl="https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/main/Xu.png"
          imgUrl={siteConfig.customFields.imgUrlPowerful}
          // imgUrl="img/Fig6.png"
          title={<Translate id="home.powerful">Powerful and Flexible</Translate>}
          description={
            <>
              <p>

              {/* {
                'All the models and datas are easy to share and track.'
              } */}
              {/* {siteConfig.title} */}
                <Translate
                  // id="home.powerful.1"
                  // values={{
                  //   minikube: <Link to="https://minikube.sigs.k8s.io/">minikube</Link>,
                  //   kind: <Link to="https://kind.sigs.k8s.io/">kind</Link>,
                  // }}
                >
                  { `Provides various calculation engines and functions:` }

                </Translate>
              </p>
              <ul>
                <li>
                    <Translate
                      // id="home.powerful.3"
                    >
                      Calculation engines includes: simulation, sensitivity analysis, uncertainty analysis and parameter estimation.
                    </Translate>
                  </li>
                <li>
                  <Translate
                    // id="home.powerful.2"
                  >
                  {/* Modles and datas can be reused and shared to the community. */}
                  {/* The two essential components of HydroSim are BioModel (models) and DataSet (data). These components can be combined in an arbitrary way, which makes HydroSim highly composable. For example, to find out the optimal model for a given dataset, one can easily switch between different models (e.g. ASM1, 2 or 3) for calculations to compare various model structures. And vice verse, one can switch between different datasets for the same model to calculate, making it quickly and easily to evaluate a model's robustness and generalizability. */}

                  { `Models and data can be combined in any way users see fit, so it's very easy to identify the optimal model for a given dataset and evaluate a model's robustness and generalizability.` }



                  </Translate>
                </li>
                <li>
                  <Translate
                    // id="home.powerful.3"
                  >
                  {/* All the algorithms are open source, the modle&apos;s structure and the data authenticity can be tracked effectively. */}
                  Models and data can be released in multiple versions, making it easy to determine the optimal model structure and parameter.
                  </Translate>
                </li>

              </ul>
            </>
          }
        />

      </div>
    </div>
  );
}
