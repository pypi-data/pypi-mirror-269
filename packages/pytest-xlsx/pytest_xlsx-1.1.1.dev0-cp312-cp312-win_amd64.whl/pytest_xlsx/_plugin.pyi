import pytest
from _typeshed import Incomplete as Incomplete
from abc import ABCMeta, abstractmethod
from pytest import FixtureRequest as FixtureRequest
from pytest_xlsx.file import XlsxItem as XlsxItem

class XlsxPlugin(metaclass=ABCMeta):
    config: Incomplete
    def __init__(self, config: pytest.Config) -> None: ...
    @abstractmethod
    def pytest_xlsx_run_step(self, item: XlsxItem, request: FixtureRequest): ...

class PrintXlsxPlugin(XlsxPlugin):
    def pytest_xlsx_run_step(self, item: XlsxItem, request: FixtureRequest): ...

class AllureXlsxPlugin(XlsxPlugin):
    meta_column_name: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def pytest_xlsx_run_step(self, item: XlsxItem, request: FixtureRequest): ...
