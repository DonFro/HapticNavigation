# Imorted Libraries
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

# Imported Modules
import coreVibrationAudioModule as cva
from uiElementModule import ButtonGroup


class MyApp(App):
    def build(self) -> FloatLayout:
        """Builds the main application layout"""
        rootScreen = FloatLayout()

        # initializes the vibrations and audio module
        self.coreVibrationAudio = cva.CoreVibrationAudioModule()

        # initializes the UI
        myButton = ButtonGroup(
            size_hint=(0.4, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        myButton.add_label(Label(text="Product Title", size_hint=(1.0, 0.3)))
        btn = Button(text="Purchase", size_hint=(1.0, 0.7))
        btn.bind(on_release=self.on_button_clicked)
        myButton.add_button(btn)

        myButton.bind(on_button=self.handle_button_feedback)

        rootScreen.add_widget(myButton)
        return rootScreen

    
    def handle_button_feedback(self, group: ButtonGroup, on_button: bool) -> None:
        """Fires when group.on_button changes"""
        if on_button:
            self.coreVibrationAudio.activateVibration()
        else:
            self.coreVibrationAudio.deactivateVibration()

            
    def on_button_clicked(self, button_instance: Button) -> None:
        """Called when the user drags onto the button and lifts their finger"""
        print(f"Triggered '{button_instance.text}'!")

        # Get the ButtonGroup that owns this button
        group: ButtonGroup = button_instance.parent

        # Loop through all labels in the group and play their text
        for label in group.labels:
            self.coreVibrationAudio.playAudio(label.text)


if __name__ == "__main__":
    MyApp().run()
