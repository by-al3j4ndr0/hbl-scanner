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

import socket
import pickle

class Connector:
    host = '192.168.43.196'  # as both code is running on same pc
    port = 9090  # socket server port number

    socket = None

    def connection():    
        Connector.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        Connector.socket.connect((Connector.host, Connector.port))  # connect to the server

    def client_program(r):
        Connector.socket.send(r.encode())  # send message
        data = Connector.socket.recv(4096) # receive response
        data_arr = pickle.loads(data) # decode recive string to a array

        ConfirmationDialog.show_confirmation(data_arr)

    def validation(status):
        status_str = pickle.dumps(status)

        if status == True:
            Connector.socket.send(status_str)   

class ConfirmationDialog(MDDialog, Connector):
    def show_confirmation(data_arr):
        def close_dialog(obj):
            dialog.dismiss()
            status = False
            Connector.validation(status)

        def validate(obj):
            dialog.dismiss()
            status = True
            Connector.validation(status)

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
                        text = "Nombre y Apellidos: " + data_arr[0],
                    ),
                    MDDialogSupportingText(
                        text = "Municipio: " + data_arr[1],
                    ),
                    MDDialogSupportingText(
                        text = "Provincia: " + data_arr[2],
                    ),
                    MDDialogSupportingText(
                        text = "HBL: " + data_arr[3],
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