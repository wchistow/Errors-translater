import re

from message_translater import translate_message

err_message = []

count = 4
while count != 0:
    line = input().strip()
    if re.match(r'File "<stdin>", line \d+, in <module>', line) is not None:
        print('It is interpreter!')
        count -= 1
    err_message.append(line)

    count -= 1

print(translate_message(err_message))
