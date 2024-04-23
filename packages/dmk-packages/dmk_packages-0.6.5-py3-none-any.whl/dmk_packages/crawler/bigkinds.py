import os
import asyncio
import pendulum
from dotenv import load_dotenv, find_dotenv
from playwright.async_api import async_playwright

"""
## bigkinds 크롤러 ##
- 사용 유의사항
해당 크롤러는 bigkinds의 분석결과까지 도달함. 이후에 분석결과의 5가지 종류중 필요한 데이터를 찾아서 다운로드

- 사용 순서
start_playwright > crawling_bigkinds > 원하는 데이터 다운로드 및 디비 적재 > stop_playwright
"""
load_dotenv(dotenv_path=find_dotenv())


class BigkindsCrawler:
    DEFAULT_DT = pendulum.yesterday(tz=pendulum.timezone("Asia/Seoul"))

    def __init__(self, date_from=None, date_until=None, login_env=None):

        _date_from = pendulum.parse(date_from) if date_from else self.DEFAULT_DT
        _date_until = pendulum.parse(date_until) if date_until else self.DEFAULT_DT
        self._date_from = _date_from.to_date_string()
        self._date_until = _date_until.to_date_string()

        self.login_id = os.environ.get(f"{login_env}_LOGIN_ID")
        self.login_pw = os.environ.get(f"{login_env}_LOGIN_PW")
        if None in (self.login_id, self.login_pw):
            raise Exception("check your login in .env")

    async def _start_playwright(self, view=True):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=view)
        self.context = await self.browser.new_context(accept_downloads=True)
        self.page = await self.context.new_page()
        return self

    async def stop_playwright_async(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def crawling_bigkinds_async(self, cat, view=True):
        """
        사이트 접속후 분석결과 페이지까지 도달
        """
        # playwright 실행
        await self._start_playwright(view)

        # 사이트 접속
        url = "https://www.bigkinds.or.kr/v2/news/index.do"
        await self.page.goto(url, wait_until="load")
        await asyncio.sleep(2)

        # 로그인
        await self.page.get_by_role("button", name="로그인").click()
        await asyncio.sleep(0.5)

        await self.page.get_by_placeholder("이메일(E-mail) 주소").fill(self.login_id)
        await self.page.get_by_placeholder("비밀번호를 입력하세요.").fill(self.login_pw)
        await self.page.click("#login-btn")
        await asyncio.sleep(2)

        await self.page.wait_for_selector(
            ".ft-map > div > div > ul > li > a", state="visible"
        )
        await self.page.click(".ft-map > div > div > ul > li > a")
        await asyncio.sleep(2)

        # 기간설정하기
        await self.page.click(".tab-btn")
        date_s = await self.page.query_selector("#search-begin-date")
        date_e = await self.page.query_selector("#search-end-date")
        await asyncio.sleep(0.3)

        await date_s.fill(self._date_from)
        await date_e.fill(self._date_until)

        # 해당되는 카테고리 설정
        await self.page.click(".tab-btn.tab3")
        set_cat = await self.page.query_selector(
            f"xpath=.//span[@data-role='display' and text()='{cat}']"
        )
        await set_cat.click()
        await self.page.get_by_role("button", name="적용하기").click()
        await asyncio.sleep(2)

        # STEP 03 분석결과 버튼 누르기
        await self.page.get_by_role("button", name="분석 결과 및 시각화").click()
        await asyncio.sleep(1)
