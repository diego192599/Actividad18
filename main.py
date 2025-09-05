class Participantes:
    def __init__(self, nombreBanda,institucion):
        self.nombreBanda=nombreBanda
        self.institucion=institucion

    def mostrar_info(self):
        return f"El nombre de la banda es: {self.nombreBanda} de la isntitucion {self.institucion}"


class Banda(Participantes):
    categoriaValidas=["Primaria","Basico","Diversificado"]
    Criterios=["ritmo","uniformidad","coreografia","alineacion","puntualidad"]
    def __init__(self,nombre,institucion,categoria):
        super().__init__(nombre,institucion)
        self.categoria=None
        self.puntaje=[]
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria not in Banda.categoriasValidas:
            raise ValueError(f"Categoría inválida: {categoria}")
        self._categoria = categoria

    def registrarPuntaje(self,puntaje: list):
        if len(puntaje)!=len(Banda.Criterios):
            raise ValueError("Los puntajes deben ser exactamente 5 valores")

        for valor in puntaje:
            if not (0<=valor<=10):
                raise ValueError("Los puntajes no pueden ser menores y mayores a 0-10")
        self.puntaje=puntaje


