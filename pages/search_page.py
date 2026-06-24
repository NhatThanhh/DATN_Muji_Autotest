import re
from playwright.sync_api import expect
from pages.base_page import BasePage

class SearchPage(BasePage):
    def search_input(self):
        return self.page.get_by_role("textbox", name="Search")

    def message_by_text(self, message: str):
        return self.page.get_by_text(message, exact=False).first

    def page_body(self):
        return self.page.locator("body")

    def product_items(self):
        return self.page.locator("h3.product-name a[href^='/vn/product/']")

    def open(self):
        self.open_path("/")
        expect(self.search_input()).to_be_visible(timeout=5000)

    def click_search_input(self):
        self.click(self.search_input())

    def fill_search_keyword(self, keyword: str):
        self.fill(self.search_input(), keyword)

    def press_enter(self):
        self.search_input().press("Enter")

        self.page.wait_for_load_state("domcontentloaded")

    def search(self, keyword: str):
        self.click_search_input()
        self.fill_search_keyword(keyword)
        self.press_enter()

    def search_by_data(self, test_data: dict):
        self.search(keyword=test_data["keyword"])

    def expect_url_contains(self, expected_text: str):
        expect(self.page).to_have_url(re.compile(f".*{re.escape(expected_text)}.*"),timeout=10000)

    def expect_current_url(self, expected_url: str):
        expect(self.page).to_have_url(re.compile(re.escape(expected_url) + r"/?$"),timeout=10000)

    def expect_search_value(self, expected_value: str):
        expect(self.search_input()).to_have_value(expected_value,timeout=10000)

    def expect_no_result_message(self, expected_message: str):
        expect(self.message_by_text(expected_message)).to_be_visible(timeout=10000)

    def expect_has_related_result(self, related_keyword: str):
        related_product = self.product_items().filter(
            has_text=re.compile(
                re.escape(related_keyword),
                re.IGNORECASE
            )
        ).first

        expect(
            related_product
        ).to_be_visible(timeout=10000)

    def expect_application_not_crash(self):
        expect(self.page_body()).to_be_visible(timeout=5000)

    def expect_search_success(self, test_data: dict):
        self.expect_url_contains(test_data["expectedUrlContains"])
        self.expect_search_value(test_data["expectedSearchValue"])
        self.expect_has_related_result(test_data["relatedKeyword"])

    def expect_search_no_result(self, test_data: dict):
        self.expect_url_contains(test_data["expectedUrlContains"])
        self.expect_search_value(test_data["expectedSearchValue"])
        self.expect_no_result_message(test_data["expectedMessage"])

    def expect_stay_home(self, test_data: dict):
        self.expect_application_not_crash()
        self.expect_current_url(test_data["expectedUrl"])

    def expect_search_result_by_data(self, test_data: dict):
        expected_result = test_data["expectedResult"]

        if expected_result == "success":
            self.expect_search_success(test_data)

        elif expected_result == "no_result":
            self.expect_search_no_result(test_data)

        elif expected_result == "stay_home":
            self.expect_stay_home(test_data)

        else:
            raise ValueError(
                f"Không hỗ trợ expectedResult: {expected_result}"
            )