class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: str):
        # Validaciones básicas
        if not nombre or not apellido:
            raise ValueError("El nombre y el apellido no pueden estar vacíos.")
        if not dni.isdigit():
            raise ValueError("El DNI debe contener solo números.")

        # Atributos privados
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni

    # Getters
    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_dni(self):
        return self.__dni

    def __str__(self):
        return f"{self.__nombre} {self.__apellido} ({self.__dni})"
