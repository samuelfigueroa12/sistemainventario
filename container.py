from tkinter import *
import tkinter as tk

from screens.UsersWindow import UsersWindow
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk
from utils import user
from tkinter import messagebox
from screens.clientesScreen import ClientesScreen
from screens.proveedoresScreen import ProveedoresScreen

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.configure(bg="#6CD9E3")
        self.place(x=0, y=0, width=800, height=400)
        self.widgets()

    def show_frame(self, container):
        Top_level = tk.Toplevel(self)
        frame = container(Top_level, self.controlador)
        frame.config(bg="#6CD9E3")
        frame.pack(fill="both", expand=True)
        Top_level.geometry("1100x650+120+20")
        Top_level.resizable(False, False)

        Top_level.transient(self.master)
        Top_level.grab_set()
        Top_level.focus_set()
        Top_level.lift()

    def ventas(self):
        self.show_frame(Ventas)

    def inventario(self):

        self.show_frame(Inventario)

    def clientes(self): # Método para mostrar ClientesScreen
        self.show_frame(ClientesScreen)

    def proveedores(self): # Método para mostrar ProveedoresScreen
        self.show_frame(ProveedoresScreen)

    def usuarios(self):
        if user().rol != 'admin':
            return

        users_window = UsersWindow()
        users_window.mainloop()

    def widgets(self):
        frame1 = tk.Frame(self, bg="#F5F5F5")
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)

        btnventas = Button(frame1, bg="#f4b400", fg="white", font="sans 14 bold", text="ir a ventas", command=self.ventas)
        btnventas.place(x=500, y=30, width=140, height=50)

        btninventario = Button(frame1, bg="#c62e26", fg="white", font="sans 14 bold", text="ir a inventario", command=self.inventario)
        btninventario.place(x=500, y=100, width=140, height=50)

        btnclientes = Button(frame1, bg="#4CAF50", fg="white", font="sans 14 bold", text="Clientes", command=self.clientes, bd=4, relief=RAISED) # Usar self.clientes
        btnclientes.place(x=650, y=30, width=140, height=50)

        btnproveedores = Button(frame1, bg="#2196F3", fg="white", font="sans 14 bold", text="Proveedores", command=self.proveedores, bd=4, relief=RAISED) # Usar self.proveedores
        btnproveedores.place(x=650, y=100, width=140, height=50)

        btnusers = Button(frame1, bg="#2196F3", fg="white", font="sans 14 bold", text="Usuarios",
                                command=self.usuarios, bd=4, relief=RAISED)
        btnusers.place(x=650, y=200, width=140, height=50)

        logout_button = Button(frame1, text="Cerrar sesión", command=self.controlador.logout)
        logout_button.place(x=680, y=350, width=100, height=30)

        self.logo_image = Image.open("imagenes/registradora.webp")
        self.logo_image = self.logo_image.resize((220,220))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = Label(frame1, image=self.logo_image, bg="#F5F5F5")
        self.logo_label.place(x=170, y=90, width=200, height=200)

        empresa_label = Label(frame1, text="AR-T-VINIL", font=("Arial", 20, "bold"), bg="#F5F5F5", fg="black")
        empresa_label.place(x=190, y=20)

        copyright_label = Label(frame1, text="© 2025 - Todos los derechos reservados", bg="#F5F5F5", fg="gray", font="sans 10")
        copyright_label.place(x=170, y=350)