from test.utilities.env_vars import set_env_vars
from test.utilities.excel import Excel


def test_simple_math_function_with_floats(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set(3.0)
                .range('A2').set(4.0)
                .range('B1').set_formula('=excelbind.add(A1, A2)')
                .range('B2').set_formula('=excelbind.mult(A1, A2)')
                .calculate()
            )

            assert excel.range('B1').value == 7.0
            assert excel.range('B2').value == 12.0


def test_simple_string_concatenation(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set('Hello ')
                .range('A2').set('World!')
                .range('B1').set_formula('=excelbind.concat(A1, A2)')
                .calculate()
            )

            assert excel.range('B1').value == 'Hello World!'


def test_matrix_operations_with_np_ndarray(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set(1.0)
                .range('B1').set(2.0)
                .range('A2').set(1.0)
                .range('B2').set(4.0)
                .range('A3').set_formula('=excelbind.det(A1:B2)')
                .range('A4:B5').set_formula('=excelbind.inv(A1:B2)')
                .calculate()
            )

            assert excel.range('A3').value == 2.0

            assert excel.range('A4').value == 2.0
            assert excel.range('B4').value == -1.0
            assert excel.range('A5').value == -0.5
            assert excel.range('B5').value == 0.5


def test_add_without_type_info(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set(3.0)
                .range('A2').set(4.0)
                .range('B1').set_formula('=excelbind.add_without_type_info(A1, A2)')
                .range('A3').set('Hello ')
                .range('A4').set('world!')
                .range('B2').set_formula('=excelbind.add_without_type_info(A3, A4)')
                .calculate()
            )

            assert excel.range('B1').value == 7.0
            assert excel.range('B2').value == 'Hello world!'


def test_list_output(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set(3.0)
                .range('A2').set(4.0)
                .range('A3').set(5.0)
                .range('D1:D3').set_formula('=excelbind.listify(A1, A2, A3)')
                .calculate()
            )

            assert excel.range('D1').value == 3.0
            assert excel.range('D2').value == 4.0
            assert excel.range('D3').value == 5.0


def test_dict_type(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set('x')
                .range('A2').set('y')
                .range('A3').set('z')
                .range('B1').set(5.0)
                .range('B2').set(6.0)
                .range('B3').set(7.0)
                .range('D1:E2').set_formula('=excelbind.filter_dict(A1:B3, A2)')
                .calculate()
            )

            expected_dict = {'x': 5.0, 'z': 7.0}

            res_keys = sorted([excel.range('D1').value, excel.range('D2').value])
            assert res_keys == sorted(expected_dict.keys())
            assert excel.range('E1').value == expected_dict[excel.range('D1').value]
            assert excel.range('E2').value == expected_dict[excel.range('D2').value]


def test_list_in_various_directions(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set(1.0)
                .range('A2').set(2.0)
                .range('A3').set(3.0)
                .range('B1').set(4.0)
                .range('C1').set(5.0)
                .range('D1').set_formula('=excelbind.dot(A1:A3, A1:C1)')
                .calculate()
            )

            assert excel.range('D1').value == 24.0


def test_no_arg(xll_addin_path):
    with set_env_vars('basic_functions'):
        with Excel() as excel:
            excel.register_xll(xll_addin_path)

            (
                excel.new_workbook()
                .range('A1').set_formula('=excelbind.no_arg()')
                .calculate()
            )

            assert excel.range('A1').value == 'Hello world!'
