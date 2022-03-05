from enum import Enum
from abc import ABC, abstractclassmethod, abstractproperty

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class ButtonLabels:
    SETTINGS = '⚙Настройки'
    FIND_CHATS = '👥Поиск чатов'
    FIND_PEOPLE = '🔎Поиск людей'
    DECLINE = '❌Отмена'
    HOME = '🏠Домой'
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
        self.kb.add_button(ButtonLabels.FIND_PEOPLE,
                           payload={'command': 'find_people'})
        self.kb.add_button(ButtonLabels.FIND_CHATS,
                           payload={'command': 'find_chats'})

        self.kb.add_line()
        self.kb.add_button(ButtonLabels.SETTINGS,
                           color=VkKeyboardColor.PRIMARY,
                           payload={'command': 'settings'})


class Settings(Stage):
    msg_text = f'{ButtonLabels.SETTINGS}\n'\
               'Здесь ты можешь изменить свою личную информацию или проверить статус подписки.'    

    def generate_kb(self):
        self.kb.add_button(ButtonLabels.SET_AGE,
                           payload={'command': 'set_age'})
        self.kb.add_button(ButtonLabels.MY_FORM,
                           payload={'command': 'my_form'})

        self.kb.add_line()
        self.kb.add_button(ButtonLabels.SUBSCRIPTION, color=VkKeyboardColor.PRIMARY)

        self.kb.add_line()
        self.kb.add_button(ButtonLabels.HOME,
                           color=VkKeyboardColor.POSITIVE,
                           payload={'command': 'home'})


class Stages(Enum):
    MAIN = Main()
    SETTINGS = Settings()
