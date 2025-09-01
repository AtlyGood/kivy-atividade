from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
import random

# Dicionário com filmes por gênero
filmes_por_genero = {
    'Ação': ['Matrix', 'John Wick', 'Mad Max: Estrada da Fúria', 'Duro de Matar', 'Missão Impossível'],
    'Comédia': ['Se Beber, Não Case', 'As Branquelas', 'Debi & Lóide', 'Escola de Rock', 'Superbad'],
    'Animação': ['Toy Story', 'Procurando Nemo', 'Shrek', 'Frozen', 'Os Incríveis']
}

class TelaBoasVindas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'boas_vindas'
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Título
        titulo = Label(text='Bem-vindo ao fodasesugestoes', font_size=28, size_hint_y=0.3)
        
        # Campo para digitar o nome
        self.input_nome = TextInput(
            hint_text='Digite seu nome', 
            size_hint_y=0.2,
            multiline=False
        )
        
        # Botão para continuar
        btn_continuar = Button(
            text='Continuar', 
            size_hint_y=0.2,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_continuar.bind(on_press=self.ir_para_sugestao)
        
        layout.add_widget(titulo)
        layout.add_widget(self.input_nome)
        layout.add_widget(btn_continuar)
        
        self.add_widget(layout)
    
    def ir_para_sugestao(self, instance):
        # Passa o nome para a próxima tela
        tela_sugestao = self.manager.get_screen('sugestao_filmes')
        tela_sugestao.nome_usuario = self.input_nome.text
        
        # Muda para a tela de sugestão
        self.manager.current = 'sugestao_filmes'

class TelaSugestaoFilmes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'sugestao_filmes'
        self.nome_usuario = ""
        self.filme_sorteado = ""
        
        self.layout_principal = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Mensagem de boas-vindas
        self.label_boas_vindas = Label(
            text=f'Olá, {self.nome_usuario}!',
            font_size=24,
            size_hint_y=0.2
        )
        
        # Seletor de gênero
        layout_genero = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.3)
        label_genero = Label(text='Selecione um gênero:', size_hint_y=0.4)
        
        self.spinner_genero = Spinner(
            text='Ação',
            values=('Ação', 'Comédia', 'Animação'),
            size_hint_y=0.6
        )
        
        layout_genero.add_widget(label_genero)
        layout_genero.add_widget(self.spinner_genero)
        
        # Botão para sugerir filme
        btn_sugerir = Button(
            text='Sugerir Filme',
            size_hint_y=0.2,
            background_color=(0.8, 0.4, 0.2, 1)
        )
        btn_sugerir.bind(on_press=self.sugerir_filme)
        
        # Label para mostrar o filme sorteado
        self.label_filme = Label(
            text='',
            font_size=20,
            size_hint_y=0.3
        )
        
        self.layout_principal.add_widget(self.label_boas_vindas)
        self.layout_principal.add_widget(layout_genero)
        self.layout_principal.add_widget(btn_sugerir)
        self.layout_principal.add_widget(self.label_filme)
        
        self.add_widget(self.layout_principal)
    
    def on_enter(self):
        # Atualiza a mensagem de boas-vindas quando a tela é exibida
        self.label_boas_vindas.text = f'Olá, {self.nome_usuario}!'
    
    def sugerir_filme(self, instance):
        genero = self.spinner_genero.text
        if genero in filmes_por_genero:
            filme = random.choice(filmes_por_genero[genero])
            self.filme_sorteado = filme
            self.label_filme.text = f'Sugestão: {filme}'

class GerenciadorTelas(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition.duration = 0.3  # Duração da transição entre telas

class CineSuggestApp(App):
    def build(self):
        gerenciador = GerenciadorTelas()
        
        # Adiciona as telas ao gerenciador
        gerenciador.add_widget(TelaBoasVindas())
        gerenciador.add_widget(TelaSugestaoFilmes())
        
        return gerenciador

if __name__ == '__main__':
    CineSuggestApp().run()