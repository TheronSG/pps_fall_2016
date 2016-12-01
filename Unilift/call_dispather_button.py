class CallDispatcherButton:
    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.state = False
# TODO: Что дальше? Как вообще будем делать? Проверять все время @state на сервере или просто посылать сигнал на сервер
# TODO: при изменении @state, а там он уже будет обрабатываться? Этот же вопрос и для других кнопок и действий.
