import re

from message_translater import translate_message

err_message = []

count = 4
while count != 0:
    line = input().strip()

    if count == 1 and re.match(r'[A-Z]\w+: .+', line) is None:  # Должна быть последняя строка, но это не она.
        err_message.append(line)
        while re.match(r'[A-Z]\w+: .+', line) is None:
            line = input().strip()
            err_message.append(line)
        break

    if re.match(r'File "<stdin>", line \d+, in <module>', line) is not None:
        count -= 1
    err_message.append(line)

    count -= 1

print(translate_message(err_message))
