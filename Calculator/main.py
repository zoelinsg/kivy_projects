from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainApp(App):
    # 建立主佈局
    def build(self):
        self.icon = "calculator.png"
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = False
        self.last_button = None

        # 建立主佈局
        main_layout = BoxLayout(orientation="vertical")
        
        # 建立顯示區域，設置字體大小並限制為單行
        self.solution = TextInput(
            background_color="black", 
            foreground_color="white", 
            font_size=32, 
            multiline=False
        )
        main_layout.add_widget(self.solution)
        
        # 建立按鈕
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        
        # 將按鈕加入佈局
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label, font_size=30, background_color="grey",
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        
        # 建立等號按鈕
        equal_button = Button(
            text="=", font_size=30, background_color="grey",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equal_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equal_button)

        return main_layout
    
    # 按鈕事件處理
    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == 'C':
            # 清除顯示區域
            self.solution.text = ""
        else:
            if current and (
                self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text

        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    # 計算結果
    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                # 計算結果並顯示
                self.solution.text = str(eval(self.solution.text))
            except Exception:
                self.solution.text = "Error"

if __name__ == "__main__":
    app = MainApp()
    app.run()