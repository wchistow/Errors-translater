from message_translater import translate_message

err_message = []

for _ in range(5):
    err_message.append(input().strip())

print(translate_message(err_message))
