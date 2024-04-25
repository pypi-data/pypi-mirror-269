import pytest
from wednesday.cpu_6502_spec import CPU6502Spec
from collections import OrderedDict


class InstructionReportPlugin:
    def __init__(self, config):
        self.config = config

    def pytest_sessionstart(session):
        session.results = OrderedDict()

    def pytest_collection_modifyitems(self, config, items):
        # Filter test items to include only those belonging to a specific subclass
        items[:] = [
            item
            for item in items
            if self.is_instance_of_subclass(item, CPU6502Spec)
        ]

    def is_instance_of_subclass(self, item, subclass):
        # Check if the test item is an instance of the specified subclass
        test_class = item.getparent(pytest.Class)
        if test_class is None:
            return False
        return issubclass(test_class.cls, subclass)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        result = outcome.get_result()
        if result.when == 'call':
            item.results[result.nodeid] = result.outcome

    def pytest_sessionfinish(self, session, exitstatus):
        report_data = self.generate_report(session)
        self.save_report(report_data)

    def generate_report(self, session):
        # Generate the report data based on session results
        report_data = {
            'total_tests': session.testscollected,
            'passed_tests': session.testscollected - session.testsfailed,
            'failed_tests': session.testsfailed,
            'test_details': self.get_test_details(),
        }
        return report_data

    def get_test_details(self):
        data = OrderedDict()
        results = OrderedDict()
        headers = []
        for item, outcome in self.results.items():
            _, class_name, method_name = item.split('::')
            if method_name not in data:
                data[method_name] = {}
            if class_name not in headers:
                headers.append(class_name)
            data[method_name][class_name] = outcome

        return headers, data

    def save_report(self, report_data):
        self.save_rst_report(report_data, 
                             'docs/cpu_spec_all_results.rst',
                             name='',
                             all_results=True,
                             )
        self.save_rst_report(report_data,
                             'docs/cpu_spec_failed_results.rst', 
                             name='',
                             all_results=False
                             )

    def save_rst_report(self, report_data, output, name='Test Details', all_results=True):
        # output_file = self.config.getoption("--output")
        headers, data = report_data['test_details']
        emulators = [self.get_header_name(h) for h in headers]
        with open(output, 'w') as rst_file:
            rst_file.write(f'.. csv-table::{name}\n')

            rst_file.write(
                f"   :header: Instruction, {','.join(emulators)}\n\n"
            )
            for test_name, values in data.items():
                vals = [values[h] == 'passed' for h in headers]
                passed = all(vals)
                cols = [self.get_col_value(v) for v in vals]
                desc = self.get_test_description(test_name)
                if all_results or not passed:
                    rst_file.write(f"   {desc},{','.join(cols)}\n")

    def get_col_value(self, value):
        return ':green:`OK`' if value else ':red:`NOT`'

    def get_header_name(self, test_class):
        if test_class == 'ArbneCPUTest':
            return 'Arbne'
        elif test_class == 'ApplepyCPUTest':
            return 'ApplePy'
        elif test_class == 'Py65CPUTest':
            return 'Py65'
        elif test_class == 'PyntendoCPUTest':
            return 'Pyntendo'
        elif test_class == 'Torlus6502Test':
            return '6502js'
        elif test_class == 'JsnesCPUTest':
            return 'JSnes'
        elif test_class == 'Py3nesCPUTest':
            return 'Py3NES'
        raise NotImplementedError(f'Unknow TestClass: {test_class}')

    def get_test_description(self, test_name):
        return test_name[5:].replace('_', ' ')


# Register the plugin
def pytest_configure(config):
    config.pluginmanager.register(
        InstructionReportPlugin(config), 'instruction_report_plugin'
    )
