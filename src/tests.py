import unittest

from message_translater import translate_message


class MessageTranslaterTestCase(unittest.TestCase):
    def test_normal_error(self):
        error = ['Traceback (most recent call last):',
                 'File "E:\\vladimir\\Python\\errors_translater\\src\\main.py", line 8, in <module>',
                 'while coun != 0:',
                 "NameError: name 'coun' is not defined"]
        good_ans = ['В файле "e:\\vladimir\\python\\errors_translater\\src\\main.py", строке 8:',
                    '  while coun != 0:',
                    "Ошибка имени: имя 'coun' не определено."]

        self.assertEqual(translate_message(error), '\n'.join(good_ans))

    def test_interpreter_error(self):
        error = ['Traceback (most recent call last):',
                 'File "<stdin>", line 1, in <module>',
                 "NameError: name 'coun' is not defined"]
        good_ans = ['В интерпретаторе:',
                    "  Ошибка имени: имя 'coun' не определено."]

        self.assertEqual(translate_message(error), '\n'.join(good_ans))

    def test_two_files_error(self):
        error = ['Traceback (most recent call last):',
                 'File "E:\\vladimir\\Python\\errors_translater\\src\\main.py", line 8, in <module>',
                 'a + b',
                 'File "E:\\vladimir\\Python\\errors_translater\\src\\lib.py", line 8, in <module>',
                 'while coun != 0:',
                 "NameError: name 'coun' is not defined"]
        good_ans = ['В файле "e:\\vladimir\\python\\errors_translater\\src\\main.py", строке 8:',
                    '  a + b',
                    'В файле "e:\\vladimir\\python\\errors_translater\\src\\lib.py", строке 8:',
                    '  while coun != 0:',
                    "Ошибка имени: имя 'coun' не определено."]

        self.assertEqual(translate_message(error), '\n'.join(good_ans))
    
    def test_one_line_error(self):
        error = ["NameError: name 'coun' is not defined"]
        good_ans = "Ошибка имени: имя 'coun' не определено."

        tr_err = translate_message(error)
        print(tr_err)
        self.assertEqual(tr_err, good_ans)


unittest.main()
