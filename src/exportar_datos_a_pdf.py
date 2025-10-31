from fpdf import FPDF
from datetime import datetime

    # --- INICIALIZAR PDF ---
    
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'REPORTE FINANCIERO DEL CLIENTE', 0, 1, 'C')
pdf.ln(5)

# --- DATOS DEL CLIENTE ---
    
pdf.set_fill_color(220, 220, 220)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'DATOS DEL CLIENTE', 1, 1, 'L', True)
    
pdf.set_font('Arial', '', 10)
pdf.cell(40, 6, 'Nombre:', 0, 0)
pdf.cell(0, 6, f'{cliente_actual.get_nombre()} {cliente_actual.get_apellido()}', 0, 1)
    
pdf.cell(40, 6, 'DNI:', 0, 0)
pdf.cell(0, 6, f'{cliente_actual._Cliente__dni}', 0, 1)
pdf.ln(2)

# ---DATOS DE LA CUENTA BANCARIA ---

if cuenta_actual:
    pdf.set_fill_color(220, 255, 220)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'CUENTA BANCARIA', 1, 1, 'L', True)

    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, 'Nro Cuenta:', 0, 0)
    pdf.cell(0, 6, f'{cuenta_actual._Cuenta__nro_cuenta}', 0, 1)
        
    pdf.cell(40, 6, 'Tipo:', 0, 0)
    pdf.cell(0, 6, f'{"Ahorro" if isinstance(cuenta_actual, CuentaAhorro) else "Base"}', 0, 1)
        
    pdf.cell(40, 6, 'SALDO ACTUAL:', 0, 0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, f'${cuenta_actual.get_saldo():.2f}', 0, 1)
    pdf.ln(2)
        
    # --- Historial de Transacciones ---
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(0, 6, 'Historial de Transacciones:', 0, 1)
        
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(40, 5, 'FECHA/HORA', 1, 0, 'C')
    pdf.cell(30, 5, 'TIPO', 1, 0, 'C')
    pdf.cell(20, 5, 'MONTO', 1, 1, 'C')
        
    pdf.set_font('Arial', '', 8)
    transacciones = cuenta_actual.get_transacciones()
    if transacciones:
        for t in transacciones:
            fecha = t.get_fecha().strftime('%Y-%m-%d %H:%M:%S')
            monto_str = f'${t.get_monto():.2f}'
            pdf.cell(40, 5, fecha, 1, 0)
            pdf.cell(30, 5, t.get_tipo().upper(), 1, 0)
            pdf.cell(20, 5, monto_str, 1, 1, 'R')
    else:
        pdf.cell(90, 5, 'No se registraron transacciones.', 1, 1, 'C')
    pdf.ln(5)

# ---DATOS DE LA TARJETA DE CRÉDITO ---
    
if tarjeta_actual:
    pdf.set_fill_color(255, 220, 220)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'TARJETA DE CRÉDITO', 1, 1, 'L', True)

    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, 'Nro Tarjeta:', 0, 0)
    pdf.cell(0, 6, f'{tarjeta_actual._Tarjeta__numero}', 0, 1)
        
    pdf.cell(40, 6, 'Límite Total:', 0, 0)
    pdf.cell(0, 6, f'${tarjeta_actual.get_limite():.2f}', 0, 1)
        
    pdf.cell(40, 6, 'DEUDA ACTUAL:', 0, 0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, f'${tarjeta_actual.get_saldo_actual():.2f}', 0, 1)
    pdf.ln(2)
        
    # --- Historial de Movimientos de Tarjeta ---
    pdf.set_font('Arial', 'U', 11)
    pdf.cell(0, 6, 'Historial de Movimientos:', 0, 1)
        
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(40, 5, 'FECHA/HORA', 1, 0, 'C')
    pdf.cell(30, 5, 'TIPO', 1, 0, 'C')
    pdf.cell(20, 5, 'MONTO', 1, 1, 'C')

    pdf.set_font('Arial', '', 8)
    movimientos = tarjeta_actual._Tarjeta__movimientos # Acceso directo a la lista de tuplas
    if movimientos:
        for fecha, monto, tipo in movimientos:
            fecha_str = fecha.strftime('%Y-%m-%d %H:%M:%S')
            monto_str = f'${monto:.2f}'
            pdf.cell(40, 5, fecha_str, 1, 0)
            pdf.cell(30, 5, tipo.upper(), 1, 0)
            pdf.cell(20, 5, monto_str, 1, 1, 'R')
    else:
        pdf.cell(90, 5, 'No se registraron movimientos.', 1, 1, 'C')
    pdf.ln(5)