import os
import asyncio
import pendulum
from loguru import logger
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
from dotenv import load_dotenv, find_dotenv

"""
## fnguide 크롤러 ##
- 사용 유의사항
해당 크롤러는 가져올 데이터는 일정하지만 카테고리가 상당히 많기때문에(서브카테고리 포함) 필요한 카테고리 elements를 매개변수로 지정
ex. click_cat = (f'//*[@id="resultDivTabs"]/ul/li/button[contains(text(), "{cat}")]')

download경로를 None으로 설정할시 pdf파일은 다운로드 하지 않음

- 사용 : run_fnguide_crawler(카테고리, clickelements, download_path, view)
"""
load_dotenv(dotenv_path=find_dotenv())


class FnguideCrawler:
    DEFAULT_DT = pendulum.yesterday(tz=pendulum.timezone("Asia/Seoul"))

    def __init__(self, date_from=None, date_until=None, login=None):

        _date_from = pendulum.parse(date_from) if date_from else self.DEFAULT_DT
        _date_until = pendulum.parse(date_until) if date_until else self.DEFAULT_DT
        self._date_from = _date_from.to_date_string()
        self._date_until = _date_until.to_date_string()

        self.login_id = os.environ.get(f"{login}_LOGIN_ID")
        self.login_pw = os.environ.get(f"{login}_LOGIN_PW")
        if None in (self.login_id, self.login_pw):
            raise Exception("check your login in .env")

        # 다운로드 에러가 가는 url 리스트
        self.url_e = []

    async def _start_playwright(self, view=True):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=view  # 창띄울지 말지 결정
        )
        self.context = await self.browser.new_context(accept_downloads=True)
        self.page = await self.context.new_page()
        return self

    async def _stop_playwright(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def _set_login_date(self):
        """
        사이트 접속후 로그인 및 기간설정
        """

        # 로그인
        url_fnguide = "https://www.fnguide.com/"
        await self.page.goto(url_fnguide, wait_until="load")
        await asyncio.sleep(2)

        await self.page.fill('input[name="MemberID"]', self.login_id)
        await self.page.fill('input[name="PassWord"]', self.login_pw)
        await self.page.click(".btn--login")
        await asyncio.sleep(2)

        # fnresearch 들어가서 기간설정 후 검색
        await self.page.click(".gnb--1dep > .p1")
        await asyncio.sleep(2)

        await self.page.fill("#frDate", self._date_from)
        await self.page.fill("#toDate", self._date_until)
        await self.page.locator("#srchBtn").click()
        await asyncio.sleep(0.5)

    async def _crawling_fnguide(self, cat, click_cat, download_path):
        """
        해당 카테고리 클릭후 크롤링 및 PDF파일 다운로드
        """
        # 카테고리 클릭
        await self.page.click(click_cat)
        await asyncio.sleep(0.5)

        data_list = []
        while True:
            # 검색결과가 없는 경우
            table = await self.page.query_selector("#resultDivGrid")
            if await table.query_selector(".nodata"):
                break

            rows = await table.query_selector_all("tbody > tr")
            for row in rows:
                tds = await row.query_selector_all("td")
                regist_date = await tds[0].inner_text()
                category_name = cat
                title = await tds[1].inner_text()
                provider = await tds[4].inner_text()
                writer = await tds[3].inner_text()
                url_tag = await tds[1].eval_on_selector(
                    "a", 'element => element.getAttribute("href")'
                )
                url = f"https://www.fnguide.com{url_tag}"

                # 찾은 데이터 list에 append
                data = {
                    "channel_name": "Fnguide",
                    "category_name": category_name,
                    "regist_date": regist_date,
                    "title": title,
                    "writer": writer,
                    "provider": provider,
                    "url": url,
                }
                data_list.append(data)

                # pdf 다운로드
                try:
                    if download_path is None:
                        continue

                    # 이미 다운로드 되어있는 파일 목록
                    url_idx = url.split("bulletkind=")[-1]
                    filename = f"{url_idx}_{regist_date}.pdf"

                    os.chdir(download_path)
                    file_list = os.listdir()

                    # 오류나는 파일과 이미 다운로드가 되어있다면 패스 아니라면 다운로드 진행
                    if (url_tag not in self.url_e) and (filename not in file_list):
                        async with self.page.expect_download(
                            timeout=15000
                        ) as download_info:
                            pdf = await row.query_selector(".btn--get")
                            await pdf.click()

                        download = await download_info.value
                        await download.save_as(download_path + filename)
                        await asyncio.sleep(0.5)

                except PlaywrightTimeoutError:
                    # 오류난 파일의 url_tag 추가
                    logger.error(f"[{cat}][{regist_date}][{title}] download error")
                    self.url_e.append(url_tag)

                    # 다시 실행
                    logger.info(f"[{cat}] rerun")
                    await self._stop_playwright
                    await self.run_fnguide_crawler_async(cat, click_cat, download_path)

            # 반목문 중단 or 다음 페이지
            try:
                await self.page.click(".paging > .btn--next", timeout=1000)
                await asyncio.sleep(0.5)

            except PlaywrightTimeoutError:
                break

        return data_list

    async def run_fnguide_crawler_async(self, cat, click_cat, download_path, view=True):
        """
        fnguide 크롤러 전체적인 실행후 데이터 반환
        """
        await self._start_playwright(view)
        await self._set_login_date()
        data = await self._crawling_fnguide(cat, click_cat, download_path)
        await self._stop_playwright()
        return data
