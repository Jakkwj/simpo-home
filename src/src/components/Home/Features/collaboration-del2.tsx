import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Feature from "./feature";

export default function FeaturesOpen() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div className="hero" style={{ marginTop: "-8vh" }}>
      <div className="container" style={{ width: "80%" }}>
        {/* paddingTop: "0vh", */}
        {/* <hr
          style={{
            marginTop: "2.8vh",
            marginBottom: "3vh",
            paddingLeft: "18vw",
            paddingRight: "18vw",
          }}
        /> */}
        <h1 className="text-center">Collaboration</h1>
        <Feature
          reverse={true}
          width="80%"
          imgUrl={siteConfig.customFields.imgUrlResource as string}
          title={
            <Translate id="home.collaboration">
              Collaboration is welcome
            </Translate>
          }
          description={
            <>
              {/* <p>
                <Translate
                >
                  { `An open-minded platform that provides OER for everyone:` }
                </Translate>
              </p> */}
              <ul>
                <li>
                  <Translate>{`Join us in building and enhancing `}</Translate>

                  <a href="https://www.simpowater.org/resource">
                    Paper Resource
                  </a>

                  <Translate>
                    {` with the help of powerful AI tools. Your contributions can significantly enhance and expand the collection, making it more valuable for the entire community.
                  `}
                  </Translate>
                </li>

                <li>
                  <Translate>
                    {`We appreciate your support and collaboration, fork and pull request are welcome in: `}
                  </Translate>
                  <a href="https://github.com/Jakkwj/simpo-home">simpo-home</a>
                </li>
              </ul>
            </>
          }
        />
      </div>
    </div>
  );
}
