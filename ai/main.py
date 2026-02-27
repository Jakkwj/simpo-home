import base64
import json
import os
import pathlib
import sys
from asyncio import TaskGroup
from asyncio import run as asy_run
from os import environ, listdir, mkdir, path
from shutil import move
from traceback import format_exc

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from pathlib2 import Path
from psutil import virtual_memory
from simpo import ic  # , logger

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
from prompt import PROMPT_CONTENT, SYSTEM_INSTRUCTION_CLAUDE, SYSTEM_INSTRUCTION_GEMINI

load_dotenv(".env")
QINGYUN_API_KEY_CLAUDE = environ.get("QINGYUN_API_KEY_CLAUDE")
QINGYUN_API_KEY_GEMINI = environ.get("QINGYUN_API_KEY_GEMINI")
N1N_API_KEY_CLAUDE = environ.get("N1N_API_KEY_CLAUDE")
N1N_API_KEY_GEMINI = environ.get("N1N_API_KEY_GEMINI")


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
    api_type: str = "qingyun",
) -> dict[str, str] | None:
    """
    这一步是固定用 gemini 回答

    如果有 resource_json 就直接读取返回, 没有才询问

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

    resource_json = "resource_gemini.json"
    if os.path.exists(resource_json):
        with open(resource_json, encoding="utf-8") as file:
            result = json.load(file)
        return result

    if api_type == "qingyun":
        api_key = QINGYUN_API_KEY_GEMINI
    else:
        api_key = N1N_API_KEY_GEMINI

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    url = f"https://api.qingyuntop.top/v1beta/models/{models}:generateContent?key={api_key}"

    if "gemini-3-" in models:  # and "thinking" in models:
        model_contnet_index: int = 1
    else:
        model_contnet_index: int = 0

    pdf_bytes = pathlib.Path(pdf_path).read_bytes()  # encode the PDF byte
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    contents_list = initial_contents_list_gemini(pdf_base64, PROMPT_CONTENT)

    payload = {  # https://ai.google.dev/api/generate-content?hl=zh-cn#v1beta.GenerationConfig
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION_GEMINI}]},
        "contents": contents_list,
        "generationConfig": {
            "temperature": 0,  # 0~2, 0 最稳定, 2 最创造性, 默认为 1
            # "thinkingConfig": {"includeThoughts": True, "thinkingBudget": 26240},
            "responseMimeType": "application/json",
            "responseSchema": {
                "title": "ResultSchema",
                "type": "object",
                "required": [
                    "Title",
                    "Year",
                    "Journal",
                    "DOI",
                    "Access",
                    "Authors",
                    "Abstract",
                    # "GEMINI_What problem does this paper attempt to solve?",
                    # "GEMINI_How the paper solves this problem?",
                    # "GEMINI_What experiments were done for the paper?",
                    # "GEMINI_What are the points that can be explored further?",
                    # "GEMINI_Summarize the main points of the paper.",
                    # "GEMINI_What are the relevant studies?",
                    # "zh_Abstract",
                    # "GEMINI_zh_What problem does this paper attempt to solve?",
                    # "GEMINI_zh_How the paper solves this problem?",
                    # "GEMINI_zh_What experiments were done for the paper?",
                    # "GEMINI_zh_What are the points that can be explored further?",
                    # "GEMINI_zh_Summarize the main points of the paper.",
                    # "GEMINI_zh_What are the relevant studies?",
                    "GEMINI_What_problem_does_this_paper_attempt_to_solve",
                    "GEMINI_How_the_paper_solves_this_problem",
                    "GEMINI_What_experiments_were_done_for_the_paper",
                    "GEMINI_What_are_the_points_that_can_be_explored_further",
                    "GEMINI_Summarize_the_main_points_of_the_paper",
                    "GEMINI_What_are_the_relevant_studies",
                    "zh_Abstract",
                    "GEMINI_zh_What_problem_does_this_paper_attempt_to_solve",
                    "GEMINI_zh_How_the_paper_solves_this_problem",
                    "GEMINI_zh_What_experiments_were_done_for_the_paper",
                    "GEMINI_zh_What_are_the_points_that_can_be_explored_further",
                    "GEMINI_zh_Summarize_the_main_points_of_the_paper",
                    "GEMINI_zh_What_are_the_relevant_studies",
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
                    # "GEMINI_What problem does this paper attempt to solve?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_How the paper solves this problem?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_What experiments were done for the paper?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_What are the points that can be explored further?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_Summarize the main points of the paper.": {
                    #     "type": "string",
                    # },
                    # "GEMINI_What are the relevant studies?": {
                    #     "type": "string",
                    # },
                    # "zh_Abstract": {
                    #     "type": "string",
                    # },
                    # "GEMINI_zh_What problem does this paper attempt to solve?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_zh_How the paper solves this problem?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_zh_What experiments were done for the paper?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_zh_What are the points that can be explored further?": {
                    #     "type": "string",
                    # },
                    # "GEMINI_zh_Summarize the main points of the paper.": {
                    #     "type": "string",
                    # },
                    # "GEMINI_zh_What are the relevant studies?": {
                    #     "type": "string",
                    # },
                    "GEMINI_What_problem_does_this_paper_attempt_to_solve": {
                        "type": "string",
                    },
                    "GEMINI_How_the_paper_solves_this_problem": {
                        "type": "string",
                    },
                    "GEMINI_What_experiments_were_done_for_the_paper": {
                        "type": "string",
                    },
                    "GEMINI_What_are_the_points_that_can_be_explored_further": {
                        "type": "string",
                    },
                    "GEMINI_Summarize_the_main_points_of_the_paper": {
                        "type": "string",
                    },
                    "GEMINI_What_are_the_relevant_studies": {
                        "type": "string",
                    },
                    "zh_Abstract": {
                        "type": "string",
                    },
                    "GEMINI_zh_What_problem_does_this_paper_attempt_to_solve": {
                        "type": "string",
                    },
                    "GEMINI_zh_How_the_paper_solves_this_problem": {
                        "type": "string",
                    },
                    "GEMINI_zh_What_experiments_were_done_for_the_paper": {
                        "type": "string",
                    },
                    "GEMINI_zh_What_are_the_points_that_can_be_explored_further": {
                        "type": "string",
                    },
                    "GEMINI_zh_Summarize_the_main_points_of_the_paper": {
                        "type": "string",
                    },
                    "GEMINI_zh_What_are_the_relevant_studies": {
                        "type": "string",
                    },
                },
            },
        },
    }
    # with open("payload_gemini.json", "w") as file:
    #     json.dump(payload, file, ensure_ascii=False, indent=4)
    payload = json.dumps(payload)

    response_text_: str = ""
    retry_counter: int = 1
    result = None

    while True:
        try:
            async with ClientSession(
                timeout=ClientTimeout(total=600)
            ) as session:  # 最长等待 600s 10 min
                async with session.post(url, headers=headers, data=payload) as response:
                    response_text_ = await response.text()

            __ = json.loads(response_text_)
            logger.info(str(__))
            result = json.loads(
                __["candidates"][0]["content"]["parts"][model_contnet_index]["text"]
            )
            with open(resource_json, "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            # logger.info(result)
            break

        except Exception:
            exc = str(format_exc())
            if "TimeoutError" not in exc:
                logger.error(exc)
            # logger.error(
            #     f"Retrying to get Resource from Gemini ({retry_counter}/5): {response_text_}"
            # )
            if retry_counter >= 1:  # 成功率太低了, 直接尝试一次, 不行就算了
                logger.error("Failed to get Resource from Gemini, please try again.")
                break
            retry_counter += 1

    return result


async def get_resource_claude(
    pdf_path: str,
    models: str,
    api_type: str = "qingyun",
) -> dict[str, str] | None:
    """
    这一步是固定用 claude 回答

    claude 要求:
    页数限制: 100 页
    大小限制: 32MB (Base64 编码后)


    如果有 resource_json 就直接读取返回, 没有才询问
    claude-opus-4-6-thinking 不能用, 因为: Thinking may not be enabled when tool_choice forces tool use
    claude-opus-4-6 不能用, 因为读不了 pdf 的 base64
    claude-sonnet-4-6 可以用，
    claude-3-5-haiku-20241022 测试时使用

    claude 的 input_schema 的字段 不能有 空格 ? .
    """

    resource_json = "resource_claude.json"
    if os.path.exists(resource_json):
        with open(resource_json, encoding="utf-8") as file:
            result = json.load(file)
        return result

    if api_type == "qingyun":
        api_key = QINGYUN_API_KEY_CLAUDE
        url = "https://api.qingyuntop.top/v1/messages"
    else:
        api_key = N1N_API_KEY_CLAUDE
        url = "https://api.n1n.ai/v1/messages"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    pdf_bytes = pathlib.Path(pdf_path).read_bytes()  # encode the PDF byte
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    contents_list = initial_contents_list_claude(pdf_base64, PROMPT_CONTENT)

    payload = {  # https://qingyuntop.apifox.cn/api-417649567
        "model": models,
        # "max_tokens": 4096,
        "temperature": 0,  # 对应 Gemini 的 temperature 0
        "system": SYSTEM_INSTRUCTION_CLAUDE,  # 对应 Gemini 的 systemInstruction
        "messages": contents_list,
        "tool_choice": {  # 强制模型必须使用这个工具，从而强制输出 JSON
            "type": "tool",
            "name": "ResultSchema",
        },
        "tools": [  # 定义工具，结构直接映射 Gemini 的 responseSchema
            {
                "name": "ResultSchema",
                "input_schema": {
                    "type": "object",
                    "required": [
                        # "Q1",
                        # "Q2",
                        # "Q3",
                        # "Q4",
                        # "Q5",
                        # "Q6",
                        "CLAUDE_What_problem_does_this_paper_attempt_to_solve",
                        "CLAUDE_How_the_paper_solves_this_problem",
                        "CLAUDE_What_experiments_were_done_for_the_paper",
                        "CLAUDE_What_are_the_points_that_can_be_explored_further",
                        "CLAUDE_Summarize_the_main_points_of_the_paper",
                        "CLAUDE_What_are_the_relevant_studies",
                        "CLAUDE_zh_What_problem_does_this_paper_attempt_to_solve",
                        "CLAUDE_zh_How_the_paper_solves_this_problem",
                        "CLAUDE_zh_What_experiments_were_done_for_the_paper",
                        "CLAUDE_zh_What_are_the_points_that_can_be_explored_further",
                        "CLAUDE_zh_Summarize_the_main_points_of_the_paper",
                        "CLAUDE_zh_What_are_the_relevant_studies",
                    ],
                    "properties": {
                        "CLAUDE_What_problem_does_this_paper_attempt_to_solve": {
                            "type": "string",
                        },
                        "CLAUDE_How_the_paper_solves_this_problem": {
                            "type": "string",
                        },
                        "CLAUDE_What_experiments_were_done_for_the_paper": {
                            "type": "string",
                        },
                        "CLAUDE_What_are_the_points_that_can_be_explored_further": {
                            "type": "string",
                        },
                        "CLAUDE_Summarize_the_main_points_of_the_paper": {
                            "type": "string",
                        },
                        "CLAUDE_What_are_the_relevant_studies": {
                            "type": "string",
                        },
                        "CLAUDE_zh_What_problem_does_this_paper_attempt_to_solve": {
                            "type": "string",
                        },
                        "CLAUDE_zh_How_the_paper_solves_this_problem": {
                            "type": "string",
                        },
                        "CLAUDE_zh_What_experiments_were_done_for_the_paper": {
                            "type": "string",
                        },
                        "CLAUDE_zh_What_are_the_points_that_can_be_explored_further": {
                            "type": "string",
                        },
                        "CLAUDE_zh_Summarize_the_main_points_of_the_paper": {
                            "type": "string",
                        },
                        "CLAUDE_zh_What_are_the_relevant_studies": {
                            "type": "string",
                        },
                    },
                },
            }
        ],
    }
    # with open("payload_claude.json", "w") as file:
    #     json.dump(payload, file, ensure_ascii=False, indent=4)
    payload = json.dumps(payload)

    response_text_: str = ""
    retry_counter: int = 1
    result = None

    while True:
        try:
            async with ClientSession(
                timeout=ClientTimeout(total=600)
            ) as session:  # 最长等待 600s 10 min
                async with session.post(url, headers=headers, data=payload) as response:
                    response_text_ = await response.text()

            __ = json.loads(response_text_)
            logger.info(str(__))
            # with open("log.log", "w") as file:
            #     file.write(str(__))
            result = __["content"][0]["input"]
            with open(resource_json, "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            # logger.info(result)
            break

        except Exception:
            exc = str(format_exc())
            if "TimeoutError" not in exc:
                logger.error(exc)
            # logger.error(
            #     f"Retrying to get Resource from Claude ({retry_counter}/5): {response_text_}"
            # )
            if retry_counter >= 1:  # 成功率太低了, 直接尝试一次, 不行就算了
                logger.error("Failed to get Resource from Claude, please try again.")
                break
            retry_counter += 1

    return result


async def get_resource(
    pdf_file: str,
    models_gemini: str,
    models_claude: str,
) -> tuple[dict[str, str] | None, dict[str, str] | None]:

    async with TaskGroup() as group:
        task1 = group.create_task(
            get_resource_gemini(
                pdf_file,
                models=models_gemini,
                # api_type="qingyun",
            )
        )
        task2 = group.create_task(
            get_resource_claude(
                pdf_file,
                models=models_claude,
                # api_type="n1n",
            )
        )
    return (
        task1.result(),
        task2.result(),
    )


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
        answer = (
            result[f"{answer_models[answer_model]}{question_key}"]
            if is_en
            else result[f"{answer_models[answer_model]}zh_{question_key}"]
        )
        if answer_model == "Gemini 3.1 Pro":
            answer = answer.replace(" - ", "\n - ")  # Gemini 的回答里经常不换行, 需要手动加上换行

        question += f"""

        ------

        **{answer_model}:**

        {answer}


        """
        # if index < len_ - 1:
        #     question += "\n------\n"

    return question


def get_content(
    answer_models: dict[str, str], result: dict[str, str], access: str, is_en: bool = True
) -> str:
    """根据 is_en 创建中英文内容

    注意:
        1. < 必须 前后有空格
        2. $ 需要转义为 \$
    """

    question_1 = get_question(
        "What_problem_does_this_paper_attempt_to_solve", answer_models, result, is_en
    )
    question_2 = get_question("How_the_paper_solves_this_problem", answer_models, result, is_en)
    question_3 = get_question(
        "What_experiments_were_done_for_the_paper", answer_models, result, is_en
    )
    question_4 = get_question(
        "What_are_the_points_that_can_be_explored_further", answer_models, result, is_en
    )
    question_5 = get_question(
        "Summarize_the_main_points_of_the_paper", answer_models, result, is_en
    )
    question_6 = get_question("What_are_the_relevant_studies", answer_models, result, is_en)

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

        <TabItem value="abstract" label="{"Abstract" if is_en else "摘要"}" >

        {result["Abstract"] if is_en else result["zh_Abstract"]}

        </TabItem>

        <TabItem value="objective" label="{"Objective" if is_en else "目标"}" >

        {"**Q: What problem does this paper attempt to solve?**" if is_en else "**Q：这篇论文试图解决什么问题？**"}

        {question_1}

        </TabItem >

        <TabItem value="solution" label="{"Solution" if is_en else "解决"}" >

        {"**Q: How the paper solves this problem?**" if is_en else "**Q：论文如何解决这个问题？**"}

       {question_2}

        </TabItem >

        <TabItem value="experiment" label="{"Experiment" if is_en else "实验"}" >

        {"**Q: What experiments were done for the paper?**" if is_en else "**Q：论文做了哪些实验？**"}

        {question_3}

        </TabItem >

        <TabItem value="exploration" label="{"Exploration" if is_en else "探索"}" >

        {"**Q: What are the points that can be explored further?**" if is_en else "**Q：有什么可以进一步探索的点？**"}

       {question_4}

        </TabItem >

        <TabItem value="summary" label="{"Summary" if is_en else "总结"}" >

        {"**Q: Summarize the main points of the paper.**" if is_en else "**Q： 总结一下论文的主要内容。**"}

        {question_5}

        </TabItem>

        <TabItem value="related" label="{"Related" if is_en else "相关"}" >


        {"**Q: What are the relevant studies?**" if is_en else "**Q： 有哪些相关研究？**"}

        {question_6}

        </TabItem >

        </Tabs>

    """.replace("        ", "")


def main(
    pdf_file: str,
    # models: str = "gemini-3-pro-preview",
    # models: str = "gemini-3-pro-preview-thinking",
    # models: str = "gemini-3.1-pro-preview",  # 生产环境用这个 2026.02.22
    # answer_model: str = "Gemini 3.1 Pro",
    models_get_BioModel: str = "gemini-3.1-pro-preview",
    # models_get_BioModel: str = "claude-opus-4-6",
    # models: str = "claude-sonnet-4-6",
    # models: str = "claude-3-haiku-20240307",  # 测试用这个
    # answer_model: str = "Claude Opus 4-6",
    prompt_content_1_add: str = "",  # 补充的 PROMPT_CONTENT_1
    prompt_content_2_add: str = "",  # 补充的 PROMPT_CONTENT_2
    is_get_BioModel: bool = True,
):
    """
    更新 生产环境时, 把更改 litestar.env 中的 ENV = production
    生成 resource 的 mdx 文件.
    并尝试生成 BioModel 写入数据库.

    本地拆解论文时, 可以用更高级的模型
    """

    result = None

    answer_models = {
        "Claude Sonnet 4.6": "CLAUDE_",
        # "Claude Haiku 3.5": "CLAUDE_",
        # "Claude Opus 4.6": "CLAUDE_",
        "Gemini 3.1 Pro": "GEMINI_",
    }
    result, result_claude = asy_run(
        get_resource(
            f"pdf/{pdf_file}",
            models_gemini="gemini-3.1-pro-preview",  # 生产环境用这个
            # models_gemini="gemini-3-pro-preview-thinking",
            # models_gemini="gemini-2.5-flash-lite-nothinking",  # 测试时使用
            models_claude="claude-sonnet-4-6",  # 生产环境用这个
            # models_claude="claude-3-5-haiku-20241022",  # 测试时使用
        )
    )

    if result:
        if result_claude:  # 合并结果
            result = result | result_claude
            with open("resource.json", "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)

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

        # 成功后改名备份, 不影响下一次运行
        if path.exists("resource_gemini.json"):
            os.rename("resource_gemini.json", f"resource_gemini_{result_title_}.json")
        if path.exists("resource_claude.json"):
            os.rename("resource_claude.json", f"resource_claude_{result_title_}.json")
        if path.exists("resource.json"):
            os.rename("resource.json", f"resource_{result_title_}.json")

        if is_get_BioModel:
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
                    models_get_BioModel,
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
        # "Competitive dynamics of anaerobes during long-term biological sulfate reduction process in a UASB reactor.pdf"
        # "Development of a kinetic model to evaluate thiosulfate-driven denitriﬁcation and anammox (TDDA) process.pdf"
        # "Development of an Extended ASM3 Model for Predicting the Nitrous Oxide Emissions in a Full-Scale Wastewater Treatment Plant.pdf"
        # "unapproved/Expanding ASM models towards integrated processes for short-cut nitrogen removal and bioplastic recovery.pdf",
        # "Mathematical modeling of simultaneous carbon-nitrogen-sulfur removal from industrial wastewater.pdf"
        # "Modeling Nitrous Oxide Production during Biological Nitrogen Removal via Nitrification and Denitrification: Extensions to the General ASM Models.pdf"
        # "Modelling Methane Production and Sulfate Reduction in Anaerobic Granular Sludge Reactor with Ethanol as Electron Donor.pdf"
        # "Phosphate release involving PAOs activity during anaerobic fermentation of EBPR sludge and the extension of ADM1.pdf"
        # "Physics-informed neural network-based serial hybrid model capturing the hidden kinetics for sulfur-driven autotrophic denitrification proces.pdf"
        # "Quantifying sensitivity and uncertainty analysis of a new mathematical model for the evaluation of greenhouse gas emissions from.pdf"
        # "Simulation of the performance of aerobic granular sludge SBR using modiﬁed ASM3 model.pdf"
        # "Simultaneous removal of sulﬁde, nitrate and acetate under denitrifying sulﬁde removal condition: Modeling and experimental validation.pdf"
        # "Sulfate-reduction, sulﬁde-oxidation and elemental sulfur bioreduction process: Modeling and experimental validation.pdf"
        # "Strategies for mitigating nitrous oxide production and decreasing the carbon footprint of a full-scale combined nitrogen and phosphorus removal activated sludge system.pdf",
        # "An Updated Process Model for Carbon Oxidation, Nitrification, and Denitrification.pdf",
        # "unapproved/Physics-informed neural network-based serial hybrid model capturing the hidden kinetics for sulfur-driven autotrophic denitrification proces.pdf",
        "unapproved/A quantified nitrogen metabolic network by reaction kinetics and mathematical model in a single-stage microaerobic system treating low COD_TN wastewater.pdf",
        # "approved/Mathematical modeling of autotrophic denitriﬁcation (AD) process with sulphide as electron donor.pdf",
        # prompt_content_1_add="""你之前已经提取了一次Component和Parameter，不用重复提取，只需要检查一下即可：
        #     {
        #     "Component": [
        #     ]
        #     }
        # """,
        # models_get_BioModel = "gemini-3.1-pro-preview",
        models_get_BioModel="claude-opus-4-6",
        is_get_BioModel=False,
    )

    # result_claude = asy_run(
    #     get_resource_claude(
    #         "pdf/An Updated Process Model for Carbon Oxidation, Nitrification, and Denitrification.pdf",
    #         models="claude-opus-4-6",
    #     )
    # )
    # ic(result_claude)

    # pdf_file_list: list = [pdf for pdf in listdir("pdf") if pdf.endswith(".pdf")]
    # # ic(pdf_file_list)

    # for pdf_file in pdf_file_list:
    #     main(pdf_file)
