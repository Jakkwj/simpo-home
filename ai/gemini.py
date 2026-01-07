import base64
from shutil import move
from asyncio import run as asy_run
from os import path, mkdir, listdir, environ
import json
import pathlib
from traceback import format_exc
from pathlib2 import Path
from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from simpo import ic
from psutil import virtual_memory
if virtual_memory().total > 33470000000:
    COMPUTER_PATH = "/media/Data/SynologyDrive/GitHub"  # 家里台式机
else:
    COMPUTER_PATH = "/media/Cloud/SynologyDrive/GitHub"  # 座机

from prompt import (
    PROMPT_CONTENT,
    SYSTEM_INSTRUCTION
)
from add_db_paper import main as add_db_paper_main
from add_db_BioModel import main as add_db_BioModel_main

from dotenv import load_dotenv

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
    # models: str = "gemini-3-pro-preview-thinking",
    models: str = "gemini-3-pro-preview",
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
            logger.error(
                f"Retrying ({retry_counter}/5): {response_text_}"
            )
            if retry_counter >= 5:
                logger.error(
                    f"Failed, please try again."
                )
                break
            retry_counter += 1


def mk_target_dir(result: dict[str, str])-> tuple[str, str]:
    """创建 mdx 所在的目标文件夹"""
    # res_dir = f"{COMPUTER_PATH}/SimpoHome/src/resource"
    target_dir = Path(f"{COMPUTER_PATH}/SimpoHome/src/resource/{result['Year']}/{result['Journal']}")
    target_dir.mkdir(parents=True, exist_ok=True)  # 多级新建文件夹

    # res_dir = f"{COMPUTER_PATH}/SimpoHome/src/i18n/zh/docusaurus-plugin-content-docs-resource/current"
    target_dir_zh = Path(f"{COMPUTER_PATH}/SimpoHome/src/i18n/zh/docusaurus-plugin-content-docs-resource/current/{result['Year']}/{result['Journal']}")
    target_dir_zh.mkdir(parents=True, exist_ok=True)  # 多级新建文件夹

    return target_dir, target_dir_zh


def get_content(result: dict[str, str], access: str, is_en: bool = True) -> str:
    """根据 is_en 创建中英文内容"""
    return f"""---
        slug: {result["DOI"]}
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

                    {'Authors' if is_en else '作者'}: {result["Authors"]}
          </div>
        </div>


        {{/* ----


        [SIMPO Dashboard](https://dash.simpowater.org/dashboard/biomodels/public/name/{result["DOI"].replace("/", "-")}/id/xxxxxx/did/yyyyyy):

        <iframe
        src="https://dash.simpowater.org/dashboard/biomodels/iframe/public/name/{result["DOI"].replace("/", "-")}/id/xxxxxx/did/yyyyyy"

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

        **Q: What problem does this paper attempt to solve?**

        **Gemini 3.0 Pro:**

        {result["What problem does this paper attempt to solve?"] if is_en else result["zh_Abstract"]}

        </TabItem >

        <TabItem value="solution" label="Solution" >

        **Q: How the paper solves this problem?**

        **Gemini 3.0 Pro:**

        {result["How the paper solves this problem?"] if is_en else result["zh_How the paper solves this problem?"]}

        </TabItem >

        <TabItem value="experiment" label="Experiment" >

        **Q: What experiments were done for the paper?**

        **Gemini 3.0 Pro:**

        {result["What experiments were done for the paper?"] if is_en else result["zh_What experiments were done for the paper?"]}

        </TabItem >

        <TabItem value="exploration" label="Exploration" >

        **Q: What are the points that can be explored further?**

        **Gemini 3.0 Pro:**

        {result["What are the points that can be explored further?"] if is_en else result["zh_What are the points that can be explored further?"]}

        </TabItem >

        <TabItem value="summary" label="Summary" >

        **Q: Summarize the main points of the paper.**

        **Gemini 3.0 Pro:**

        {result["Summarize the main points of the paper."] if is_en else result["zh_Summarize the main points of the paper."]}

        </TabItem>

        <TabItem value="related" label="Related" >

        **Q: What are the relevant studies?**

        **Gemini 3.0 Pro:**

        {result["What are the relevant studies?"] if is_en else result["zh_What are the relevant studies?"]}

        </TabItem >

        </Tabs>

    """.replace("        ", "")


def main(pdf_file: str):
    """
    更新 生成环境时, 把更改 litestar.env 中的 ENV = production
    生成 resource 的 mdx 文件.
    并尝试生成 BioModel 写入数据库.
    """

    # result = asy_run(main_one_step(f"pdf/{pdf_file}"))

    result = {'Title': 'Growth, maintenance and product formation of autotrophs in activated sludge: Taking the nitrite-oxidizing bacteria as an example', 'Year': '2008', 'Journal': 'Water Research', 'DOI': '10.1016/j.watres.2008.06.024', 'Access': 'SUBSCRIPTION', 'Authors': 'Bing-Jie Ni, Fang Fang, Wen-Ming Xie, Han-Qing Yu', 'Abstract': 'The autotrophs in activated sludge play an important role in biological wastewater treatment, especially in the nitrification process. Compared with the heterotrophs in activated sludge, information about the growth, maintenance, and product formation of the autotrophs is still sparse. In this work both experimental and modeling approaches are used to investigate the growth, nitrite inhibition, maintenance, and formation of extracellular polymeric substances (EPS) and soluble microbial products (SMP) of the autotrophs, with nitrite-oxidizing bacteria (NOB) in activated sludge as an example. The unified theory for EPS and SMP is integrated into our model to describe the microbial product formation of the NOB. Extensive experiments were carried out using the NOB-enriched in a sequencing batch reactor for the calibration and validation of the developed model. Results show that the NOB spend a considerable amount of energy on maintenance processes. Their apparent growth yield is estimated to be 0.044 mg COD biomass mg⁻¹ N. The model simulations reveal that the concentrations of EPS and SMP in the NOB-enriched culture initially increase, but later decrease gradually, and that the SMP formed in the nitrite oxidation process are biodegradable.', 'What problem does this paper attempt to solve?': 'The paper attempts to address the lack of information regarding the growth, maintenance, and microbial product formation (specifically EPS and SMP) of autotrophs in activated sludge systems. While extensive work exists for heterotrophs, the specific behaviors of autotrophs, such as Nitrite-Oxidizing Bacteria (NOB), are less understood, particularly concerning how they produce Extracellular Polymeric Substances (EPS) and Soluble Microbial Products (SMP) and how maintenance energy affects their yield.', 'How the paper solves this problem?': 'The paper solves this problem by:\n- Developing a new mathematical model that integrates the "unified theory for EPS and SMP" (originally by Laspidou and Rittmann) into the kinetics of autotrophic growth.\n- Using Nitrite-Oxidizing Bacteria (NOB) as a representative autotroph.\n- Calibrating and validating the model using extensive experimental data obtained from an NOB-enriched Sequencing Batch Reactor (SBR).\n- Using the model to quantify maintenance energy requirements and distinguish between true and apparent growth yields.', 'What experiments were done for the paper?': 'The following experiments were conducted:\n- **Enrichment of NOB:** A Sequencing Batch Reactor (SBR) was operated with synthetic wastewater containing nitrite as the sole energy source to selectively enrich NOB.\n- **Batch Tests:** Five sets of batch experiments were conducted with different initial nitrite concentrations (ranging from approx. 100 to 500 mg N/L) to monitor the process kinetics.\n- **Respirometry:** Oxygen Uptake Rate (OUR) was measured to determine microbial activity and yield coefficients.\n- **Chemical Analysis:** Regular measurements of Nitrite-N, Nitrate-N, SMP (as COD), EPS (extracted using cation exchange resin and measured as COD), MLSS, and MLVSS.\n- **Yield Determination:** Specific experiments to calculate the true growth yield ($Y_N$) based on oxygen consumption versus substrate consumption.', 'What are the points that can be explored further?': '- **Source of BAP:** The paper notes a disagreement in the literature regarding the unified theory; specifically, whether Biomass-Associated Products (BAP) come solely from EPS hydrolysis (as modeled here) or also from cell lysis. The model assumes only hydrolysis, but lysis might be significant.\n- **Model Structure Differences:** The paper mentions that different model structures might explain variability in parameter values compared to other studies.\n- **Long-term vs. Short-term Exposure:** The sensitivity of microorganisms to nitrite pulses versus long-term exposure could be investigated further, as this affects inhibition parameters ($K_I$).', 'Summarize the main points of the paper.': '- **Model Development:** A mathematical model describing NOB growth, nitrite inhibition, maintenance, death, and EPS/SMP formation was successfully developed and validated.\n- **Maintenance Energy:** NOB spend a considerable amount of energy on maintenance (estimated at 26.7% of energy generated at maximum growth rate).\n- **Yields:** The true growth yield ($Y_N$) was determined to be 0.06 mg COD biomass/mg N, while the apparent yield was 0.044 mg COD biomass/mg N.\n- **Product Dynamics:** EPS and SMP concentrations initially increase during the rapid growth phase and decrease/stabilize as nitrite is depleted. The SMP formed consists of Utilization-Associated Products (UAP) and Biomass-Associated Products (BAP), which are biodegradable.\n- **Validation:** The model accurately predicted OUR profiles, nitrogen species changes, and EPS/SMP trends in the batch tests.', 'What are the relevant studies?': '- **Laspidou and Rittmann (2002a,b):** Proposed the unified theory for EPS and SMP, which forms the backbone of the model in this paper.\n- **Vadivelu et al. (2006):** Provided stoichiometric and kinetic characterization of *Nitrobacter*, used for method comparison.\n- **Moussa et al. (2005):** Relevant for NOB kinetics and modeling nitrification.\n- **Aquino and Stuckey (2008):** Discussed the mechanisms of SMP/EPS formation, specifically regarding cell lysis vs. hydrolysis.', 'zh_Abstract': '活性污泥中的自养菌在生物废水处理中起着重要作用，特别是在硝化过程中。与活性污泥中的异养菌相比，关于自养菌的生长、维持和产物形成的信息仍然很少。在这项工作中，以活性污泥中的亚硝酸盐氧化菌（NOB）为例，采用实验和模拟相结合的方法研究了自养菌的生长、亚硝酸盐抑制、维持以及胞外聚合物（EPS）和溶解性微生物产物（SMP）的形成。我们将EPS和SMP的统一理论整合到我们的模型中，以描述NOB的微生物产物形成。利用序批式反应器中富集的NOB进行了大量实验，用于校准和验证开发的模型。结果表明，NOB在维持过程中消耗了大量的能量。它们的表观生长产率估计为0.044 mg COD生物量 mg⁻¹ N。模型模拟显示，富集NOB的培养物中EPS和SMP的浓度最初增加，但随后逐渐降低，并且在亚硝酸盐氧化过程中形成的SMP是可生物降解的。', 'zh_What problem does this paper attempt to solve?': '本文试图解决活性污泥系统中关于自养菌的生长、维持和微生物产物（特别是EPS和SMP）形成方面信息匮乏的问题。虽然关于异养菌的研究已经很广泛，但对于自养菌（如亚硝酸盐氧化菌 NOB）的具体行为，特别是它们如何产生胞外聚合物（EPS）和溶解性微生物产物（SMP）以及维持能量如何影响其产率，了解较少。', 'zh_How the paper solves this problem?': '本文通过以下方式解决该问题：\n- 开发了一个新的数学模型，将“EPS和SMP的统一理论”（最初由Laspidou和Rittmann提出）整合到自养菌生长动力学中。\n- 使用亚硝酸盐氧化菌（NOB）作为代表性的自养菌。\n- 利用从富集NOB的序批式反应器（SBR）中获得的大量实验数据对模型进行校准和验证。\n- 使用该模型量化维持能量需求，并区分真实生长产率和表观生长产率。', 'zh_What experiments were done for the paper?': '进行了以下实验：\n- **NOB的富集：** 运行一个以亚硝酸盐为唯一能源的合成废水的序批式反应器（SBR），以选择性地富集NOB。\n- **批次测试：** 进行了五组不同初始亚硝酸盐浓度（范围约为100至500 mg N/L）的批次实验，以监测过程动力学。\n- **呼吸测量：** 测量摄氧率（OUR）以确定微生物活性和产率系数。\n- **化学分析：** 定期测量亚硝酸盐氮、硝酸盐氮、SMP（以COD计）、EPS（使用阳离子交换树脂提取并以COD计）、MLSS和MLVSS。\n- **产率测定：** 基于氧消耗与底物消耗的特定实验，计算真实生长产率（$Y_N$）。', 'zh_What are the points that can be explored further?': '- **BAP的来源：** 论文指出文献中关于统一理论存在分歧；具体来说，生物量相关产物（BAP）是仅来自EPS水解（如本文模型假设），还是也来自细胞裂解。模型假设仅来自水解，但裂解可能也很重要。\n- **模型结构的差异：** 论文提到，不同的模型结构可能解释了与其他研究相比参数值的变异性。\n- **长期与短期暴露：** 微生物对亚硝酸盐脉冲与长期暴露的敏感性差异可以进一步研究，因为这会影响抑制参数（$K_I$）。', 'zh_Summarize the main points of the paper.': '- **模型开发：** 成功开发并验证了一个描述NOB生长、亚硝酸盐抑制、维持、死亡以及EPS/SMP形成的数学模型。\n- **维持能量：** NOB在维持上消耗了大量能量（估计在最大生长速率下占产生能量的26.7%）。\n- **产率：** 测得真实生长产率（$Y_N$）为0.06 mg COD生物量/mg N，而表观产率为0.044 mg COD生物量/mg N。\n- **产物动态：** EPS和SMP浓度在快速生长期最初增加，随着亚硝酸盐耗尽而减少/稳定。形成的SMP由利用相关产物（UAP）和生物量相关产物（BAP）组成，且是可生物降解的。\n- **验证：** 该模型准确预测了批次测试中的OUR曲线、氮物种变化以及EPS/SMP趋势。', 'zh_What are the relevant studies?': '- **Laspidou and Rittmann (2002a,b):** 提出了EPS和SMP的统一理论，构成了本文模型的骨架。\n- **Vadivelu et al. (2006):** 提供了*Nitrobacter*的化学计量和动力学表征，用于方法比较。\n- **Moussa et al. (2005):** 与NOB动力学和硝化作用建模相关。\n- **Aquino and Stuckey (2008):** 讨论了SMP/EPS形成的机制，特别是关于细胞裂解与水解的问题。'}

    if result:
        ic(123)
        if result["Access"] == "OPEN":
            access = """<img style={{marginBottom: '0.8rem', marginRight: '0.8rem'}} alt="" src="https://img.shields.io/badge/access-open-42A5F5?style=for-the-badge" />"""
        else:
            access = """<img style={{marginBottom: '0.8rem', marginRight: '0.8rem'}} alt="" src="https://img.shields.io/badge/access-subscription-orange?style=for-the-badge" />"""

        target_dir, target_dir_zh = mk_target_dir(result)

        content = get_content(result, access)
        with open(target_dir / f"{result['Title']}.mdx", "w") as file:  # type: ignore
            file.write(content)

        content = get_content(result, access, is_en=False)
        with open(target_dir_zh / f"{result['Title']}.mdx", "w") as file:  # type: ignore
            file.write(content)

        # try:
        #     add_db_paper_main(result)
        #     # 移动 pdf/xlsx 文件到 unapproved 文件夹下等待人工 approve
        # except Exception:
        #     exc = format_exc()
        #     if 'unique constraint "sourcepaper_DOI_key"' not in exc:
        #         raise ValueError(exc)

        # create_BioModel_result = asy_run(add_db_BioModel_main(result, pdf_file))

        # move(f"pdf/{pdf_file}", f"pdf/unapproved/{pdf_file}")
        # if path.exists(f"{result['Title']}.xlsx"):
        #     move(f"{result['Title']}.xlsx", f"pdf/unapproved/{result['Title']}.xlsx")


if __name__ == "__main__":

    main("pdf_file")
    # pdf_file_list: list = [pdf for pdf in listdir("pdf") if pdf.endswith(".pdf")]
    # # ic(pdf_file_list)

    # for pdf_file in pdf_file_list:
    #     main(pdf_file)

