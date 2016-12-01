import time


class CallDispatcherButton:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.state = False
        self.status = True

    def press(self):
        self.state = True

    def set_end_status(self):
        self.status = False

    def main_cycle(self):
        while self.status:
            if self.state:
                self.cabin_link.start_record_speaker_message()
            time.sleep(self.SLEEP_TIME)



# TODO: Что дальше? Как вообще будем делать? Проверять все время @state на сервере или просто посылать сигнал на сервер
# TODO: при изменении @state, а там он уже будет обрабатываться? Этот же вопрос и для других кнопок и действий.
