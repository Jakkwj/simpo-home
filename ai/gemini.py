import base64
import json
import pathlib
from asyncio import run as asy_run
from os import environ, listdir, mkdir, path
from shutil import move
from traceback import format_exc

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from pathlib2 import Path
from psutil import virtual_memory
from simpo import ic

if virtual_memory().total > 33470000000:
    COMPUTER_PATH = "/media/Data/SynologyDrive/GitHub"  # 家里台式机
else:
    COMPUTER_PATH = "/media/Cloud/SynologyDrive/GitHub"  # 座机

from dotenv import load_dotenv

from add_db_BioModel import main as add_db_BioModel_main
from add_db_paper import main as add_db_paper_main
from prompt import PROMPT_CONTENT, SYSTEM_INSTRUCTION

load_dotenv(".env")
QINGYUN_API_KEY = environ.get("QINGYUN_API_KEY")


def initial_contents_list(pdf_base64: str, prompt_content: str) -> list[dict]:
    """初始化 contents_list, 失败重试的时候需要重置."""
    return [
        {
            "role": "user",
            "parts": [
                {
                    "inline_data": {
                        "mime_type": "application/pdf",
                        "data": pdf_base64,
                    }
                },
                {"text": prompt_content},
            ],
        }
    ]


async def main_one_step(
    pdf_path: str,
    # models: str = "gemini-3-pro-preview-11-2025-thinking",
    # models: str = "gemini-3-pro-preview-11-2025",
    models: str = "gemini-3-pro-preview-thinking",
    # models: str = "gemini-3-pro-preview",
    # models: str = "gemini-2.5-flash",
    # models: str = "gemini-2.5-flash-lite",
    # models: str = "gemini-2.5-flash-lite-nothinking",
) -> dict[str, str] | None:
    """
    向 gemini 发送 pdf 的 bytes 的 base64, 通过提示词提取 BioModel 的 json.
    gemini 要求单个 pdf 不能大于 20 mb.
    只能是 pdf 文件, docx 的公式识别会出问题.
    gemini 有时候会卡, 这里设置 timeout 为 5 min, 总计尝试 5 次, 即最长等待 25 min.

    gemini-3-pro-preview 效果最好, 但是经常卡住, 几乎不用改, 处理时间约 100s, 每次消耗约 $0.1 (0.7元).
    gemini-2.5-flash 效果也不错, 几乎能成功解析, 但是要稍作修改, 处理时间约 60s, 每次消耗约 $0.022 (0.15元).
    gemini-2.5-flash-lite 效果一般, 可接受, 经常不能成功解析, 要去excel修改, 处理时间约 s, 每次消耗约 $0.001 (0.007元).

    一次问完

    使用 青云聚合 API, 模型列表: https://api.qingyuntop.top/pricing

    文档理解:
        https://qingyuntop.apifox.cn/api-368011980
        https://ai.google.dev/gemini-api/docs/document-processing?hl=zh-cn
        Schema: https://ai.google.dev/api/caching?hl=zh-cn#Schema
    """
    headers = {
        "Authorization": f"Bearer {QINGYUN_API_KEY}",
        "Content-Type": "application/json",
    }
    url = f"https://api.qingyuntop.top/v1beta/models/{models}:generateContent?key={QINGYUN_API_KEY}"

    if "gemini-3" in models:  # and "thinking" in models:
        model_contnet_index: int = 1
    else:
        model_contnet_index: int = 0

    pdf_bytes = pathlib.Path(pdf_path).read_bytes()  # encode the PDF byte
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    contents_list = initial_contents_list(pdf_base64, PROMPT_CONTENT)

    payload = (
        json.dumps(  # https://ai.google.dev/api/generate-content?hl=zh-cn#v1beta.GenerationConfig
            {
                "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
                "contents": contents_list,
                "generationConfig": {
                    "temperature": 0,  # 0~2, 0 最稳定, 2 最创造性, 默认为 1
                    # "thinkingConfig": {"includeThoughts": True, "thinkingBudget": 26240},
                    "responseMimeType": "application/json",
                    "responseSchema": {
                        "title": "Result",
                        "type": "object",
                        "required": [
                            "Title",
                            "Year",
                            "Journal",
                            "DOI",
                            "Access",
                            "Authors",
                            "Abstract",
                            "What problem does this paper attempt to solve?",
                            "How the paper solves this problem?",
                            "What experiments were done for the paper?",
                            "What are the points that can be explored further?",
                            "Summarize the main points of the paper.",
                            "What are the relevant studies?",
                            "zh_Abstract",
                            "zh_What problem does this paper attempt to solve?",
                            "zh_How the paper solves this problem?",
                            "zh_What experiments were done for the paper?",
                            "zh_What are the points that can be explored further?",
                            "zh_Summarize the main points of the paper.",
                            "zh_What are the relevant studies?",
                        ],
                        "propertyOrdering": [
                            "Title",
                            "Year",
                            "Journal",
                            "DOI",
                            "Access",
                            "Authors",
                            "Abstract",
                            "What problem does this paper attempt to solve?",
                            "How the paper solves this problem?",
                            "What experiments were done for the paper?",
                            "What are the points that can be explored further?",
                            "Summarize the main points of the paper.",
                            "What are the relevant studies?",
                            "zh_Abstract",
                            "zh_What problem does this paper attempt to solve?",
                            "zh_How the paper solves this problem?",
                            "zh_What experiments were done for the paper?",
                            "zh_What are the points that can be explored further?",
                            "zh_Summarize the main points of the paper.",
                            "zh_What are the relevant studies?",
                        ],
                        "properties": {
                            "Title": {
                                "type": "string",
                            },
                            "Year": {
                                "type": "string",
                            },
                            "Journal": {
                                "type": "string",
                            },
                            "DOI": {
                                "type": "string",
                            },
                            "Access": {
                                "type": "string",
                            },
                            "Authors": {
                                "type": "string",
                            },
                            "Abstract": {
                                "type": "string",
                            },
                            "What problem does this paper attempt to solve?": {
                                "type": "string",
                            },
                            "How the paper solves this problem?": {
                                "type": "string",
                            },
                            "What experiments were done for the paper?": {
                                "type": "string",
                            },
                            "What are the points that can be explored further?": {
                                "type": "string",
                            },
                            "Summarize the main points of the paper.": {
                                "type": "string",
                            },
                            "What are the relevant studies?": {
                                "type": "string",
                            },
                            "zh_Abstract": {
                                "type": "string",
                            },
                            "zh_What problem does this paper attempt to solve?": {
                                "type": "string",
                            },
                            "zh_How the paper solves this problem?": {
                                "type": "string",
                            },
                            "zh_What experiments were done for the paper?": {
                                "type": "string",
                            },
                            "zh_What are the points that can be explored further?": {
                                "type": "string",
                            },
                            "zh_Summarize the main points of the paper.": {
                                "type": "string",
                            },
                            "zh_What are the relevant studies?": {
                                "type": "string",
                            },
                        },
                    },
                },
            }
        )
    )

    response_text_: str = ""
    retry_counter: int = 1
    while True:
        try:
            async with ClientSession(
                timeout=ClientTimeout(total=300)
            ) as session:  # 最长等待 300s 5 min
                async with session.post(url, headers=headers, data=payload) as response:
                    response_text_ = await response.text()

            __ = json.loads(response_text_)
            logger.info(__)
            result = json.loads(
                __["candidates"][0]["content"]["parts"][model_contnet_index]["text"]
            )
            logger.info(result)

            return result

        except Exception:
            exc = str(format_exc())
            if "TimeoutError" not in exc:
                logger.error(exc)
            logger.error(f"Retrying ({retry_counter}/5): {response_text_}")
            if retry_counter >= 5:
                logger.error("Failed, please try again.")
                break
            retry_counter += 1


def mk_target_dir(result: dict[str, str]) -> tuple[str, str]:
    """创建 mdx 所在的目标文件夹"""
    # res_dir = f"{COMPUTER_PATH}/SimpoHome/src/resource"
    target_dir = Path(
        f"{COMPUTER_PATH}/SimpoHome/src/resource/{result['Year']}/{result['Journal']}"
    )
    target_dir.mkdir(parents=True, exist_ok=True)  # 多级新建文件夹

    # res_dir = f"{COMPUTER_PATH}/SimpoHome/src/i18n/zh/docusaurus-plugin-content-docs-resource/current"
    target_dir_zh = Path(
        f"{COMPUTER_PATH}/SimpoHome/src/i18n/zh/docusaurus-plugin-content-docs-resource/current/{result['Year']}/{result['Journal']}"
    )
    target_dir_zh.mkdir(parents=True, exist_ok=True)  # 多级新建文件夹

    return target_dir, target_dir_zh


def get_content(result: dict[str, str], access: str, is_en: bool = True) -> str:
    """根据 is_en 创建中英文内容"""
    return f"""---
        slug: /{result["DOI"]}
        title: {result["Title"].replace(": ", "-")}
        ---

        import config from "@generated/docusaurus.config";
        import Tabs from "@theme/Tabs";
        import TabItem from "@theme/TabItem";

        # [{result["Title"]}](https://doi.org/{result["DOI"]})

        <img style={{{{marginBottom: '0.8rem', marginRight: '0.8rem'}}}} alt="" src="https://img.shields.io/badge/unapproved-red?style=for-the-badge" />


        {{/*
        <img style={{{{marginBottom: '0.8rem', marginRight: '0.8rem'}}}} alt="" src="https://img.shields.io/badge/approved-brightgreen?style=for-the-badge" /> */}}


        {access}

        <div class="theme-admonition theme-admonition-info admonition_node_modules-@docusaurus-theme-classic-lib-theme-Admonition-Layout-styles-module alert alert--info">
          <div class="admonitionContent_node_modules-@docusaurus-theme-classic-lib-theme-Admonition-Layout-styles-module">
                    DOI: [{result["DOI"]}](https://doi.org/{result["DOI"]})

                    {"Authors" if is_en else "作者"}: {result["Authors"]}
          </div>
        </div>


        {{/* ----


        [SIMPO Dashboard](https://dash.simpowater.com/dashboard/biomodels/public/name/{result["DOI"].replace("/", "-")}/id/xxxxxx/did/yyyyyy):

        <iframe
        src="https://dash.simpowater.com/dashboard/biomodels/iframe/public/name/{result["DOI"].replace("/", "-")}/id/xxxxxx/did/yyyyyy"

        width="100%"
        height="400"
        style={{{{ border: 'none', marginBottom: '0.8rem' }}}}
        ></iframe> */}}


        ------

        <Tabs>

        <TabItem value="abstract" label="Abstract" >

        {result["Abstract"] if is_en else result["zh_Abstract"]}

        </TabItem>

        <TabItem value="objective" label="Objective" >

        {"**Q: What problem does this paper attempt to solve?**" if is_en else "**Q：这篇论文试图解决什么问题？**"}

        **Gemini 3.0 Pro:**

        {result["What problem does this paper attempt to solve?"] if is_en else result["zh_What problem does this paper attempt to solve?"]}

        </TabItem >

        <TabItem value="solution" label="Solution" >

        {"**Q: How the paper solves this problem?**" if is_en else "**Q：论文如何解决这个问题？**"}

        **Gemini 3.0 Pro:**

        {result["How the paper solves this problem?"] if is_en else result["zh_How the paper solves this problem?"]}

        </TabItem >

        <TabItem value="experiment" label="Experiment" >

        {"**Q: What experiments were done for the paper?**" if is_en else "**Q：论文做了哪些实验？**"}

        **Gemini 3.0 Pro:**

        {result["What experiments were done for the paper?"] if is_en else result["zh_What experiments were done for the paper?"]}

        </TabItem >

        <TabItem value="exploration" label="Exploration" >

        {"**Q: What are the points that can be explored further?**" if is_en else "**Q：有什么可以进一步探索的点？**"}

        **Gemini 3.0 Pro:**

        {result["What are the points that can be explored further?"] if is_en else result["zh_What are the points that can be explored further?"]}

        </TabItem >

        <TabItem value="summary" label="Summary" >

        {"**Q: Summarize the main points of the paper.**" if is_en else "**Q： 总结一下论文的主要内容。**"}

        **Gemini 3.0 Pro:**

        {result["Summarize the main points of the paper."] if is_en else result["zh_Summarize the main points of the paper."]}

        </TabItem>

        <TabItem value="related" label="Related" >

        {"**Q: What are the relevant studies?**" if is_en else "**Q： 有哪些相关研究？**"}

        **Gemini 3.0 Pro:**

        {result["What are the relevant studies?"] if is_en else result["zh_What are the relevant studies?"]}

        </TabItem >

        </Tabs>

    """.replace("        ", "")


def main(
    pdf_file: str,
    # models: str = "gemini-3-pro-preview",
    models: str = "gemini-3-pro-preview-thinking",
):
    """
    更新 生产环境时, 把更改 litestar.env 中的 ENV = production
    生成 resource 的 mdx 文件.
    并尝试生成 BioModel 写入数据库.

    本地拆解论文时, 可以用更高级的模型
    """

    result = asy_run(main_one_step(f"pdf/{pdf_file}"))
    logger.info(result)

    # result = {
    #     "Title": "Growth, maintenance and product formation of autotrophs in activated sludge: Taking the nitrite-oxidizing bacteria as an example",
    #     "Year": "2008",
    #     "Journal": "Water Research",
    #     "DOI": "10.1016/j.watres.2008.06.024",
    #     "Access": "SUBSCRIPTION",
    #     "Authors": "Bing-Jie Ni, Fang Fang, Wen-Ming Xie, Han-Qing Yu",
    #     "Abstract": "The autotrophs in activated sludge play an important role in biological wastewater treatment, especially in the nitrification process. Compared with the heterotrophs in activated sludge, information about the growth, maintenance, and product formation of the autotrophs is still sparse. In this work both experimental and modeling approaches are used to investigate the growth, nitrite inhibition, maintenance, and formation of extracellular polymeric substances (EPS) and soluble microbial products (SMP) of the autotrophs, with nitrite-oxidizing bacteria (NOB) in activated sludge as an example. The unified theory for EPS and SMP is integrated into our model to describe the microbial product formation of the NOB. Extensive experiments were carried out using the NOB-enriched in a sequencing batch reactor for the calibration and validation of the developed model. Results show that the NOB spend a considerable amount of energy on maintenance processes. Their apparent growth yield is estimated to be 0.044 mg COD biomass mg⁻¹ N. The model simulations reveal that the concentrations of EPS and SMP in the NOB-enriched culture initially increase, but later decrease gradually, and that the SMP formed in the nitrite oxidation process are biodegradable.",
    #     "What problem does this paper attempt to solve?": "The paper attempts to address the lack of information regarding the growth, maintenance, and microbial product formation (specifically EPS and SMP) of autotrophs in activated sludge systems. While extensive work exists for heterotrophs, the specific behaviors of autotrophs, such as Nitrite-Oxidizing Bacteria (NOB), are less understood, particularly concerning how they produce Extracellular Polymeric Substances (EPS) and Soluble Microbial Products (SMP) and how maintenance energy affects their yield.",
    #     "How the paper solves this problem?": 'The paper solves this problem by:\n- Developing a new mathematical model that integrates the "unified theory for EPS and SMP" (originally by Laspidou and Rittmann) into the kinetics of autotrophic growth.\n- Using Nitrite-Oxidizing Bacteria (NOB) as a representative autotroph.\n- Calibrating and validating the model using extensive experimental data obtained from an NOB-enriched Sequencing Batch Reactor (SBR).\n- Using the model to quantify maintenance energy requirements and distinguish between true and apparent growth yields.',
    #     "What experiments were done for the paper?": "The following experiments were conducted:\n- **Enrichment of NOB:** A Sequencing Batch Reactor (SBR) was operated with synthetic wastewater containing nitrite as the sole energy source to selectively enrich NOB.\n- **Batch Tests:** Five sets of batch experiments were conducted with different initial nitrite concentrations (ranging from approx. 100 to 500 mg N/L) to monitor the process kinetics.\n- **Respirometry:** Oxygen Uptake Rate (OUR) was measured to determine microbial activity and yield coefficients.\n- **Chemical Analysis:** Regular measurements of Nitrite-N, Nitrate-N, SMP (as COD), EPS (extracted using cation exchange resin and measured as COD), MLSS, and MLVSS.\n- **Yield Determination:** Specific experiments to calculate the true growth yield ($Y_N$) based on oxygen consumption versus substrate consumption.",
    #     "What are the points that can be explored further?": "- **Source of BAP:** The paper notes a disagreement in the literature regarding the unified theory; specifically, whether Biomass-Associated Products (BAP) come solely from EPS hydrolysis (as modeled here) or also from cell lysis. The model assumes only hydrolysis, but lysis might be significant.\n- **Model Structure Differences:** The paper mentions that different model structures might explain variability in parameter values compared to other studies.\n- **Long-term vs. Short-term Exposure:** The sensitivity of microorganisms to nitrite pulses versus long-term exposure could be investigated further, as this affects inhibition parameters ($K_I$).",
    #     "Summarize the main points of the paper.": "- **Model Development:** A mathematical model describing NOB growth, nitrite inhibition, maintenance, death, and EPS/SMP formation was successfully developed and validated.\n- **Maintenance Energy:** NOB spend a considerable amount of energy on maintenance (estimated at 26.7% of energy generated at maximum growth rate).\n- **Yields:** The true growth yield ($Y_N$) was determined to be 0.06 mg COD biomass/mg N, while the apparent yield was 0.044 mg COD biomass/mg N.\n- **Product Dynamics:** EPS and SMP concentrations initially increase during the rapid growth phase and decrease/stabilize as nitrite is depleted. The SMP formed consists of Utilization-Associated Products (UAP) and Biomass-Associated Products (BAP), which are biodegradable.\n- **Validation:** The model accurately predicted OUR profiles, nitrogen species changes, and EPS/SMP trends in the batch tests.",
    #     "What are the relevant studies?": "- **Laspidou and Rittmann (2002a,b):** Proposed the unified theory for EPS and SMP, which forms the backbone of the model in this paper.\n- **Vadivelu et al. (2006):** Provided stoichiometric and kinetic characterization of *Nitrobacter*, used for method comparison.\n- **Moussa et al. (2005):** Relevant for NOB kinetics and modeling nitrification.\n- **Aquino and Stuckey (2008):** Discussed the mechanisms of SMP/EPS formation, specifically regarding cell lysis vs. hydrolysis.",
    #     "zh_Abstract": "活性污泥中的自养菌在生物废水处理中起着重要作用，特别是在硝化过程中。与活性污泥中的异养菌相比，关于自养菌的生长、维持和产物形成的信息仍然很少。在这项工作中，以活性污泥中的亚硝酸盐氧化菌（NOB）为例，采用实验和模拟相结合的方法研究了自养菌的生长、亚硝酸盐抑制、维持以及胞外聚合物（EPS）和溶解性微生物产物（SMP）的形成。我们将EPS和SMP的统一理论整合到我们的模型中，以描述NOB的微生物产物形成。利用序批式反应器中富集的NOB进行了大量实验，用于校准和验证开发的模型。结果表明，NOB在维持过程中消耗了大量的能量。它们的表观生长产率估计为0.044 mg COD生物量 mg⁻¹ N。模型模拟显示，富集NOB的培养物中EPS和SMP的浓度最初增加，但随后逐渐降低，并且在亚硝酸盐氧化过程中形成的SMP是可生物降解的。",
    #     "zh_What problem does this paper attempt to solve?": "本文试图解决活性污泥系统中关于自养菌的生长、维持和微生物产物（特别是EPS和SMP）形成方面信息匮乏的问题。虽然关于异养菌的研究已经很广泛，但对于自养菌（如亚硝酸盐氧化菌 NOB）的具体行为，特别是它们如何产生胞外聚合物（EPS）和溶解性微生物产物（SMP）以及维持能量如何影响其产率，了解较少。",
    #     "zh_How the paper solves this problem?": "本文通过以下方式解决该问题：\n- 开发了一个新的数学模型，将“EPS和SMP的统一理论”（最初由Laspidou和Rittmann提出）整合到自养菌生长动力学中。\n- 使用亚硝酸盐氧化菌（NOB）作为代表性的自养菌。\n- 利用从富集NOB的序批式反应器（SBR）中获得的大量实验数据对模型进行校准和验证。\n- 使用该模型量化维持能量需求，并区分真实生长产率和表观生长产率。",
    #     "zh_What experiments were done for the paper?": "进行了以下实验：\n- **NOB的富集：** 运行一个以亚硝酸盐为唯一能源的合成废水的序批式反应器（SBR），以选择性地富集NOB。\n- **批次测试：** 进行了五组不同初始亚硝酸盐浓度（范围约为100至500 mg N/L）的批次实验，以监测过程动力学。\n- **呼吸测量：** 测量摄氧率（OUR）以确定微生物活性和产率系数。\n- **化学分析：** 定期测量亚硝酸盐氮、硝酸盐氮、SMP（以COD计）、EPS（使用阳离子交换树脂提取并以COD计）、MLSS和MLVSS。\n- **产率测定：** 基于氧消耗与底物消耗的特定实验，计算真实生长产率（$Y_N$）。",
    #     "zh_What are the points that can be explored further?": "- **BAP的来源：** 论文指出文献中关于统一理论存在分歧；具体来说，生物量相关产物（BAP）是仅来自EPS水解（如本文模型假设），还是也来自细胞裂解。模型假设仅来自水解，但裂解可能也很重要。\n- **模型结构的差异：** 论文提到，不同的模型结构可能解释了与其他研究相比参数值的变异性。\n- **长期与短期暴露：** 微生物对亚硝酸盐脉冲与长期暴露的敏感性差异可以进一步研究，因为这会影响抑制参数（$K_I$）。",
    #     "zh_Summarize the main points of the paper.": "- **模型开发：** 成功开发并验证了一个描述NOB生长、亚硝酸盐抑制、维持、死亡以及EPS/SMP形成的数学模型。\n- **维持能量：** NOB在维持上消耗了大量能量（估计在最大生长速率下占产生能量的26.7%）。\n- **产率：** 测得真实生长产率（$Y_N$）为0.06 mg COD生物量/mg N，而表观产率为0.044 mg COD生物量/mg N。\n- **产物动态：** EPS和SMP浓度在快速生长期最初增加，随着亚硝酸盐耗尽而减少/稳定。形成的SMP由利用相关产物（UAP）和生物量相关产物（BAP）组成，且是可生物降解的。\n- **验证：** 该模型准确预测了批次测试中的OUR曲线、氮物种变化以及EPS/SMP趋势。",
    #     "zh_What are the relevant studies?": "- **Laspidou and Rittmann (2002a,b):** 提出了EPS和SMP的统一理论，构成了本文模型的骨架。\n- **Vadivelu et al. (2006):** 提供了*Nitrobacter*的化学计量和动力学表征，用于方法比较。\n- **Moussa et al. (2005):** 与NOB动力学和硝化作用建模相关。\n- **Aquino and Stuckey (2008):** 讨论了SMP/EPS形成的机制，特别是关于细胞裂解与水解的问题。",
    # }

    if result:
        # if True:
        # result = {
        #     "Title": "Simulation of the performance of aerobic granular sludge SBR using modified ASM3 model",
        #     "Year": "2013",
        #     "Journal": "Bioresource Technology",
        #     "DOI": "10.1016/j.biortech.2012.09.076",
        #     "Access": "SUBSCRIPTION",
        #     "Authors": "Man Zhou, Jianyu Gong, Changzhu Yang, Wenhong Pu",
        #     "Abstract": "The activated sludge model No. 3 (ASM3) was modified to describe the biological reactions in aerobic granular sludge SBR. The simultaneous storage and growth, nitrification and denitrification were all accounted for in modified model. The sensitivities of effluent COD, NH4+-N, and TN toward the stoichiometric and kinetic coefficients were analyzed. A standard set of parameters obtained from a combination of literature data was chosen for the model. The experimental results for the time profile of COD, NH4+-N, and TN in a typical cycle were used to verify the ASM3 model. The verification results show the model established is applicable for simulating the performance of an aerobic granule-based SBR. A comparison of the measured and predicted values of substrate removal for both the modified ASM3 and the original ASM3 was also performed. The verification and comparison results show the modified ASM3 model describes the aerobic granule-based SBR better and more mechanistically.",
        #     "What problem does this paper attempt to solve?": "The paper attempts to address the limitations of the original Activated Sludge Model No. 3 (ASM3) when applied to Aerobic Granular Sludge (AGS) systems in Sequencing Batch Reactors (SBR). Specifically:\n- **Inaccurate Storage Mechanism:** Original ASM3 assumes sequential storage and growth (storage only during feast phase), which does not match the simultaneous storage and growth observed in AGS under feast-famine conditions.\n- **Simplified Nitrogen Removal:** Original ASM3 assumes single-step nitrification and denitrification, neglecting nitrite ($$NO_2^-$$) accumulation, which is a significant intermediate in AGS systems.",
        #     "How the paper solves this problem?": "The authors developed a **modified ASM3 model** with the following key extensions:\n- **Simultaneous Processes:** Introduced the concept of simultaneous heterotrophic storage and growth on readily biodegradable substrates ($$S_S$$).\n- **Two-Step Nitrogen Removal:** Modeled nitrification and denitrification as two-step processes involving nitrite ($$NO_2^-$$) as an explicit intermediate ($$NH_4^+ \\to NO_2^- \\to NO_3^-$$ and $$NO_3^- \\to NO_2^- \\to N_2$$).\n- **Microbial Population Split:** Split autotrophic biomass into Ammonia Oxidizing Bacteria ($$X_{AOB}$$) and Nitrite Oxidizing Bacteria ($$X_{NOB}$$).\n- **Parameter Calibration:** Performed sensitivity analysis to identify 11 key parameters and calibrated them using experimental data.",
        #     "What experiments were done for the paper?": "- **Reactor Operation:** Operated a laboratory-scale SBR (8L) fed with synthetic wastewater to cultivate aerobic granules.\n- **Cycle Analysis:** Measured concentration profiles of COD, $$NH_4^+-N$$, and TN during a typical 6-hour cycle (feeding, aeration, settling, discharge).\n- **Sensitivity Analysis:** Evaluated the sensitivity of model outputs to stoichiometric and kinetic parameters to identify the most influential ones.\n- **Model Verification:** Compared the modified ASM3 simulation results with experimental data.\n- **Model Comparison:** Simulated the system using both the original ASM3 and the modified ASM3 to demonstrate the improvement.",
        #     "What are the points that can be explored further?": "- **DO Competition and Lag Time:** The paper noted a deviation in TN simulation due to a lag time caused by competition for Dissolved Oxygen (DO) between heterotrophs and autotrophs. Further exploration into oxygen diffusion limitations within the granule structure could improve this.\n- **Phosphorus Removal:** The current modification focuses on COD and Nitrogen. Since AGS is known for excellent biological phosphorus removal, extending the model to include PAOs (Polyphosphate Accumulating Organisms) would be a logical next step.\n- **Substrate Diversity:** The model was tested with synthetic wastewater; testing with real, complex wastewater would validate the hydrolysis and storage mechanisms further.",
        #     "Summarize the main points of the paper.": "- A modified ASM3 model was successfully developed for AGS SBR systems, incorporating simultaneous storage-growth and two-step nitrification-denitrification.\n- Sensitivity analysis identified parameters like $$Y_{H,O2}$$, $$K_S$$, and $$\\mu_{AOB}$$ as highly influential.\n- The modified model showed excellent agreement with experimental data (Goodness of fit: COD 99.7%, $$NH_4^+-N$$ 97.9%, TN 92.4%).\n- Comparative analysis proved that the modified model predicts substrate removal and nitrite accumulation significantly better than the original ASM3, which failed to capture the rapid initial COD removal and intermediate nitrite dynamics.",
        #     "What are the relevant studies?": "- **Henze et al. (2000)** Activated Sludge Models ASM1, ASM2, ASM2d, and ASM3.\n- **Ni et al. (2008)** Modeling simultaneous autotrophic and heterotrophic growth in aerobic granules.\n- **Krishna and van Loosdrecht (1999)** Substrate flux into storage and growth in relation to activated sludge modelling.\n- **Kaelin et al. (2009)** Extension of ASM3 for two-step nitrification and denitrification and its calibration and validation with batch tests and pilot scale data.\n- **de Kreuk et al. (2007)** Kinetic model of a granular sludge SBR: influences on nutrient removal.",
        #     "zh_Abstract": "活性污泥3号模型（ASM3）经过修正，用于描述好氧颗粒污泥SBR中的生物反应。修正后的模型考虑了同步储存与生长、硝化和反硝化过程。分析了出水COD、$$NH_4^+-N$$和TN对化学计量系数和动力学系数的敏感性。模型选用了一组结合文献数据的标准参数。利用典型周期内COD、$$NH_4^+-N$$和TN的时间变化实验结果验证了ASM3模型。验证结果表明，建立的模型适用于模拟好氧颗粒污泥SBR的性能。此外，还比较了修正后的ASM3和原始ASM3对底物去除的测量值与预测值。验证和比较结果表明，修正后的ASM3模型能更好、更符合机理地描述好氧颗粒污泥SBR。",
        #     "zh_What problem does this paper attempt to solve?": "本文旨在解决原始活性污泥3号模型（ASM3）在应用于序批式反应器（SBR）中的好氧颗粒污泥（AGS）系统时存在的局限性。具体包括：\n- **不准确的储存机制：** 原始ASM3假设储存和生长是顺序进行的（仅在盛宴期储存），这与AGS在盛宴-饥荒条件下观察到的同步储存和生长现象不符。\n- **简化的脱氮过程：** 原始ASM3假设单步硝化和反硝化，忽略了亚硝酸盐（$$NO_2^-$$）的积累，而亚硝酸盐是AGS系统中重要的中间产物。",
        #     "zh_How the paper solves this problem?": "作者开发了一个**修正的ASM3模型**，主要扩展如下：\n- **同步过程：** 引入了异养菌在利用易生物降解底物（$$S_S$$）时的同步储存和生长概念。\n- **两步脱氮：** 将硝化和反硝化模拟为涉及亚硝酸盐（$$NO_2^-$$）作为明确中间产物的两步过程（$$NH_4^+ \\to NO_2^- \\to NO_3^-$$ 和 $$NO_3^- \\to NO_2^- \\to N_2$$）。\n- **微生物种群细分：** 将自养菌群分为氨氧化细菌（$$X_{AOB}$$）和亚硝酸盐氧化细菌（$$X_{NOB}$$）。\n- **参数校准：** 进行敏感性分析以确定11个关键参数，并利用实验数据对其进行校准。",
        #     "zh_What experiments were done for the paper?": "- **反应器运行：** 运行一个进水为合成废水的实验室规模SBR（8L），培养好氧颗粒污泥。\n- **周期分析：** 测量典型6小时周期（进水、曝气、沉淀、排水）内COD、$$NH_4^+-N$$和TN的浓度变化曲线。\n- **敏感性分析：** 评估模型输出对化学计量和动力学参数的敏感性，以识别最具影响力的参数。\n- **模型验证：** 将修正后的ASM3模拟结果与实验数据进行对比。\n- **模型比较：** 分别使用原始ASM3和修正后的ASM3模拟系统，以展示改进效果。",
        #     "zh_What are the points that can be explored further?": "- **DO竞争与滞后时间：** 论文指出由于异养菌和自养菌之间对溶解氧（DO）的竞争导致了TN模拟的偏差（滞后时间）。进一步探索颗粒结构内的氧扩散限制可能改善这一点。\n- **除磷：** 目前的修正主要关注COD和氮。由于AGS以优异的生物除磷能力著称，扩展模型以包含聚磷菌（PAOs）将是合乎逻辑的下一步。\n- **底物多样性：** 该模型是使用合成废水测试的；使用真实的复杂废水进行测试将进一步验证水解和储存机制。",
        #     "zh_Summarize the main points of the paper.": "- 成功开发了适用于AGS SBR系统的修正ASM3模型，整合了同步储存-生长和两步硝化-反硝化过程。\n- 敏感性分析确定了如$$Y_{H,O2}$$、$$K_S$$和$$\\mu_{AOB}$$等参数具有高度影响力。\n- 修正后的模型与实验数据表现出极好的一致性（拟合优度：COD 99.7%，$$NH_4^+-N$$ 97.9%，TN 92.4%）。\n- 对比分析证明，修正后的模型在预测底物去除和亚硝酸盐积累方面显著优于原始ASM3，原始模型未能捕捉到快速的初始COD去除和中间亚硝酸盐的动态变化。",
        #     "zh_What are the relevant studies?": "- **Henze et al. (2000)** Activated Sludge Models ASM1, ASM2, ASM2d, and ASM3.\n- **Ni et al. (2008)** Modeling simultaneous autotrophic and heterotrophic growth in aerobic granules.\n- **Krishna and van Loosdrecht (1999)** Substrate flux into storage and growth in relation to activated sludge modelling.\n- **Kaelin et al. (2009)** Extension of ASM3 for two-step nitrification and denitrification and its calibration and validation with batch tests and pilot scale data.\n- **de Kreuk et al. (2007)** Kinetic model of a granular sludge SBR: influences on nutrient removal.",
        # }

        if result["Access"] == "OPEN":
            access = """<img style={{marginBottom: '0.8rem', marginRight: '0.8rem'}} alt="" src="https://img.shields.io/badge/access-open-42A5F5?style=for-the-badge" />"""
        else:
            access = """<img style={{marginBottom: '0.8rem', marginRight: '0.8rem'}} alt="" src="https://img.shields.io/badge/access-subscription-orange?style=for-the-badge" />"""

        target_dir, target_dir_zh = mk_target_dir(result)

        result_title_ = result["Title"].replace("/", "_")  # 替换文件名中的 / 为 _
        content = get_content(result, access)
        with open(target_dir / f"{result_title_}.mdx", "w") as file:  # type: ignore
            file.write(content)

        content = get_content(result, access, is_en=False)
        with open(target_dir_zh / f"{result_title_}.mdx", "w") as file:  # type: ignore
            file.write(content)

        try:
            add_db_paper_main(result)
            # 移动 pdf/xlsx 文件到 unapproved 文件夹下等待人工 approve
        except Exception:
            exc = format_exc()
            if 'unique constraint "sourcepaper_DOI_key"' not in exc:
                raise ValueError(exc)

        create_BioModel_result = asy_run(
            add_db_BioModel_main(result, f"pdf/{pdf_file}", models)
        )  # 本地拆解论文时, 可以用更高级的模型

        logger.info(create_BioModel_result)

        move(f"pdf/{pdf_file}", f"pdf/unapproved/{pdf_file}")
        if path.exists(f"{result_title_}.xlsx"):
            move(f"{result_title_}.xlsx", f"pdf/unapproved/{result_title_}.xlsx")


if __name__ == "__main__":
    main(
        # "Simulation of the performance of aerobic granular sludge SBR using modiﬁed ASM3 model.pdf"
        # "Simultaneous removal of sulﬁde, nitrate and acetate under denitrifying sulﬁde removal condition: Modeling and experimental validation.pdf"
        #
        # "Achieving Complete Nitrogen Removal by Coupling Nitritation-Anammox and Methane-Dependent Denitrification: A Model-Based Study.pdf"
        # "A modeling approach to describe ZVI-based anaerobic system.pdf"
        # "A quantified nitrogen metabolic network by reaction kinetics and mathematical model in a single-stage microaerobic system treating low COD_TN wastewater.pdf"
        # "Competitive dynamics of anaerobes during long-term biological sulfate reduction process in a UASB reactor.pdf"
        # "Development of a kinetic model to evaluate thiosulfate-driven denitriﬁcation and anammox (TDDA) process.pdf"
        # "Development of an Extended ASM3 Model for Predicting the Nitrous Oxide Emissions in a Full-Scale Wastewater Treatment Plant.pdf"
        # "Evaluating two concepts for the modelling of intermediates accumulation during biological denitrification in wastewater treatment.pdf"
        # "Expanding ASM models towards integrated processes for short-cut nitrogen removal and bioplastic recovery.pdf"
        # "Mathematical modeling of simultaneous carbon-nitrogen-sulfur removal from industrial wastewater.pdf"
        # "Modeling Nitrous Oxide Production during Biological Nitrogen Removal via Nitrification and Denitrification: Extensions to the General ASM Models.pdf"
        # "Modelling Methane Production and Sulfate Reduction in Anaerobic Granular Sludge Reactor with Ethanol as Electron Donor.pdf"
        # "Phosphate release involving PAOs activity during anaerobic fermentation of EBPR sludge and the extension of ADM1.pdf"
        # "Physics-informed neural network-based serial hybrid model capturing the hidden kinetics for sulfur-driven autotrophic denitrification proces.pdf"
        # "Quantifying sensitivity and uncertainty analysis of a new mathematical model for the evaluation of greenhouse gas emissions from.pdf"
        # "Simulation of the performance of aerobic granular sludge SBR using modiﬁed ASM3 model.pdf"
        # "Simultaneous removal of sulﬁde, nitrate and acetate under denitrifying sulﬁde removal condition: Modeling and experimental validation.pdf"
        "Sulfate-reduction, sulﬁde-oxidation and elemental sulfur bioreduction process: Modeling and experimental validation.pdf"
    )

    # pdf_file_list: list = [pdf for pdf in listdir("pdf") if pdf.endswith(".pdf")]
    # # ic(pdf_file_list)

    # for pdf_file in pdf_file_list:
    #     main(pdf_file)
