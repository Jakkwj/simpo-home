import React, { useEffect, useRef, useState } from "react";
import Translate from "@docusaurus/Translate";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { useLocation } from "@docusaurus/router";
import { isMobile } from "react-device-detect";
import { LuCheck, LuCopy, LuTriangleAlert } from "react-icons/lu";
import {
  AiFillTablet,
  AiFillFund,
  AiFillSliders,
  AiFillDatabase,
} from "react-icons/ai";
import styles from "./publications.module.css";

const SIMPO_BIBTEX = `@article{WANG2025100021,
  title = {SIMPO – A Simplified Intelligent Modelling Platform Online for Code-free and Shareable Wastewater Treatment Process Modelling},
  journal = {Water & Ecology},
  volume = {1},
  number = {4},
  pages = {100021},
  year = {2025},
  issn = {3050-4724},
  doi = {https://doi.org/10.1016/j.wateco.2025.100021},
  url = {https://www.sciencedirect.com/science/article/pii/S3050472425000231},
  author = {Jun Wang and Hao Li and Zhensheng Liang and Zhaowei Huang and Feng Jiang},
  keywords = {wastewater treatment modelling, simulation platform, sensitivity analysis, uncertainty assessment, parameter estimation},
  abstract = {The expansion of knowledge of and demand for wastewater treatment has driven the increasing complexity of its models. The establishment or use of such complicated models is difficult for environmental engineers, researchers and students, which hinders model development, knowledge transformation, and practical use of the wastewater treatment process. Even for reviewers and readers, it is difficult to evaluate whether a complicated model proposed in an article is reliable without time-consuming coding work. Thus, a new wastewater treatment modelling tool that is easy to use, code free, powerful, and open for sharing is necessary. To simplify wastewater treatment modelling and enhance accessibility, this study developed a Simplified Intelligent Modelling Platform Online for wastewater process modelling (SIMPO, https://www.simpowater.org), an open-source and free-of-charge platform. SIMPO introduces the following innovative features: 1) Intuitive drag-and-drop graphical user interfaces enable code-free modelling. 2) Dynamic adaptive algorithms (forward/improved Euler methods) optimize step size in real time to ensure computational accuracy and efficiency. 3) Balance checking of chemical stoichiometric matrix, automatic visualization of results, and Nash Sutcliffe efficiency (NSE)–based goodness-of-fit evaluation can help researchers identify subtle but impactful errors. 4) Advanced algorithms for sensitivity analysis, uncertainty assessment, and parameter estimation help researchers identify the importance of ranking parameters, understand the transmission of input uncertainty to output, and achieve a balance between parameter estimation time and accuracy in complex scenarios. 5) Open and shareable mathematical models, modification processes and calculation results promote knowledge sharing and exchange. The combination of SIMPO with artificial intelligence (AI) tools helps researchers understand and apply mathematical model papers. Validated against classic modelling tools, such as AQUASIM 2.1 (EAWAG, Zurich, Switzerland), SIMPO achieves consistent accuracy while significantly reducing barriers to its use. The calculation result of a classic case is consistent with AQUASIM and with weighted Nash Sutcliffe efficiency (WNSE) > 0.999. Case studies demonstrate its capability to detect and resolve flaws in published models (eg, stoichiometric matrix imbalances in an extended model of Activated Sludge Model 3 and poor fitting of some variables in an autotrophic denitrification model). By combining powerful algorithms with a user-centric design, SIMPO provides an efficient, reliable and open solution for wastewater treatment modelling, driving innovation and accessibility in environmental engineering research. Currently, the use of large language model (LLM) tools such as KIMI can help users understand water quality modelling more quickly. In the future, application programming interface (API) integration with more AI tools such as DeepSeek would enable the possibility of linking classic mechanism-driven modelling with AI-assisted data-driven modelling.}
}`;

async function copyText(text: string) {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return;
    } catch {
      // Fall back for browsers that expose the API but deny clipboard access.
    }
  }

  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.opacity = "0";
  document.body.appendChild(textArea);
  textArea.select();

  const copied = document.execCommand("copy");
  textArea.remove();

  if (!copied) {
    throw new Error("Unable to copy BibTeX");
  }
}

export default function Algorithms() {
  const { siteConfig } = useDocusaurusContext();
  const location = useLocation();
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "error">(
    "idle",
  );
  const feedbackTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  const hasZh = location.pathname.includes("/zh");
  const className = hasZh
    ? isMobile
      ? "refine-card fade-in-up"
      : "refine-card refine-card-height-zh fade-in-up"
    : isMobile
      ? "refine-card fade-in-up"
      : "refine-card refine-card-height fade-in-up";

  useEffect(
    () => () => {
      if (feedbackTimeout.current) {
        clearTimeout(feedbackTimeout.current);
      }
    },
    [],
  );

  const handleCopyBibtex = async () => {
    if (feedbackTimeout.current) {
      clearTimeout(feedbackTimeout.current);
    }

    try {
      await copyText(SIMPO_BIBTEX);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("error");
    }

    feedbackTimeout.current = setTimeout(() => setCopyStatus("idle"), 1500);
  };

  return (
    <div className="hero">
      <div
        className="tw-container tw-mx-auto tw-px-14"
        style={{ width: "100%" }}
      >
        <h1 className="text-center">
          <Translate>Publications</Translate>
        </h1>
        <p className={styles.citationPrompt}>
          <span>
            <Translate
              id="homepage.publications.citationPrompt"
              values={{ simpo: <strong>SIMPO</strong> }}
            >
              {"Please cite our paper if {simpo} is useful to your work."}
            </Translate>
          </span>
          <button
            type="button"
            className={`${styles.copyButton} ${
              copyStatus === "copied"
                ? styles.copyButtonSuccess
                : copyStatus === "error"
                  ? styles.copyButtonError
                  : ""
            }`}
            onClick={handleCopyBibtex}
          >
            {copyStatus === "copied" ? (
              <LuCheck aria-hidden="true" />
            ) : copyStatus === "error" ? (
              <LuTriangleAlert aria-hidden="true" />
            ) : (
              <LuCopy aria-hidden="true" />
            )}
            <span aria-live="polite">
              {copyStatus === "copied" ? (
                <Translate id="homepage.publications.copied">Copied</Translate>
              ) : copyStatus === "error" ? (
                <Translate id="homepage.publications.copyFailed">
                  Copy failed
                </Translate>
              ) : (
                <Translate id="homepage.publications.copyBibtex">
                  Copy BibTeX
                </Translate>
              )}
            </span>
          </button>
        </p>

        <p>
          <Translate
            id="homepage.publications.adopted"
            values={{ simpo: <strong>SIMPO</strong> }}
          >
            {
              "The following papers have adopted {simpo} as their experimental tool."
            }
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
