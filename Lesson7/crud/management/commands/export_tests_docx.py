import inspect
import unittest

from django.core.management.base import BaseCommand
from django.test.runner import DiscoverRunner
from docx import Document
from docx.shared import Pt


def iter_tests(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_tests(item)
        else:
            yield item


class Command(BaseCommand):
    help = "Запускает все тесты проекта и записывает их (код + результат) в Word-файл"

    def add_arguments(self, parser):
        parser.add_argument("--output", default="tests_report.docx")

    def handle(self, *args, **options):
        runner = DiscoverRunner(verbosity=0)
        runner.setup_test_environment()
        suite = runner.build_suite(None)
        tests = list(iter_tests(suite))

        old_config = runner.setup_databases()
        result = unittest.TestResult()
        suite.run(result)
        runner.teardown_databases(old_config)
        runner.teardown_test_environment()

        failed = {t.id(): tb for t, tb in result.failures}
        errored = {t.id(): tb for t, tb in result.errors}

        doc = Document()
        doc.add_heading("Отчёт по тестам Django-проекта", level=0)
        doc.add_paragraph(
            f"Всего тестов: {result.testsRun}. "
            f"Провалено: {len(failed)}. Ошибок: {len(errored)}."
        )

        for test in tests:
            test_id = test.id()
            method = getattr(type(test), test._testMethodName)

            if test_id in failed:
                status = "FAIL"
            elif test_id in errored:
                status = "ERROR"
            else:
                status = "OK"

            doc.add_heading(test_id, level=2)
            doc.add_paragraph(f"Статус: {status}")
            if method.__doc__:
                doc.add_paragraph(f"Описание: {method.__doc__.strip()}")

            code = doc.add_paragraph().add_run(inspect.getsource(method))
            code.font.name = "Courier New"
            code.font.size = Pt(9)

            if status != "OK":
                tb = failed.get(test_id) or errored.get(test_id)
                doc.add_paragraph(tb)

        doc.save(options["output"])
        self.stdout.write(self.style.SUCCESS(f"Готово: {options['output']}"))
