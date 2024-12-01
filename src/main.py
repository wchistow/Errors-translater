from message_translater import translate_message

raw_err_message = []

last_line = ''
line = ''

while True:
    line = input().strip()

    if last_line == '' and line == '':
        break

    raw_err_message.append(line)

    last_line = line

err_message = []
for line in raw_err_message:
    if line:
        err_message.append(line)

print(translate_message(err_message))
