"""Quantas ofertas enviar por hora, conforme o horário."""

# ═════════════════════════════════════════════════════════════════════════════
# SISTEMA DE AGENDAMENTO INTELIGENTE (6 ou 12 ofertas/hora)
# ═════════════════════════════════════════════════════════════════════════════

def get_offers_per_hour():
    """
    Retorna quantas ofertas devem ser enviadas por hora
    12 ofertas/hora em horários de pico
    6 ofertas/hora em horários normais
    """
    from datetime import datetime
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()  # 0=segunda, 6=domingo
    
    # ── HORÁRIOS DE PICO ──
    # Manhã: 8h-10h (pessoas chegando no trabalho)
    # Almoço: 12h-14h (pausa do trabalho)
    # Noite: 18h-22h (após o trabalho, navegando)
    
    peak_hours = [
        8, 9, 10,      # Manhã
        12, 13,        # Almoço
        18, 19, 20, 21 # Noite
    ]
    
    # Final de semana tem mais tempo livre
    if weekday >= 5:  # Sábado ou Domingo
        peak_hours.extend([14, 15, 16, 17, 22])
    
    if hour in peak_hours:
        return 12  # 12 ofertas/hora = a cada 5 minutos
    else:
        return 6   # 6 ofertas/hora = a cada 10 minutos

def get_send_interval():
    """
    Retorna o intervalo em segundos entre envios
    """
    offers_per_hour = get_offers_per_hour()
    # 3600 segundos (1 hora) / quantidade de ofertas
    interval = 3600 / offers_per_hour
    return int(interval)
