from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.graphics import Line, Color, Rectangle

from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
from PIL import Image

from gestures4kivy import CommonGestures
from camera4kivy import Preview

from confirmation_dialog import ConfirmationDialog

class QRReader(Preview, CommonGestures):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.annotations = []

    ####################################
    # Analyze a Frame - NOT on UI Thread
    ####################################
    
    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        # pixels : Kivy Texture pixels
        # image_size   : pixels size (w,h)
        # image_pos    : location of Te/devxture in Preview Widget (letterbox)
        # scale  : scale from Analysis resolution to Preview resolution
        # mirror : true if Preview is mirrored

        pil_image = Image.frombytes(mode='RGBA', size=image_size, data= pixels)
        barcodes = pyzbar.decode(pil_image, symbols=[ZBarSymbol.QRCODE])
        found = []
        for barcode in barcodes:
            text = barcode.data.decode('utf-8')
            if 'GDT' in text:
                x, y, w, h = barcode.rect
                # Map Zbar coordinates to Kivy coordinates
                y = max(image_size[1] -y -h, 0)
                # Map Analysis coordinates to Preview coordinates
                if mirror:
                    x = max(image_size[0] -x -w, 0)
                x = round(x * scale + image_pos[0])
                y = round(y * scale + image_pos[1])
                w = round(w * scale)
                h = round(h * scale)
                found.append({'x':x, 'y':y, 'w':w, 'h':h, 't':text})

        self.make_thread_safe(list(found)) ## A COPY of the list

    @mainthread
    def make_thread_safe(self, found):
        if self.camera_connected:
            self.annotations = found
        else:
            # Clear local state so no thread related ghosts on re-connect
            self.annotations = []

    ################################
    # Annotate Screen - on UI Thread
    ################################
        
    def canvas_instructions_callback(self, texture, tex_size, tex_pos):
        # Add the analysis annotations
        Color(0,1,0,1)
        for r in self.annotations:
            Line(rectangle=(r['x'], r['y'], r['w'], r['h']), width = dp(2))

    #################################
    # User Touch Event - on UI Thread
    #################################

    def cgb_select(self, touch, x, y, lp):
        self.send_request(x, y)

    def send_request(self, x, y):
        for r in self.annotations:
            if x >= r['x'] and x <= r['x'] + r['w'] and\
               y >= r['y'] and y <= r['y'] + r['h']:
                ConfirmationDialog.client_program(r['t'])