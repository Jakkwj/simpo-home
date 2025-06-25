import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Feature from "./feature";

export default function Collaboration() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div style={{ marginTop: "0vh", paddingTop: "1vh" }}>
      <Feature
        reverse={false}
        width="100%"
        imgUrl={siteConfig.customFields.imgUrlFeature_5 as string}
        title={
          <Translate>
            Collaborative science facilitates the dissemination, exchange, and
            development of models:
          </Translate>
        }
        description={
          <>
            <ul>
              <li>
                <Translate>
                  SIMPO supports version-controlled models, data and results
                  sharing, provides public/private repositories, and advocates a
                  new type of peer review workflow for modelling papers, in line
                  with the principles of open science.
                </Translate>
              </li>
            </ul>
          </>
        }
      />
    </div>
  );
}
