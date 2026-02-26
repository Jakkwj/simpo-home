import base64
import json
import pathlib
import sys
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

sys.path.append(f"{COMPUTER_PATH}/SimpoBackend/backend/litestar")

from app.api.biomodel.crud.ai.claude import initial_contents_list as initial_contents_list_claude
from app.api.biomodel.crud.ai.gemini import initial_contents_list as initial_contents_list_gemini
from dotenv import load_dotenv

from add_db_BioModel import main as add_db_BioModel_main
from add_db_paper import main as add_db_paper_main
from prompt import PROMPT_CONTENT, SYSTEM_INSTRUCTION

load_dotenv(".env")
QINGYUN_API_KEY_CLAUDE = environ.get("QINGYUN_API_KEY_CLAUDE")
QINGYUN_API_KEY_GEMINI = environ.get("QINGYUN_API_KEY_GEMINI")


# def initial_contents_list(pdf_base64: str, prompt_content: str) -> list[dict]:
#     """初始化 contents_list, 失败重试的时候需要重置."""
#     return [
#         {
#             "role": "user",
#             "parts": [
#                 {
#                     "inline_data": {
#                         "mime_type": "application/pdf",
#                         "data": pdf_base64,
#                     }
#                 },
#                 {"text": prompt_content},
#             ],
#         }
#     ]


async def get_resource_gemini(
    pdf_path: str,
    models: str,
    # models: str = "gemini-3-pro-preview-thinking",
    # models: str = "gemini-2.5-flash-lite-nothinking",
    # models: str = "gemini-3-pro-preview-11-2025-thinking",
    # models: str = "gemini-3-pro-preview-11-2025",
    # models: str = "gemini-3-pro-preview",
    # models: str = "gemini-2.5-flash",
    # models: str = "gemini-2.5-flash-lite",
) -> dict[str, str] | None:
    """
    这一步是固定用 gemini 回答

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
        "Authorization": f"Bearer {QINGYUN_API_KEY_GEMINI}",
        "Content-Type": "application/json",
    }
    url = f"https://api.qingyuntop.top/v1beta/models/{models}:generateContent?key={QINGYUN_API_KEY_GEMINI}"

    if "gemini-3" in models:  # and "thinking" in models:
        model_contnet_index: int = 1
    else:
        model_contnet_index: int = 0

    pdf_bytes = pathlib.Path(pdf_path).read_bytes()  # encode the PDF byte
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    contents_list = initial_contents_list_gemini(pdf_base64, PROMPT_CONTENT)

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
                            "GEMINI_What problem does this paper attempt to solve?",
                            "GEMINI_How the paper solves this problem?",
                            "GEMINI_What experiments were done for the paper?",
                            "GEMINI_What are the points that can be explored further?",
                            "GEMINI_Summarize the main points of the paper.",
                            "GEMINI_What are the relevant studies?",
                            "GEMINI_zh_Abstract",
                            "GEMINI_zh_What problem does this paper attempt to solve?",
                            "GEMINI_zh_How the paper solves this problem?",
                            "GEMINI_zh_What experiments were done for the paper?",
                            "GEMINI_zh_What are the points that can be explored further?",
                            "GEMINI_zh_Summarize the main points of the paper.",
                            "GEMINI_zh_What are the relevant studies?",
                        ],
                        # "propertyOrdering": [
                        #     "Title",
                        #     "Year",
                        #     "Journal",
                        #     "DOI",
                        #     "Access",
                        #     "Authors",
                        #     "Abstract",
                        #     "What problem does this paper attempt to solve?",
                        #     "How the paper solves this problem?",
                        #     "What experiments were done for the paper?",
                        #     "What are the points that can be explored further?",
                        #     "Summarize the main points of the paper.",
                        #     "What are the relevant studies?",
                        #     "zh_Abstract",
                        #     "zh_What problem does this paper attempt to solve?",
                        #     "zh_How the paper solves this problem?",
                        #     "zh_What experiments were done for the paper?",
                        #     "zh_What are the points that can be explored further?",
                        #     "zh_Summarize the main points of the paper.",
                        #     "zh_What are the relevant studies?",
                        # ],
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
                            "GEMINI_What problem does this paper attempt to solve?": {
                                "type": "string",
                            },
                            "GEMINI_How the paper solves this problem?": {
                                "type": "string",
                            },
                            "GEMINI_What experiments were done for the paper?": {
                                "type": "string",
                            },
                            "GEMINI_What are the points that can be explored further?": {
                                "type": "string",
                            },
                            "GEMINI_Summarize the main points of the paper.": {
                                "type": "string",
                            },
                            "GEMINI_What are the relevant studies?": {
                                "type": "string",
                            },
                            "zh_Abstract": {
                                "type": "string",
                            },
                            "GEMINI_zh_What problem does this paper attempt to solve?": {
                                "type": "string",
                            },
                            "GEMINI_zh_How the paper solves this problem?": {
                                "type": "string",
                            },
                            "GEMINI_zh_What experiments were done for the paper?": {
                                "type": "string",
                            },
                            "GEMINI_zh_What are the points that can be explored further?": {
                                "type": "string",
                            },
                            "GEMINI_zh_Summarize the main points of the paper.": {
                                "type": "string",
                            },
                            "GEMINI_zh_What are the relevant studies?": {
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
            # logger.info(__)
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
                f"Retrying to get Resource from Gemini ({retry_counter}/5): {response_text_}"
            )
            if retry_counter >= 5:
                logger.error("Failed to get Resource from Gemini, please try again.")
                break
            retry_counter += 1


async def get_resource_claude(
    pdf_path: str,
    models: str,
) -> dict[str, str] | None:
    """
    这一步是固定用 claude 回答
    """
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {QINGYUN_API_KEY_CLAUDE}",
        "Content-Type": "application/json",
    }
    url = "https://api.qingyuntop.top/v1/messages"

    pdf_bytes = pathlib.Path(pdf_path).read_bytes()  # encode the PDF byte
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    contents_list = initial_contents_list_claude(pdf_base64, PROMPT_CONTENT)

    payload = json.dumps(  # https://qingyuntop.apifox.cn/api-417649567
        {
            "model": models,
            # "max_tokens": 4096,
            "temperature": 0,  # 对应 Gemini 的 temperature 0
            "system": SYSTEM_INSTRUCTION,  # 对应 Gemini 的 systemInstruction
            "messages": contents_list,
            "tools": [  # 定义工具，结构直接映射 Gemini 的 responseSchema
                {
                    "name": "Result",
                    "input_schema": {
                        "type": "object",
                        "required": [
                            # "Title",
                            # "Year",
                            # "Journal",
                            # "DOI",
                            # "Access",
                            # "Authors",
                            # "Abstract",
                            "CLAUDE_What problem does this paper attempt to solve?",
                            "CLAUDE_How the paper solves this problem?",
                            "CLAUDE_What experiments were done for the paper?",
                            "CLAUDE_What are the points that can be explored further?",
                            "CLAUDE_Summarize the main points of the paper.",
                            "CLAUDE_What are the relevant studies?",
                            "CLAUDE_zh_Abstract",
                            "CLAUDE_zh_What problem does this paper attempt to solve?",
                            "CLAUDE_zh_How the paper solves this problem?",
                            "CLAUDE_zh_What experiments were done for the paper?",
                            "CLAUDE_zh_What are the points that can be explored further?",
                            "CLAUDE_zh_Summarize the main points of the paper.",
                            "CLAUDE_zh_What are the relevant studies?",
                        ],
                        "properties": {
                            # "Title": {
                            #     "type": "string",
                            # },
                            # "Year": {
                            #     "type": "string",
                            # },
                            # "Journal": {
                            #     "type": "string",
                            # },
                            # "DOI": {
                            #     "type": "string",
                            # },
                            # "Access": {
                            #     "type": "string",
                            # },
                            # "Authors": {
                            #     "type": "string",
                            # },
                            # "Abstract": {
                            #     "type": "string",
                            # },
                            "CLAUDE_What problem does this paper attempt to solve?": {
                                "type": "string",
                            },
                            "CLAUDE_How the paper solves this problem?": {
                                "type": "string",
                            },
                            "CLAUDE_What experiments were done for the paper?": {
                                "type": "string",
                            },
                            "CLAUDE_What are the points that can be explored further?": {
                                "type": "string",
                            },
                            "CLAUDE_Summarize the main points of the paper.": {
                                "type": "string",
                            },
                            "CLAUDE_What are the relevant studies?": {
                                "type": "string",
                            },
                            "CLAUDE_zh_Abstract": {
                                "type": "string",
                            },
                            "CLAUDE_zh_What problem does this paper attempt to solve?": {
                                "type": "string",
                            },
                            "CLAUDE_zh_How the paper solves this problem?": {
                                "type": "string",
                            },
                            "CLAUDE_zh_What experiments were done for the paper?": {
                                "type": "string",
                            },
                            "CLAUDE_zh_What are the points that can be explored further?": {
                                "type": "string",
                            },
                            "CLAUDE_zh_Summarize the main points of the paper.": {
                                "type": "string",
                            },
                            "CLAUDE_zh_What are the relevant studies?": {
                                "type": "string",
                            },
                        },
                    },
                }
            ],
            "tool_choice": {  # 强制模型必须使用这个工具，从而强制输出 JSON
                "type": "tool",
                "name": "BioModelSchema",
            },
        }
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
            # logger.info(__)
            result = __["content"][0]["input"]
            logger.info(result)

            return result

        except Exception:
            exc = str(format_exc())
            if "TimeoutError" not in exc:
                logger.error(exc)
            logger.error(
                f"Retrying to get Resource from Claude ({retry_counter}/5): {response_text_}"
            )
            if retry_counter >= 5:
                logger.error("Failed to get Resource from Claude, please try again.")
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


def get_question(
    question_key: str, answer_models: dict[str, str], result: dict[str, str], is_en: bool
) -> str:
    len_ = len(answer_models)

    question = ""

    for index, answer_model in enumerate(answer_models):
        question += f"""
        **{answer_model}:**

        {result[f"{answer_models[answer_model]}{question_key}"] if is_en else result[f"{answer_models[answer_model]}zh_{question_key}"]}

        """
        if index < len_ - 1:
            question += "------n\n"

    return question


def get_content(
    answer_models: dict[str, str], result: dict[str, str], access: str, is_en: bool = True
) -> str:
    """根据 is_en 创建中英文内容"""

    question_1 = get_question(
        "What problem does this paper attempt to solve?", answer_models, result, is_en
    )

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

        **{model}:**

        {result["GEMINI_What problem does this paper attempt to solve?"] if is_en else result["GEMINI_zh_What problem does this paper attempt to solve?"]}

        ------

        **{model}:**

        {result["CLAUDE_What problem does this paper attempt to solve?"] if is_en else result["CLAUDE_zh_What problem does this paper attempt to solve?"]}



        </TabItem >

        <TabItem value="solution" label="Solution" >

        {"**Q: How the paper solves this problem?**" if is_en else "**Q：论文如何解决这个问题？**"}

        **{model}:**

        {result["How the paper solves this problem?"] if is_en else result["zh_How the paper solves this problem?"]}

        </TabItem >

        <TabItem value="experiment" label="Experiment" >

        {"**Q: What experiments were done for the paper?**" if is_en else "**Q：论文做了哪些实验？**"}

        **{model}:**

        {result["What experiments were done for the paper?"] if is_en else result["zh_What experiments were done for the paper?"]}

        </TabItem >

        <TabItem value="exploration" label="Exploration" >

        {"**Q: What are the points that can be explored further?**" if is_en else "**Q：有什么可以进一步探索的点？**"}

        **{model}:**

        {result["What are the points that can be explored further?"] if is_en else result["zh_What are the points that can be explored further?"]}

        </TabItem >

        <TabItem value="summary" label="Summary" >

        {"**Q: Summarize the main points of the paper.**" if is_en else "**Q： 总结一下论文的主要内容。**"}

        **{model}:**

        {result["Summarize the main points of the paper."] if is_en else result["zh_Summarize the main points of the paper."]}

        </TabItem>

        <TabItem value="related" label="Related" >

        {"**Q: What are the relevant studies?**" if is_en else "**Q： 有哪些相关研究？**"}

        **{model}:**

        {result["What are the relevant studies?"] if is_en else result["zh_What are the relevant studies?"]}

        </TabItem >

        </Tabs>

    """.replace("        ", "")


def main(
    pdf_file: str,
    # models: str = "gemini-3-pro-preview",
    # models: str = "gemini-3-pro-preview-thinking",
    # models: str = "gemini-3.1-pro-preview",  # 生产环境用这个 2026.02.22
    # answer_model: str = "Gemini 3.1 Pro",
    models: str = "claude-opus-4-6",
    # models: str = "claude-sonnet-4-6",
    # models: str = "claude-3-haiku-20240307",  # 测试用这个
    answer_model: str = "Claude Opus 4-6",
    prompt_content_1_add: str = "",  # 补充的 PROMPT_CONTENT_1
    prompt_content_2_add: str = "",  # 补充的 PROMPT_CONTENT_2
):
    """
    更新 生产环境时, 把更改 litestar.env 中的 ENV = production
    生成 resource 的 mdx 文件.
    并尝试生成 BioModel 写入数据库.

    本地拆解论文时, 可以用更高级的模型
    """

    result = asy_run(
        get_resource_gemini(
            f"pdf/{pdf_file}",
            models="gemini-3.1-pro-preview",
            # models="gemini-2.5-flash-lite-nothinking",  # 测试时使用
        )
    )

    result_claude = asy_run(
        get_resource_claude(
            f"pdf/{pdf_file}",
            models="claude-opus-4-6",
        )
    )

    if result and result_claude:
        result = result | result_claude

    answer_models = {"GEMINI 3.1 PRO": "GEMINI_", "CLAUDE OPUS 4.6": "CLAUDE_"}
    # answer_model = "gemini-2.5-flash-lite-nothinking"
    logger.info(result)

    if result:
        if result["Access"] == "OPEN":
            access = """<img style={{marginBottom: '0.8rem', marginRight: '0.8rem'}} alt="" src="https://img.shields.io/badge/access-open-42A5F5?style=for-the-badge" />"""
        else:
            access = """<img style={{marginBottom: '0.8rem', marginRight: '0.8rem'}} alt="" src="https://img.shields.io/badge/access-subscription-orange?style=for-the-badge" />"""

        target_dir, target_dir_zh = mk_target_dir(result)

        result_title_ = result["Title"].replace("/", "_")  # 替换文件名中的 / 为 _
        content = get_content(answer_models, result, access)
        with open(target_dir / f"{result_title_}.mdx", "w") as file:  # type: ignore
            file.write(content)

        content = get_content(answer_models, result, access, is_en=False)
        with open(target_dir_zh / f"{result_title_}.mdx", "w") as file:  # type: ignore
            file.write(content)

        try:
            add_db_paper_main(result)
        except Exception:
            exc = format_exc()
            if 'unique constraint "sourcepaper_DOI_key"' not in exc:
                raise ValueError(exc)

        create_BioModel_result = asy_run(
            add_db_BioModel_main(
                result,
                f"pdf/{pdf_file}",
                models,
                prompt_content_1_add,
                prompt_content_2_add,
            )
        )  # 本地拆解论文时, 可以用更高级的模型

        logger.info(create_BioModel_result)

        move(
            f"pdf/{pdf_file}", f"pdf/unapproved/{pdf_file}"
        )  # 移动 pdf/xlsx 文件到 unapproved 文件夹下等待人工 approve
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
        # "Expanding ASM models towards integrated processes for short-cut nitrogen removal and bioplastic recovery.pdf"
        # "Mathematical modeling of simultaneous carbon-nitrogen-sulfur removal from industrial wastewater.pdf"
        # "Modeling Nitrous Oxide Production during Biological Nitrogen Removal via Nitrification and Denitrification: Extensions to the General ASM Models.pdf"
        # "Modelling Methane Production and Sulfate Reduction in Anaerobic Granular Sludge Reactor with Ethanol as Electron Donor.pdf"
        # "Phosphate release involving PAOs activity during anaerobic fermentation of EBPR sludge and the extension of ADM1.pdf"
        # "Physics-informed neural network-based serial hybrid model capturing the hidden kinetics for sulfur-driven autotrophic denitrification proces.pdf"
        # "Quantifying sensitivity and uncertainty analysis of a new mathematical model for the evaluation of greenhouse gas emissions from.pdf"
        # "Simulation of the performance of aerobic granular sludge SBR using modiﬁed ASM3 model.pdf"
        # "Simultaneous removal of sulﬁde, nitrate and acetate under denitrifying sulﬁde removal condition: Modeling and experimental validation.pdf"
        # "Sulfate-reduction, sulﬁde-oxidation and elemental sulfur bioreduction process: Modeling and experimental validation.pdf"
        "Strategies for mitigating nitrous oxide production and decreasing the carbon footprint of a full-scale combined nitrogen and phosphorus removal activated sludge system.pdf",
        # "An Updated Process Model for Carbon Oxidation, Nitrification, and Denitrification.pdf",
        # prompt_content_1_add="""你之前已经提取了一次Component和Parameter，不用重复提取，只需要检查一下即可：
        #     {
        #     "Component": [
        #         {
        #         "0": "Symbol",
        #         "1": "Unit",
        #         "2": "Name",
        #         "3": "Description"
        #         },
        #         {
        #         "0": "S_O",
        #         "1": "mg/L",
        #         "2": "Dissolved oxygen",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "S_NO3",
        #         "1": "mg/L",
        #         "2": "Nitrate",
        #         "3": "mg/L as N"
        #         },
        #         {
        #         "0": "S_NO2",
        #         "1": "mg/L",
        #         "2": "Nitrite",
        #         "3": "mg/L as N"
        #         },
        #         {
        #         "0": "S_NO",
        #         "1": "mg/L",
        #         "2": "Nitric oxide",
        #         "3": "mg/L as N"
        #         },
        #         {
        #         "0": "S_N2O",
        #         "1": "mg/L",
        #         "2": "Nitrous oxide",
        #         "3": "mg/L as N"
        #         },
        #         {
        #         "0": "S_ALK",
        #         "1": "molar",
        #         "2": "Alkalinity",
        #         "3": "molar units"
        #         },
        #         {
        #         "0": "S_I",
        #         "1": "mg/L",
        #         "2": "Inert soluble organic matter",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "S_J",
        #         "1": "mg/L",
        #         "2": "Biodegradable AOB inhibitor",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "S_NH",
        #         "1": "mg/L",
        #         "2": "Ammonia",
        #         "3": "mg/L as N"
        #         },
        #         {
        #         "0": "S_NS",
        #         "1": "mg/L",
        #         "2": "Soluble biodegradable organic nitrogen",
        #         "3": "mg/L as N"
        #         },
        #         {
        #         "0": "S_S",
        #         "1": "mg/L",
        #         "2": "Readily biodegradable substrate",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "S_W",
        #         "1": "mg/L",
        #         "2": "Priority pollutant",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "S_Z",
        #         "1": "mg/L",
        #         "2": "Salt",
        #         "3": "mg/L"
        #         },
        #         {
        #         "0": "X_BA1",
        #         "1": "mg/L",
        #         "2": "Active AOB biomass",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "X_BA2",
        #         "1": "mg/L",
        #         "2": "Active NOB biomass",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "X_BH",
        #         "1": "mg/L",
        #         "2": "Active heterotrophic biomass",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "X_D",
        #         "1": "mg/L",
        #         "2": "Debris from biomass death and lysis",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "X_I",
        #         "1": "mg/L",
        #         "2": "Inert particulate organic matter",
        #         "3": "mg/L as COD"
        #         },
        #         {
        #         "0": "X_NS",
        #         "1": "mg/L",
        #         "2": "Particulate biodegradable organic nitrogen",
        #         "3": "mg/L as N"
        #         },
        #         {
        #         "0": "X_S",
        #         "1": "mg/L",
        #         "2": "Slowly biodegradable substrate",
        #         "3": "mg/L as COD"
        #         }
        #     ],
        #     "Parameter": [
        #         {
        #         "0": "Symbol",
        #         "1": "Unit",
        #         "2": "DefaultValue",
        #         "3": "LowerBound",
        #         "4": "UpperBound",
        #         "5": "Name",
        #         "6": "Description"
        #         },
        #         {
        #         "0": "mu_BH",
        #         "1": "/d",
        #         "2": 6.25,
        #         "3": "",
        #         "4": "",
        #         "5": "Maximum specific growth rate, heterotrophs",
        #         "6": ""
        #         },
        #         {
        #         "0": "b_LH",
        #         "1": "/d",
        #         "2": 0.408,
        #         "3": "",
        #         "4": "",
        #         "5": "Decay coefficient, heterotrophs",
        #         "6": ""
        #         },
        #         {
        #         "0": "Y_H",
        #         "1": "mg/mg",
        #         "2": 0.6,
        #         "3": "",
        #         "4": "",
        #         "5": "Heterotrophic yield",
        #         "6": "mg biomass COD formed/mg substrate COD removed"
        #         },
        #         {
        #         "0": "eta_Y",
        #         "1": "-",
        #         "2": 0.9,
        #         "3": "",
        #         "4": "",
        #         "5": "Anoxic yield factor",
        #         "6": ""
        #         },
        #         {
        #         "0": "eta_g",
        #         "1": "-",
        #         "2": 0.8,
        #         "3": "",
        #         "4": "",
        #         "5": "Anoxic growth factor, R17, R18",
        #         "6": ""
        #         },
        #         {
        #         "0": "eta_g2",
        #         "1": "-",
        #         "2": 0.28,
        #         "3": "",
        #         "4": "",
        #         "5": "Anoxic growth factor, R2",
        #         "6": ""
        #         },
        #         {
        #         "0": "eta_g3",
        #         "1": "-",
        #         "2": 0.16,
        #         "3": "",
        #         "4": "",
        #         "5": "Anoxic growth factor, R3",
        #         "6": ""
        #         },
        #         {
        #         "0": "eta_g4",
        #         "1": "-",
        #         "2": 0.35,
        #         "3": "",
        #         "4": "",
        #         "5": "Anoxic growth factor, R4",
        #         "6": ""
        #         },
        #         {
        #         "0": "eta_g5",
        #         "1": "-",
        #         "2": 0.35,
        #         "3": "",
        #         "4": "",
        #         "5": "Anoxic growth factor, R5",
        #         "6": ""
        #         },
        #         {
        #         "0": "K_S1",
        #         "1": "mg/L",
        #         "2": 20,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for substrate, R1",
        #         "6": "mg/L, as COD"
        #         },
        #         {
        #         "0": "K_S2",
        #         "1": "mg/L",
        #         "2": 20,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for substrate, R2",
        #         "6": "mg/L, as COD"
        #         },
        #         {
        #         "0": "K_S3",
        #         "1": "mg/L",
        #         "2": 20,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for substrate, R3",
        #         "6": "mg/L, as COD"
        #         },
        #         {
        #         "0": "K_S4",
        #         "1": "mg/L",
        #         "2": 20,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for substrate, R4",
        #         "6": "mg/L, as COD"
        #         },
        #         {
        #         "0": "K_S5",
        #         "1": "mg/L",
        #         "2": 40,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for substrate, R5",
        #         "6": "mg/L, as COD"
        #         },
        #         {
        #         "0": "K_OH1",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for O2, heterotrophs, R1",
        #         "6": "mg/L, as O2"
        #         },
        #         {
        #         "0": "K_OH2",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for O2, heterotrophs, R2",
        #         "6": "mg/L, as O2"
        #         },
        #         {
        #         "0": "K_OH3",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for O2, heterotrophs, R3",
        #         "6": "mg/L, as O2"
        #         },
        #         {
        #         "0": "K_OH4",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for O2, heterotrophs, R4",
        #         "6": "mg/L, as O2"
        #         },
        #         {
        #         "0": "K_OH5",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for O2, heterotrophs, R5",
        #         "6": "mg/L, as O2"
        #         },
        #         {
        #         "0": "K_NO3",
        #         "1": "mg/L",
        #         "2": 0.2,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for nitrate-nitrogen, heterotrophs",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_NO2",
        #         "1": "mg/L",
        #         "2": 0.2,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for nitrite-nitrogen, heterotrophs",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_NO",
        #         "1": "mg/L",
        #         "2": 0.05,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for nitric oxide-nitrogen, heterotrophs",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_N2O",
        #         "1": "mg/L",
        #         "2": 0.05,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for nitrous oxide-nitrogen, heterotrophs",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I3NO",
        #         "1": "mg/L",
        #         "2": 0.5,
        #         "3": "",
        #         "4": "",
        #         "5": "Nitric oxide inhibition coefficient, R3",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I4NO",
        #         "1": "mg/L",
        #         "2": 0.3,
        #         "3": "",
        #         "4": "",
        #         "5": "Nitric oxide inhibition coefficient, R4",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I5NO",
        #         "1": "mg/L",
        #         "2": 0.075,
        #         "3": "",
        #         "4": "",
        #         "5": "Nitric oxide inhibition coefficient, R5",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_6NO3",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for nitrate-nitrogen, ANRA R6",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I6NO2",
        #         "1": "mg/L",
        #         "2": 0.05,
        #         "3": "",
        #         "4": "",
        #         "5": "Nitrite inhibition coefficient, ANRA R6",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I6NH",
        #         "1": "mg/L",
        #         "2": 0.05,
        #         "3": "",
        #         "4": "",
        #         "5": "Ammonia inhibition coefficient, ANRA R6",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_7NO2",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for nitrite-nitrogen, ANRA R7",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I7NH",
        #         "1": "mg/L",
        #         "2": 0.05,
        #         "3": "",
        #         "4": "",
        #         "5": "Ammonia inhibition coefficient, ANRA R7",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "mu_BA1",
        #         "1": "/d",
        #         "2": 0.78,
        #         "3": "",
        #         "4": "",
        #         "5": "Maximum specific growth rate, AOB",
        #         "6": ""
        #         },
        #         {
        #         "0": "mu_BA2",
        #         "1": "/d",
        #         "2": 0.78,
        #         "3": "",
        #         "4": "",
        #         "5": "Maximum specific growth rate, NOB (autotrophic)",
        #         "6": ""
        #         },
        #         {
        #         "0": "beta_g",
        #         "1": "-",
        #         "2": 6,
        #         "3": "",
        #         "4": "",
        #         "5": "NOB mixotrophic growth factor",
        #         "6": ""
        #         },
        #         {
        #         "0": "b_LA1",
        #         "1": "/d",
        #         "2": 0.096,
        #         "3": "",
        #         "4": "",
        #         "5": "Decay coefficient, AOB",
        #         "6": ""
        #         },
        #         {
        #         "0": "b_LA2",
        #         "1": "/d",
        #         "2": 0.096,
        #         "3": "",
        #         "4": "",
        #         "5": "Decay coefficient, NOB",
        #         "6": ""
        #         },
        #         {
        #         "0": "Y_A1",
        #         "1": "mg/mg",
        #         "2": 0.18,
        #         "3": "",
        #         "4": "",
        #         "5": "Autotrophic yield, AOB",
        #         "6": "mg biomass COD formed/mg nitrogen removed"
        #         },
        #         {
        #         "0": "Y_A2",
        #         "1": "mg/mg",
        #         "2": 0.06,
        #         "3": "",
        #         "4": "",
        #         "5": "Autotrophic yield, NOB",
        #         "6": "mg biomass COD formed/mg nitrogen removed"
        #         },
        #         {
        #         "0": "K_FA",
        #         "1": "mg/L",
        #         "2": 0.0075,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for free ammonia",
        #         "6": ""
        #         },
        #         {
        #         "0": "K_FNA",
        #         "1": "mg/L",
        #         "2": 0.0001,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for free nitrous acid",
        #         "6": ""
        #         },
        #         {
        #         "0": "K_S11",
        #         "1": "mg/L",
        #         "2": 20,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for substrate, SS, R11",
        #         "6": "mg/L, as COD"
        #         },
        #         {
        #         "0": "K_OA1",
        #         "1": "mg/L",
        #         "2": 0.6,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for O2, AOB",
        #         "6": "mg/L, as O2"
        #         },
        #         {
        #         "0": "K_OA2",
        #         "1": "mg/L",
        #         "2": 1.2,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for O2, NOB",
        #         "6": "mg/L, as O2"
        #         },
        #         {
        #         "0": "K_I9FA",
        #         "1": "mg/L",
        #         "2": 1,
        #         "3": "",
        #         "4": "",
        #         "5": "Free ammonia inhibition coefficient, R9",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I9FNA",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Free nitrous acid inhibition coefficient, R9",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I10FA",
        #         "1": "mg/L",
        #         "2": 0.2,
        #         "3": "",
        #         "4": "",
        #         "5": "Free ammonia inhibition coefficient, R10",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "K_I10FNA",
        #         "1": "mg/L",
        #         "2": 0.04,
        #         "3": "",
        #         "4": "",
        #         "5": "Free nitrous acid inhibition coefficient, R10",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "f_D",
        #         "1": "mg/mg",
        #         "2": 0.08,
        #         "3": "",
        #         "4": "",
        #         "5": "Fraction active biomass contributing to biomass debris",
        #         "6": "mg debris COD/mg biomass COD"
        #         },
        #         {
        #         "0": "i_NXB",
        #         "1": "mg/mg",
        #         "2": 0.086,
        #         "3": "",
        #         "4": "",
        #         "5": "Mass of nitrogen per mass of COD in active biomass",
        #         "6": "mg N/mg COD in active biomass"
        #         },
        #         {
        #         "0": "i_NXD",
        #         "1": "mg/mg",
        #         "2": 0.06,
        #         "3": "",
        #         "4": "",
        #         "5": "Mass of nitrogen per mass of COD in biomass debris",
        #         "6": "mg N/mg COD in biomass debris"
        #         },
        #         {
        #         "0": "eta_h",
        #         "1": "-",
        #         "2": 0.4,
        #         "3": "",
        #         "4": "",
        #         "5": "Anoxic hydrolysis factor",
        #         "6": ""
        #         },
        #         {
        #         "0": "k_a",
        #         "1": "L/mg/h",
        #         "2": 0.1608,
        #         "3": "",
        #         "4": "",
        #         "5": "Ammonification rate coefficient",
        #         "6": "L/(mg biomass COD * h)"
        #         },
        #         {
        #         "0": "K_X",
        #         "1": "mg/mg",
        #         "2": 0.15,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for hydrolysis of slowly biodegradable substrate",
        #         "6": "mg COD/mg biomass COD"
        #         },
        #         {
        #         "0": "K_N1",
        #         "1": "mg/L",
        #         "2": 0.1,
        #         "3": "",
        #         "4": "",
        #         "5": "Half-saturation coefficient for NH3, heterotrophs",
        #         "6": "mg/L, as nitrogen"
        #         },
        #         {
        #         "0": "k_h",
        #         "1": "mg/mg/d",
        #         "2": 2.208,
        #         "3": "",
        #         "4": "",
        #         "5": "Hydrolysis coefficient",
        #         "6": "mg COD/(mg biomass COD * d)"
        #         }
        #     ]
        #     }
        # """,
    )

    # pdf_file_list: list = [pdf for pdf in listdir("pdf") if pdf.endswith(".pdf")]
    # # ic(pdf_file_list)

    # for pdf_file in pdf_file_list:
    #     main(pdf_file)
