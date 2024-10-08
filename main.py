from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock
from applayout import AppLayout
from android_permissions import AndroidPermissions
from confirmation_dialog import HBLWritter

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread 
        # so use Window.width and Window.height
        if Window.width > Window.height: 
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar 
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
else:
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config 
    Config.set('input', 'mouse', 'mouse, disable_multitouch')

class MyApp(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.layout = AppLayout()
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
        return self.layout

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
        # Can't connect camera till after on_start()
        Clock.schedule_once(self.connect_camera)

    def connect_camera(self,dt):
        self.layout.qr_reader.connect_camera(enable_analyze_pixels = True,
                                             enable_video = False)

    def on_stop(self):
        self.layout.qr_reader.disconnect_camera()

    def open_input(self):
        HBLWritter().show_dialog()

MyApp().run()

