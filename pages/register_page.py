import re
from pages.base_page import BasePage


class RegisterPage(BasePage):

    def email_input(self):
        return self.page.get_by_role("textbox", name="Địa Chỉ Email *")

    def password_input(self):
        return self.page.get_by_role("textbox", name="Mật Khẩu *")

    def phone_input(self):
        return self.page.get_by_role("textbox", name="Nhập số điện thoại")

    def full_name_input(self):
        return self.page.get_by_role("textbox", name="Họ và tên *")

    def date_of_birth_input(self):
        return self.page.get_by_role("textbox", name="Ngày sinh *")

    def gender_dropdown(self):
        return self.page.get_by_role("combobox").filter(has_text="Khác")

    def gender_option(self, gender: str):
        return self.page.get_by_role("option", name=gender)

    def terms_checkbox(self):
        return self.page.get_by_role(
            "checkbox",
            name=re.compile("Tôi trên 16 tuổi")
        )

    def create_account_button(self):
        return self.page.get_by_role("button", name="Tạo Tài Khoản Mới")

    def message_by_text(self, message: str):
        return self.page.get_by_text(message, exact=False)

    def page_body(self):
        return self.page.locator("body")

    # =========================
    # Actions
    # =========================

    def open(self):
        self.open_path("/register")

    def fill_email(self, email: str):
        self.fill(self.email_input(), email)

    def fill_password(self, password: str):
        self.fill(self.password_input(), password)

    def fill_phone(self, phone: str):
        self.fill(self.phone_input(), phone)

    def fill_full_name(self, full_name: str):
        self.fill(self.full_name_input(), full_name)

    def fill_date_of_birth(self, date_of_birth: str):
        self.fill(self.date_of_birth_input(), date_of_birth)

    def select_gender(self, gender: str):
        if not gender:
            return

        self.click(self.gender_dropdown())
        self.click(self.gender_option(gender))

    def accept_terms(self):
        self.check(self.terms_checkbox(), force=True)

    def submit(self):
        self.click(self.create_account_button())

    def register(self, email, password, phone, full_name, date_of_birth, gender):
        self.fill_email(email)
        self.fill_password(password)
        self.fill_phone(phone)
        self.fill_full_name(full_name)
        self.fill_date_of_birth(date_of_birth)
        self.select_gender(gender)
        self.accept_terms()
        self.submit()

    def register_by_data(self, test_data: dict):
        self.register(
            email=test_data["email"],
            password=test_data["password"],
            phone=test_data["phone"],
            full_name=test_data["fullName"],
            date_of_birth=test_data["dateOfBirth"],
            gender=test_data["gender"]
        )