import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, Frame, Label, Scrollbar, VERTICAL, HORIZONTAL, BOTH, X, Y, LEFT, RIGHT, BOTTOM

from PIL import Image, ImageTk

from services.ProveedorServices import ProveedorService
from utils.fs_util import get_resource_path


class ProveedoresScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._proveedores_service = ProveedorService()
        self._proveedor_seleccionado = None
        self._proveedores = self._proveedores_service.get_all_proveedores()
        self.widgets()
        self.actualizar_proveedores()

    def widgets(self):
        # Frame para el título
        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="PROVEEDORES", font=("Arial", 20), bg="#dddddd", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        # Frame para el contenido principal
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        # LabelFrame para el formulario de proveedor
        lblframe_proveedor = tk.LabelFrame(frame2, text="Datos del proveedor", font=("Arial", 12), bg="#C6D9E3",
                                           fg="black")
        lblframe_proveedor.place(x=20, y=30, width=400, height=500)

        # Campos del formulario

        self.id_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))

        tk.Label(lblframe_proveedor, text="Nombre:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=10)
        self.nombre_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))
        self.nombre_entry.place(x=140, y=20, width=240, height=40)

        tk.Label(lblframe_proveedor, text="Teléfono:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=80)
        self.telefono_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))
        self.telefono_entry.place(x=140, y=80, width=240, height=40)

        tk.Label(lblframe_proveedor, text="Dirección:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=140)
        self.direccion_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))
        self.direccion_entry.place(x=140, y=140, width=240, height=40)

        # Botones del formulario
        ttk.Button(lblframe_proveedor, text="Agregar", command=self.agregar_proveedor).place(x=80, y=200, width=240,
                                                                                             height=40)
        ttk.Button(lblframe_proveedor, text="Editar", command=self.editar_proveedor).place(x=80, y=260, width=240,
                                                                                           height=40)
        ttk.Button(lblframe_proveedor, text="Reporte de proveedores",
                   command=lambda: ProveedorReporteScreen(self)).place(x=80, y=320, width=240,
                                                                       height=40)

        # Treeview para la tabla de proveedores
        treframe = tk.Frame(frame2, bg="white")
        treframe.place(x=450, y=30, width=630, height=400)

        Scrol_y = ttk.Scrollbar(treframe)
        Scrol_y.pack(side=tk.RIGHT, fill=tk.Y)

        Scrol_x = ttk.Scrollbar(treframe, orient=tk.HORIZONTAL)
        Scrol_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(treframe, columns=("Nombre", "Telefono", "Direccion"), show="headings",
                                 yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set, selectmode='browse')

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', func=self.on_proveedor_selected)

        Scrol_y.config(command=self.tree.yview)
        Scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Nombre")
        self.tree.heading("#2", text="Teléfono")
        self.tree.heading("#3", text="Dirección")

        self.tree.column("Nombre", anchor="center")
        self.tree.column("Telefono", anchor="center")
        self.tree.column("Direccion", anchor="center")

        # Botón para actualizar la tabla
        btn_actualizar = ttk.Button(frame2, text="Actualizar Proveedores", command=self.actualizar_proveedores)
        btn_actualizar.place(x=440, y=480, width=260, height=50)

    def agregar_proveedor(self):
        # Implementar la lógica para agregar un proveedor
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        direccion = self.direccion_entry.get()

        try:
            self._proveedores_service.save(nombre, telefono, direccion)
            self.limpiar_campos()
            self.actualizar_proveedores()

            tk.messagebox.showinfo('Proveedor registrado', 'Proveedor registrado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar guardar al proveedor')

        pass

    def editar_proveedor(self):
        if self._proveedor_seleccionado is None:
            return

        proveedor_id = self._proveedor_seleccionado.id
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        direccion = self.direccion_entry.get()

        data = {'nombre': nombre, 'telefono': telefono, 'direccion': direccion}

        try:
            self._proveedores_service.update_proveedor(proveedor_id, data)
            self.limpiar_campos()
            self.actualizar_proveedores()

            tk.messagebox.showinfo('Proveedor actualizado', 'Proveedor actualizado exitosamente')
        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar actualizar al proveedor')

    def eliminar_proveedor(self):
        # todo remove
        return
        id = self.id_entry.get()

        try:

            self._proveedores_service.delete_proveedor(int(id))
            self.limpiar_campos()
            self.actualizar_proveedores()

            tk.messagebox.showinfo('Proveedor eliminado', 'Proveedor eliminado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar eliminar al proveedor')

    def actualizar_proveedores(self):
        # Implementar la lógica para actualizar la tabla de proveedores
        proveedores = self._proveedores_service.get_all_proveedores()

        self.tree.delete(*self.tree.get_children())

        for proveedor in proveedores:
            self.tree.insert('', tk.END, values=(proveedor.nombre, proveedor.telefono, proveedor.direccion),
                             iid=proveedor.id)

        self._proveedor_seleccionado = None

    def on_proveedor_selected(self, event) -> None:
        selection = self.tree.selection()

        if len(selection) == 0:
            return

        iid = selection[0]

        for proveedor in self._proveedores:
            if proveedor.id == int(iid):
                self._proveedor_seleccionado = proveedor
                break

        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, self._proveedor_seleccionado.id)

        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, self._proveedor_seleccionado.nombre)

        self.telefono_entry.delete(0, tk.END)
        self.telefono_entry.insert(0, self._proveedor_seleccionado.telefono)

        self.direccion_entry.delete(0, tk.END)
        self.direccion_entry.insert(0, self._proveedor_seleccionado.direccion)

    def limpiar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)


class ProveedorReporteScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Reporte de Proveedores")
        self.geometry("800x550")
        self.resizable(False, False)
        self.config(bg="#C6D9E3")

        self.proveedor_service = ProveedorService()
        self.proveedores = []

        # Header
        images_folder = get_resource_path('imagenes')
        image_path = os.path.join(images_folder, "artvinil.png")

        header_frame = Frame(self, bg="#C6D9E3")
        header_frame.pack(fill='x')

        self.logo_image = Image.open(image_path)
        self.logo_image = self.logo_image.resize((150, 150))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = Label(header_frame, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.pack(pady=10)

        # Search Fields
        frame_busqueda = Frame(self, bg="#C6D9E3")
        frame_busqueda.pack(fill=X, padx=10, pady=5)

        label_buscar_nombre = Label(frame_busqueda, text="Nombre:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_nombre.pack(side=LEFT, padx=5)
        self.entry_buscar_nombre = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_nombre.pack(side=LEFT, padx=5)
        self.entry_buscar_nombre.bind("<KeyRelease>", self.buscar_proveedores)

        label_buscar_telefono = Label(frame_busqueda, text="Teléfono:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_telefono.pack(side=LEFT, padx=5)
        self.entry_buscar_telefono = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_telefono.pack(side=LEFT, padx=5)
        self.entry_buscar_telefono.bind("<KeyRelease>", self.buscar_proveedores)

        # Treeview
        treframe = Frame(self, bg="#C6D9E3")
        treframe.pack(fill=BOTH, expand=True, padx=10, pady=5)

        Scrol_y = Scrollbar(treframe, orient=VERTICAL)
        Scrol_y.pack(side=RIGHT, fill=Y)

        Scrol_x = Scrollbar(treframe, orient=HORIZONTAL)
        Scrol_x.pack(side=BOTTOM, fill=X)

        self.tree_proveedores = ttk.Treeview(treframe, columns=("Nombre", "Teléfono", "Dirección"), show="headings",
                                             yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)

        Scrol_y.config(command=self.tree_proveedores.yview)
        Scrol_x.config(command=self.tree_proveedores.xview)

        self.tree_proveedores.heading("#1", text="Nombre")
        self.tree_proveedores.heading("#2", text="Teléfono")
        self.tree_proveedores.heading("#3", text="Dirección")

        self.tree_proveedores.column("Nombre", width=200, anchor="center")
        self.tree_proveedores.column("Teléfono", width=130, anchor="center")
        self.tree_proveedores.column("Dirección", width=200, anchor="center")

        self.tree_proveedores.pack(fill=BOTH, expand=True)

        self.refrescar_proveedores()

    def buscar_proveedores(self, event=None):
        termino_nombre = self.entry_buscar_nombre.get().lower()
        termino_telefono = self.entry_buscar_telefono.get().lower()
        self.refrescar_proveedores(termino_nombre, termino_telefono)

    def refrescar_proveedores(self, termino_nombre="", termino_telefono=""):
        self.proveedores = self.proveedor_service.get_all_proveedores()
        self.tree_proveedores.delete(*self.tree_proveedores.get_children())

        for proveedor in self.proveedores:
            nombre = proveedor.nombre.lower()
            telefono = proveedor.telefono.lower()

            if termino_nombre in nombre and termino_telefono in telefono:
                self.tree_proveedores.insert("", "end",
                                             values=(proveedor.nombre, proveedor.telefono, proveedor.direccion))
