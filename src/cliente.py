class Cliente:
    def __init__(self, nombre, apellido, dni):
        # Validaciones básicas
        if not nombre or not apellido or not dni:
            raise ValueError("Todos los campos del cliente son obligatorios.")

        # Validación: solo letras en nombre y apellido
        if not nombre.replace(" ", "").isalpha() or not apellido.replace(" ", "").isalpha():
            raise ValueError(
                "El nombre y apellido deben contener solo letras.")

        # Validación: solo números en DNI
        if not dni.isdigit():
            raise ValueError("El DNI debe contener solo números.")

        self.__nombre = nombre.strip().title()
        self.__apellido = apellido.strip().title()
        self.__dni = dni.strip()

    # Métodos getters
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
