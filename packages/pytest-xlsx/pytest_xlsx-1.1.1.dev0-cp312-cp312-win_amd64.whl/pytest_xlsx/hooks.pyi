from _pytest.fixtures import FixtureRequest as FixtureRequest
from pytest_xlsx.file import XlsxItem as XlsxItem

def pytest_xlsx_run_step(item: XlsxItem, request: FixtureRequest): ...
