from playwright.sync_api import expect, Locator


class BasePage:
    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open_path(self, path: str):
        self.page.goto(f"{self.base_url}{path}", wait_until="domcontentloaded", timeout=6000)

    def click(self, locator: Locator):
        locator.click()

    def fill(self, locator: Locator, value: str):
        if value is not None:
            locator.fill(value)

    def check(self, locator: Locator, force: bool = False):
        if not locator.is_checked():
            locator.check(force=force)

    def expect_visible(self, locator: Locator):
        expect(locator).to_be_visible()

    def expect_text_contains(self, locator: Locator, text: str):
        expect(locator).to_contain_text(text)

    def get_body(self):
        return self.page.locator("body")