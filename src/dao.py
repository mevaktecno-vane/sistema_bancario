from pathlib import Path
from typing import List, Optional, Tuple

from sqlalchemy import create_engine, delete, event, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.cliente import Cliente
from src.models import (
    Base, ClienteModel, CuentaModel, MovimientoTarjetaModel,
    TarjetaModel, TransaccionModel,
)


class DAO:
    """Data Access Object para la persistencia bancaria con SQLAlchemy y SQLite."""

    def __init__(self, db_path: str = "sistema_bancario.db"):
        self.db_path = db_path
        url = "sqlite://" if db_path == ":memory:" else f"sqlite:///{Path(db_path).resolve()}"
        self.engine = create_engine(url, future=True)
        event.listen(self.engine, "connect", self._enable_foreign_keys)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.create_tables()

    @staticmethod
    def _enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def connect(self):
        return self.session_factory()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    @staticmethod
    def _cliente_tuple(item: ClienteModel) -> Tuple:
        return item.id_cliente, item.nombre, item.apellido, item.dni, item.fecha_registro

    @staticmethod
    def _cuenta_tuple(item: CuentaModel) -> Tuple:
        return (item.id_cuenta, item.nro_cuenta, item.id_cliente, item.tipo_cuenta,
                item.saldo, item.tasa_interes, item.fecha_creacion)

    @staticmethod
    def _tarjeta_tuple(item: TarjetaModel) -> Tuple:
        return (item.id_tarjeta, item.numero_tarjeta, item.id_cliente,
                item.limite_credito, item.saldo_actual, item.fecha_emision)

    @staticmethod
    def _transaccion_tuple(item: TransaccionModel) -> Tuple:
        return item.id_transaccion, item.id_cuenta, item.tipo_transaccion, item.monto, item.fecha

    @staticmethod
    def _movimiento_tuple(item: MovimientoTarjetaModel) -> Tuple:
        return item.id_movimiento, item.id_tarjeta, item.tipo_movimiento, item.monto, item.fecha

    def guardar_cliente(self, cliente: Cliente) -> int:
        try:
            with self.session_factory.begin() as session:
                item = ClienteModel(nombre=cliente.get_nombre(), apellido=cliente.get_apellido(), dni=cliente.get_dni())
                session.add(item)
                session.flush()
                return item.id_cliente
        except IntegrityError as error:
            raise ValueError(f"Ya existe un cliente con DNI {cliente.get_dni()}") from error

    def obtener_cliente_por_dni(self, dni: str) -> Optional[Tuple]:
        with self.session_factory() as session:
            item = session.scalar(select(ClienteModel).where(ClienteModel.dni == dni))
            return self._cliente_tuple(item) if item else None

    def obtener_todos_clientes(self) -> List[Tuple]:
        with self.session_factory() as session:
            items = session.scalars(select(ClienteModel).order_by(ClienteModel.fecha_registro.desc())).all()
            return [self._cliente_tuple(item) for item in items]

    def guardar_cuenta(self, nro_cuenta: str, id_cliente: int, tipo_cuenta: str,
                       saldo: float = 0.0, tasa_interes: float = 0.0) -> int:
        try:
            with self.session_factory.begin() as session:
                item = CuentaModel(nro_cuenta=nro_cuenta, id_cliente=id_cliente,
                                   tipo_cuenta=tipo_cuenta, saldo=saldo, tasa_interes=tasa_interes)
                session.add(item)
                session.flush()
                return item.id_cuenta
        except IntegrityError as error:
            raise ValueError(f"Ya existe una cuenta con número {nro_cuenta}") from error

    def obtener_cuentas_por_cliente(self, id_cliente: int) -> List[Tuple]:
        with self.session_factory() as session:
            items = session.scalars(select(CuentaModel).where(CuentaModel.id_cliente == id_cliente)
                                    .order_by(CuentaModel.fecha_creacion.desc())).all()
            return [self._cuenta_tuple(item) for item in items]

    def obtener_cuenta_por_numero(self, nro_cuenta: str) -> Optional[Tuple]:
        with self.session_factory() as session:
            item = session.scalar(select(CuentaModel).where(CuentaModel.nro_cuenta == nro_cuenta))
            return self._cuenta_tuple(item) if item else None

    def actualizar_saldo_cuenta(self, id_cuenta: int, nuevo_saldo: float) -> bool:
        try:
            with self.session_factory.begin() as session:
                session.execute(update(CuentaModel).where(CuentaModel.id_cuenta == id_cuenta).values(saldo=nuevo_saldo))
            return True
        except SQLAlchemyError:
            return False

    def guardar_tarjeta(self, numero_tarjeta: str, id_cliente: int, limite_credito: float) -> int:
        try:
            with self.session_factory.begin() as session:
                item = TarjetaModel(numero_tarjeta=numero_tarjeta, id_cliente=id_cliente, limite_credito=limite_credito)
                session.add(item)
                session.flush()
                return item.id_tarjeta
        except IntegrityError as error:
            raise ValueError(f"Ya existe una tarjeta con número {numero_tarjeta}") from error

    def obtener_tarjetas_por_cliente(self, id_cliente: int) -> List[Tuple]:
        with self.session_factory() as session:
            items = session.scalars(select(TarjetaModel).where(TarjetaModel.id_cliente == id_cliente)
                                    .order_by(TarjetaModel.fecha_emision.desc())).all()
            return [self._tarjeta_tuple(item) for item in items]

    def actualizar_saldo_tarjeta(self, id_tarjeta: int, nuevo_saldo: float) -> bool:
        try:
            with self.session_factory.begin() as session:
                session.execute(update(TarjetaModel).where(TarjetaModel.id_tarjeta == id_tarjeta)
                                .values(saldo_actual=nuevo_saldo))
            return True
        except SQLAlchemyError:
            return False

    def guardar_transaccion(self, id_cuenta: int, tipo_transaccion: str, monto: float) -> int:
        with self.session_factory.begin() as session:
            item = TransaccionModel(id_cuenta=id_cuenta, tipo_transaccion=tipo_transaccion, monto=monto)
            session.add(item)
            session.flush()
            return item.id_transaccion

    def obtener_transacciones_por_cuenta(self, id_cuenta: int) -> List[Tuple]:
        with self.session_factory() as session:
            items = session.scalars(select(TransaccionModel).where(TransaccionModel.id_cuenta == id_cuenta)
                                    .order_by(TransaccionModel.fecha.desc())).all()
            return [self._transaccion_tuple(item) for item in items]

    def guardar_movimiento_tarjeta(self, id_tarjeta: int, tipo_movimiento: str, monto: float) -> int:
        with self.session_factory.begin() as session:
            item = MovimientoTarjetaModel(id_tarjeta=id_tarjeta, tipo_movimiento=tipo_movimiento, monto=monto)
            session.add(item)
            session.flush()
            return item.id_movimiento

    def obtener_movimientos_por_tarjeta(self, id_tarjeta: int) -> List[Tuple]:
        with self.session_factory() as session:
            items = session.scalars(select(MovimientoTarjetaModel).where(MovimientoTarjetaModel.id_tarjeta == id_tarjeta)
                                    .order_by(MovimientoTarjetaModel.fecha.desc())).all()
            return [self._movimiento_tuple(item) for item in items]

    def limpiar_base_datos(self):
        with self.session_factory.begin() as session:
            for model in (MovimientoTarjetaModel, TransaccionModel, TarjetaModel, CuentaModel, ClienteModel):
                session.execute(delete(model))

    def cerrar_conexion(self):
        self.engine.dispose()

    def __del__(self):
        engine = getattr(self, "engine", None)
        if engine:
            engine.dispose()
