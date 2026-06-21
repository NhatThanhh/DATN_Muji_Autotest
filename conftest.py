import os
import shutil
from datetime import datetime

import pytest

try:
    import allure
    HAS_ALLURE = True
except ImportError:
    HAS_ALLURE = False

# Cấu hình thư mục report
REPORTS_DIR = "reports"
ALLURE_RESULTS_DIR = os.path.join(REPORTS_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(REPORTS_DIR, "allure-report")
SCREENSHOTS_DIR = os.path.join(ALLURE_RESULTS_DIR, "screenshots")
TRACES_DIR = os.path.join(ALLURE_RESULTS_DIR, "traces")
ALLURE_REPORT_HISTORY_DIR = os.path.join(ALLURE_REPORT_DIR, "history")
ALLURE_RESULTS_HISTORY_DIR = os.path.join(ALLURE_RESULTS_DIR, "history")

def safe_file_name(nodeid: str) -> str:
    return (
        nodeid
        .replace("::", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(".py", "")
        .replace("[", "_")
        .replace("]", "")
        .replace(" ", "_")
        .replace(":", "_")
    )

def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config._test_run_timestamp = timestamp

def pytest_sessionstart(session):
    temp_history_dir = os.path.join(REPORTS_DIR, "temp-history")
    if os.path.exists(temp_history_dir):
        shutil.rmtree(temp_history_dir)
    if os.path.exists(ALLURE_REPORT_HISTORY_DIR):
        shutil.copytree(
            ALLURE_REPORT_HISTORY_DIR,
            temp_history_dir,
            dirs_exist_ok=True
        )
        print("\n[Allure History] Backed up previous history.")
    else:
        print("\n[Allure History] No previous allure-report/history found.")
    if os.path.exists(ALLURE_RESULTS_DIR):
        shutil.rmtree(ALLURE_RESULTS_DIR)

    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    if os.path.exists(temp_history_dir):
        shutil.copytree(
            temp_history_dir,
            ALLURE_RESULTS_HISTORY_DIR,
            dirs_exist_ok=True
        )
        print("\n[Allure History] Restored history to allure-results/history.")

@pytest.fixture(scope="session")
def base_url():
    return "https://www.muji.com.vn/vn"

@pytest.fixture
def page(context, base_url, request):
    page = None
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    page = context.new_page()
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(90000)

    page.goto(
        base_url,
        wait_until="domcontentloaded",
        timeout=90000
    )

    yield page
    report = getattr(request.node, "rep_call", None)
    test_failed = report.failed if report else False

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    test_name = safe_file_name(request.node.nodeid)

    if test_failed:
        os.makedirs(TRACES_DIR, exist_ok=True)

        trace_path = os.path.join(
            TRACES_DIR,
            f"{test_name}_{timestamp}.zip"
        )
        try:
            context.tracing.stop(path=trace_path)
            print(f"\n[Trace] Saved trace: {trace_path}")
            if HAS_ALLURE:
                allure.attach.file(
                    trace_path,
                    name=f"Playwright trace - {test_name}",
                    attachment_type="application/zip",
                    extension="zip"
                )

        except Exception as error:
            print(f"\n[Trace] Failed to save trace: {error}")

    else:
        try:
            context.tracing.stop()
        except Exception as error:
            print(f"\n[Trace] Failed to stop trace: {error}")

    if page is not None:
        page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page is None:
            return

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        test_name = safe_file_name(item.nodeid)

        screenshot_path = os.path.join(
            SCREENSHOTS_DIR,
            f"{test_name}_{timestamp}.png"
        )

        page.screenshot(
            path=screenshot_path,
            full_page=True
        )

        print(f"\n[Screenshot] Saved screenshot: {screenshot_path}")

        if HAS_ALLURE:
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot on failure - {test_name}",
                attachment_type=allure.attachment_type.PNG
            )

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

    if os.path.exists(TRACES_DIR):
        print(f"[Trace] Failure traces are saved in: {TRACES_DIR}")