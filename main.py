import tkinter as tk


class Participantes:
    def __init__(self, nombreBanda, institucion):
        self.nombreBanda = nombreBanda
        self.institucion = institucion

    def mostrar_info(self):
        return f"El nombre de la banda es: {self.nombreBanda} de la institución {self.institucion}"


class Banda(Participantes):
    categoriasValidas = ["Primaria", "Basico", "Diversificado"]
    criterios = ["ritmo", "uniformidad", "coreografia", "alineacion", "puntualidad"]

    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion)
        self._categoria = None
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria not in Banda.categoriasValidas:
            raise ValueError(f"Categoría inválida: {categoria}")
        self._categoria = categoria

    def registrarPuntajes(self, puntajes):
        for criterio in Banda.criterios:
            if criterio not in puntajes or puntajes[criterio] is None:
                raise ValueError(f"Falta el puntaje de: {criterio}")
            try:
                valor = float(puntajes[criterio])
                if not (0 <= valor <= 10):
                    raise ValueError(f"Puntaje de {criterio} fuera del rango 0-10")
                self._puntajes[criterio] = valor
            except ValueError:
                raise ValueError(f"El puntaje de {criterio} debe ser un número válido.")

    def Total(self):
        return sum(self._puntajes.values()) if self._puntajes else 0

    def promedio(self):
        if not self._puntajes:
            return 0
        return self.Total() / len(self._puntajes)

    def mostrar_info(self):
        base = super().mostrar_info()
        if self._puntajes:
            return f"{base} | Categoría: {self._categoria} | Total: {self.Total()} | Promedio: {self.promedio():.2f}"
        return f"{base} | Categoría: {self._categoria} | Sin evaluación"


class OrdenadorBandas:
    def quicksort(self, lista, criterio):
        if len(lista) <= 1:
            return lista
        else:
            pivote = lista[0]
            if criterio == "nombre":
                menores = [x for x in lista[1:] if x.nombreBanda.lower() <= pivote.nombreBanda.lower()]
                mayores = [x for x in lista[1:] if x.nombreBanda.lower() > pivote.nombreBanda.lower()]
            elif criterio == "puntaje":
                menores = [x for x in lista[1:] if x.Total() <= pivote.Total()]
                mayores = [x for x in lista[1:] if x.Total() > pivote.Total()]
            else:
                return lista
            return self.quicksort(menores, criterio) + [pivote] + self.quicksort(mayores, criterio)


class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = []

    def inscribir(self, banda):
        if any(b.nombreBanda == banda.nombreBanda for b in self.bandas):
            return False
        self.bandas.append(banda)
        return True

    def guardar_en_archivo(self, label_mensaje):
        try:
            with open("Bandas", "w", encoding="utf-8") as archivo:
                for b in self.bandas:
                    puntajes_str = ";".join([f"{criterio}:{valor}" for criterio, valor in b._puntajes.items()])
                    archivo.write(f"{b.nombreBanda},{b.institucion},{b._categoria},{puntajes_str}\n")
            label_mensaje.config(text="Bandas guardadas en archivo correctamente.", fg="green")
        except Exception as e:
            label_mensaje.config(text=f"Error al guardar bandas: {e}", fg="red")

    def cargar_desde_archivo(self, label_mensaje):
        try:
            self.bandas.clear()
            with open("Bandas", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    partes = linea.split(",", 3)
                    nombre, institucion, categoria = partes[:3]
                    banda = Banda(nombre, institucion, categoria)
                    if len(partes) > 3 and partes[3]:
                        puntajes_str = partes[3].split(";")
                        puntajes = {}
                        for p in puntajes_str:
                            if ":" in p:
                                criterio, valor = p.split(":", 1)
                                try:
                                    puntajes[criterio] = float(valor)
                                except ValueError:
                                    pass
                        if puntajes:
                            banda.registrarPuntajes(puntajes)
                    self.bandas.append(banda)
            label_mensaje.config(text="Bandas cargadas desde archivo.", fg="green")
        except FileNotFoundError:
            label_mensaje.config(text="No existe el archivo, se creará al guardar.", fg="blue")
        except Exception as e:
            label_mensaje.config(text=f"Error al cargar bandas: {e}", fg="red")


class ConcursoBandasApp:
    def __init__(self):
        self.concurso = Concurso("Concurso Escolar", "14/09/2025")
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("700x500")
        self.ventana.configure(bg="#f0f0f0")

        self.menu()

        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 14, "bold"),
            justify="center",
            bg="#f0f0f0"
        ).pack(pady=(50, 10))

        self.label_feedback = tk.Label(self.ventana, text="", bg="#f0f0f0", font=("Arial", 10))
        self.label_feedback.pack(pady=(0, 10))
        self.concurso.cargar_desde_archivo(self.label_feedback)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Inscribir Banda", command=self.inscribir_banda)
        opciones.add_command(label="Registrar Evaluación", command=self.registrar_evaluacion)
        opciones.add_command(label="Listar Bandas", command=self.listar_bandas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu=barra)

    def inscribir_banda(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Inscribir Banda")
        ventana.geometry("400x300")
        ventana.configure(bg="#f9f9f9")

        frame = tk.Frame(ventana, padx=15, pady=15, bg="#f9f9f9")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Nombre de la Banda:", bg="#f9f9f9").pack(anchor="w", pady=(10, 0))
        entry_nombre = tk.Entry(frame, width=40)
        entry_nombre.pack(fill="x")

        tk.Label(frame, text="Institución:", bg="#f9f9f9").pack(anchor="w", pady=(10, 0))
        entry_institucion = tk.Entry(frame, width=40)
        entry_institucion.pack(fill="x")

        tk.Label(frame, text="Categoría (Primaria, Basico, Diversificado):", bg="#f9f9f9").pack(anchor="w",
                                                                                                pady=(10, 0))
        var_categoria = tk.StringVar(ventana)
        var_categoria.set(Banda.categoriasValidas[0])
        opciones_categoria = tk.OptionMenu(frame, var_categoria, *Banda.categoriasValidas)
        opciones_categoria.pack(fill="x")

        label_feedback = tk.Label(frame, text="", bg="#f9f9f9")
        label_feedback.pack(pady=10)

        def guardar():
            nombre = entry_nombre.get().strip()
            institucion = entry_institucion.get().strip()
            categoria = var_categoria.get()
            if not nombre or not institucion or not categoria:
                label_feedback.config(text="Error: Todos los campos son obligatorios.", fg="red")
                return

            try:
                banda = Banda(nombre, institucion, categoria)
                if self.concurso.inscribir(banda):
                    self.concurso.guardar_en_archivo(label_feedback)
                    label_feedback.config(text=f"Banda '{nombre}' inscrita correctamente.", fg="green")
                    self.limpiar_campos(entry_nombre, entry_institucion)
                    var_categoria.set(Banda.categoriasValidas[0])
                else:
                    label_feedback.config(text=f"Error: La banda '{nombre}' ya está inscrita.", fg="red")
            except ValueError as e:
                label_feedback.config(text=str(e), fg="red")

        def limpiar():
            self.limpiar_campos(entry_nombre, entry_institucion)
            var_categoria.set(Banda.categoriasValidas[0])
            label_feedback.config(text="")

        button_frame = tk.Frame(frame, bg="#f9f9f9")
        button_frame.pack(fill="x", pady=15)
        tk.Button(button_frame, text="Guardar ✅", command=guardar, bg="#4caf50", fg="white").pack(side="left",
                                                                                                  expand=True, padx=5)
        tk.Button(button_frame, text="Limpiar 🧹", command=limpiar, bg="#ff9800", fg="white").pack(side="right",
                                                                                                  expand=True, padx=5)

    def registrar_evaluacion(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Registrar Evaluación")
        ventana.geometry("450x450")
        ventana.configure(bg="#f9f9f9")

        frame = tk.Frame(ventana, padx=15, pady=15, bg="#f9f9f9")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Nombre de la Banda a Evaluar:", bg="#f9f9f9").pack(anchor="w", pady=(10, 0))
        var_banda = tk.StringVar(ventana)
        opciones_banda = tk.OptionMenu(frame, var_banda, *[b.nombreBanda for b in self.concurso.bandas])
        opciones_banda.pack(fill="x")

        entradas_puntajes = {}
        for criterio in Banda.criterios:
            tk.Label(frame, text=f"Puntaje de {criterio} (0-10):", bg="#f9f9f9").pack(anchor="w", pady=(10, 0))
            e = tk.Entry(frame, width=10)
            e.pack(anchor="w")
            e.insert(0, "0")
            entradas_puntajes[criterio] = e

        label_feedback = tk.Label(frame, text="", bg="#f9f9f9")
        label_feedback.pack(pady=10)

        def guardar():
            nombre = var_banda.get().strip()
            banda = next((b for b in self.concurso.bandas if b.nombreBanda == nombre), None)
            if not banda:
                label_feedback.config(text="Error: Banda no encontrada. Por favor, selecciona una banda.", fg="red")
                return

            try:
                puntajes = {criterio: entry.get() for criterio, entry in entradas_puntajes.items()}
                banda.registrarPuntajes(puntajes)
                self.concurso.guardar_en_archivo(label_feedback)
                label_feedback.config(text=f"Puntajes registrados para '{nombre}'.", fg="green")
                self.limpiar_campos_evaluacion(var_banda, entradas_puntajes)
            except ValueError as e:
                label_feedback.config(text=str(e), fg="red")

        def limpiar():
            self.limpiar_campos_evaluacion(var_banda, entradas_puntajes)
            label_feedback.config(text="")

        button_frame = tk.Frame(frame, bg="#f9f9f9")
        button_frame.pack(fill="x", pady=15)
        tk.Button(button_frame, text="Guardar Puntajes ✅", command=guardar, bg="#4caf50", fg="white").pack(side="left",
                                                                                                           expand=True,
                                                                                                           padx=5)
        tk.Button(button_frame, text="Limpiar 🧹", command=limpiar, bg="#ff9800", fg="white").pack(side="right",
                                                                                                  expand=True, padx=5)

    def listar_bandas(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Listado de Bandas")
        ventana.geometry("700x500")
        ventana.configure(bg="#f9f9f9")

        frame = tk.Frame(ventana, padx=15, pady=15, bg="#f9f9f9")
        frame.pack(expand=True, fill="both")

        text = tk.Text(frame, wrap="word", bg="white", fg="#333", font=("Arial", 10), bd=0, padx=10, pady=10)
        text.pack(expand=True, fill="both")

        for b in self.concurso.bandas:
            text.insert("end", b.mostrar_info() + "\n\n")

    def ver_ranking(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Ranking Final")
        ventana.geometry("700x500")
        ventana.configure(bg="#f9f9f9")

        frame = tk.Frame(ventana, padx=15, pady=15, bg="#f9f9f9")
        frame.pack(expand=True, fill="both")

        text = tk.Text(frame, wrap="word", bg="white", fg="#333", font=("Arial", 10), bd=0, padx=10, pady=10)
        text.pack(expand=True, fill="both")

        ordenador = OrdenadorBandas()
        bandas_ordenadas = ordenador.quicksort(self.concurso.bandas, "puntaje")

        for i, b in enumerate(bandas_ordenadas, 1):
            text.insert("end", f"Posición {i}: {b.mostrar_info()}\n\n")

    def limpiar_campos(self, *widgets):
        for widget in widgets:
            widget.delete(0, tk.END)

    def limpiar_campos_evaluacion(self, var_banda, entradas_puntajes):
        var_banda.set("")
        for entry in entradas_puntajes.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")


if __name__ == "__main__":
    ConcursoBandasApp()