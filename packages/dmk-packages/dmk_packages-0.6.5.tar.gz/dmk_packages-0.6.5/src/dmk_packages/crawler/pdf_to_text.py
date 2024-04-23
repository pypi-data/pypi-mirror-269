import os
import pdftotext

"""
## PDF파일을 Text로 변환 ##
- file_name, pdf_text, update_idx 딕셔너리들을 리스트로 반환
디비 적재시 원하는 키값을 확인

- update 쿼리 작성시 유의사항
다운로드 파일 제일 앞에 where문으로 검색할 인덱스값을 붙어야함
ex. (where문으로 컬럼에서 찾을 인덱스)_파일명.pdf
"""


class PdftoText:
    def pdf_to_text(self, download_path):
        pdf_list = []
        for file in os.listdir(download_path):
            if not file.endswith(".pdf"):
                continue

            pdf_path = os.path.join(download_path, file)
            if os.path.getsize(pdf_path) == 0:
                os.remove(pdf_path)
                continue

            # pdf -> text 변환
            with open(pdf_path, "rb") as f:
                pdf = pdftotext.PDF(f)

            pdf_text = ""
            for page in pdf:
                pdf_text += page

            if len(pdf_text) == 0:
                os.remove(pdf_path)
                continue

            # 디비에 update시 where문으로 찾기위한 인덱스
            update_idx = file.split("_")[0]

            data = {
                "file_name": str(file),
                "pdf_text": pdf_text,
                "update_idx": str(update_idx),
            }
            pdf_list.append(data)
        return pdf_list
