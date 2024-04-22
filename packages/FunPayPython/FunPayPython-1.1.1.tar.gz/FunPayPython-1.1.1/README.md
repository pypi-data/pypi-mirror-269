<img src="https://i.ibb.co/tJKk0QS/Fun-Pay-API-darkmode.png">
<h1 align="center">FunPay API</h1>
<h4 align="center">Библиотека для легкого написания ботов FunPay. (Исправленная версия)</h4>

<h1 align="center">Важные ссылки</h1>
<h4 align="center">
    <a href="https://discord.gg/HNhrWJKz3T">Discord Сервер</a><br>
    <a href="https://pypi.org/project/FunPayPy/">PyPi</a><br>
</h4>

<h1 align="center">Быстрый старт</h1>
<h4 align="center">Пример простого бота, который будет отвечать на сообщение с текстом «привет».</h4>

```python
from FunPayAPI import Account, Runner, types, enums


TOKEN = "<golden_key>"

# Создаем класс аккаунта и сразу же получаем данные аккаунта.
acc = Account(TOKEN).get()

# Создаем класс "прослушивателя" событий.
runner = Runner(acc)


# "Слушаем" события
for event in runner.listen(requests_delay=4):
    # Если событие - новое сообщение
    if event.type is enums.EventTypes.NEW_MESSAGE:
        # Если текст сообщения == "привет" и оно отправлено не нами
        if event.message.text.lower() == "привет" and event.message.author_id != acc.id:
            acc.send_message(event.message.chat_id, "Ну привет...")  # отправляем ответное сообщение
```

<h4 align="center">Пример простого бота, который выдает товар при новом заказе, если в названии заказа есть слово «аккаунт».</h4>

```python
from FunPayAPI import Account, Runner, types, enums


TOKEN = "<golden_key>"

# Создаем класс аккаунта и сразу же получаем данные аккаунта.
acc = Account(TOKEN).get()

# Создаем класс "прослушивателя" событий.
runner = Runner(acc)


# "Слушаем" события
for event in runner.listen(requests_delay=4):
    # Если событие - новый заказ
    if event.type is enums.EventTypes.NEW_ORDER:
        # Если "аккаунт" есть в названии заказа
        if "аккаунт" in event.order.description:
            chat = acc.get_chat_by_name(event.order.buyer_username, True)  # получаем ID чата по никнейму
            acc.send_message(chat.id, f"Привет, {event.order.buyer_username}!\n"
                                      f"Вот твой аккаунт:\n"
                                      f"Почта: mail@somemail.ru\n"
                                      f"Пароль: somepassword!123")  # отправляем ответное сообщение
```

