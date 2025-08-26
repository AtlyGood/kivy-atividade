from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import random

# Lista de filmes com ano de lançamento
FILMES = [
    {"titulo": "Matrix", "ano": 1999},
    {"titulo": "Toy Story", "ano": 1995},
    {"titulo": "Avatar", "ano": 2009},
    {"titulo": "O Rei Leão", "ano": 1994},
    {"titulo": "Homem-Aranha", "ano": 2002},
    {"titulo": "Interestelar", "ano": 2014},
    {"titulo": "Os Vingadores", "ano": 2012},
    {"titulo": "Titanic", "ano": 1997},
    {"titulo": "De Volta para o Futuro", "ano": 1985},
    {"titulo": "O Poderoso Chefão", "ano": 1972},
    {"titulo": "Cidade de Deus", "ano": 2002},
    {"titulo": "Forrest Gump", "ano": 1994},
    {"titulo": "Clube da Luta", "ano": 1999},
    {"titulo": "Os Incríveis", "ano": 2004},
    {"titulo": "Coringa", "ano": 2019}
]

class FilmeAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 20
        
        # Adicionar fundo gradiente
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Título
        titulo = Label(
            text='Sugestor de Filmes',
            font_size='28sp',
            bold=True,
            color=(1, 0.8, 0.2, 1)
        )
        self.add_widget(titulo)
        
        # Instruções
        instrucoes = Label(
            text='Digite seu nome e clique no botão para receber\numa sugestão de filme!',
            font_size='16sp',
            color=(0.9, 0.9, 0.9, 1)
        )
        self.add_widget(instrucoes)
        
        # Campo para nome
        self.nome_input = TextInput(
            hint_text='Digite seu nome aqui...',
            size_hint=(1, None),
            height=60,
            font_size='20sp',
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            cursor_color=(1, 1, 1, 1),
            multiline=False,
            padding=15
        )
        self.add_widget(self.nome_input)
        
        # Botão sugerir
        sugerir_btn = Button(
            text='Sugerir Filme',
            size_hint=(1, None),
            height=70,
            font_size='20sp',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        sugerir_btn.bind(on_press=self.sugerir_filme)
        self.add_widget(sugerir_btn)
        
        # Label para resultado
        self.resultado_label = Label(
            text='',
            font_size='22sp',
            bold=True,
            color=(1, 1, 1, 1),
            text_size=(Window.width - 80, None),
            halign='center',
            valign='middle'
        )
        self.resultado_label.bind(size=self.resultado_label.setter('text_size'))
        self.add_widget(self.resultado_label)
        
        # Adicionar alguns filmes populares como dica
        dica_label = Label(
            text='Filmes em nossa lista: Matrix, Toy Story, Avatar, O Rei Leão e muitos outros!',
            font_size='14sp',
            color=(0.8, 0.8, 0.8, 1),
            italic=True
        )
        self.add_widget(dica_label)
        
        # Espaçador
        self.add_widget(Widget(size_hint=(1, 0.3)))
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def sugerir_filme(self, instance):
        nome = self.nome_input.text.strip()
        
        # Validação do campo nome
        if not nome:
            self.mostrar_erro('Por favor, digite seu nome!')
            return
        
        # Sortear um filme aleatório
        filme_sorteado = random.choice(FILMES)
        titulo = filme_sorteado["titulo"]
        ano = filme_sorteado["ano"]
        
        # Gerar mensagem personalizada
        mensagem = f"Olá, [b]{nome}[/b]! Sua sugestão de filme é:\n\n[color=#FFD700][b]{titulo}[/b][/color] ({ano})"
        
        # Exibir resultado
        self.resultado_label.markup = True
        self.resultado_label.text = mensagem
    
    def mostrar_erro(self, mensagem):
        popup = Popup(
            title='Atenção',
            content=Label(text=mensagem, font_size='18sp'),
            size_hint=(0.8, 0.4),
            background_color=(0.2, 0.2, 0.3, 1),
            separator_color=(0.3, 0.3, 0.4, 1)
        )
        popup.open()

class FilmeApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return FilmeAppLayout()

if __name__ == '__main__':
    FilmeApp().run()