import React from "react";
import Translate from "@docusaurus/Translate";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
// import Feature from '@site/src/components/Home/Features/feature';
import Feature from "./feature";

export default function AboutLiangzhensheng() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <div style={{ marginTop: "-4vh", marginBottom: "4vh" }}>
      <div className="container">
        <Feature
          reverse={true}
          width="70%"
          marginTop="0vh"
          imgUrl={siteConfig.customFields.imgUrlLiangzhensheng}
          title={
            <Translate id="about.liangzhensheng">Zhensheng Liang</Translate>
          }
          description={
            <>
              <p>
                <Translate>
                  {
                    "Ph.D. in Environmental Chemistry, Guangdong University of Education. Email: "
                  }
                </Translate>
                <a href="mailto: liangzhensheng@gdei.edu.cn">
                  liangzhensheng@gdei.edu.cn
                </a>
                <Translate>.</Translate>
              </p>
            </>
          }
        />
      </div>
    </div>
  );
}
