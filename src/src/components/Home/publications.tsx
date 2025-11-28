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
          <Translate>Publications</Translate>
        </h1>

        <p>
          <Translate>
            The following papers have adopted SIMPO as their experimental tool.
          </Translate>
        </p>

        <div
          // className="lg:tw-columns-4 sm:tw-columns-1 tw-space-y-6"
          className="lg:tw-columns-3 sm:tw-columns-1 tw-space-y-6"
        >
          <div>
            {/* <img
              src={siteConfig.customFields?.imgUrlResource as string}
              width="100%"
            />

            <p style={{ fontSize: "0.8rem", lineHeight: "1.3" }}>
              <a href="https://doi.org/10.1016/j.wateco.2025.100021">
                SIMPO—A Simplified Intelligent Modelling Platform Online for
                Code-free and Shareable Wastewater Treatment Process Modelling
              </a>
            </p> */}
          </div>

          <div className={className}>
            <img
              src={siteConfig.customFields?.imgUrlPaper_1 as string}
              width="100%"
            />

            {/* <div
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
                <a href="https://doi.org/10.1016/j.wateco.2025.100021">
                  SIMPO—A Simplified Intelligent Modelling Platform Online for
                  Code-free and Shareable Wastewater Treatment Process Modelling
                </a>
              </h3>
            </div> */}

            <p style={{ fontSize: "0.8rem", lineHeight: "1.3" }}>
              {/* <strong> */}
              <a href="https://doi.org/10.1016/j.wateco.2025.100021">
                SIMPO—A Simplified Intelligent Modelling Platform Online for
                Code-free and Shareable Wastewater Treatment Process Modelling
                (W&E 2025)
              </a>
              {/* </strong> */}
              {/* <Translate>
                provides accurate and efficient ODE solvers, negative value
                response strategy to cater to diverse modelling needs. The WNSE
                is employed as the goodness-of-fit criterion for model
                evaluation.
              </Translate> */}
            </p>
          </div>

          {/* <div className={className}>
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
          </div> */}
        </div>
      </div>
    </div>
  );
}
