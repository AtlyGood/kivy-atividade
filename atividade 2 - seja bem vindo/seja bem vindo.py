from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

app = App()

input = TextInput(hint_text="digite seu nome:")
botao = Button(text="Enviar")
label = Label(text='')

def Enviar(instance):
    nome = input.text.strip()
    if nome:
        label.text = f'Seja bem-vindo, {nome}!'
    else:
        label.text = 'Por favor, digite seu nome!'
botao.bind(on_press=Enviar)

layout = BoxLayout(orientation='vertical')
layout.add_widget(input)
layout.add_widget(botao)
layout.add_widget(label)

app.build = lambda: layout
app.run()