import string
import pytest
from task1 import PrintableFile, PrintableFolder
from task2 import Graph
from task3 import ShiftDescriptor

"""
Написать тесты(pytest) к предыдущим 3 заданиям, запустив которые, я бы смог бы проверить их корректность
"""

file3 = PrintableFile('file3')
folder3 = PrintableFolder('folder3', [file3])
file2 = PrintableFile('file2')
folder2 = PrintableFolder('folder2', [folder3, file2])
file1 = PrintableFile('file1')
folder1 = PrintableFolder('folder1', [folder2, file1])
folder1_string = 'V folder1\n|-> V folder2\n|   |-> V folder3\n|   |   |-> file3\n|   |-> file2\n|-> file1'

empty_folder = PrintableFolder('EmptyFolder', [])
empty_folder_string = f'V {empty_folder.name}'
rearranged_folder = PrintableFolder('Swapped_Folder', [file1, folder3])
rearranged_folder_string = 'V Swapped_Folder\n|-> file1\n|-> V folder3\n|   |-> file3'


@pytest.mark.parametrize('file, file_string', [(folder1, folder1_string),
                                               (rearranged_folder, rearranged_folder_string),
                                               (empty_folder, empty_folder_string),
                                               (file1, 'file1')])
def test_str(file, file_string):
    assert str(file) == file_string


@pytest.mark.parametrize('folder, file, in_or_not', [(rearranged_folder, file1, True),
                                                     (empty_folder, file1, False),
                                                     (folder1, file1, True),
                                                     (folder1, folder2, True),
                                                     (folder1, file3, True),
                                                     (folder2, file1, False),
                                                     (folder3, file3, True),
                                                     (folder3, file1, False)])
def test_in(folder, file, in_or_not):
    assert (file in folder) == in_or_not


graph1 = {'A': ['B', 'C', 'D', 'F', 'G'], 'B': ['K', 'L', 'M'], 'C': ['X', 'Y'], 'D': [], 'F': ['E', 'H'],
          'H': ['A'], 'G': [], 'Y': ['W', 'Z'], 'K': [], 'L': [], 'M': [], 'X': [], 'E': [], 'W': [], 'Z': []}
graph1result = 'ABCDFGKLMXYEHWZ'
graph_E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}
graph_E_result = 'ABCD'


@pytest.mark.parametrize('graph, bfs_result', [(Graph(graph1), graph1result),
                                               (Graph(graph_E), graph_E_result)])
def test_task2(graph, bfs_result):
    assert ''.join(graph) == bfs_result


@pytest.mark.parametrize('number', [i for i in range(-100, 100)])
def test_task3(number):
    class CeasarSipher:
        message = ShiftDescriptor(number)
        another_message = ShiftDescriptor(number)

    a = CeasarSipher()
    a.message = 'abc'
    a.another_message = 'hello'
    if number == 4:
        assert a.message == 'efg'
    elif number == 7:
        assert a.another_message == 'olssv'
    elif number == 1:
        assert a.message == 'bcd'
        assert a.another_message == 'ifmmp'
    elif number == -1:
        assert a.message == 'zab'
        assert a.another_message == 'gdkkn'
    else:
        assert all([char in string.ascii_lowercase for char in a.message])
        assert all(char in string.ascii_lowercase for char in a.another_message)
