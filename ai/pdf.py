import sys

from psutil import virtual_memory

if virtual_memory().total > 33470000000:
    COMPUTER_PATH = "/media/Data/SynologyDrive/GitHub"  # 家里台式机
else:
    COMPUTER_PATH = "/media/Cloud/SynologyDrive/GitHub"  # 座机

sys.path.append(f"{COMPUTER_PATH}/SimpoBackend/backend/litestar")

from os import listdir

from app.api.biomodel.crud.ai.pdf import merge_pdfs
from icecream import ic

ic.configureOutput(includeContext=True)  # print with line number


def main() -> None:
    """把需要合并的 多 个 pdf 放入 pdf/merge 文件夹"""
    pdf_file_list: list = [
        f"pdf/merge/{pdf}" for pdf in listdir("pdf/merge") if pdf.endswith(".pdf")
    ]
    pdf_file_list.sort()
    # pdf_file_list.reverse()
    merge_pdfs(pdf_file_list, "pdf/merge/merged_pdf.pdf")


if __name__ == "__main__":
    main()
