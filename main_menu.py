import arcade
import arcade.gui


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "UIFlatButton Example", resizable=True)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.v_box = arcade.gui.UIBoxLayout()

        button_1 = arcade.gui.UIFlatButton(text="Level 1", width=200)
        self.v_box.add(button_1.with_space_around(bottom=20))

        button_2 = arcade.gui.UIFlatButton(text="Level 2", width=200)
        self.v_box.add(button_2.with_space_around(bottom=20))

        button_3 = arcade.gui.UIFlatButton(text="Level 3", width=200)
        self.v_box.add(button_3.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        button_1.on_click = self.on_click_start
        button_2.on_click = self.on_click_start
        button_3.on_click = self.on_click_start


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        print("Start:", event)

    def on_draw(self):
        self.clear()
        self.manager.draw()


window = MyWindow()
arcade.run()