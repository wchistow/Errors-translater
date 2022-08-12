from message_translater import translate_message

err_message = []

last_line = ''
line = ''

while True:
    line = input().strip()

    if last_line == '' and line == '':
        break

    err_message.append(line)

    last_line = line

print(translate_message(err_message))
