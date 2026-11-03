# Imported libraries
from kivy.utils import platform
from plyer import vibrator, tts as plyer_tts

# Android TTS configuration
if platform == "android":
    from jnius import autoclass, cast, PythonJavaClass, java_method

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Context = autoclass("android.content.Context")
    try:
        VibrationEffect = autoclass("android.os.VibrationEffect")  # Android 8+
    except Exception:
        VibrationEffect = None
    TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
    Locale = autoclass("java.util.Locale")

    class _TTSInitListener(PythonJavaClass):
        """Java listener interface for Android TTS initialization."""
        __javainterfaces__ = ["android/speech/tts/TextToSpeech$OnInitListener"]
        __javacontext__ = "app"

        def __init__(self, callback):
            """Initializes the listener with a status callback."""
            super().__init__()
            self.callback = callback

        @java_method("(I)V")
        def onInit(self, status):
            """Triggers the callback upon TTS engine initialization."""
            self.callback(status)


class CoreVibrationAudioModule:
    """Manages device vibration and text-to-speech output."""

    def __init__(self):
        """Initializes hardware interfaces and the Android TTS engine."""
        # initialize default state
        self.vibrator = vibrator
        self.isActive = False
        self.ttsReady = False
        self.engine = None
        self.androidVibrator = None
        self.hasAmplitudeControl = False

        # setup android vibrator (needed for vibration intensity)
        if platform == "android" and VibrationEffect is not None:
            try:
                service = PythonActivity.mActivity.getSystemService(Context.VIBRATOR_SERVICE)
                self.androidVibrator = cast("android.os.Vibrator", service)
                self.hasAmplitudeControl = bool(self.androidVibrator.hasAmplitudeControl())
                print(f"Vibrator ready, amplitude control: {self.hasAmplitudeControl}")
            except Exception as e:
                print(f"Android vibrator setup failed, using plyer: {e}")

        # setup android tts engine
        if platform == "android":
            try:
                self._listener = _TTSInitListener(self._on_tts_init)  # keep reference
                self.engine = TextToSpeech(PythonActivity.mActivity, self._listener)
            except Exception as e:
                print(f"TTS engine setup failed, using plyer: {e}")

    def _on_tts_init(self, status) -> None:
        """Configures TTS language upon successful engine initialization."""
        # set language on success
        if status == TextToSpeech.SUCCESS:
            self.engine.setLanguage(Locale.US)
            self.ttsReady = True
            print("TTS ready")
            
        # log initialization failure
        else:
            print(f"TTS init failed ({status}), using plyer")

    def activateVibration(self, intensity: float = 1.0) -> None:
        """Vibrates continuously at the given intensity (0.0-1.0) until cancelled."""
        self.isActive = True
        intensity = max(0.0, min(1.0, intensity))
        if intensity == 0:
            return

        # android: real intensity control
        if self.androidVibrator is not None:
            try:
                self.androidVibrator.vibrate(self._continuous_effect(intensity))
                return
            except Exception as e:
                print(f"Intensity vibration failed, using plyer: {e}")

        # fallback: plyer continuous vibration (full strength only)
        try:
            self.vibrator.pattern(pattern=[0, 1], repeat=0)
        except NotImplementedError:
            print(f"[PC Test] Vibration ON (intensity {intensity})")
        except Exception as e:
            print(f"Continuous vibration failed, using long pulse: {e}")
            try:
                self.vibrator.vibrate(60)
            except Exception as e2:
                print(f"Vibration failed: {e2}")

    def _continuous_effect(self, intensity: float):
        """Builds a looping Android VibrationEffect for an intensity.

        Phones with amplitude control get a steady vibration at that strength
        (1-255). Phones without it get rapid on/off pulses instead: a lower
        intensity means shorter "on" time, which feels weaker.
        """
        if self.hasAmplitudeControl:
            amplitude = max(1, int(round(intensity * 255)))
            return VibrationEffect.createWaveform([0, 1000], [0, amplitude], 0)

        if intensity >= 0.95:
            return VibrationEffect.createWaveform([0, 1000], 0)
        period_ms = 100
        on_ms = max(10, int(period_ms * intensity))
        return VibrationEffect.createWaveform([0, on_ms, period_ms - on_ms], 1)

    def deactivateVibration(self) -> None:
        """Stops any active device vibration."""
        self.isActive = False
        
        # cancel active vibration
        try:
            if self.androidVibrator is not None:
                self.androidVibrator.cancel()
            else:
                self.vibrator.cancel()
        except NotImplementedError:
            print("[PC Test] Vibration OFF")
        except Exception as e:
            print(f"Vibration cancel failed: {e}")

    def playAudio(self, text: str) -> None:
        """Synthesizes and plays speech from text, interrupting active audio."""
        # speak using active engine or fallback
        try:
            if self.ttsReady:
                self.engine.speak(text, TextToSpeech.QUEUE_FLUSH, None)
            else:
                plyer_tts.speak(text)
                
        # handle desktop testing and errors
        except NotImplementedError:
            print(f"[PC Test] Playing Audio: '{text}'")
        except Exception as e:
            print(f"TTS speak failed: {e}")