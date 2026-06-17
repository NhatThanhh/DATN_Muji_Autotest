import allure
import pytest
from pages.login_page import LoginPage
from utils.data_reader import read_json


# =========================
# Đọc dữ liệu test
# =========================

login_data = read_json("login_data.json")["login_test_data"]

login_cases = login_data["test_cases"]

login_case_map = {
    case["testId"]: case for case in login_cases
}


# =========================
# DN_01 - Đăng nhập với tài khoản hợp lệ
# =========================

@allure.epic("Xác thực người dùng")
@allure.story("Đăng nhập")
@allure.title("DN_01 - Đăng nhập với tài khoản hợp lệ")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_with_valid_account(page, base_url):
    test_data = login_case_map["DN_01"]
    login_page = LoginPage(page, base_url)

    with allure.step("Mở trang chủ MUJI"):
        login_page.open()

    with allure.step("Nhập email và mật khẩu hợp lệ"):
        login_page.login_by_data(test_data)

    with allure.step("Kiểm tra đăng nhập thành công"):
        login_page.expect_login_success()


# =========================
# DN_02 - Đăng nhập với email chưa đăng ký
# =========================

@allure.epic("Xác thực người dùng")
@allure.story("Đăng nhập")
@allure.title("DN_02 - Đăng nhập với email chưa đăng ký")
@allure.severity(allure.severity_level.NORMAL)
def test_login_with_unregistered_email(page, base_url):
    test_data = login_case_map["DN_02"]
    login_page = LoginPage(page, base_url)

    with allure.step("Mở trang chủ MUJI"):
        login_page.open()

    with allure.step("Nhập email chưa đăng ký và mật khẩu"):
        login_page.login_by_data(test_data)

    with allure.step("Kiểm tra đăng nhập thất bại và hiển thị thông báo lỗi"):
        login_page.expect_login_failure(
            test_data["expectedMessage"]
        )

# DN_03 -> DN_10: Đăng nhập thất bại
invalid_login_test_ids = ["DN_03", "DN_04", "DN_05", "DN_06", "DN_07", "DN_08", "DN_09", "DN_10"]

invalid_login_case_map = {
    test_id: login_case_map[test_id]
    for test_id in invalid_login_test_ids
}

@allure.epic("Xác thực người dùng")
@allure.story("Đăng nhập")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize( "test_id", invalid_login_test_ids, ids=invalid_login_test_ids)
def test_login_with_invalid_data(page, base_url, test_id):
    test_data = invalid_login_case_map[test_id]
    login_page = LoginPage(page, base_url)
    allure.dynamic.title(f"{test_data['testId']} - {test_data['description']}")

    with allure.step("Mở trang chủ MUJI"):
        login_page.open()

    with allure.step(f"Nhập dữ liệu cho test case {test_data['testId']}"):
        login_page.login_by_data(test_data)

    with allure.step("Kiểm tra đăng nhập thất bại và hiển thị thông báo lỗi"):
        login_page.expect_login_failure(
            test_data["expectedMessage"]
        )