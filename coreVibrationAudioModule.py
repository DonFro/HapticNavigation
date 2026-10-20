from plyer import vibrator, tts


class CoreVibrationAudioModule:
    """A class to manage vibration and audio functionality"""
    
    def __init__(self):
        """Constructor for the CoreVibrationAudioModule class"""
        self.vibrator = vibrator
        self.tts = tts
        self.isActive = False
        self.vibrationStrength = 0.5

    def activateVibration(self) -> None:
        """Activate the vibration module"""
        self.isActive = True
        try:
            self.vibrator.vibrate(self.vibrationStrength)
        except NotImplementedError:
            print("[PC Test] Vibration ON")
            
    def deactivateVibration(self) -> None:
        """Deactivate the vibration module"""
        self.isActive = False
        try:
            self.vibrator.cancel()
        except NotImplementedError:
            print("[PC Test] Vibration OFF")

    def playAudio(self, text: str) -> None:
        """Play audio using text-to-speech"""
        try:
            self.tts.speak(text)
        except NotImplementedError:
            print(f"[PC Test] Playing Audio: '{text}'")