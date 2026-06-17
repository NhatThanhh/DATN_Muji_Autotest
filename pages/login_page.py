import logging
import re
from playwright.sync_api import expect
from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class LoginPage(BasePage):

    # =========================
    # Locators
    # =========================
    def login_link(self):
        return self.page.locator('div.header-login a[title="Đăng nhập"]')

    def register_link(self):
        return self.page.locator('div.header-login a[title="Đăng ký"]')

    def email_input(self):
        return self.page.get_by_role("textbox", name="Địa chỉ Email *")

    def password_input(self):
        return self.page.get_by_role("textbox", name="Mật khẩu *")

    def login_button(self):
        return self.page.get_by_role("button", name="Đăng nhập")

    def logout_text(self):
        return self.page.get_by_text("Đăng xuất", exact=False).first

    def message_by_text(self, message: str):
        return self.page.get_by_text(message, exact=False).first

    def page_body(self):
        return self.page.locator("body")

    # =========================
    # Debug helpers
    # =========================

    def log_current_page_state(self, action_name: str):
        try:
            logger.info("[LoginPage] %s | URL: %s | Title: %s", action_name, self.page.url, self.page.title())
        except Exception as error:
            logger.warning("[LoginPage] Không thể lấy trạng thái page tại bước '%s'. Error: %s", action_name, error)

    # =========================
    # Actions
    # =========================

    def open(self):
        logger.info("[LoginPage] Mở trang chủ MUJI")
        self.open_path("/")
        self.log_current_page_state("Sau khi mở trang chủ")

    def open_login_form(self):
        logger.info("[LoginPage] Click link Đăng nhập")
        self.click(self.login_link())
        logger.info("[LoginPage] Chờ form đăng nhập hiển thị")
        expect(self.email_input()).to_be_visible(timeout=10000)
        expect(self.password_input()).to_be_visible(timeout=10000)

        self.log_current_page_state("Sau khi mở form đăng nhập")

    def fill_email(self, email: str):
        logger.info("[LoginPage] Nhập email: %s", email)

        self.fill(self.email_input(), email)

    def fill_password(self, password: str):
        logger.info("[LoginPage] Nhập mật khẩu: ******")

        self.fill(self.password_input(), password)

    def submit(self):
        logger.info("[LoginPage] Click button Đăng nhập")

        self.click(self.login_button())

        self.log_current_page_state("Sau khi click button Đăng nhập")

    def login(self, email: str, password: str):
        logger.info("[LoginPage] Bắt đầu flow đăng nhập")

        self.open_login_form()
        self.fill_email(email)
        self.fill_password(password)
        self.submit()

        logger.info("[LoginPage] Đã thực hiện xong thao tác đăng nhập")

    def login_by_data(self, test_data: dict):
        logger.info(
            "[LoginPage] Login bằng test data: %s",
            test_data.get("testId", "No testId")
        )

        self.login(
            email=test_data["email"],
            password=test_data["password"]
        )

    # =========================
    # Assertions
    # =========================

    def expect_login_success(self):
        logger.info("[LoginPage] Verify đăng nhập thành công")
        expect(self.page).to_have_url(re.compile(r"https://www\.muji\.com\.vn/vn/?$"), timeout=10000)
        expect(self.login_link()).to_be_hidden(timeout=10000)
        expect(self.register_link()).to_be_hidden(timeout=10000)
        logger.info("[LoginPage] Verify đăng nhập thành công: PASSED")

    def expect_login_failure(self, expected_message: str):
        logger.info("[LoginPage] Verify đăng nhập thất bại với message: %s", expected_message)
        expect(self.message_by_text(expected_message)).to_be_visible(timeout=5000)
        logger.info("[LoginPage] Verify đăng nhập thất bại: PASSED")

    # =========================
    # Combined actions + assertions
    # =========================

    def login_expect_success(self, email: str, password: str):
        logger.info("[LoginPage] Login expect success")
        self.login(email, password)
        self.expect_login_success()

    def login_expect_failure(self, email: str, password: str, expected_message: str):
        logger.info("[LoginPage] Login expect failure")

        self.login(email, password)
        self.expect_login_failure(expected_message)