import logging
import re

from playwright.sync_api import expect

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class SearchPage(BasePage):

    # =========================
    # Locators
    # =========================

    def search_input(self):
        return self.page.get_by_role("textbox", name="Search")

    def message_by_text(self, message: str):
        return self.page.get_by_text(message, exact=False).first

    def page_body(self):
        return self.page.locator("body")

    def product_items(self):
        return self.page.locator("h3.product-name a[href^='/vn/product/']")

    # =========================
    # Debug helpers
    # =========================

    def log_current_page_state(self, action_name: str):
        try:
            logger.info(
                "[SearchPage] %s | URL: %s | Title: %s",
                action_name,
                self.page.url,
                self.page.title()
            )
        except Exception as error:
            logger.warning(
                "[SearchPage] Không thể lấy trạng thái page tại bước '%s'. Error: %s",
                action_name,
                error
            )

    def log_search_data(self, keyword: str):
        logger.info("[SearchPage] Keyword tìm kiếm: '%s'", keyword)

    # =========================
    # Actions
    # =========================

    def open(self):
        logger.info("[SearchPage] Mở trang chủ MUJI")

        self.open_path("/")

        expect(
            self.search_input()
        ).to_be_visible(timeout=5000)

        self.log_current_page_state("Sau khi mở trang chủ")

    def click_search_input(self):
        logger.info("[SearchPage] Click vào ô tìm kiếm")

        self.click(self.search_input())

    def fill_search_keyword(self, keyword: str):
        logger.info("[SearchPage] Nhập keyword vào ô tìm kiếm: '%s'", keyword)

        self.fill(self.search_input(), keyword)

    def press_enter(self):
        logger.info("[SearchPage] Nhấn Enter để tìm kiếm")

        self.search_input().press("Enter")

        self.page.wait_for_load_state("domcontentloaded")

        self.log_current_page_state("Sau khi nhấn Enter tìm kiếm")

    def search(self, keyword: str):
        logger.info("[SearchPage] Bắt đầu flow tìm kiếm")
        self.log_search_data(keyword)

        self.click_search_input()
        self.fill_search_keyword(keyword)
        self.press_enter()

        logger.info("[SearchPage] Đã thực hiện xong thao tác tìm kiếm")

    def search_by_data(self, test_data: dict):
        logger.info(
            "[SearchPage] Search bằng test data: %s",
            test_data.get("testId", "No testId")
        )

        self.search(
            keyword=test_data["keyword"]
        )

    # =========================
    # Assertions
    # =========================

    def expect_url_contains(self, expected_text: str):
        logger.info("[SearchPage] Verify URL có chứa: '%s'", expected_text)

        expect(
            self.page
        ).to_have_url(
            re.compile(f".*{re.escape(expected_text)}.*"),
            timeout=10000
        )

        logger.info("[SearchPage] Verify URL contains: PASSED")

    def expect_current_url(self, expected_url: str):
        logger.info("[SearchPage] Verify URL hiện tại là: '%s'", expected_url)

        expect(
            self.page
        ).to_have_url(
            re.compile(re.escape(expected_url) + r"/?$"),
            timeout=10000
        )

        logger.info("[SearchPage] Verify current URL: PASSED")

    def expect_search_value(self, expected_value: str):
        logger.info("[SearchPage] Verify ô search có giá trị: '%s'", expected_value)

        expect(
            self.search_input()
        ).to_have_value(
            expected_value,
            timeout=10000
        )

        logger.info("[SearchPage] Verify search value: PASSED")

    def expect_no_result_message(self, expected_message: str):
        logger.info(
            "[SearchPage] Verify hiển thị thông báo không có kết quả: '%s'",
            expected_message
        )

        expect(
            self.message_by_text(expected_message)
        ).to_be_visible(timeout=10000)

        logger.info("[SearchPage] Verify no result message: PASSED")

    def expect_has_related_result(self, related_keyword: str):
        logger.info(
            "[SearchPage] Verify tiêu đề sản phẩm có liên quan keyword: '%s'",
            related_keyword
        )

        related_product = self.product_items().filter(
            has_text=re.compile(
                re.escape(related_keyword),
                re.IGNORECASE
            )
        ).first
        expect(related_product).to_be_visible(timeout=10000)
        logger.info("[SearchPage] Verify related product title: PASSED")

    def expect_application_not_crash(self):
        logger.info("[SearchPage] Verify ứng dụng không bị crash")

        expect(
            self.page_body()
        ).to_be_visible(timeout=5000)

        logger.info("[SearchPage] Verify application not crash: PASSED")

    def expect_search_success(self, test_data: dict):
        logger.info(
            "[SearchPage] Verify search success cho test case: %s",
            test_data.get("testId", "No testId")
        )

        self.expect_url_contains(test_data["expectedUrlContains"])
        self.expect_search_value(test_data["expectedSearchValue"])
        self.expect_has_related_result(test_data["relatedKeyword"])

        logger.info("[SearchPage] Verify search success: PASSED")

    def expect_search_no_result(self, test_data: dict):
        logger.info(
            "[SearchPage] Verify search no result cho test case: %s",
            test_data.get("testId", "No testId")
        )

        self.expect_url_contains(test_data["expectedUrlContains"])
        self.expect_search_value(test_data["expectedSearchValue"])
        self.expect_no_result_message(test_data["expectedMessage"])

        logger.info("[SearchPage] Verify search no result: PASSED")

    def expect_stay_home(self, test_data: dict):
        logger.info(
            "[SearchPage] Verify search keyword rỗng cho test case: %s",
            test_data.get("testId", "No testId")
        )

        self.expect_application_not_crash()
        self.expect_current_url(test_data["expectedUrl"])

        logger.info("[SearchPage] Verify stay home: PASSED")

    def expect_search_result_by_data(self, test_data: dict):
        expected_result = test_data["expectedResult"]

        logger.info(
            "[SearchPage] Verify search result theo expectedResult: %s",
            expected_result
        )

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