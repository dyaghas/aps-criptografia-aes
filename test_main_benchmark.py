import pytest
from main import *
from key_expansion import key_expansion


@pytest.mark.parametrize("message, key_expanded, s_box", [
    ("This message shouldn't be visible",
        [
            [
                ['2f', 'a3', 'b1', 'c4'],
                ['5d', '8e', '91', 'f2'],
                ['7c', 'd9', 'e0', '3a'],
                ['4b', '60', 'fc', '19']
            ],
            [
                ['a7', '4', 'b5', '71'],
                ['dd', '53', 'c2', '30'],
                ['a8', '71', '91', 'ab'],
                ['57', '37', 'cb', 'd2']
            ],
            [
                ['a1', '2', 'b3', '77'],
                ['bf', '31', 'a0', '52'],
                ['1d', 'c4', '24', '1e'],
                ['f4', '94', '68', '71']
            ],
            [
                ['a5', '6', 'b7', '73'],
                ['cd', '43', 'd2', '20'],
                ['be', '67', '87', 'bd'],
                ['1', '61', '9d', '84']
            ],
            [
                ['1a', 'b9', '8', 'cc'],
                ['b7', '39', 'a8', '5a'],
                ['e1', '38', 'd8', 'e2'],
                ['8e', 'ee', '12', 'b']],
            [
                ['b4', '17', 'a6', '62'],
                ['2f', 'a1', '30', 'c2'],
                ['ca', '13', 'f3', 'c9'],
                ['c5', 'a5', '59', '40']
            ],
            [
                ['b1', '12', 'a3', '67'],
                ['f2', '7c', 'ed', '1f'],
                ['c3', '1a', 'fa', 'c0'],
                ['6f', 'f', 'f3', 'ea']
            ],
            [
                ['31', '92', '23', 'e7'],
                ['48', 'c6', '57', 'a5'],
                ['44', '9d', '7d', '47'],
                ['ea', '8a', '76', '6f']
            ],
            [
                ['b7', '14', 'a5', '61'],
                ['e8', '66', 'f7', '5'],
                ['ec', '35', 'd5', 'ef'],
                ['7e', '1e', 'e2', 'fb']
            ],
            [
                ['c7', '64', 'd5', '11'],
                ['37', 'b9', '28', 'da'],
                ['e3', '3a', 'da', 'e0'],
                ['91', 'f1', 'd', '14']
            ],
            [
                ['a6', '5', 'b4', '70'],
                ['d6', '58', 'c9', '3b'],
                ['19', 'c0', '20', '1a'],
                ['13', '73', '8f', '96']
            ]
        ],
        s_box_map)
])
def test_encrypt_benchmark(benchmark, message, key_expanded, s_box):
    def benchmarked_function():
        msg_array = text_to_array(message)
        encrypt(msg_array, key_expanded, s_box)
    benchmark(benchmarked_function)
