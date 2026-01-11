import sys

from psutil import virtual_memory

if virtual_memory().total > 33470000000:
    COMPUTER_PATH = "/media/Data/SynologyDrive/GitHub"  # 家里台式机
else:
    COMPUTER_PATH = "/media/Cloud/SynologyDrive/GitHub"  # 座机

sys.path.append(f"{COMPUTER_PATH}/SimpoBackend/backend/litestar")

from datetime import datetime
from os import environ

from app.database.models import SourcePaper
from dotenv import load_dotenv
from icecream import ic
from sqlalchemy import (
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker

load_dotenv(".env")
DATABASE_URL_SYNC = environ.get("DATABASE_URL_SYNC")

ic.configureOutput(includeContext=True)  # print with line number


def get_sync_session():
    engine = create_engine(DATABASE_URL_SYNC)  # 同步引擎, 初始化数据库表时使用
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def re_index():
    """
    如果报:
        psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "sourcepaper_pkey"
        DETAIL:  Key (id)=(6) already exists.

    执行本函数刷新 index
    """
    SessionLocal = get_sync_session()
    session = SessionLocal()
    session.execute(
        text("SELECT setval('sourcepaper_id_seq',(SELECT max(id) FROM sourcepaper))")
    )  # re-index


def main(result: dict[str, str]) -> None:
    """is_BioModel 默认为 False, 如果后续成功解析再自动更改"""
    SessionLocal = get_sync_session()
    session = SessionLocal()

    session.add(
        SourcePaper(
            title=result["Title"],
            issue_year=int(result["Year"]),
            DOI=result["DOI"],
            publisher=result["Journal"],
            creator_id=1,
            created_timestamp=datetime.now(),
            is_BioModel=False,
            is_BioModel_Public=False,
            is_Resource=True,
            is_open_access=True if result["Access"] == "OPEN" else False,
            is_BioModel_approved=False,
            is_Resource_approved=False,
        )
    )
    session.commit()
    session.close()


if __name__ == "__main__":
    ...
    # re_index()
