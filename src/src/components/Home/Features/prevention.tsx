import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Feature from "./feature";

export default function Prevention() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div style={{ marginTop: "0vh", paddingTop: "1vh" }}>
      <Feature
        reverse={false}
        width="100%"
        imgUrl={siteConfig.customFields.imgUrlFeature_3 as string}
        title={
          <Translate>
            Automatic error-proofing and intuitive display help to quickly
            identify errors:
          </Translate>
        }
        description={
          <>
            <ul>
              <li>
                <Translate>
                  Balance checking can help users review the rationality of
                  stoichiometry matrices from a theoretical perspective.
                </Translate>
              </li>

              <li>
                <Translate>
                  NSE intuitively reflects the goodness-of-fit of various
                  variables, and the automated and interactive display of
                  results exposes the problem of certain variables being
                  obscured by graphical scales.
                </Translate>
              </li>
            </ul>
          </>
        }
      />
    </div>
  );
}
