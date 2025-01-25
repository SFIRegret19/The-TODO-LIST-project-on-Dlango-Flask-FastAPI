from enum import Enum

class Priority(Enum):
    NOT_URGENT_NOT_IMPORTANT = 'Не важное/Не срочное'
    IMPORTANT_NOT_URGENT = 'Важное/Не срочное'
    NOT_URGENT_URGENT = 'Не важное/Срочное'
    IMPORTANT_URGENT = 'Важное/Срочное'