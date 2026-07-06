import re
from playwright.sync_api import expect
from pages.base_page import BasePage


class LoginPage(BasePage):

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

    def message_by_text(self, message: str):
        return self.page.get_by_text(message, exact=False).first

    def open(self):
        self.open_path("/")

    def open_login_form(self):
        self.click(self.login_link())
        expect(self.email_input()).to_be_visible(timeout=10000)
        expect(self.password_input()).to_be_visible(timeout=10000)

    def fill_email(self, email: str):
        self.fill(self.email_input(), email)

    def fill_password(self, password: str):
        self.fill(self.password_input(), password)

    def submit(self):
        self.click(self.login_button())

    def login(self, email: str, password: str):
        self.open_login_form()
        self.fill_email(email)
        self.fill_password(password)
        self.submit()

    def login_by_data(self, test_data: dict):
        self.login(email=test_data["email"], password=test_data["password"])