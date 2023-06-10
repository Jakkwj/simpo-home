import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Feature from './feature';


export default function FeaturesOpen() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <div className="hero" style={{marginTop: '-6vh'}}>
      <div className="container" >
        <Feature
          // imgUrl="img/Xu2.jpg"
          // reverse={true}
          reverse={false}
          width='90%'
          // imgUrl="img/tables.jpg"
          // imgUrl="img/Fig5.png"
          // imgUrl="img/Fig6.png"
          // imgUrl="https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/main/Fig6.png"
          imgUrl={siteConfig.customFields.imgUrlOpen}
          // imgUrl="img/gif/import_biomodel.gif"
          title={<Translate id="home.easytouse">Open-Minded</Translate>}
          description={
            <>
              <p>
                <Translate
                >
                  { `${siteConfig.title} is an open-minded platform that provides OER for everyone:` }
                </Translate>
              </p>
              <ul>
                <li>
                  <Translate
                  >
                    { `The core source code of ${siteConfig.title} is open-source, and everyone is encouraged to contribute code to co-create algorithms.` }
                  </Translate>
                </li>

                <li>
                  <Translate
                  >
                    {/* HydroSim is an open-source, collaborative cross-platform application that provides OER for all the researchers and students. */}

                    { `${siteConfig.title} works on Windows, Linux, and Mac, it can leverage the power of supercomputers, as their systems are usually Linux-based.` }

                  </Translate>
                </li>

                <li>
                  <Translate
                  >
                    {/* { `${siteConfig.title} works on Windows, Linux, and Mac, it can leverage the power of supercomputers, as their systems are usually Linux-based.` } */}

                    Models, datasets and calculation results can be published in public version to share the research findings to the entire research community.

                  </Translate>
                </li>

                <li>
                  <Translate
                    // id="home.easytouse.3"
                  >

                    {/* { `${siteConfig.title} will automatically generate a process flow diagram and a series of graphs of the calculation results, users can export the result data for further processing.` } */}
                    {/* It works on Windows, Linux and Mac operating systems, which means it can make use of the computing power of supercomputers for model computation if necessary. Models, datasets and calculation project results can be published in public or private mode, making it easy to share the research findings to the entire research community. In addition, the source code of the core algorithms are open-sourced on Github (https://github.com/Jakkwj/sludge), providing transparency and allowing all researchers to scrutinize the correctness and accuracy of the source code. Furthermore, all researchers are encouraged to contribute their own code and to co-create and develop various model algorithms together through the Fork feature of Github. */}

                    { `${siteConfig.title} provides OER to all researchers and students. This endeavor aligns with the United Nations' Sustainable Development Goal 4: Quality Education.` }


                    {/* according to the input data, then users can edit and modify the data directly on the diagram. After inputting the model and data, simulation and evaluation can be started in just a few clicks. The platform will automatically draw a series of graphs of the calculation results according to the calculation engine, users can also export the result data for further processing. */}

                    {/* The 3 essential elements of SIMPO are: BioModel (model), DataSet (data) and Project (solution), which makes
                    SIMPO is highly composable: one can arbitrary combine the modles and datas only if the model&apos;s components are the same as the data&apos;s targets. */}

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
