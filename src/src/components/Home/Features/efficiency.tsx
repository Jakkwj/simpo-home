import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Feature from "./feature";

export default function Efficiency() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div style={{ marginTop: "0vh", paddingTop: "1vh" }}>
      <Feature
        reverse={false}
        width="100%"
        imgUrl={siteConfig.customFields.imgUrlFeature_2 as string}
        title={
          <Translate>
            Dynamic algorithm ensures the accuracy and efficiency of modelling:
          </Translate>
        }
        description={
          <>
            <ul>
              <li>
                <strong>SIMPO </strong>
                <Translate>
                  adopts self-adjusting solvers to ensure computational
                  efficiency without affecting accuracy, which is evaluated by
                  weighted Nash Sutcliffe efficiency (WNSE).
                </Translate>
              </li>

              <li>
                <Translate>
                  Dynamic real time step size optimization can alleviate common
                  pitfalls such as negative concentration, which is a frequent
                  problem in traditional tools.
                </Translate>
              </li>
            </ul>
          </>
        }
      />
    </div>
  );
}
