from enum import Enum

class Priority(Enum):
    NOT_URGENT_NOT_IMPORTANT = 'Не важное_Не срочное'
    IMPORTANT_NOT_URGENT = 'Важное_Не срочное'
    NOT_URGENT_URGENT = 'Не важное_Срочное'
    IMPORTANT_URGENT = 'Важное_Срочное'