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
            if criterio not in puntajes:
                raise ValueError(f"Falta el puntaje de: {criterio}")
            if not (0 <= puntajes[criterio] <= 10):
                raise ValueError(f"Puntaje de {criterio} fuera del rango 0-10")
        self._puntajes = puntajes

    def Total(self):
        total = 0
        for valor in self._puntajes.values():
            total += valor
        return total

    def promedio(self):
        if not self._puntajes:
            return 0
        return self.Total() / len(self._puntajes)

    def mostrar_info(self):
        base = super().mostrar_info()
        if self._puntajes:
            return f"{base} | Categoría: {self._categoria} | Total: {self.Total()} | Promedio: {self.promedio():.2f}"
        else:
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
        for b in self.bandas:
            if b.nombreBanda == banda.nombreBanda:
                print(f"La banda {banda.nombreBanda} ya está inscrita")
                return
        self.bandas.append(banda)
        print(f"La banda {banda.nombreBanda} ha sido inscrita correctamente")

    def guardar_en_archivo(self, nombre_archivo="bandas.txt"):
        try:
            archivo = open(nombre_archivo, "w", encoding="utf-8")
            for b in self.bandas:
                puntajes_str = ""
                for criterio, valor in b._puntajes.items():
                    puntajes_str += f"{criterio}:{valor};"
                archivo.write(f"{b.nombreBanda},{b.institucion},{b._categoria},{puntajes_str}\n")
            archivo.close()
            print("Bandas guardadas en archivo correctamente")
        except Exception as e:
            print(f"Error al guardar bandas: {e}")

    def cargar_desde_archivo(self, nombre_archivo="bandas.txt"):
        try:
            archivo = open(nombre_archivo, "r", encoding="utf-8")
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    partes = linea.split(",")
                    nombre, institucion, categoria = partes[:3]
                    banda = Banda(nombre, institucion, categoria)
                    if len(partes) > 3 and partes[3]:
                        puntajes_str = partes[3].split(";")
                        puntajes = {}
                        for p in puntajes_str:
                            if ":" in p and p.strip() != "":
                                criterio, valor = p.split(":")
                                puntajes[criterio] = float(valor)
                        banda.registrarPuntajes(puntajes)
                    self.bandas.append(banda)
            archivo.close()
            print("Bandas cargadas desde archivo")
        except FileNotFoundError:
            print("No existe el archivo, se creará al guardar")
        except Exception as e:
            print(f"Error al cargar bandas: {e}")

    def listar_bandas(self):
        for b in self.bandas:
            print(b.mostrar_info())

    def listar_bandas_ordenadas(self, criterio="nombre"):
        ordenador = OrdenadorBandas()
        bandas_ordenadas = ordenador.quicksort(self.bandas, criterio)
        print(f"\nBandas ordenadas por {criterio}:")
        for b in bandas_ordenadas:
            print(b.mostrar_info())


class ConcursoAPP:
    def __init__(self):
        self.concurso = Concurso("Concurso Escolar", "14/09/2025")
        self.concurso.cargar_desde_archivo()
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("600x400")

        self.menu()
        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 12, "bold"),
            justify="center"
        ).pack(pady=20)

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

        tk.Label(ventana, text="Nombre de la Banda:").pack()
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()

        tk.Label(ventana, text="Institución:").pack()
        entry_institucion = tk.Entry(ventana)
        entry_institucion.pack()

        tk.Label(ventana, text="Categoría (Primaria, Basico, Diversificado):").pack()
        entry_categoria = tk.Entry(ventana)
        entry_categoria.pack()

        def guardar():
            nombre = entry_nombre.get()
            institucion = entry_institucion.get()
            categoria = entry_categoria.get()
            try:
                banda = Banda(nombre, institucion, categoria)
                if self.concurso.inscribir(banda):
                    self.concurso.guardar_en_archivo()
                    tk.Label(ventana, text=f"Banda {nombre} inscrita correctamente", fg="green").pack()
                else:
                    tk.Label(ventana, text=f"La banda {nombre} ya está inscrita", fg="red").pack()
            except ValueError as e:
                tk.Label(ventana, text=str(e), fg="red").pack()

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

    def registrar_evaluacion(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Registrar Evaluación")
        ventana.geometry("400x400")

        tk.Label(ventana, text="Nombre de la Banda a Evaluar:").pack()
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()

        entradas_puntajes = {}
        for criterio in Banda.criterios:
            tk.Label(ventana, text=f"Puntaje {criterio} (0-10):").pack()
            e = tk.Entry(ventana)
            e.pack()
            entradas_puntajes[criterio] = e

        def guardar():
            nombre = entry_nombre.get()
            banda = next((b for b in self.concurso.bandas if b.nombreBanda == nombre), None)
            if not banda:
                tk.Label(ventana, text=f"Banda {nombre} no encontrada", fg="red").pack()
                return
            try:
                puntajes = {}
                for criterio, entry in entradas_puntajes.items():
                    valor = float(entry.get())
                    puntajes[criterio] = valor
                banda.registrarPuntajes(puntajes)
                self.concurso.guardar_en_archivo()
                tk.Label(ventana, text=f"Puntajes registrados para {nombre}", fg="green").pack()
            except ValueError as e:
                tk.Label(ventana, text=str(e), fg="red").pack()

        tk.Button(ventana, text="Guardar Puntajes", command=guardar).pack(pady=10)

    def listar_bandas(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Listado de Bandas")
        ventana.geometry("600x400")

        text = tk.Text(ventana)
        text.pack(expand=True, fill="both")

        for b in self.concurso.bandas:
            text.insert("end", b.mostrar_info() + "\n\n")

    def ver_ranking(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Ranking Final")
        ventana.geometry("600x400")

        text = tk.Text(ventana)
        text.pack(expand=True, fill="both")

        ordenador = OrdenadorBandas()
        bandas_ordenadas = ordenador.quicksort(self.concurso.bandas, "puntaje")

        for i, b in enumerate(bandas_ordenadas, 1):
            text.insert("end", f"Posición {i}: {b.mostrar_info()}\n\n")


if __name__ == "__main__":
    ConcursoAPP()
