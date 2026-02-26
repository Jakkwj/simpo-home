import sys

from psutil import virtual_memory

if virtual_memory().total > 33470000000:
    COMPUTER_PATH = "/media/Data/SynologyDrive/GitHub"  # 家里台式机
else:
    COMPUTER_PATH = "/media/Cloud/SynologyDrive/GitHub"  # 座机

sys.path.append(f"{COMPUTER_PATH}/SimpoBackend/backend/litestar")

from asyncio import run as asy_run
from base64 import b64decode
from datetime import datetime
from random import random
from time import time
from traceback import format_exc

from app.api.biomodel.crud.ai.claude import main_two_step as claude_main
from app.api.biomodel.crud.ai.gemini import main_two_step as gemini_main
from app.database.models import (
    BioModel,
    SourcePaper,
)
from app.tasks.task_download.task_download import downloads_input_file_biomodel_task
from app.tasks.task_parse import parse_BioModel_task
from config.config import get_settings

# from funboost import BrokerEnum, boost
from icecream import ic
from loguru import logger
from orjson import loads as ploads
from simpo.biomodel import BioModel as SimpoBioModel

from add_db_paper import get_sync_session

settings = get_settings()


ic.configureOutput(includeContext=True)  # print with line number


async def main(
    result: dict[str, str],
    biomodel_file: str,
    # models: str = "gemini-3-pro-preview",
    models: str = "gemini-3-pro-preview-thinking",
    prompt_content_1_add: str = "",  # 补充的 PROMPT_CONTENT_1
    prompt_content_2_add: str = "",  # 补充的 PROMPT_CONTENT_2
) -> str:
    """这里的 pdf 必须是合并了 SI 后的单文件. 且应该不用再次压缩.
    本地拆解论文时, 可以用更高级的模型
    """
    # biomodel_file = "pdf/Growth, maintenance and product formation of autotrophs in activated sludge: Taking the nitrite-oxidizing bacteria as an example.pdf"
    # biomodel_file = f"pdf/{biomodel_file}"
    if "gemini" in models:
        biomodel_file_gemini = await gemini_main(
            biomodel_file,
            models=models,
            is_skip_SCI_check=True,
            prompt_content_1_add=prompt_content_1_add,
            prompt_content_2_add=prompt_content_2_add,
        )
    else:
        biomodel_file_gemini = await claude_main(
            biomodel_file,
            models=models,
            is_skip_SCI_check=True,
            prompt_content_1_add=prompt_content_1_add,
            prompt_content_2_add=prompt_content_2_add,
        )

    if isinstance(biomodel_file_gemini, str):
        raise ValueError(biomodel_file_gemini)

    try:
        bm_str = await parse_BioModel_task(biomodel_file_gemini)

        biomodel_pickle = b64decode(bm_str)
        bm: SimpoBioModel = ploads(biomodel_pickle)  # 将 pickle 结果解码后加载
        replacer_parameter = bm.replacer[bm.replacer["type"] == "BioParameter"].index.tolist()
        replacer_component = bm.replacer[bm.replacer["type"] == "BioComponent"].index.tolist()

        SessionLocal = get_sync_session()
        session = SessionLocal()

        name = result["DOI"].replace("/", "-")
        version = 0
        state = "Draft"
        current_user_id = 1
        sourcepaper_id = (
            session.query(SourcePaper.id).where(SourcePaper.DOI == result["DOI"]).first()[0]
        )

        session.add(
            BioModel(
                name=name,
                abbreviate=f"empty_{int(time() + random() * 1000)}",  # only Standard needs abbreviate
                replacer_parameter=replacer_parameter,
                replacer_component=replacer_component,
                state=state,  # Draft/Release/Standard
                privacy="Private",  #  Private/Public
                version=version,
                version_counter=0,
                unique_judger=f"{name}|{state}|{version}|{current_user_id}",
                amount_parameter=bm.amount_parameter,
                amount_component=bm.amount_component,
                amount_component_soluble=bm.amount_component_soluble,
                amount_rate=bm.amount_rate,
                amount_composition=bm.amount_composition,
                detail=bm.biomodel_input,
                pickle=biomodel_pickle,
                if_parse_save=True,
                description="",
                creator_id=current_user_id,
                sourcepaper_id=sourcepaper_id,
                created_timestamp=datetime.now(),
            )
        )

        session.query(SourcePaper).filter(SourcePaper.id == sourcepaper_id).update(
            {"is_BioModel": True}
        )

        session.commit()
        session.close()

        return "ok"

    except Exception as error:  # 解析失败, 未通过 Simpo 的解析算法
        logger.error(format_exc())
        logger.error(error)

        if isinstance(
            biomodel_file_gemini, dict
        ):  # 未通过 simpo 算法验证, 但是 AI 已经成功解析成了 json 则尝试导出 excel 模版文件本地修改
            excel_file = f"{result['Title']}.xlsx"
            try:
                await downloads_input_file_biomodel_task(
                    biomodel_detail=biomodel_file_gemini,
                    excel_file=excel_file,
                )

            except Exception as inner_error:
                logger.error(format_exc())
                inner_err = str(inner_error).replace("\n", "").replace("\r", "")
                logger.error(inner_err)
                # raise ValueError(f"BioModel create with AI failed: {inner_err}")
                return "xlsx"

        return "failed"


if __name__ == "__main__":
    ...
    # asy_run(main({}))
    # SessionLocal = get_sync_session()
    # session = SessionLocal()
    # sourcepaper_id = session.query(SourcePaper.id).where(SourcePaper.DOI == "10.1016/j.watres.2008.06.024").first()[0]

    # logger.error(sourcepaper_id)
