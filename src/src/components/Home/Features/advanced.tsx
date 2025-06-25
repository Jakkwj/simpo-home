import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Feature from "./feature";

export default function Advanced() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div style={{ marginTop: "0vh", paddingTop: "1vh" }}>
      <Feature
        reverse={false}
        width="100%"
        imgUrl={siteConfig.customFields.imgUrlFeature_4 as string}
        title={
          <Translate>
            Advanced evaluation algorithms bring comprehensive and systematic
            understanding of models:
          </Translate>
        }
        description={
          <>
            <ul>
              <li>
                <Translate>
                  Sensitivity analysis identifies sensitive parameters and their
                  correlations, reducing the number of parameters to enhance
                  computational efficiency.
                </Translate>
              </li>

              <li>
                <Translate>
                  Uncertainty assessment evaluates the uncertainty of each
                  parameter, determines the predicted range of model outputs,
                  and refines parameter ranges for more accurate simulations.
                </Translate>
              </li>

              <li>
                <Translate>
                  Parameter estimation identifies the local optima of parameters
                  that best fit the measured data, ensuring robust and reliable
                  model calibration.
                </Translate>
              </li>
            </ul>
          </>
        }
      />
    </div>
  );
}
