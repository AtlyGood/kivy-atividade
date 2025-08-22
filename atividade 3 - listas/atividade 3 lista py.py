from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Definindo cores para estilização
PRIMARY_COLOR = [0.2, 0.6, 0.8, 1]  # Azul
SECONDARY_COLOR = [0.9, 0.3, 0.3, 1]  # Vermelho
BACKGROUND_COLOR = [0.95, 0.95, 0.95, 1]  # Cinza claro
TASK_BG_COLOR = [0, 0, 0, 1]  # Preto para o fundo das tarefas
TASK_TEXT_COLOR = [1, 1, 1, 1]  # Branco para o texto das tarefas

class TaskWidget(BoxLayout):
    def __init__(self, task_text, remove_callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 40
        self.spacing = 10
        self.padding = [5, 5]
        
        # Adicionar fundo preto
        with self.canvas.before:
            Color(*TASK_BG_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Label com o texto da tarefa
        task_label = Label(
            text=task_text,
            size_hint=(0.8, 1),
            text_size=(None, None),
            halign='left',
            valign='middle',
            color=TASK_TEXT_COLOR  # Texto branco para contraste com fundo preto
        )
        task_label.bind(texture_size=task_label.setter('size'))
        self.add_widget(task_label)
        
        # Botão para remover tarefa individual
        remove_button = Button(
            text="X",
            size_hint=(0.2, 1),
            background_color=SECONDARY_COLOR
        )
        remove_button.task_text = task_text  # Armazenar o texto da tarefa no botão
        remove_button.bind(on_press=remove_callback)
        self.add_widget(remove_button)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class TodoApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        Window.clearcolor = BACKGROUND_COLOR
        
        # Título do aplicativo
        title = Label(
            text="Minha Lista de Tarefas",
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True,
            color=[0, 0, 0, 1]
        )
        self.add_widget(title)
        
        # Layout para entrada de dados
        input_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        # Campo de texto para entrada de tarefas
        self.task_input = TextInput(
            hint_text="Digite sua tarefa aqui...",
            size_hint=(0.7, 1),
            multiline=False
        )
        input_layout.add_widget(self.task_input)
        
        # Botão para adicionar tarefa
        add_button = Button(
            text="Adicionar",
            size_hint=(0.3, 1),
            background_color=PRIMARY_COLOR
        )
        add_button.bind(on_press=self.add_task)
        input_layout.add_widget(add_button)
        
        self.add_widget(input_layout)
        
        # Área de scroll para a lista de tarefas
        scroll = ScrollView(size_hint=(1, 0.7))
        self.tasks_layout = BoxLayout(
            orientation='vertical', 
            size_hint_y=None,
            spacing=5
        )
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        scroll.add_widget(self.tasks_layout)
        self.add_widget(scroll)
        
        # Botão para limpar toda a lista
        clear_button = Button(
            text="Limpar Lista",
            size_hint=(1, 0.1),
            background_color=SECONDARY_COLOR
        )
        clear_button.bind(on_press=self.clear_tasks)
        self.add_widget(clear_button)
        
        # Label para mensagens de feedback
        self.message_label = Label(
            text="",
            size_hint=(1, 0.05),
            color=[1, 0, 0, 1]  # Vermelho para mensagens de erro
        )
        self.add_widget(self.message_label)
        
        # Lista para armazenar as tarefas
        self.tasks = []
    
    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        
        if task_text:
            # Criar widget personalizado para a tarefa com fundo preto
            task_widget = TaskWidget(task_text, self.remove_task)
            
            # Adicionar à lista e ao layout
            self.tasks.append(task_text)
            self.tasks_layout.add_widget(task_widget)
            
            # Limpar campo de entrada
            self.task_input.text = ""
            self.message_label.text = ""
        else:
            self.message_label.text = "Insira uma tarefa válida"
    
    def remove_task(self, instance):
        # Encontrar o widget pai (TaskWidget que contém a tarefa)
        task_widget = instance.parent
        task_text = instance.task_text
        
        # Remover da lista
        if task_text in self.tasks:
            self.tasks.remove(task_text)
        
        # Remover do layout
        self.tasks_layout.remove_widget(task_widget)
    
    def clear_tasks(self, instance):
        # Limpar a lista de tarefas
        self.tasks = []
        
        # Limpar todos os widgets do layout de tarefas
        self.tasks_layout.clear_widgets()
        
        self.message_label.text = "Lista limpa com sucesso!"

class TodoAppMain(App):
    def build(self):
        self.title = "Lista de Tarefas"
        return TodoApp()

if __name__ == '__main__':
    TodoAppMain().run()