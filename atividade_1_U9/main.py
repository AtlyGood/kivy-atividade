from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock

import database

# Gerenciador de telas
class GerenciadorTelas(ScreenManager):
    pass

# Tela de cadastro de filmes
class TelaCadastro(Screen):
    titulo_input = ObjectProperty(None)
    genero_input = ObjectProperty(None)
    ano_input = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filme_editando = None
    
    def salvar_filme(self):
        titulo = self.titulo_input.text.strip()
        genero = self.genero_input.text.strip()
        ano_texto = self.ano_input.text.strip()
        
        # Validação dos campos
        if not titulo or not genero or not ano_texto:
            self.mostrar_popup("Erro", "Todos os campos devem ser preenchidos!")
            return
        
        try:
            ano = int(ano_texto)
            if ano < 1888 or ano > 2100:  # 1888 é considerado o primeiro filme da história
                self.mostrar_popup("Erro", "Ano deve estar entre 1888 e 2100!")
                return
        except ValueError:
            self.mostrar_popup("Erro", "Ano deve ser um número válido!")
            return
        
        # Salvar ou editar filme
        if self.filme_editando:
            database.editar_filme(self.filme_editando, titulo, genero, ano)
            self.mostrar_popup("Sucesso", "Filme atualizado com sucesso!")
        else:
            database.adicionar_filme(titulo, genero, ano)
            self.mostrar_popup("Sucesso", "Filme adicionado com sucesso!")
        
        # Limpar campos e voltar para a listagem
        self.limpar_campos()
        self.manager.current = 'listagem'
        self.manager.get_screen('listagem').carregar_filmes()
    
    def preencher_campos(self, filme_id, titulo, genero, ano):
        self.filme_editando = filme_id
        self.titulo_input.text = titulo
        self.genero_input.text = genero
        self.ano_input.text = str(ano)
    
    def limpar_campos(self):
        self.filme_editando = None
        self.titulo_input.text = ""
        self.genero_input.text = ""
        self.ano_input.text = ""
    
    def mostrar_popup(self, titulo, mensagem):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_layout.add_widget(Label(text=mensagem))
        
        fechar_btn = Button(text="Fechar", size_hint_y=0.4)
        popup_layout.add_widget(fechar_btn)
        
        popup = Popup(title=titulo, content=popup_layout, size_hint=(0.8, 0.4))
        fechar_btn.bind(on_release=popup.dismiss)
        popup.open()

# Tela de listagem de filmes
class TelaListagem(Screen):
    container_lista = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.carregar_filmes, 0.1)
    
    def carregar_filmes(self, *args):
        # Limpar lista atual
        self.container_lista.clear_widgets()
        
        # Buscar filmes no banco
        filmes = database.listar_filmes()
        
        if not filmes:
            sem_registros = Label(
                text="Nenhum filme cadastrado.\nClique em 'Adicionar Filme' para começar.",
                size_hint_y=None,
                height=100,
                halign="center"
            )
            self.container_lista.add_widget(sem_registros)
            return
        
        # Adicionar cada filme à lista
        for filme in filmes:
            filme_id, titulo, genero, ano = filme
            
            item = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=60,
                padding=5
            )
            
            info = Label(
                text=f"{titulo} ({ano}) - {genero}",
                size_hint_x=0.7,
                text_size=(None, None),
                halign="left",
                valign="middle"
            )
            info.bind(texture_size=info.setter('size'))
            
            botoes = BoxLayout(orientation='horizontal', size_hint_x=0.3, spacing=5)
            
            editar_btn = Button(
                text="Editar",
                size_hint_x=0.5,
                background_color=(0.2, 0.6, 1, 1)
            )
            editar_btn.filme_id = filme_id
            editar_btn.bind(on_release=self.editar_filme)
            
            excluir_btn = Button(
                text="Excluir",
                size_hint_x=0.5,
                background_color=(1, 0.2, 0.2, 1)
            )
            excluir_btn.filme_id = filme_id
            excluir_btn.bind(on_release=self.confirmar_exclusao)
            
            botoes.add_widget(editar_btn)
            botoes.add_widget(excluir_btn)
            
            item.add_widget(info)
            item.add_widget(botoes)
            
            self.container_lista.add_widget(item)
    
    def editar_filme(self, instance):
        filme_id = instance.filme_id
        filme = database.buscar_filme_por_id(filme_id)
        
        if filme:
            tela_cadastro = self.manager.get_screen('cadastro')
            tela_cadastro.preencher_campos(filme[0], filme[1], filme[2], filme[3])
            self.manager.current = 'cadastro'
    
    def confirmar_exclusao(self, instance):
        filme_id = instance.filme_id
        filme = database.buscar_filme_por_id(filme_id)
        
        if filme:
            popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_layout.add_widget(Label(
                text=f"Tem certeza que deseja excluir\n\"{filme[1]}\"?"
            ))
            
            botoes = BoxLayout(orientation='horizontal', size_hint_y=0.4, spacing=5)
            
            cancelar_btn = Button(text="Cancelar")
            confirmar_btn = Button(text="Excluir", background_color=(1, 0.2, 0.2, 1))
            
            botoes.add_widget(cancelar_btn)
            botoes.add_widget(confirmar_btn)
            
            popup_layout.add_widget(botoes)
            
            popup = Popup(
                title="Confirmar Exclusão",
                content=popup_layout,
                size_hint=(0.8, 0.4)
            )
            
            cancelar_btn.bind(on_release=popup.dismiss)
            confirmar_btn.bind(on_release=lambda x: self.excluir_filme(filme_id, popup))
            
            popup.open()
    
    def excluir_filme(self, filme_id, popup):
        database.deletar_filme(filme_id)
        popup.dismiss()
        self.carregar_filmes()
        self.mostrar_popup("Sucesso", "Filme excluído com sucesso!")
    
    def mostrar_popup(self, titulo, mensagem):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_layout.add_widget(Label(text=mensagem))
        
        fechar_btn = Button(text="Fechar", size_hint_y=0.4)
        popup_layout.add_widget(fechar_btn)
        
        popup = Popup(title=titulo, content=popup_layout, size_hint=(0.8, 0.4))
        fechar_btn.bind(on_release=popup.dismiss)
        popup.open()
    
    def ir_para_cadastro(self):
        tela_cadastro = self.manager.get_screen('cadastro')
        tela_cadastro.limpar_campos()
        self.manager.current = 'cadastro'

# Aplicação principal
class GerenciadorFilmesApp(App):
    def build(self):
        # Criar banco de dados se não existir
        database.criar_banco()
        
        # Retornar o gerenciador de telas
        return GerenciadorTelas()

if __name__ == '__main__':
    GerenciadorFilmesApp().run()