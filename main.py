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
