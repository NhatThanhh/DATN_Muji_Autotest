import os
import shutil
from datetime import datetime
import pytest

try:
    import allure
    HAS_ALLURE = True
except ImportError:
    HAS_ALLURE = False


# =========================
# Cấu hình thư mục report
# =========================

REPORTS_DIR = "reports"

# Nơi pytest + allure-pytest ghi kết quả test
ALLURE_RESULTS_DIR = os.path.join(REPORTS_DIR, "allure-results")

# Nơi lưu report HTML sau khi chạy lệnh allure generate
ALLURE_REPORT_DIR = os.path.join(REPORTS_DIR, "allure-report")

# Nơi lưu screenshot khi test fail
SCREENSHOTS_DIR = os.path.join(ALLURE_RESULTS_DIR, "screenshots")

# Folder history do Allure tạo ra sau khi generate report
ALLURE_REPORT_HISTORY_DIR = os.path.join(ALLURE_REPORT_DIR, "history")

# Folder history cần nằm trong allure-results để Allure đọc được ở lần generate tiếp theo
ALLURE_RESULTS_HISTORY_DIR = os.path.join(ALLURE_RESULTS_DIR, "history")


# =========================
# Tạo timestamp cho lần chạy test
# =========================

def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config._test_run_timestamp = timestamp


# =========================
# Chuẩn bị allure-results trước khi chạy test
# =========================

def pytest_sessionstart(session):
    temp_history_dir = os.path.join(REPORTS_DIR, "temp-history")

    # Xoá temp-history cũ nếu có
    if os.path.exists(temp_history_dir):
        shutil.rmtree(temp_history_dir)

    # Backup history cũ từ allure-report/history nếu đã có report trước đó
    if os.path.exists(ALLURE_REPORT_HISTORY_DIR):
        shutil.copytree(
            ALLURE_REPORT_HISTORY_DIR,
            temp_history_dir,
            dirs_exist_ok=True
        )
        print("\n[Allure History] Backed up previous history.")
    else:
        print("\n[Allure History] No previous allure-report/history found.")

    # Xoá allure-results cũ để tránh bị dồn result vào tab Retries
    if os.path.exists(ALLURE_RESULTS_DIR):
        shutil.rmtree(ALLURE_RESULTS_DIR)

    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Restore history cũ vào allure-results/history
    if os.path.exists(temp_history_dir):
        shutil.copytree(
            temp_history_dir,
            ALLURE_RESULTS_HISTORY_DIR,
            dirs_exist_ok=True
        )
        print("\n[Allure History] Restored history to allure-results/history.")

# =========================
# Base URL web MUJI
# =========================

@pytest.fixture(scope="session")
def base_url():
    return "https://www.muji.com.vn/vn"


# =========================
# Tạo page fixture
# browser fixture lấy từ pytest-playwright
# =========================

@pytest.fixture
def page(context, base_url):
    page = context.new_page()
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(90000)
    page.goto(base_url, wait_until="domcontentloaded", timeout=90000)
    yield page
    page.close()


# =========================
# Chụp screenshot khi test fail
# Attach screenshot vào Allure
# =========================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page is None:
            return

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        test_name = (
            item.nodeid
            .replace("::", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(".py", "")
        )

        screenshot_path = os.path.join(
            SCREENSHOTS_DIR,
            f"{test_name}_{timestamp}.png"
        )

        page.screenshot(
            path=screenshot_path,
            full_page=True
        )

        if HAS_ALLURE:
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot on failure - {test_name}",
                attachment_type=allure.attachment_type.PNG
            )


# =========================
# Thông báo sau khi chạy xong test
# =========================

def pytest_sessionfinish(session, exitstatus):
    if not os.path.exists(ALLURE_RESULTS_DIR):
        print("\n[Allure] No allure-results folder found.")
        return

    json_files = [
        file for file in os.listdir(ALLURE_RESULTS_DIR)
        if file.endswith("-result.json")
    ]

    if not json_files:
        print("\n[Allure] No Allure result files found.")
        return

    print(f"\n[Allure] Current results are saved in: {ALLURE_RESULTS_DIR}")