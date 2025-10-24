class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: str):
        # atributos privados
        self.__nombre = nombre.strip()
        self.__apellido = apellido.strip()
        self.__dni = dni.strip()

    # getters
    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_dni(self):
        return self.__dni

    # setters (validaciones simples)
    def set_nombre(self, nombre):
        if not nombre.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe contener letras y espacios.")
        self.__nombre = nombre.strip()

    def set_apellido(self, apellido):
        if not apellido.replace(" ", "").isalpha():
            raise ValueError(
                "El apellido solo debe contener letras y espacios.")
        self.__apellido = apellido.strip()

    def set_dni(self, dni):
        if not dni.isdigit():
            raise ValueError("El DNI debe contener solo dígitos.")
        self.__dni = dni.strip()

    def mostrar_datos(self):
        return f"{self.__nombre} {self.__apellido} - DNI: {self.__dni}"
