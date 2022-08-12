import unittest

from message_translater import translate_message


class MessageTranslaterTestCase(unittest.TestCase):
    def test_normal_error(self):
        error = ['Traceback (most recent call last):',
                 'File "E:\\vladimir\\Python\\errors_translater\\src\\main.py", line 8, in <module>',
                 'while coun != 0:',
                 "NameError: name 'coun' is not defined."]
        good_ans = ['В файле "e:\\vladimir\\python\\errors_translater\\src\\main.py", строке 8:',
                    '  while coun != 0:',
                    "Ошибка имени: имя 'coun' не определено."]

        self.assertEqual(translate_message(error), '\n'.join(good_ans))

    def test_interpreter_error(self):
        error = ['Traceback (most recent call last):',
                 'File "<stdin>", line 1, in <module>',
                 "NameError: name 'coun' is not defined."]
        good_ans = ['В интерпретаторе:',
                    "  Ошибка имени: имя 'coun' не определено."]

        self.assertEqual(translate_message(error), '\n'.join(good_ans))

    def test_two_files_error(self):
        error = ['Traceback (most recent call last):',
                 'File "E:\\vladimir\\Python\\errors_translater\\src\\main.py", line 8, in <module>',
                 'a + b',
                 'File "E:\\vladimir\\Python\\errors_translater\\src\\lib.py", line 8, in <module>',
                 'while coun != 0:',
                 "NameError: name 'coun' is not defined."]
        good_ans = ['В файле "e:\\vladimir\\python\\errors_translater\\src\\main.py", строке 8:',
                    '  a + b',
                    'В файле "e:\\vladimir\\python\\errors_translater\\src\\lib.py", строке 8:',
                    '  while coun != 0:',
                    "Ошибка имени: имя 'coun' не определено."]

        self.assertEqual(translate_message(error), '\n'.join(good_ans))

    def test_multi_parts_error(self):
        error = ['Traceback (most recent call last):',
                 'File "C:/Users/test_usr/main.py", line 7, in email_parse',
                 'raise ValueError()',
                 'ValueError: None',
                 '',
                 'During handling of the above exception, another exception occurred:',
                 '',
                 'Traceback (most recent call last):',
                 'File "C:/Users/test_usr/test.py", line 22, in <module>',
                 'raise ValueError(msg)',
                 'ValueError: wrong email !!!!!f@gma',
                 '',
                 'During handling of the above exception, another exception occurred:',
                 '',
                 'Traceback (most recent call last):',
                 'File "C:/Users/test_usr/test.py", line 22, in <module>',
                 'raise ValueError(msg)',
                 'ValueError: wrong email !!!!!f@gma']

        good_ans = ['В файле "c:/users/test_usr/main.py", строке 7:',
                    '  raise ValueError()',
                    'Ошибка значения',
                    '',
                    'Во время обработки вышеупомянутого исключения произошло следующее исключение:',
                    '',
                    'В файле "c:/users/test_usr/test.py", строке 22:',
                    '  raise ValueError(msg)',
                    'Ошибка значения: wrong email !!!!!f@gma.',
                    '',
                    'Во время обработки вышеупомянутого исключения произошло следующее исключение:',
                    '',
                    'В файле "c:/users/test_usr/test.py", строке 22:',
                    '  raise ValueError(msg)',
                    'Ошибка значения: wrong email !!!!!f@gma.']

        self.assertEqual(translate_message(error), '\n'.join(good_ans))


unittest.main()
