import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Feature from "@site/src/components/Home/Features/feature";

export default function Resourses() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div
      className="hero"
      // style={{ marginTop: "-0vh" }}
    >
      <div
        // className="container-features"
        className="tw-container tw-mx-auto tw-px-14"
        style={{ width: "100%" }}
      >
        {/* paddingTop: "0vh", */}
        {/* <hr
          style={{
            marginTop: "2.8vh",
            marginBottom: "3vh",
            paddingLeft: "18vw",
            paddingRight: "18vw",
          }}
        /> */}
        <h1 className="text-center">
          <Translate>Resourses</Translate>
        </h1>

        <p>
          <Translate>Let's build and use the </Translate>
          <a href="https://www.simpowater.org/resource">
            <Translate>Paper Resource</Translate>
          </a>{" "}
          <Translate>together.</Translate>
        </p>

        <Feature
          reverse={true}
          width="80%"
          imgUrl={siteConfig.customFields?.imgUrlResource as string}
          title={
            <Translate id="home.collaboration">Everyone is welcome</Translate>
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
                    <Translate>Paper Resource</Translate>
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
