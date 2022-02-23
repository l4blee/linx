from enum import Enum
from abc import ABC, abstractclassmethod, abstractproperty

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class ButtonLabels:
    SETTINGS = '⚙Настройки'
    FIND_CHATS = '👥Поиск чатов'
    FIND_PEOPLE = '🔎Поиск людей'
    DECLINE = '❌Отмена'
    BACK = '🏠Домой'
    SUBSCRIPTION = '💳Подписка'
    MY_FORM = '📝Моя анкета'
    SET_AGE = '📅Изменить возраст'
    MAIN_MENU = '🏠Главное меню'


class Stage(ABC):
    def __init__(self):
        self.kb = VkKeyboard()
        self.generate_kb()

    @abstractproperty
    def msg_text(self):
        raise NotImplementedError('msg_text attribute must be implemented for Stage clssses.')

    @abstractclassmethod
    def generate_kb(self) -> None:
        raise NotImplementedError('generate method must be implemented for Stage clssses.')
    
    def get_keyboard(self):
        return self.kb.get_keyboard()


class Main(Stage):    
    msg_text = f'{ButtonLabels.MAIN_MENU}\n'\
               'У нас ты можешь:\n'\
               '• Знакомиться с людьми с общими интересами\n'\
               '• Вступать в тематические группы\n'

    def generate_kb(self):
        self.kb.add_button(ButtonLabels.FIND_PEOPLE)
        self.kb.add_button(ButtonLabels.FIND_CHATS)

        self.kb.add_line()
        self.kb.add_button(ButtonLabels.SETTINGS, color=VkKeyboardColor.PRIMARY)


class Settings(Stage):
    msg_text = f'{ButtonLabels.SETTINGS}\n'\
               'Здесь ты можешь изменить свою личную информацию или проверить статус подписки.'    

    def generate_kb(self):
        self.kb.add_button(ButtonLabels.SET_AGE)
        self.kb.add_button(ButtonLabels.MY_FORM)

        self.kb.add_line()
        self.kb.add_button(ButtonLabels.SUBSCRIPTION, color=VkKeyboardColor.PRIMARY)

        self.kb.add_line()
        self.kb.add_button(ButtonLabels.BACK, color=VkKeyboardColor.POSITIVE)


class Stages(Enum):
    MAIN = Main()
    SETTINGS = Settings()
