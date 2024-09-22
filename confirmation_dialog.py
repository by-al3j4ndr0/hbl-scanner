from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider

from kivy.uix.widget import Widget

import requests

class APIRequest():
    def query(r):
        hbl_splitted = str.split(r, "/")
        hbl = hbl_splitted[0]
        params = {'hbl': hbl}
        url = 'http://127.0.0.1:8000/v1/query'

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
            dialog.dismiss()
            params = {'hbl': hbl}
            url = 'http://127.0.0.1:8000/v1/confirm'

            response = requests.get(url=url, params=params)

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