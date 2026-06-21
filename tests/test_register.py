import allure
from playwright.sync_api import expect
import pytest
from pages.register_page import RegisterPage
from utils.data_reader import read_json

register_data = read_json("register_data.json")["register_test_data"]
register_cases = register_data["test_cases"]
register_case_map = {case["testId"]: case for case in register_cases}
def assert_message_contains(register_page: RegisterPage, expected_message: str):
    for line in expected_message.split("\n"):
        text = line.strip()
        if text:
            message_locator = register_page.page.get_by_text(text,exact=False).first
            expect(message_locator).to_be_visible(timeout=5000)

# DK_01 - Đăng ký với thông tin hợp lệ
@allure.epic("Xác thực người dùng")
@allure.story("Đăng ký")
@allure.title("DK_01 - Đăng ký với thông tin hợp lệ")
def test_dk_01_register_with_valid_information(page, base_url):
    test_data = register_case_map["DK_01"]
    register_page = RegisterPage(page, base_url)
    with allure.step("Mở trang đăng ký"):
        register_page.open()
    with allure.step("Nhập thông tin hợp lệ vào form đăng ký"):
        register_page.register_by_data(test_data)
    with allure.step("Kiểm tra đăng ký thành công và hiển thị thông báo xác nhận email"):
        assert_message_contains(register_page, test_data["expectedMessage"])


# DK_02 - Đăng ký với email đã tồn tại
@allure.epic("Xác thực người dùng")
@allure.story("Đăng ký")
@allure.title("DK_02 - Đăng ký với email đã tồn tại")
def test_dk_02_register_with_existing_email(page, base_url):
    test_data = register_case_map["DK_02"]
    register_page = RegisterPage(page, base_url)
    with allure.step("Mở trang đăng ký"):
        register_page.open()
    with allure.step("Nhập thông tin đăng ký với email đã tồn tại"):
        register_page.register_by_data(test_data)
    with allure.step("Kiểm tra đăng ký thất bại và hiển thị thông báo email đã tồn tại"):
        assert_message_contains(
            register_page,
            test_data["expectedMessage"]
        )


# invalid_test_ids = ["DK_03", "DK_04", "DK_05", "DK_06", "DK_07", "DK_08", "DK_09","DK_10", "DK_11", "DK_12", "DK_13"]
invalid_test_ids = ["DK_09"]
invalid_register_cases = [
    case
    for case in register_data["test_cases"]
    if case["testId"] in invalid_test_ids
]

invalid_register_case_map = {case["testId"]: case for case in invalid_register_cases}

@allure.epic("Xác thực người dùng")
@allure.story("Đăng ký")
@pytest.mark.parametrize("test_id",invalid_test_ids
)
def test_register_with_invalid_data(page, base_url, test_id):
    test_data = invalid_register_case_map[test_id]
    register_page = RegisterPage(page, base_url)
    allure.dynamic.title(f"{test_data['testId']} - {test_data['description']}")
    with allure.step("Mở trang đăng ký"):
        register_page.open()
    with allure.step(f"Nhập dữ liệu cho test case {test_data['testId']}"):
        register_page.register_by_data(test_data)
    with allure.step("Kiểm tra đăng ký thất bại và hiển thị thông báo lỗi"):
        assert_message_contains(
            register_page,
            test_data["expectedMessage"])