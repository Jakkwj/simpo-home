import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Feature from "./feature";

export default function Simple() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div style={{ marginTop: "0vh", paddingTop: "1vh" }}>
      <Feature
        reverse={false}
        width="100%"
        imgUrl={siteConfig.customFields.imgUrlTheEasiestWay as string}
        title={
          <Translate>
            Interaction and visualization of GUI provide a user-friendly
            modelling approach:
          </Translate>
        }
        description={
          <>
            <ul>
              <li>
                <Translate>
                  Intuitive tools, such as candidate boxes and color coding,
                  visually assist in correctly inputting variables and
                  parameters in a complex matrix.
                </Translate>
              </li>

              <li>
                <Translate>
                  The drag-and-drop GUI simplifies the design of complex
                  wastewater treatment processes to the point of simply adding
                  and connecting tanks on a webpage.
                </Translate>
              </li>

              <li>
                The automatic drawing display helps users quickly,
                comprehensively, and intuitively understand the simulation and
                evaluation results.
              </li>
            </ul>
          </>
        }
      />
    </div>
  );
}
