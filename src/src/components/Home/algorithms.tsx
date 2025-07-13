import React, { JSX, ReactNode } from "react";
import Translate from "@docusaurus/Translate";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { useLocation } from "@docusaurus/router";
import { isMobile } from "react-device-detect";
import {
  AiFillTablet,
  AiFillFund,
  AiFillSliders,
  AiFillDatabase,
} from "react-icons/ai";

// import Algorithm from "@site/src/components/Home/Algorithms/Algorithm";

type AlgorithmItem = {
  title: string;
  description: JSX.Element;
  icon: string | ReactNode;
  iconColor: string;
  link: string;
};

const AlgorithmList: AlgorithmItem[] = [
  // svg: https://www.svgrepo.com/
  {
    title: "Simulation",
    icon: "💻",
    iconColor: "grey",
    link: "/solution_docs/digital",
    description: (
      <>
        助力企业实现全方位的数字化升级。
        定制化开发数据中台、ERP、CRM等核心系统，
        包括数据采集、处理、分析和可视化的一站式解决方案。
      </>
    ),
  },
  {
    title: "信息系统集成",
    icon: "🌐",
    iconColor: "blue",
    link: "/solution_docs/integration",
    description: (
      <>
        通过API、RPA接口等技术，打破企业信息系统间的数据孤岛，让数据自由流动，实现跨部门无缝协同，流程自动化管理，提高企业效率。
      </>
    ),
  },
  {
    title: "AI解决方案",
    icon: "🤖",
    iconColor: "green",
    link: "/solution_docs/ai",
    description: (
      <>
        结合最新AI技术，为企业提供智能化的业务解决方案，提升运营效率和决策质量。
        显著降低运营成本，大幅提升工作效率，创造更大商业价值。
      </>
    ),
  },
  {
    title: "数据分析与洞察",
    icon: "📈",
    iconColor: "red",
    link: "/solution_docs/bi",
    description: (
      <>
        通过数据分析和可视化技术，化繁为简，帮助企业从数据中发现商业洞察和增长机会。
        精准定位目标客户，数据驱动增长，洞察成就未来。
      </>
    ),
  },
];

function Algorithm({
  title,
  description,
  icon,
  iconColor,
  link,
}: AlgorithmItem) {
  return (
    <div className="refine-card fade-in-up">
      <div className={`refine-card__icon refine-card__icon--${iconColor}`}>
        {icon}
        {/* <DocusaurusSvg className="themedDocusaurus" width="100" height="100"/> */}
        {/* <img id="mySvgImage" src="/img/icons/database-svgrepo-com.svg" alt="My SVG" /> */}
      </div>
      {/* <div className="row"> */}
      {/* <div className="tw-grid tw-grid-cols-2 tmd:tw-grid-cols-2 lg:tw-grid-cols-4"> */}
      {/* <div className="tw-columns-2 tw-sm:tw-columns-6"> */}

      {/* <div className="tw-grid tw-grid-cols-1 sm:tw-grid-cols-2 lg:tw-grid-cols-4">
        <div className="tw-bg-red-500">Item 1</div>
        <div className="tw-bg-green-500">Item 2</div>
        <div className="tw-bg-blue-500">Item 3</div>
        <div className="tw-bg-yellow-500">Item 4</div>
      </div> */}

      <div className="tw-grid md:tw-grid-cols-1 lg:tw-grid-cols-2">
        {/* <div className="tw-grid tw-grid-cols-1"> */}
        {/* <div className="col col--7"> */}
        <div className="">
          <h3>{title}</h3>
        </div>

        {/* <div className="sm:tw-text-left md:tw-text-right">
          <Link
            to={`${link}`}
            className="btn-gradient"
            style={{
              marginTop: "-0.5rem",
              marginRight: "-0.8rem",
            }}
          >
            Learn More
          </Link>
        </div> */}
      </div>
      <p>{description}</p>
    </div>
  );
}

export default function Algorithms() {
  const { siteConfig } = useDocusaurusContext();
  const location = useLocation();
  const hasZh = location.pathname.includes("/zh");
  const className = hasZh
    ? isMobile
      ? "refine-card fade-in-up"
      : "refine-card refine-card-height-zh fade-in-up"
    : isMobile
    ? "refine-card fade-in-up"
    : "refine-card refine-card-height fade-in-up";

  return (
    <div className="hero">
      <div
        className="tw-container tw-mx-auto tw-px-14"
        style={{ width: "100%" }}
      >
        <h1 className="text-center">
          <Translate>Algorithms</Translate>
        </h1>

        <p>
          <strong>SIMPO</strong>
          <Translate>'s core algorithms:</Translate>
        </p>

        <div
          // className="lg:tw-columns-4 sm:tw-columns-1 lg:tw-space-x-4 sm:tw-space-x-18"
          className="lg:tw-columns-4 sm:tw-columns-1 tw-space-y-6"
        >
          {/* {AlgorithmList.map((props, idx) => (
            <Algorithm key={idx} {...props} />
          ))} */}

          <div className={className}>
            <img
              src={siteConfig.customFields.imgUrlAlgorithm_1 as string}
              width="100%"
            />

            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginTop: "0.5rem",
              }}
            >
              <AiFillTablet style={{ fontSize: "16px", color: "#5e72e4" }} />
              <Link> &nbsp;&nbsp; </Link>
              <h3
                className="hero__title fade-in-up"
                style={{ marginTop: "0.8rem" }}
              >
                <Translate>Simulation</Translate>
              </h3>
            </div>

            <p>
              <strong>SIMPO </strong>
              <Translate>
                provides accurate and efficient ODE solvers, negative value
                response strategy to cater to diverse modelling needs. The WNSE
                is employed as the goodness-of-fit criterion for model
                evaluation.
              </Translate>
            </p>
          </div>

          <div className={className}>
            <img
              src={siteConfig.customFields.imgUrlAlgorithm_2 as string}
              width="100%"
            />

            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginTop: "0.5rem",
              }}
            >
              <AiFillSliders style={{ fontSize: "16px", color: "#087ce8" }} />
              <Link> &nbsp;&nbsp; </Link>
              <h3
                className="hero__title_blue fade-in-up"
                style={{
                  marginTop: "0.8rem",
                }}
              >
                <Translate>Sensitivity</Translate>
              </h3>
            </div>

            <p>
              <Translate>
                Sensitivity analysis identifies the most sensitive parameters
                that have the greatest impact on outcomes, and improve
                computational efficiency by reducing the number of parameters.
              </Translate>
            </p>
          </div>

          <div className={className}>
            <img
              src={siteConfig.customFields.imgUrlAlgorithm_3 as string}
              width="100%"
            />

            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginTop: "0.5rem",
              }}
            >
              <AiFillFund style={{ fontSize: "16px", color: "#62aa57" }} />
              <Link> &nbsp;&nbsp; </Link>
              <h3
                className="hero__title_green fade-in-up"
                style={{ marginTop: "0.8rem" }}
              >
                <Translate>Uncertainty</Translate>
              </h3>
            </div>

            <p>
              <Translate>
                Uncertainty assessment evaluates the uncertainty, distributions
                and equifinality of parameters, determine the predicted range
                distribution of model outputs, and refine the range of parameter
                values.
              </Translate>
            </p>
          </div>

          <div className={className}>
            <img
              src={siteConfig.customFields.imgUrlAlgorithm_4 as string}
              width="100%"
            />

            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginTop: "0.5rem",
              }}
            >
              <AiFillDatabase style={{ fontSize: "16px", color: "#aa5757" }} />
              <Link> &nbsp;&nbsp; </Link>
              <h3
                className="hero__title_red fade-in-up"
                style={{ marginTop: "0.8rem" }}
              >
                <Translate>Estimation</Translate>
              </h3>
            </div>

            <p>
              <Translate>
                Parameter estimation, which is performed using Genetic
                Algorithms (GA), obtains the local optimal solutions of the
                parameters by approximating the maximum value of the WNSE.
              </Translate>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
