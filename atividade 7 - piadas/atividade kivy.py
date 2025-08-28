import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class PiadaApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.piada_carregar = Label(
            text = "clique nesse botão para ver a piada",
            halign = "center",
            valign = "middle",
            font_size=20,
        )
        self.piada_carregar.bind(size=self.piada_carregar.setter('text_size'))

        self.botao = Button(
            text="Nova piada",
            size_hint = (1,0.2),
            font_size=18
        )
        self.botao.bind(on_press=self.get_piada)
        self.layout.add_widget(self.piada_carregar)
        self.layout.add_widget(self.botao)

        return self.layout

    def get_piada(self, instance):
        try:
            url = 'https://official-joke-api.appspot.com/random_joke'
            response = requests.get(url, timeout=5)
            if response == response.status_code == 200:
                piada = response.json()
                setup = piada.get("setup", "")
                punchiline = piada.get("punchiline", "")
                self.piada_carregar.text = f"{setup}\n\n{punchiline}"
            else:
                self.piada_carregar.text = "Erro ao carregar piada"

        except Exception as e:
            self.piada_carregar.text = f"Erro: {e}"

        
if __name__ == "__main__":
    PiadaApp().run()
