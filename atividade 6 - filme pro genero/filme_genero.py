from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import random

# Listas de filmes por gênero com ano de lançamento
FILMES_POR_GENERO = {
    "Ação": [
        {"titulo": "Matrix", "ano": 1999},
        {"titulo": "Mad Max: Estrada da Fúria", "ano": 2015},
        {"titulo": "John Wick", "ano": 2014},
        {"titulo": "Duro de Matar", "ano": 1988},
        {"titulo": "Missão Impossível", "ano": 1996}
    ],
    "Comédia": [
        {"titulo": "Se Beber, Não Case", "ano": 2009},
        {"titulo": "As Branquelas", "ano": 2004},
        {"titulo": "Debi & Lóide", "ano": 1994},
        {"titulo": "Escola de Rock", "ano": 2003},
        {"titulo": "Superbad", "ano": 2007}
    ],
    "Animação": [
        {"titulo": "Toy Story", "ano": 1995},
        {"titulo": "O Rei Leão", "ano": 1994},
        {"titulo": "Divertidamente", "ano": 2015},
        {"titulo": "Shrek", "ano": 2001},
        {"titulo": "Procurando Nemo", "ano": 2003}
    ],
    "Drama": [
        {"titulo": "O Poderoso Chefão", "ano": 1972},
        {"titulo": "Forrest Gump", "ano": 1994},
        {"titulo": "Cidade de Deus", "ano": 2002},
        {"titulo": "Clube da Luta", "ano": 1999},
        {"titulo": "Coringa", "ano": 2019}
    ],
    "Ficção Científica": [
        {"titulo": "Avatar", "ano": 2009},
        {"titulo": "Interestelar", "ano": 2014},
        {"titulo": "Blade Runner 2049", "ano": 2017},
        {"titulo": "De Volta para o Futuro", "ano": 1985},
        {"titulo": "O Exterminador do Futuro", "ano": 1984}
    ]
}

class FilmeAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 15
        self.genero_selecionado = None
        
        # Adicionar fundo gradiente
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Título
        titulo = Label(
            text='Sugestor de Filmes por Gênero',
            font_size='28sp',
            bold=True,
            color=(1, 0.8, 0.2, 1),
            size_hint_y=None,
            height=60
        )
        self.add_widget(titulo)
        
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
        
        # Label para seleção de gênero
        genero_label = Label(
            text='Selecione um gênero:',
            font_size='18sp',
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=None,
            height=40
        )
        self.add_widget(genero_label)
        
        # Grid para botões de gênero
        genero_grid = GridLayout(cols=3, spacing=10, size_hint_y=None, height=120)
        self.toggle_buttons = {}
        
        for genero in FILMES_POR_GENERO.keys():
            btn = ToggleButton(
                text=genero,
                group='generos',
                background_color=(0.3, 0.3, 0.4, 1),
                background_normal='',
                size_hint_y=None,
                height=50
            )
            btn.bind(on_press=self.selecionar_genero)
            genero_grid.add_widget(btn)
            self.toggle_buttons[genero] = btn
        
        self.add_widget(genero_grid)
        
        # Layout para botões principais
        botoes_layout = BoxLayout(spacing=15, size_hint_y=None, height=80)
        
        # Botão sugerir
        sugerir_btn = Button(
            text='Sugerir Filme',
            font_size='18sp',
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            bold=True
        )
        sugerir_btn.bind(on_press=self.sugerir_filme)
        botoes_layout.add_widget(sugerir_btn)
        
        # Botão limpar
        limpar_btn = Button(
            text='Limpar',
            font_size='18sp',
            background_color=(0.8, 0.3, 0.3, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        limpar_btn.bind(on_press=self.limpar_campos)
        botoes_layout.add_widget(limpar_btn)
        
        self.add_widget(botoes_layout)
        
        # Label para resultado
        self.resultado_label = Label(
            text='',
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1),
            text_size=(Window.width - 60, None),
            halign='center',
            valign='middle'
        )
        self.resultado_label.bind(size=self.resultado_label.setter('text_size'))
        self.add_widget(self.resultado_label)
        
        # Espaçador
        self.add_widget(Widget(size_hint=(1, 0.3)))
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def selecionar_genero(self, instance):
        if instance.state == 'down':
            self.genero_selecionado = instance.text
            # Resetar outras cores
            for genero, btn in self.toggle_buttons.items():
                if genero != self.genero_selecionado:
                    btn.background_color = (0.3, 0.3, 0.4, 1)
            # Destacar o selecionado
            instance.background_color = (0.2, 0.5, 0.7, 1)
        else:
            self.genero_selecionado = None
            instance.background_color = (0.3, 0.3, 0.4, 1)
    
    def sugerir_filme(self, instance):
        nome = self.nome_input.text.strip()
        
        # Validações
        if not nome:
            self.mostrar_erro('Por favor, digite seu nome!')
            return
        
        if not self.genero_selecionado:
            self.mostrar_erro('Por favor, selecione um gênero!')
            return
        
        # Sortear um filme do gênero selecionado
        filmes_genero = FILMES_POR_GENERO[self.genero_selecionado]
        filme_sorteado = random.choice(filmes_genero)
        titulo = filme_sorteado["titulo"]
        ano = filme_sorteado["ano"]
        
        # Gerar mensagem personalizada
        mensagem = f"Olá, [b]{nome}[/b]! Sua sugestão de filme de [color=#FFD700][b]{self.genero_selecionado}[/b][/color] é:\n\n[color=#FFD700][b]{titulo}[/b][/color] ({ano})"
        
        # Exibir resultado
        self.resultado_label.markup = True
        self.resultado_label.text = mensagem
    
    def limpar_campos(self, instance):
        self.nome_input.text = ''
        self.resultado_label.text = ''
        self.genero_selecionado = None
        
        # Resetar todos os botões de gênero
        for btn in self.toggle_buttons.values():
            btn.state = 'normal'
            btn.background_color = (0.3, 0.3, 0.4, 1)
    
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