from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ClienteModel(Base):
    __tablename__ = "clientes"

    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    dni: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class CuentaModel(Base):
    __tablename__ = "cuentas"

    id_cuenta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nro_cuenta: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    id_cliente: Mapped[int] = mapped_column(
        ForeignKey("clientes.id_cliente"), nullable=False
    )
    tipo_cuenta: Mapped[str] = mapped_column(String, nullable=False)
    saldo: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    tasa_interes: Mapped[float] = mapped_column(Float, default=0.0)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class TarjetaModel(Base):
    __tablename__ = "tarjetas"

    id_tarjeta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero_tarjeta: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    id_cliente: Mapped[int] = mapped_column(
        ForeignKey("clientes.id_cliente"), nullable=False
    )
    limite_credito: Mapped[float] = mapped_column(Float, nullable=False)
    saldo_actual: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    fecha_emision: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class TransaccionModel(Base):
    __tablename__ = "transacciones"

    id_transaccion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cuenta: Mapped[int] = mapped_column(
        ForeignKey("cuentas.id_cuenta"), nullable=False
    )
    tipo_transaccion: Mapped[str] = mapped_column(String, nullable=False)
    monto: Mapped[float] = mapped_column(Float, nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class MovimientoTarjetaModel(Base):
    __tablename__ = "movimientos_tarjeta"

    id_movimiento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_tarjeta: Mapped[int] = mapped_column(
        ForeignKey("tarjetas.id_tarjeta"), nullable=False
    )
    tipo_movimiento: Mapped[str] = mapped_column(String, nullable=False)
    monto: Mapped[float] = mapped_column(Float, nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
