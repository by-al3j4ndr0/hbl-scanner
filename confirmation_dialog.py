from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.textfield import (
    MDTextField, 
    MDTextFieldHintText, 
    MDTextFieldMaxLengthText,
)
from kivymd.uix.divider import MDDivider

from kivy.uix.widget import Widget

import requests

class APIRequest():
    def query(self, r):
        hbl_splitted = str.split(r, "/")
        hbl = hbl_splitted[0]
        params = {'hbl': hbl}
        url = 'https://alejandroperezhdez.pythonanywhere.com/v1/query'

        response = requests.get(url=url, params=params)

        API_DATA = response.json()

        hbl = str(API_DATA['hbl']).replace("['", "").replace("']", "")
        name = str(API_DATA['name']).replace("['", "").replace("']", "")
        city = str(API_DATA['city']).replace("['", "").replace("']", "")
        state = str(API_DATA['state']).replace("['", "").replace("']", "")

        ConfirmationDialog.show_confirmation(hbl, name, city, state)

class ConfirmationDialog(MDDialog):
    def show_confirmation(hbl, name, city, state):
        def close_dialog(obj):
            dialog.dismiss()

        def validate(obj):
            params = {'hbl': hbl}
            url = 'https://alejandroperezhdez.pythonanywhere.com/v1/confirm'
            response = requests.get(url=url, params=params)
            if response.status_code == 200:
                dialog.dismiss()
            
        dialog = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon = "ticket-confirmation",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text = "Confirmacion",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text = "Confirme la siguiente informacion con la del HBL",
            ),
            # -----------------------Custom content------------------------
            MDDialogContentContainer(
                MDDivider(),
                    MDDialogSupportingText(
                        text = "Nombre y Apellidos: " + name,
                    ),
                    MDDialogSupportingText(
                        text = "Municipio: " + city,
                    ),
                    MDDialogSupportingText(
                        text = "Provincia: " + state,
                    ),
                    MDDialogSupportingText(
                        text = "HBL: " + hbl,
                    ),
                MDDivider(),
                orientation = "vertical",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "No"),
                    style="text",
                    on_release = close_dialog
                ),
                MDButton(
                    MDButtonText(text = "Si"),
                    style="text",
                    on_release = validate
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        dialog.open()

class HBLWritter(MDDialog):
    def show_dialog(self):
        def close(self):
            hbl_dialog.dismiss()
        
        def send_hbl(self):
            hbl = hbl_input._get_text()
            APIRequest().query(hbl)
            hbl_dialog.dismiss()
    
        dialog_icon = MDDialogIcon(icon = "keyboard")
        dialog_headline_text = MDDialogHeadlineText(text = "HBL Input")
        
        content_container = MDDialogContentContainer(orientation = "vertical")

        hbl_input = MDTextField(
                        MDTextFieldHintText(
                            text = "HBL"
                        ),
                        MDTextFieldMaxLengthText(
                            max_text_length = 11
                        ),
                        mode = "outlined",
                        required = True,
                        text = "GDT",
                        input_type = "number"
                    )
        
        button_container = MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text = "Cancel"),
                        style="text",
                        on_release=close
                    ),
                    MDButton(
                        MDButtonText(text = "Send"),
                        style="text",
                        on_release=send_hbl
                    ),
                    spacing="8dp",
                )
        
        content_container.add_widget(hbl_input)

        hbl_dialog = MDDialog()
        hbl_dialog.add_widget(dialog_icon)
        hbl_dialog.add_widget(dialog_headline_text)
        hbl_dialog.add_widget(content_container)
        hbl_dialog.add_widget(button_container)
        hbl_dialog.open()