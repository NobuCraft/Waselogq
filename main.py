import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import webbrowser
from PIL import Image, ImageDraw, ImageFont
import io
import os

class PythonTutorAI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Python Tutor AI - Обучение с нуля до PRO")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        # Настройка стилей
        self.setup_styles()
        
        # Основной контейнер
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        self.create_header()
        
        # Панель с уроками и контентом
        self.create_content_panel()
        
        # Текущий урок
        self.current_lesson = 0
        
        # Уроки
        self.lessons = [
            {
                "title": "Урок 1: Введение в Python",
                "content": """🐍 Python - это язык программирования, который похож на английский язык!
                
✨ Почему Python?
• Простой и понятный синтаксис
• Много готовых решений
• Можно создавать игры, сайты, программы

🎯 Первая программа:
print('Привет, мир!')

💡 print() - это функция для вывода текста""",
                "code": "print('Привет, мир!')\nprint('Я учу Python!')",
                "image": "intro"
            },
            {
                "title": "Урок 2: Переменные",
                "content": """📦 Переменные - это коробочки для хранения данных!

🎨 Типы данных:
• Числа: age = 25
• Текст: name = 'Анна'
• Дроби: price = 99.99

🌟 Пример:
name = 'Мария'
age = 20
print(f'Меня зовут {name}, мне {age} лет')""",
                "code": "name = 'Анна'\nage = 25\ncity = 'Москва'\nprint(f'Привет! Я {name}, мне {age} лет, живу в {city}')",
                "image": "variables"
            },
            {
                "title": "Урок 3: Условные операторы",
                "content": """⚖️ Условные операторы помогают принимать решения!

🔍 Структура if-else:
if условие:
    действие 1
else:
    действие 2

🌰 Пример:
age = 18
if age >= 18:
    print('Ты совершеннолетний!')
else:
    print('Ты еще ребенок!')""",
                "code": "temperature = 25\nif temperature > 20:\n    print('Тепло! Идем гулять!')\nelse:\n    print('Холодно, сидим дома')",
                "image": "conditions"
            },
            {
                "title": "Урок 4: Циклы",
                "content": """🔄 Циклы - это повторение действий!

🪄 Цикл for:
for i in range(5):
    print(f'Шаг {i}')

🌀 Цикл while:
count = 0
while count < 3:
    print('Привет!')
    count += 1""",
                "code": "# Считаем до 5\nfor number in range(1, 6):\n    print(f'Число: {number}')\n\n# Танцевальный цикл\nsteps = ['влево', 'вправо', 'кругом']\nfor step in steps:\n    print(f'Танцуем {step}!')",
                "image": "loops"
            },
            {
                "title": "Урок 5: Функции",
                "content": """🎯 Функции - это маленькие программы в программе!

📝 Создание функции:
def приветствие(имя):
    print(f'Привет, {имя}!')

✨ Пример:
def сложить(a, b):
    return a + b

результат = сложить(5, 3)
print(результат)  # 8""",
                "code": "def greet(name):\n    return f'✨ Привет, {name}!'\n\ndef add_numbers(x, y):\n    return x + y\n\n# Используем функции\nprint(greet('Python'))\nprint(f'5 + 3 = {add_numbers(5, 3)}')",
                "image": "functions"
            }
        ]
        
        # Показываем первый урок
        self.show_lesson(0)
    
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка цветов
        style.configure('Header.TLabel', 
                       background='#1e1e1e', 
                       foreground='#00ff88',
                       font=('Arial', 24, 'bold'))
        
        style.configure('Title.TLabel',
                       background='#2b2b2b',
                       foreground='#ffffff',
                       font=('Arial', 18, 'bold'))
        
        style.configure('Content.TLabel',
                       background='#363636',
                       foreground='#ffffff',
                       font=('Arial', 12))
        
        style.configure('Lesson.TButton',
                       background='#404040',
                       foreground='#ffffff',
                       font=('Arial', 11))
        
        style.map('Lesson.TButton',
                 background=[('active', '#505050')])
    
    def create_header(self):
        """Создание шапки с анимацией"""
        header_frame = ttk.Frame(self.main_container, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Анимированный заголовок
        self.header_label = ttk.Label(header_frame, 
                                      text="🐍 Python Tutor AI",
                                      style='Header.TLabel')
        self.header_label.pack(pady=10)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(header_frame, length=500, mode='determinate')
        self.progress.pack(pady=5)
        self.progress['maximum'] = len(self.lessons)
    
    def create_content_panel(self):
        """Создание панели с уроками и контентом"""
        # Левая панель - список уроков
        left_panel = ttk.Frame(self.main_container, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        ttk.Label(left_panel, text="📚 Уроки:", style='Title.TLabel').pack(pady=5)
        
        # Кнопки уроков
        self.lesson_buttons = []
        for i, lesson in enumerate(self.lessons):
            btn = ttk.Button(left_panel, 
                           text=lesson['title'],
                           style='Lesson.TButton',
                           command=lambda idx=i: self.show_lesson(idx))
            btn.pack(fill=tk.X, pady=2)
            self.lesson_buttons.append(btn)
        
        # Правая панель - контент
        right_panel = ttk.Frame(self.main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Заголовок урока
        self.lesson_title = ttk.Label(right_panel, text="", style='Title.TLabel')
        self.lesson_title.pack(pady=5)
        
        # Контейнер для контента и изображения
        content_frame = ttk.Frame(right_panel)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Текст урока
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.lesson_text = scrolledtext.ScrolledText(text_frame,
                                                     wrap=tk.WORD,
                                                     font=('Arial', 12),
                                                     bg='#363636',
                                                     fg='#ffffff',
                                                     insertbackground='white')
        self.lesson_text.pack(fill=tk.BOTH, expand=True)
        
        # Изображение
        self.image_frame = ttk.Frame(content_frame, width=300)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0))
        self.image_frame.pack_propagate(False)
        
        self.image_label = ttk.Label(self.image_frame, text="🎨 Генерация\nиллюстрации...",
                                     font=('Arial', 14), foreground='#888888')
        self.image_label.pack(expand=True)
        
        # Поле для кода
        code_frame = ttk.Frame(right_panel)
        code_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(code_frame, text="💻 Попробуй сам:", 
                 style='Title.TLabel').pack(anchor=tk.W)
        
        self.code_text = scrolledtext.ScrolledText(code_frame,
                                                   height=8,
                                                   wrap=tk.WORD,
                                                   font=('Courier', 11),
                                                   bg='#1e1e1e',
                                                   fg='#00ff88',
                                                   insertbackground='white')
        self.code_text.pack(fill=tk.X, pady=5)
        
        # Кнопки
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="▶ Запустить код",
                  command=self.run_code).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🎨 Сгенерировать новую картинку",
                  command=self.generate_image).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="➡ Следующий урок",
                  command=self.next_lesson).pack(side=tk.RIGHT, padx=5)
        
        # Вывод результата
        self.output_text = scrolledtext.ScrolledText(right_panel,
                                                     height=5,
                                                     wrap=tk.WORD,
                                                     font=('Courier', 10),
                                                     bg='#1e1e1e',
                                                     fg='#ffffff')
        self.output_text.pack(fill=tk.X, pady=5)
    
    def show_lesson(self, index):
        """Показать урок"""
        self.current_lesson = index
        lesson = self.lessons[index]
        
        # Обновляем заголовок
        self.lesson_title.config(text=lesson['title'])
        
        # Обновляем текст
        self.lesson_text.delete(1.0, tk.END)
        self.lesson_text.insert(1.0, lesson['content'])
        
        # Обновляем код
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, lesson['code'])
        
        # Обновляем прогресс
        self.progress['value'] = index + 1
        
        # Генерируем изображение
        self.generate_image()
        
        # Подсвечиваем текущий урок
        for i, btn in enumerate(self.lesson_buttons):
            if i == index:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])
    
    def generate_image(self):
        """Генерация иллюстрации для урока"""
        lesson = self.lessons[self.current_lesson]
        
        # Создаем изображение
        img = Image.new('RGB', (300, 250), color='#404040')
        draw = ImageDraw.Draw(img)
        
        # Рисуем в зависимости от темы
        if lesson['image'] == 'intro':
            draw.rectangle([50, 50, 250, 200], fill='#00ff88', outline='#ffffff', width=2)
            draw.text((100, 120), "print('Hello!')", fill='#ffffff', font=None)
            draw.text((80, 150), "🐍 Python", fill='#ffffff', font=None)
            
        elif lesson['image'] == 'variables':
            # Рисуем коробки
            draw.rectangle([50, 80, 120, 150], fill='#ff9900', outline='#ffffff', width=2)
            draw.text((70, 110), "name", fill='#ffffff')
            draw.rectangle([140, 80, 210, 150], fill='#ff9900', outline='#ffffff', width=2)
            draw.text((165, 110), "age", fill='#ffffff')
            draw.text((90, 180), "📦 Переменные", fill='#ffffff')
            
        elif lesson['image'] == 'conditions':
            # Рисуем развилку
            draw.line([150, 50, 150, 200], fill='#ffffff', width=3)
            draw.line([150, 120, 80, 180], fill='#ffffff', width=3)
            draw.line([150, 120, 220, 180], fill='#ffffff', width=3)
            draw.text((40, 190), "if True", fill='#ffffff')
            draw.text((200, 190), "else", fill='#ffffff')
            
        elif lesson['image'] == 'loops':
            # Рисуем цикл
            for i in range(4):
                x = 80 + i * 50
                draw.ellipse([x, 100, x+30, 130], fill='#00ff88', outline='#ffffff')
            draw.text((120, 150), "🔄 Цикл", fill='#ffffff')
            
        elif lesson['image'] == 'functions':
            # Рисуем функцию как коробку с шестеренками
            draw.rectangle([70, 70, 230, 180], fill='#ff66aa', outline='#ffffff', width=3)
            draw.text((120, 120), "def", fill='#ffffff', font=None)
            draw.text((130, 140), "func():", fill='#ffffff', font=None)
        
        # Сохраняем во временный файл и отображаем
        img.save('temp_lesson.png')
        
        # Загружаем изображение в tkinter
        from PIL import ImageTk
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo, text='')
        self.image_label.image = photo
    
    def run_code(self):
        """Запуск кода пользователя"""
        code = self.code_text.get(1.0, tk.END)
        
        # Перенаправляем вывод
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output
        
        try:
            exec(code)
            output = redirected_output.getvalue()
            if not output:
                output = "✅ Код выполнен успешно!"
        except Exception as e:
            output = f"❌ Ошибка: {str(e)}"
        finally:
            sys.stdout = old_stdout
        
        # Показываем результат
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, output)
    
    def next_lesson(self):
        """Переход к следующему уроку"""
        if self.current_lesson < len(self.lessons) - 1:
            self.show_lesson(self.current_lesson + 1)
        else:
            messagebox.showinfo("Поздравляю! 🎉", 
                              "Ты прошел все уроки!\nТеперь ты настоящий Python-программист!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonTutorAI(root)
    root.mainloop()
