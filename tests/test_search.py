import pytest
import allure

from pages.search_page import SearchPage
from utils.data_reader import read_json


search_data = read_json("search_data.json")["search_test_data"]
search_cases = search_data["test_cases"]

search_case_map = {
    case["testId"]: case
    for case in search_cases
}


search_test_ids = [
    "TK_01",
    "TK_02",
    "TK_03",
    "TK_04",
    "TK_05",
    "TK_06",
    "TK_07",
    "TK_08",
    "TK_09",
    "TK_10"
]
# Hàm sinh test data cho test case keyword > 100 kí tự
def prepare_search_test_data(test_data: dict):
    prepared_data = test_data.copy()
    if prepared_data.get("generateKeyword") is True:
        keyword_length = prepared_data.get("keywordLength", 120)
        keyword_char = prepared_data.get("keywordChar", "a")
        generated_keyword = keyword_char * keyword_length
        prepared_data["keyword"] = generated_keyword
        prepared_data["expectedSearchValue"] = generated_keyword
    return prepared_data

@allure.epic("Tìm kiếm sản phẩm")
@allure.story("Tìm kiếm")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "test_id",
    search_test_ids,
    ids=search_test_ids
)
def test_search_function(page, base_url, test_id):
    test_data = prepare_search_test_data(search_case_map[test_id])
    search_page = SearchPage(page, base_url)

    allure.dynamic.title(
        f"{test_data['testId']} - {test_data['description']}"
    )

    allure.dynamic.parameter(
        "test_id",
        test_id,
        mode=allure.parameter_mode.HIDDEN
    )

    with allure.step("Mở trang chủ MUJI"):
        search_page.open()

    with allure.step("Thực hiện tìm kiếm"):
        search_page.search_by_data(test_data)

    with allure.step("Kiểm tra kết quả tìm kiếm"):
        search_page.expect_search_result_by_data(test_data)