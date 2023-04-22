import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Feature from './feature';


export default function FeaturesTrackable() {
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
          // width='60%'
          marginTop='2vh'
          imgUrl="img/matrix2.png"
          // imgUrl="img/Xu.png"
          // imgUrl="img/tables.jpg"
          // imgUrl="img/Fig4.png"
          // imgUrl="img/Fig5.png"
          // imgUrl="img/Fig6.png"
          title={<Translate id="home.easytouse">Trackable</Translate>}
          description={
            <>
              <p>
                <Translate
                >
                  { `Not way to cheat:` }

                </Translate>
              </p>

              <ul>

                <li>
                  <Translate>
                    All results are calculated according to open-source code, there is no possibility of modifying the calculation results.
                  </Translate>
                </li>

                <li>
                  <Translate>

                    {/* This also provides great convenience to reviewers, */}

                    { `All model submissions can be calculated and published publicly on ${siteConfig.title}, thereby precluding the possibility of algorithmic cheating.` }



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
