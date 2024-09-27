from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from kivy.utils import platform
from qrreader import QRReader

class AppLayout(FloatLayout):
    qr_reader = ObjectProperty()
        
class ButtonsLayout(RelativeLayout):
    normal = StringProperty()
    down = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
  
    def on_size(self, layout, size):
        if Window.width < Window.height:
            self.pos = (0 , 0)
            self.size_hint = (1 , 0.2)
            self.ids.torch.pos_hint  = {'center_x':.5,'center_y':.5}
            self.ids.torch.size_hint = (.2, None)
        else:
            self.pos = (Window.width * 0.8, 0)
            self.size_hint = (0.2 , 1)
            self.ids.torch.pos_hint  = {'center_x':.5,'center_y':.5}
            self.ids.torch.size_hint = (None, .2)

Builder.load_string("""
<AppLayout>:        
    qr_reader: self.ids.preview
    QRReader:
        aspect_ratio: '4:3'
        pos_hint: {"center_x": .5, "center_y": .5}
        id:preview
                    
    MDTopAppBar:
        type: "small"
        pos_hint: {"center_x": .5, "center_y": .95}
                    
        MDTopAppBarTitle:
            text: "Scanner"

    MDBottomAppBar:
        md_bg_color: app.theme_cls.surfaceColor
        size_hint_y: 0.1
        pos_hint: {"center_x": .5, "center_y": 0.05}
                    
    MDButton:
        pos_hint: {"center_x": .8, "center_y": .05}

        MDButtonIcon:
            icon: "keyboard"

        MDButtonText:
            text: "Ingresar HBL"    
    """)

            
