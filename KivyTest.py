from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import datetime
from kivy.config import Config

# Важно: все Config.set должны быть В САМОМ НАЧАЛЕ, до импорта Window!
Config.set('graphics', 'borderless', '1')  # Используем borderless режим
Config.set('graphics', 'resizable', '0')   # Отключаем изменение размера
Config.set('kivy', 'exit_on_escape', '0')  # Отключаем закрытие по Escape

# Теперь импортируем Window
from kivy.core.window import Window

class MyBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag_start = None
        self.window_start = None
        self.dragging = False
        # Обновляем дату через небольшой промежуток времени
        Clock.schedule_once(self.update_date, 0.1)
    
    def update_date(self, dt=None):
        """Обновление даты на реальную"""
        now = datetime.datetime.now()
        
        # Day Update
        self.ids.dateLabel.text = str(now.day)
        
        # Month update
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        self.ids.monthLabel.text = months[now.month - 1]

    # Draggable
    def on_touch_down(self, touch):
         # Сначала даем обработать касание дочерним виджетам
        if super().on_touch_down(touch):
            return True
        # Проверяем, не нажали ли мы на кнопку закрытия
        # Координаты кнопки: (ширина окна - 36, высота окна - 36)
        button_x = Window.width - 36
        button_y = Window.height - 36
        
        if (button_x <= touch.x <= button_x + 36 and 
            button_y <= touch.y <= button_y + 36):
            # Это клик по кнопке - не начинаем перетаскивание
            return False
        
        if ((touch.y < self.height - 40) or (touch.x <self.width - 40)):
            # Разрешаем перетаскивание из любой точки окна
            self.drag_start = (touch.x, touch.y)
            self.window_start = (Window.left, Window.top)
            self.dragging = True
        return True
    
    def on_touch_move(self, touch):
        if self.dragging:
            Window.left = Window.left + touch.x - self.drag_start[0]
            Window.top = Window.top - touch.y + self.drag_start[1]
        return False
    
    def on_touch_up(self, touch):
        self.drag_start = None
        self.dragging = False
        return False
    

class Calendar(App):
    def build(self):
        Window.size = (220, 268)
        return MyBoxLayout()

if __name__ == '__main__':
    Calendar().run()