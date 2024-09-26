import React from 'react';
// import clsx from 'clsx';
import Translate from '@docusaurus/Translate'
// import styles from './index.module.css';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Link from '@docusaurus/Link';
// import useBaseUrl from '@docusaurus/useBaseUrl'
// import ThemedImage from '@theme/ThemedImage';
import Feature from './feature';


// function Feature({ imgUrl, title, description, reverse }) {
//   return (
//     <div className={clsx('row', styles.feature, reverse && styles.featureReverse)}>
//       <div className="col col--6 text--center">
//         {/* <img className={styles.featureImage} src={useBaseUrl(imgUrl)} alt={title}/> */}
//         <img  src={useBaseUrl(imgUrl)} alt={title}/>
//         {/* width={'80%'} */}
//       </div>
//       <div className={clsx('col col--6', styles.featureContent)}>
//         <div>
//           <h3>{title}</h3>
//           <div>{description}</div>
//         </div>
//       </div>
//     </div>
//   )
// }

export default function FeaturesEasyToUse() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <div className="hero" style={{marginTop: '0vh'}}>
      <div className="container" >
        <Feature
          // imgUrl="img/Xu2.jpg"
          // reverse={true}
          reverse={false}
          width='90%'
          // imgUrl="img/Xu.png"
          // imgUrl="img/gif/import_biomodel.gif"
          // imgUrl="https://sludge.readthedocs.io/en/latest/_images/TheEasiestWay.gif"
          // https://github.com/Jakkwj/simpo_resource/blob/master/simpo_resource/source/_static/images/quick_start/TheEasiestWay/TheEasiestWay.gif
          // imgUrl="https://cdn.jsdelivr.net/gh/Jakkwj/simpo_resource@master/simpo_resource/source/_static/images/quick_start/TheEasiestWay/TheEasiestWay.gif"

          imgUrl={siteConfig.customFields.imgUrlTheEasiestWay}
          title={<Translate id="home.easytouse">Easy to Use</Translate>}
          description={
            <>
              <p>

              {/* {siteConfig.title} */}
                <Translate
                  id="home.easytouse.1"
                  // values={{
                  //   minikube: <Link to="https://minikube.sigs.k8s.io/">minikube</Link>,
                  //   kind: <Link to="https://kind.sigs.k8s.io/">kind</Link>,
                  // }}
                >
                  { `Lets you focus on your model deducing and experimental datas, we\'ll do the computing:` }


                </Translate>
              </p>
              <ul>
                <li>
                  {/* Ability to perform chaos experiments in production environments without modifying the deployment */}
                  {/* logic of the application. */}
                  {/* Provides a convenient way to simulate and evaluate the modles and datas, at most 3 xlsx files and you are good to go. */}
                  {/* Ability to perform simulation and evaluation without programing. */}
                  {/* After installing the calculaiton client, you can just build a calculaiton by created, cloned or imported (at most 3) xlsx files. */}

                  {/* To facilitate the study, research and development of wastewater treatment mathematical modelling, HydroSim platform provides various calculation engines for simulation, sensitivity analysis, uncertainty analysis and parameter estimation. */}
                  {/* can be import directly */}
                  <Translate
                    id="home.easytouse.2"
                  >
                    Through the user-friendly front-end interface, model building can be done quickly without any programming.
                  </Translate>
                </li>

                <li>
                  {/* The input way of a model matrix is in the same manner as the ASMs' model matrix, allowing one to create a model matrix quickly without extra learning. */}


                  {/* The 3 essential elements of SIMPO are: BioModel (model), DataSet (data) and Project (solution), which makes
                  SIMPO is highly composable: one can arbitrary combine the modles and datas only if the model&apos;s components are the same as the data&apos;s targets. */}
                  <Translate
                    id="home.easytouse.3"
                  >
                    The input of models and data can be accomplished through: 1) importing xlsx files, 2) copying public models/data, or 3) creating new ones directly.

                  </Translate>
                </li>

                <li>
                {/* according to the input data, then users can edit and modify the data directly on the diagram. After inputting the model and data, simulation and evaluation can be started in just a few clicks. The platform will automatically draw a series of graphs of the calculation results according to the calculation engine, users can also export the result data for further processing. */}

                {/* The 3 essential elements of SIMPO are: BioModel (model), DataSet (data) and Project (solution), which makes
                SIMPO is highly composable: one can arbitrary combine the modles and datas only if the model&apos;s components are the same as the data&apos;s targets. */}
                {siteConfig.title}
                  <Translate
                    id="home.easytouse.4"
                  >
                    { ` will automatically generate a process flow diagram and a series of graphs of the calculation results, users can export the result data for further processing.` }



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
