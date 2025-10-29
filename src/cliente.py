class Cliente:
    def __init__(self, nombre, apellido, dni):
        if not nombre or not apellido or not dni:
            raise ValueError("Todos los campos del cliente son obligatorios.")
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_dni(self):
        return self.__dni

    def mostrar_datos(self):
        return f"{self.__nombre} {self.__apellido} (DNI: {self.__dni})"

    def __str__(self):
        return self.mostrar_datos()
