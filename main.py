class Participantes:
    def __init__(self, nombreBanda,institucion,categoria):
        self.nombreBanda=nombreBanda
        self.institucion=institucion
        self.categoria=categoria

    def mostrar_info(self):
        return f"El nombre de la banda es: {self.nombreBanda} de la isntitucion {self.institucion} y con la categoria {self.categoria}"


