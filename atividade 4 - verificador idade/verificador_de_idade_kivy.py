from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

class IdadeAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20
        
        # Título
        titulo = Label(
            text='Verificador de Idade',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        self.add_widget(titulo)
        
        # Campo para nome
        self.nome_input = TextInput(
            hint_text='Digite seu nome',
            size_hint=(1, None),
            height=50,
            font_size='18sp',
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.nome_input)
        
        # Campo para idade
        self.idade_input = TextInput(
            hint_text='Digite sua idade (apenas números)',
            size_hint=(1, None),
            height=50,
            font_size='18sp',
            input_filter='int',
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.idade_input)
        
        # Botão enviar
        enviar_btn = Button(
            text='Enviar',
            size_hint=(1, None),
            height=60,
            font_size='18sp',
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        enviar_btn.bind(on_press=self.verificar_idade)
        self.add_widget(enviar_btn)
        
        # Label para resultado
        self.resultado_label = Label(
            text='',
            font_size='20sp',
            bold=True,
            color=(0.3, 0.3, 0.3, 1)
        )
        self.add_widget(self.resultado_label)
        
        # Espaçador
        self.add_widget(Widget(size_hint=(1, 0.5)))
    
    def verificar_idade(self, instance):
        nome = self.nome_input.text.strip()
        idade_texto = self.idade_input.text.strip()
        
        # Validação dos campos
        if not nome:
            self.mostrar_erro('Por favor, digite seu nome!')
            return
        
        if not idade_texto:
            self.mostrar_erro('Por favor, digite sua idade!')
            return
        
        try:
            idade = int(idade_texto)
            
            if idade < 0:
                self.mostrar_erro('Idade não pode ser negativa!')
                return
                
            if idade > 120:
                self.mostrar_erro('Idade parece muito alta. Verifique!')
                return
            
            # Determinar a mensagem baseada na idade
            if idade >= 60:
                mensagem = f"Olá, {nome}! Você é idoso e merece muito respeito ❤️."
                cor = (0.8, 0.2, 0.2, 1)  # Vermelho
            elif idade >= 18:
                mensagem = f"Olá, {nome}! Você é maior de idade."
                cor = (0.2, 0.6, 0.2, 1)  # Verde
            else:
                mensagem = f"Olá, {nome}! Você é menor de idade."
                cor = (0.2, 0.4, 0.8, 1)  # Azul
            
            # Exibir resultado
            self.resultado_label.text = mensagem
            self.resultado_label.color = cor
            
        except ValueError:
            self.mostrar_erro('Por favor, digite apenas números na idade!')
    
    def mostrar_erro(self, mensagem):
        popup = Popup(
            title='Erro',
            content=Label(text=mensagem),
            size_hint=(0.8, 0.4),
            background_color=(0.9, 0.6, 0.6, 1)
        )
        popup.open()

class IdadeApp(App):
    def build(self):
        Window.clearcolor = (0.98, 0.98, 0.98, 1)  # Cor de fundo clara
        return IdadeAppLayout()

if __name__ == '__main__':
    IdadeApp().run()