import time
import pandas as pd
import talib
import numpy as np
from iqoptionapi.stable_api import IQ_Option

# 🔹 Credenciales de IQ Option
IQ_EMAIL = "danielacopana@gmail.com"
IQ_PASSWORD = "bolivianas"

# 🔹 Conectar a IQ Option
iq = IQ_Option(IQ_EMAIL, IQ_PASSWORD)
iq.connect()

if iq.check_connect():
    print("✅ Conectado a IQ Option")
else:
    print("❌ Error al conectar")
    exit()

# 🔹 Configuración
PAR = "EURUSD"
TIEMPO_VELA = 60  # Velas de 1 minuto
CANTIDAD_VELAS = 100
MONTO_OPERACION = 100
EXPIRACION = 1  # Expiración en minutos

# 🔹 Obtener datos de velas
def obtener_velas():
    velas = iq.get_candles(PAR, TIEMPO_VELA, CANTIDAD_VELAS, time.time())
    df = pd.DataFrame(velas)
    df.rename(columns={'open': 'open', 'max': 'high', 'min': 'low', 'close': 'close'}, inplace=True)
    return df

# 🔹 Estrategias de velas japonesas
def detectar_martillo(df):
    return talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close']).iloc[-1]

def detectar_martillo_invertido(df):
    return talib.CDLINVERTEDHAMMER(df['open'], df['high'], df['low'], df['close']).iloc[-1]

def detectar_estrella_fugaz(df):
    return talib.CDLHANGINGMAN(df['open'], df['high'], df['low'], df['close']).iloc[-1]

def detectar_vela_doji(df):
    return talib.CDLDOJI(df['open'], df['high'], df['low'], df['close']).iloc[-1]

# 🔹 Estrategia RSI + MACD (mejorada)
def estrategia_rsi_macd(df):
    rsi = talib.RSI(df['close'], timeperiod=14)
    macd, macd_signal, _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    
    if rsi.iloc[-1] < 30 and macd.iloc[-1] > macd_signal.iloc[-1]:
        if df['close'].iloc[-1] > df['open'].iloc[-1]:  # Confirmar vela alcista
            return "call"
    elif rsi.iloc[-1] > 70 and macd.iloc[-1] < macd_signal.iloc[-1]:
        if df['close'].iloc[-1] < df['open'].iloc[-1]:  # Confirmar vela bajista
            return "put"
    return "hold"

# 🔹 Estrategia Bandas de Bollinger (mejorada)
def estrategia_bollinger(df):
    upper, middle, lower = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    rsi = talib.RSI(df['close'], timeperiod=14)

    if df['close'].iloc[-1] <= lower.iloc[-1] and rsi.iloc[-1] < 30:
        if df['close'].iloc[-1] > df['open'].iloc[-1]:  # Confirmar vela alcista
            return "call"
    elif df['close'].iloc[-1] >= upper.iloc[-1] and rsi.iloc[-1] > 70:
        if df['close'].iloc[-1] < df['open'].iloc[-1]:  # Confirmar vela bajista
            return "put"
    return "hold"

# 🔹 Estrategia Triple Cruce de Medias Móviles (mejorada)
def estrategia_triple_cruce(df):
    sma10 = talib.SMA(df['close'], timeperiod=10)
    sma50 = talib.SMA(df['close'], timeperiod=50)
    sma200 = talib.SMA(df['close'], timeperiod=200)

    if sma10.iloc[-1] > sma50.iloc[-1] > sma200.iloc[-1]:
        return "call"
    elif sma10.iloc[-1] < sma50.iloc[-1] < sma200.iloc[-1]:
        return "put"
    return "hold"

# 🔹 Estrategia Ruptura Dinámica (mejorada)
def estrategia_ruptura_dinamica(df):
    maximo = df['high'].iloc[-50:].max()
    minimo = df['low'].iloc[-50:].min()
    ultimo_precio = df['close'].iloc[-1]

    if ultimo_precio > maximo * 1.01:  # Confirmar ruptura superior
        return "call"
    elif ultimo_precio < minimo * 0.99:  # Confirmar ruptura inferior
        return "put"
    return "hold"

# 🔹 Estrategia de cruce de medias móviles (agresiva)
def estrategia_cruce_agresivo(df):
    sma5 = talib.SMA(df['close'], timeperiod=5)
    sma20 = talib.SMA(df['close'], timeperiod=20)

    if sma5.iloc[-1] > sma20.iloc[-1]:
        return "call"
    elif sma5.iloc[-1] < sma20.iloc[-1]:
        return "put"
    return "hold"

# 🔹 Estrategia Estocástico
def estrategia_estocastico(df):
    slowk, slowd = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    
    if slowk.iloc[-1] < 20 and slowk.iloc[-1] > slowd.iloc[-1]:
        return "call"
    elif slowk.iloc[-1] > 80 and slowk.iloc[-1] < slowd.iloc[-1]:
        return "put"
    return "hold"

# 🔹 Estrategia CCI (Commodity Channel Index)
def estrategia_cci(df):
    cci = talib.CCI(df['high'], df['low'], df['close'], timeperiod=14)

    if cci.iloc[-1] < -100:
        return "call"
    elif cci.iloc[-1] > 100:
        return "put"
    return "hold"

# 🔹 Ejecutar operación
def operar():
    df = obtener_velas()
    # Mostrar mensaje de búsqueda
    print("🔍 Buscando estrategia...")
    # Detectar patrones de velas
    patron_martillo = detectar_martillo(df)
    patron_martillo_invertido = detectar_martillo_invertido(df)
    patron_estrella_fugaz = detectar_estrella_fugaz(df)
    patron_doji = detectar_vela_doji(df)

    # Aplicar estrategias técnicas
    senal_rsi_macd = estrategia_rsi_macd(df)
    senal_bollinger = estrategia_bollinger(df)
    senal_triple_cruce = estrategia_triple_cruce(df)
    senal_ruptura_dinamica = estrategia_ruptura_dinamica(df)
    senal_cruce_agresivo = estrategia_cruce_agresivo(df)
    senal_estocastico = estrategia_estocastico(df)
    senal_cci = estrategia_cci(df)

    # Ejecutar operaciones según las señales detectadas
    if patron_martillo != 0:
        print(f"⚡ Martillo detectado en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif patron_martillo_invertido != 0:
        print(f"⚡ Martillo Invertido detectado en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif patron_estrella_fugaz != 0:
        print(f"⚡ Estrella Fugaz detectada en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif patron_doji != 0:
        print(f"⚡ Vela Doji detectada en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif senal_rsi_macd == "call":
        print(f"📈 Señal de compra detectada con RSI + MACD en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif senal_rsi_macd == "put":
        print(f"📉 Señal de venta detectada con RSI + MACD en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif senal_bollinger == "call":
        print(f"📈 Señal de compra con Bandas de Bollinger en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif senal_bollinger == "put":
        print(f"📉 Señal de venta con Bandas de Bollinger en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif senal_triple_cruce == "call":
        print(f"📈 Señal de compra con Triple Cruce de Medias en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif senal_triple_cruce == "put":
        print(f"📉 Señal de venta con Triple Cruce de Medias en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif senal_ruptura_dinamica == "call":
        print(f"📈 Señal de compra con Ruptura Dinámica en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif senal_ruptura_dinamica == "put":
        print(f"📉 Señal de venta con Ruptura Dinámica en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif senal_cruce_agresivo == "call":
        print(f"📈 Señal de compra con Cruce Agresivo de Medias Móviles en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif senal_cruce_agresivo == "put":
        print(f"📉 Señal de venta con Cruce Agresivo de Medias Móviles en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif senal_estocastico == "call":
        print(f"📈 Señal de compra con Estocástico en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif senal_estocastico == "put":
        print(f"📉 Señal de venta con Estocástico en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    elif senal_cci == "call":
        print(f"📈 Señal de compra con CCI en {PAR}, ejecutando compra... 🟢")
        iq.buy(MONTO_OPERACION, PAR, "call", EXPIRACION)
    elif senal_cci == "put":
        print(f"📉 Señal de venta con CCI en {PAR}, ejecutando venta... 🔴")
        iq.buy(MONTO_OPERACION, PAR, "put", EXPIRACION)
    else:
        print("⏳ No se detectó patrón, esperando...")

# 🔹 Loop de monitoreo en tiempo real
while True:
    operar()
    time.sleep(60)  # Esperar 1 minuto antes de revisar nuevamente