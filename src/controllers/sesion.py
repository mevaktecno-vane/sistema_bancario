class Sesion:
    """Estado simple de sesión (FE-04): guarda el usuario logueado."""

    _usuario = None

    @classmethod
    def iniciar(cls, usuario):
        cls._usuario = usuario

    @classmethod
    def actual(cls):
        return cls._usuario

    @classmethod
    def activa(cls):
        return cls._usuario is not None

    @classmethod
    def cerrar(cls):
        cls._usuario = None