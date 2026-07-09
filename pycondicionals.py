"""
PyCondicionals Suite v7.0.0 "Master Elite"
Desarrollador: Isaac Tamayo Garcia 

Librería completa con herramientas de validación, persistencia atómica,
motores de control de estado y utilidades de simplificación de datos estructurados.
y conexiones online para juegos o, cosas mucho mas serias 
"""
#Si estas leyendo esto, significa que estas usando la version 7.0.0 de PyCondicionals, la cual es la mas reciente y estable.
#Y que eres chismoso, pero no te preocupes, no hay nada que ocultar, todo esta a la vista, 
# y si quieres saber mas sobre el proyecto, puedes visitar el repositorio oficial en GitHub:
# Gracias por usar PyCondicionals, y recuerda, si quieres aprender a programar, no hay mejor manera que hacerlo con PyCondicionals, ya que es una libreria completa y facil de usar, y ademas, es gratis :D
import requests
import random
import json
import random
import json
import time
import random
import json
import time
import threading
import paho.mqtt.client as mqtt
import pickle #Yo no sabia que se podia importar un pepinillo 
import smtplib
from email.message import EmailMessage

class EmailSender:
    def __init__(self, username, password, server="smtp.gmail.com", port=587):
        self.username = username
        self.password = password
        self.server = server
        self.port = port

    def send(self, to, subject, body, html=False):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = to

        if html:
            msg.set_content("HTML not supported.")
            msg.add_alternative(body, subtype="html")
        else:
            msg.set_content(body)

        try:
            with smtplib.SMTP(self.server, self.port) as session:
                session.starttls()
                session.login(self.username, self.password)
                session.send_message(msg)
            return True
        except Exception:
            return False
class Server:
    def __init__(self, client_script_callback=None):
        self.data_store = {}
        self.active_clients = set()
        self.combination_code = str(random.randint(100000, 999999))
        self.broker = "broker.hivemq.com"
        self.port = 1883
        
        self.server_topic = f"global_network/{self.combination_code}/to_server"
        self.client_topic = f"global_network/{self.combination_code}/to_client"
        
        try:
            self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        except AttributeError:
            self.mqtt_client = mqtt.Client()
            
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.connect(self.broker, self.port, 60)
        self.mqtt_client.subscribe(self.server_topic)
        self.mqtt_client.loop_start()
        
        if client_script_callback is not None:
            threading.Thread(target=client_script_callback, args=(self.combination_code,), daemon=True).start()

    def _on_message(self, client, userdata, msg):
        try:
            payload = pickle.loads(msg.payload)
            client_name = payload.get("client_name")
            action = payload.get("action")
            
            if client_name:
                self.active_clients.add(client_name)
            
            if action == "load_dict":
                self.data_store[client_name] = payload.get("data", {})
            elif action == "set_item":
                if client_name not in self.data_store:
                    self.data_store[client_name] = {}
                key = payload.get("key")
                value = payload.get("value")
                self.data_store[client_name][key] = value
            elif action == "disconnect":
                self.active_clients.discard(client_name)
                if client_name in self.data_store:
                    del self.data_store[client_name]

            response = {
                "action": "server_update",
                "data_store": self.data_store
            }
            self.mqtt_client.publish(self.client_topic, pickle.dumps(response))
        except Exception:
            pass

    @property
    def online_count(self):
        return len(self.active_clients)

    def __setitem__(self, client_name, dictionary_data):
        self.data_store[client_name] = dictionary_data

    def __getitem__(self, client_name):
        return self.data_store.get(client_name, {})

    def get_all(self):
        return self.data_store

    def close(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()


class Client:
    def __init__(self, combination_code, name="Default_Client", on_update_callback=None):
        self.name = name
        self.combination_code = str(combination_code)
        self.broker = "broker.hivemq.com"
        self.port = 1883
        
        self.server_topic = f"global_network/{self.combination_code}/to_server"
        self.client_topic = f"global_network/{self.combination_code}/to_client"
        
        self.on_update_callback = on_update_callback
        self.server_data = {}
        
        try:
            self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        except AttributeError:
            self.mqtt_client = mqtt.Client()
            
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.connect(self.broker, self.port, 60)
        self.mqtt_client.subscribe(self.client_topic)
        self.mqtt_client.loop_start()
        
        time.sleep(0.2)
        self.load_dictionary({})

    def _on_message(self, client, userdata, msg):
        try:
            payload = pickle.loads(msg.payload)
            if payload.get("action") == "server_update":
                self.server_data = payload.get("data_store", {})
                if self.on_update_callback:
                    self.on_update_callback(self.server_data)
        except Exception:
            pass

    def __setitem__(self, key, value):
        payload = {
            "client_name": self.name,
            "action": "set_item",
            "key": key,
            "value": value
        }
        self.mqtt_client.publish(self.server_topic, pickle.dumps(payload))

    def load_dictionary(self, complete_dict):
        payload = {
            "client_name": self.name,
            "action": "load_dict",
            "data": complete_dict
        }
        self.mqtt_client.publish(self.server_topic, pickle.dumps(payload))

    def get_server_data(self):
        return self.server_data

    def close(self):
        payload = {
            "client_name": self.name,
            "action": "disconnect"
        }
        self.mqtt_client.publish(self.server_topic, pickle.dumps(payload))
        time.sleep(0.1)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
class Cloud_PQR:
    def __init__(self):
        self.url = "https://webhook.site/7f28bcbe-6c59-4203-b69e-a59f3e305d2b"

    def enviar(self, mensaje, usuario="Anónimo"):
        """
        Envía quejas, sugerencias o 'confabulaciones' directamente 
        a tu panel privado de monitoreo.
        """
        payload = {
            "usuario": usuario, 
            "mensaje": mensaje
        }
        try:
            requests.post(self.url, json=payload)
            return True
        except Exception:
            return False
#================================================================
#  -1.SISTEMA DE TRANSCRIPCION Y HABLA
#================================================================
import speech_recognition as sr
import sounddevice as sd
import numpy as np

class VoiceTranscript:#Creditos a speech_recognition muy util :D
    """
    Clase encargada de capturar audio del micrófono por un tiempo fijo 
    y transcribirlo a texto utilizando la API de Google.
    """
    
    def __init__(self, idioma="es-ES", sample_rate=16000):
        """
        Inicializa los componentes de reconocimiento y configuración de audio.
        """
        self.recognizer = sr.Recognizer()
        self.idioma = idioma
        self.sample_rate = sample_rate

    def record_and_transcript(self, time_recording=5):
        """
        Graba audio del micrófono durante una cantidad fija de segundos y lo transcribe.

        Args:
            time_recording (int, float): Duración de la grabación en segundos. Por defecto es 5.

            str: Texto transcrito obtenido del audio o un mensaje de error.
        """
        fs = self.sample_rate
        
        recording = sd.rec(int(time_recording * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        
        audio_bytes = recording.tobytes()
        audio_data = sr.AudioData(audio_bytes, fs, 2)
        
        try:
            return self.recognizer.recognize_google(audio_data, language=self.idioma)
        except sr.UnknownValueError:
            return "[Error]: No se pudo entender el audio."
        except sr.RequestError as e:
            return f"[Error]: Error de conexión ({e})."
from gtts import gTTS
import os
import playsound

class VoiceSpeaker: #Usalo por que si, es la forma mas facil de hacer que tu programa hable, y ademas, es gratis :D(creditos a Google por la API de gTTS)
    def __init__(self):
        self.lang = 'es'

    def set_config(self, gender=None, lang='es'):
        """Configura el idioma de habla"""
        self.lang = lang

    def speak(self, text):
        """Habla el texto dado"""
        try:
            if not text: return
            tts = gTTS(text=text, lang=self.lang)
            tts.save("temp_speech.mp3")
            playsound.playsound("temp_speech.mp3")
            os.remove("temp_speech.mp3")
        except Exception as e:
            print(f"Error inesperado: {e}")
import random
import time
import math
import json
import os
import inspect
from typing import Any, Dict, List, Optional, Union, Iterator, Callable, Set, Tuple, Iterable
import time
import functools

def time_count(func):#Nunca lo use pero sirve,(creo....)
    """Un decorador que mide el tiempo de ejecución de una función."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"--- La función {func.__name__} tardó {fin - inicio:.4f} segundos ---")
        return resultado
    return wrapper
# =====================================================================
# 0. SISTEMAS DE PERSISTENCIA AVANZADA (Clases Base)
# =====================================================================

import json
import os
import shutil
import inspect
from typing import Any, Dict, List, Optional

class InstantData:#Ni se como cree esto
    """Gestiona persistencia atómica inmediata para configuraciones en archivos JSON."""
    
    def __init__(self, access: str = "public", secret_key: Optional[str] = None) -> None:
        """Inicializa la instancia definiendo el tipo de acceso (public/private)."""
        self.filename: Optional[str] = None
        self.access = access
        self.secret_key = secret_key
        self._data: Dict[str, Any] = {}

    @classmethod
    def load_data(cls, filename: str, access: str = "public", secret_key: Optional[str] = None) -> 'InstantData':
        """Carga un archivo JSON existente o prepara uno nuevo si no existe."""
        instancia = cls(access=access, secret_key=secret_key)
        instancia.filename = filename if filename.endswith('.json') else f"{filename}.json"
        
        if os.path.exists(instancia.filename):
            try:
                with open(instancia.filename, 'r', encoding='utf-8') as f:
                    instancia._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                instancia._data = {}
        return instancia

    def _save(self) -> None:
        """Guarda los datos en el disco de forma atómica usando un archivo temporal."""
        if not self.filename:
            return
        temp_name = self.filename + ".tmp"
        try:
            with open(temp_name, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
            os.replace(temp_name, self.filename)
        except Exception as e:
            if os.path.exists(temp_name):
                os.remove(temp_name)
            raise IOError(f"Error al guardar datos: {e}")

    def _verify_access(self, key_provided: Optional[str] = None) -> None:
        """Verifica si la clave provista coincide con la clave secreta en modo privado."""
        if self.access == "private" and key_provided != self.secret_key:
            raise PermissionError("Acceso denegado: Clave incorrecta para este archivo privado.")

    def set(self, key: str, value: Any, secret_key: Optional[str] = None) -> None:
        """Asigna un valor a una clave y lo guarda inmediatamente en el archivo."""
        self._verify_access(secret_key)
        self._data[key] = value
        self._save()

    def get(self, key: str, default: Any = None, secret_key: Optional[str] = None) -> Any:
        """Obtiene el valor de una clave. Si no existe y se define un valor por defecto, lo crea y guarda."""
        self._verify_access(secret_key)
        if key not in self._data and default is not None:
            self._data[key] = default
            self._save()
        return self._data.get(key, default)

    def delete_file(self, secret_key: Optional[str] = None) -> None:
        """Elimina permanentemente el archivo JSON del disco y vacía los datos en memoria."""
        self._verify_access(secret_key)
        if self.filename and os.path.exists(self.filename):
            os.remove(self.filename)
        self._data = {}

    def clean_nulls(self) -> None:
        """Elimina todos los elementos cuyo valor sea None y actualiza el archivo."""
        self._data = {k: v for k, v in self._data.items() if v is not None}
        self._save()

    def exists(self, key: str) -> bool:
        """Comprueba si una clave existe en la configuración."""
        return key in self._data

    def keys(self) -> List[str]:
        """Devuelve una lista con todas las claves guardadas."""
        return list(self._data.keys())

    def update(self, data_dict: Dict[str, Any], secret_key: Optional[str] = None) -> None:
        """Actualiza varios elementos a la vez usando un diccionario y guarda los cambios."""
        self._verify_access(secret_key)
        self._data.update(data_dict)
        self._save()

    def size(self) -> int:
        """Devuelve la cantidad total de elementos guardados."""
        return len(self._data)
# =====================================================================
        #==============================
# NUEVAS UTILIDADES EXCLUSIVAS ( v7.0.0 )
# =====================================================================
import inspect
def create_bar(valor, emoji_lleno, emoji_vacio, max_valor=10):
    llenos = max(0, min(valor // 10, max_valor))
    vacios = max_valor - llenos
    return (emoji_lleno * llenos) + (emoji_vacio * vacios)
def variable_exist(var_name):#Creo que deberia dejar de escribir codigo en python deberia usar JavaScript o C++ o C# o Rust o Go, pero no, sigo usando Python por que es facil de usar y rapido de aprender, y ademas, es gratis :D  
    frame = inspect.currentframe().f_back
    try:
        if var_name in frame.f_locals:
            return True
        if var_name in frame.f_globals:
            return True
        return False
    except:
        return False
    finally:
        del frame

def exists(key: Any, container: Union[Dict[Any, Any], List[Any], Set[Any], Tuple[Any, ...], Any]) -> bool:
    """Verifica de forma segura si una clave existe en un diccionario o si un elemento está en una colección."""
    try:
        if isinstance(container, dict):
            return key in container
        return key in container
    except Exception:
        return False

def apply_to_all(coleccion: Iterable[Any], funcion: Callable[..., Any], *args: Any, **kwargs: Any) -> List[Any]:
    """
    Ejecuta una función o método sobre cada elemento o instancia de una colección,
    evitando la necesidad de declarar bucles 'for' manuales.
    """
    try:
        return [funcion(item, *args, **kwargs) for item in coleccion]
    except Exception:
        return []

def deep_get(diccionario: Dict[str, Any], ruta_claves: str, default: Any = None) -> Any:
    """Accede de manera directa a claves anidadas profundas usando notación de puntos ('usuario.perfil.id')."""
    try:
        actual: Any = diccionario
        for clave in ruta_claves.split('.'):
            if isinstance(actual, dict):
                actual = actual.get(clave, default)
            else:
                return default
        return actual
    except Exception:
        return default

def flatten_dict(diccionario: Dict[str, Any], clave_padre: str = '', separador: str = '_') -> Dict[str, Any]:
    """Aplana un diccionario con anidaciones complejas a un solo nivel de profundidad."""
    elementos: List[Tuple[str, Any]] = []
    for k, v in diccionario.items():
        nueva_clave = f"{clave_padre}{separador}{k}" if clave_padre else k
        if isinstance(v, dict):
            elementos.extend(flatten_dict(v, nueva_clave, separador=separador).items())
        else:
            elementos.append((nueva_clave, v))
    return dict(elementos)

def merge_dicts(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> Dict[Any, Any]:
    """Combina de forma recursiva y profunda dos diccionarios sin destruir sub-estructuras."""
    resultado = d1.copy()
    for k, v in d2.items():
        if k in resultado and isinstance(resultado[k], dict) and isinstance(v, dict):
            resultado[k] = merge_dicts(resultado[k], v)
        else:
            resultado[k] = v
    return resultado


# =====================================================================
# 1. VALIDACIONES NUMÉRICAS Y MATEMÁTICAS
# =====================================================================

def between(valor: Any, minimo: Any, maximo: Any, inclusivo: bool = True) -> bool:
    try:
        val, mini, maxi = float(valor), float(minimo), float(maximo)
        if inclusivo: return mini <= val <= maxi
        return mini < val < maxi
    except (ValueError, TypeError): return False

def chance(porcentaje_exito: Any) -> bool:#Aquien se le ocurrio poner esta funcion,ha espera lo hize yo
    try:
        pct = float(porcentaje_exito)
        if 0.0 < pct <= 1.0: pct = pct * 100.0
        pct = max(0.0, min(100.0, pct))
        return random.uniform(0, 100) <= pct
    except (ValueError, TypeError): return False

def is_prime(n: Any) -> bool:
    try:
        n = int(n)
        if n <= 1: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0: return False
        return True
    except (ValueError, TypeError): return False

def is_multiple(valor: Any, divisor: Any) -> bool:
    try: return float(valor) % float(divisor) == 0
    except (ValueError, TypeError, ZeroDivisionError): return False

def is_negative(valor: Any) -> bool:
    try: return float(valor) < 0
    except (ValueError, TypeError): return False

def is_even(valor: Any) -> bool:
    try: return int(valor) % 2 == 0
    except (ValueError, TypeError): return False

def is_odd(valor: Any) -> bool:
    try: return int(valor) % 2 != 0
    except (ValueError, TypeError): return False

def is_percent(valor: Any) -> bool:
    try: return 0.0 <= float(valor) <= 100.0
    except (ValueError, TypeError): return False

def is_perfect_square(numero: Any) -> bool:
    try:
        num = int(numero)
        if num < 0: return False
        raiz = math.isqrt(num)
        return raiz * raiz == num
    except Exception: return False

def is_percentage_drop(valor_inicial: Any, valor_actual: Any, porcentaje_limite: Any) -> bool:
    try:
        vi, va, pl = float(valor_inicial), float(valor_actual), float(porcentaje_limite)
        if vi <= 0: return False
        return (((vi - va) / vi) * 100) >= pl
    except Exception: return False

def is_in_tolerance(valor_medido: Any, valor_esperado: Any, tolerance_porcentaje: Any) -> bool:
    try:
        vm, ve, tp = float(valor_medido), float(valor_esperado), float(tolerance_porcentaje)
        if ve == 0: return abs(vm) <= tp
        return (abs(vm - ve) / ve) * 100 <= tp
    except Exception: return False

def clamp(valor: Any, minimo: Any, maximo: Any) -> Any:
    try: return max(minimo, min(valor, maximo))
    except TypeError: return valor

def lerp(inicio: Any, fin: Any, factor: Any) -> Any:
    try: return inicio + (fin - inicio) * clamp(factor, 0.0, 1.0)
    except TypeError: return inicio

def is_positive(valor: Any) -> bool:
    try: return float(valor) > 0
    except (ValueError, TypeError): return False

def is_zero(valor: Any) -> bool:
    try: return float(valor) == 0.0
    except (ValueError, TypeError): return False


# =====================================================================
# 2. VALIDACIONES DE TEXTO E HILOS / STRINGS #Y la verguenza de que no sepa como se escribe hilo en ingles
# =====================================================================

def is_string(variable: Any) -> bool: 
    return isinstance(variable, str)

def is_number(variable: Any) -> bool: 
    return isinstance(variable, (int, float)) and not isinstance(variable, bool)

def is_vowel(caracter: Any) -> bool:
    try:
        char = str(caracter).lower()
        return len(char) == 1 and char in 'aeiouáéíóúü'
    except (ValueError, TypeError): return False

def is_alphabetic(texto: Any) -> bool:
    if not isinstance(texto, str): return False
    return texto.isalpha()

def is_numeric_string(texto: Any) -> bool:
    if not isinstance(texto, str): return False
    return texto.isdigit()

def has_min_words(texto: Any, cantidad: Any) -> bool:
    if not isinstance(texto, str): return False
    return len(texto.split()) >= int(cantidad)

def has_uppercase(texto: Any) -> bool:
    try: return any(c.isupper() for c in texto) if isinstance(texto, str) else False
    except Exception: return False

def is_binary_string(texto: Any) -> bool:
    try: return set(texto) <= {'0', '1'} if isinstance(texto, str) and texto else False
    except Exception: return False

def content_text(texto_completo: Any, buscar: Any) -> bool:
    try:
        if texto_completo is None or buscar is None: return False
        return str(buscar).lower() in str(texto_completo).lower()
    except Exception: return False

def is_palindrome(texto: Any) -> bool:
    if not isinstance(texto, str): return False
    limpio = "".join(texto.split()).lower()
    return limpio == limpio[::-1]

def has_lowercase(texto: Any) -> bool:
    try: return any(c.islower() for c in texto) if isinstance(texto, str) else False
    except Exception: return False


# =====================================================================
# 3. SISTEMAS CRONOLÓGICOS Y CICLOS MÁQUINA / TIME-BASED
# =====================================================================

_tiempos_every: Dict[str, float] = {}
def every(segundos: float, id_evento: str = "defecto", reset: bool = False) -> bool:
    global _tiempos_every
    if reset:
        if id_evento in _tiempos_every: del _tiempos_every[id_evento]
        return False
    tiempo_actual = time.time()
    tiempo_anterior = _tiempos_every.get(id_evento, 0.0)
    if tiempo_actual - tiempo_anterior >= segundos:
        _tiempos_every[id_evento] = tiempo_actual
        return True
    return False

_eventos_unicos: Set[str] = set()
def once(id_evento: Optional[str] = None, reset: bool = False) -> bool:
    """Registra o comprueba un evento de disparo único. Si id_evento es None, se autogenera."""
    global _eventos_unicos
    if id_evento is None:
        frame = inspect.stack()[1]
        id_evento = f"{frame.filename}:{frame.lineno}"
        
    if reset:
        if id_evento in _eventos_unicos: _eventos_unicos.remove(id_evento)
        return False
    if id_evento not in _eventos_unicos:
        _eventos_unicos.add(id_evento)
        return True
    return False

def is_leap_year(anio: Any) -> bool:#Creo que no necesito saber si es año bisiesto, pero bueno, por si acaso, aqui esta la funcion
    try:
        a = int(anio)
        return a % 4 == 0 and (a % 100 != 0 or a % 400 == 0)
    except Exception: return False

def get_timestamp() -> str: 
    return time.strftime("%Y-%m-%d %H:%M:%S")

def is_night(hora_actual: Optional[Any] = None) -> bool:
    try:
        hora = int(hora_actual if hora_actual is not None else time.strftime("%H"))
        return hora >= 20 or hora < 6
    except Exception: return False


# =====================================================================
# 4. ITERADORES Y COLECCIONES AVANZADAS 
# =====================================================================

def variable_loop(coleccion: Any) -> Iterator[Any]:
    if coleccion is None or not hasattr(coleccion, '__iter__') or isinstance(coleccion, str): return
    try:
        if isinstance(coleccion, dict):
            for llave in coleccion.keys(): yield llave
        else:
            for elemento in coleccion: yield elemento
    except Exception: return

def is_any_in(lista_buscar: Any, lista_destino: Any) -> bool:
    try: return any(item in lista_destino for item in lista_buscar)
    except TypeError: return False

def is_all_in(lista_buscar: Any, lista_destino: Any) -> bool:
    try: return all(item in lista_destino for item in lista_buscar)
    except TypeError: return False

def is_ordered(lista: Any, descendente: bool = False) -> bool:
    try:
        if len(lista) <= 1: return True
        if descendente: return all(lista[i] >= lista[i + 1] for i in range(len(lista) - 1))
        return all(lista[i] <= lista[i + 1] for i in range(len(lista) - 1))
    except TypeError: return False

def has_duplicates(lista: Any) -> bool:
    try: return len(lista) != len(set(lista))
    except TypeError: return False

def is_unique_collection(lista: Any) -> bool:
    try: return len(lista) == len(set(lista))
    except TypeError: return False

def is_consecutive(lista: Any) -> bool:
    try:
        if not lista: return False
        lista_ordenada = sorted(lista)
        return all(lista_ordenada[i] + 1 == lista_ordenada[i + 1] for i in range(len(lista_ordenada) - 1))
    except (TypeError, ValueError): return False

def is_empty(coleccion: Any) -> bool:
    try: return len(coleccion) == 0
    except TypeError: return False

def has_length(coleccion: Any, longitud_requerida: Any) -> bool:
    try: return len(coleccion) == int(longitud_requerida)
    except (TypeError, ValueError): return False

def has_min_length(coleccion: Any, minimo: Any) -> bool:
    try: return len(coleccion) >= int(minimo)
    except (TypeError, ValueError): return False

def has_max_length(coleccion: Any, maximo: Any) -> bool:
    try: return len(coleccion) <= int(maximo)
    except (TypeError, ValueError): return False

def has_element(coleccion: Any, elemento: Any) -> bool:
    try: return elemento in coleccion
    except TypeError: return False

def has_keys(diccionario: Any, llaves_requeridas: Any) -> bool:
    try: return all(llave in diccionario for llave in llaves_requeridas)
    except Exception: return False

def is_matrix(objeto: Any, filas_esperadas: Optional[int] = None, columnas_esperadas: Optional[int] = None) -> bool:
    try:
        if not isinstance(objeto, list) or not objeto or not isinstance(objeto[0], list): return False
        ancho = len(objeto[0])
        if ancho == 0 or not all(isinstance(fila, list) and len(fila) == ancho for fila in objeto): return False
        if filas_esperadas is not None and len(objeto) != filas_esperadas: return False
        if columnas_esperadas is not None and ancho != columnas_esperadas: return False
        return True
    except Exception: return False

def choose_weighted(opciones: List[Any], pesos: List[float]) -> Any:
    try: return random.choices(opciones, weights=pesos, k=1)[0]
    except (ValueError, TypeError, IndexError): return None

def is_trending_up(lista_numeros: Any) -> bool:
    try:
        if len(lista_numeros) < 2: return False
        return lista_numeros[-1] > lista_numeros[-2]
    except TypeError: return False

def get_random_element(coleccion: Any) -> Any:
    try: return random.choice(list(coleccion)) if coleccion else None
    except Exception: return None

def filter_list(lista: List[Any], condicion_funcion: Callable[[Any], bool]) -> List[Any]:
    try: return [e for e in lista if condicion_funcion(e)] if callable(condicion_funcion) else lista
    except Exception: return []

def count_element(coleccion: Any, elemento_a_contar: Any) -> int:
    try: return coleccion.count(elemento_a_contar)
    except Exception: return 0

def shuffle_list(lista: Any) -> List[Any]:
    try:
        copia = list(lista)
        random.shuffle(copia)
        return copia
    except TypeError: return lista


# =====================================================================
# 5. VALIDACIONES CIBERSEGURIDAD ENGINES / NETWORK
# =====================================================================

def is_valid_json(texto: Any) -> bool:
    try:
        if not isinstance(texto, str): return False
        json.loads(texto)
        return True
    except (ValueError, TypeError): return False

def is_valid_ip(texto: Any) -> bool:
    try:
        if not isinstance(texto, str): return False
        bloques = texto.split('.')
        return len(bloques) == 4 and all(b.isdigit() and 0 <= int(b) <= 255 for b in bloques)
    except Exception: return False

def is_valid_email(texto: Any) -> bool:#Ni como fuera a enviar un gmail en python
    try:
        if not isinstance(texto, str) or "@" not in texto: return False
        usuario, dominio = texto.split("@", 1)
        return len(usuario) > 0 and "." in dominio and len(dominio.split(".")[-1]) >= 2
    except Exception: return False

def is_secure_password(password: Any, min_longitud: int = 8) -> bool:#Yo se una contraseña segura,es Contraseña,si super segura,pero no la voy a decir por que es mia y no quiero que me la roben,ademas,es facil de recordar
    try:
        if not isinstance(password, str) or len(password) < min_longitud: return False
        return any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)
    except Exception: return False


# =====================================================================
# 6. GEOMETRÍA, FÍSICA Y RENDERIZADO DE VIDEOJUEGOS
# =====================================================================
import sys

def draw_at(x: int, y: int, contenido: str):
    """Escribe un objeto en coordenadas específicas sin limpiar toda la consola."""
    # El código \033[y;xH mueve el cursor a la fila y, columna x mas o menos, dependiendo de la terminal. Asegúrate de que tu terminal soporte ANSI escape codes.
    sys.stdout.write(f"\033[{y};{x}H{contenido}")
    sys.stdout.flush()

class Console_Object:#Para que quiero caracteres garrapatas de consolas, si puedo usar emojis y caracteres unicode
    """Un objeto que vive en la consola y recuerda su posición."""
    def __init__(self, x, y, simbolo):
        self.x = x
        self.y = y
        self.simbolo = simbolo
    
    def render(self):
        draw_at(self.x, self.y, self.simbolo)
    
    def clear(self):
        draw_at(self.x, self.y, " ")
    def move(self, nuevo_x, nuevo_y):
        self.clear()
        self.x = nuevo_x
        self.y = nuevo_y
        self.render()
def is_inside_screen(x: Any, y: Any, max_x: Any, max_y: Any) -> bool: 
    try: return 0 <= float(x) <= float(max_x) and 0 <= float(y) <= float(max_y)
    except Exception: return False

def is_near(pos1: Any, pos2: Any, distancia_maxima: Any) -> bool:
    try: return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) <= float(distancia_maxima)
    except (TypeError, IndexError): return False

def is_colliding_rect(rect1: Any, rect2: Any) -> bool:
    try:
        return (rect1['x'] < rect2['x'] + rect2['width'] and rect1['x'] + rect1['width'] > rect2['x'] and
                rect1['y'] < rect2['y'] + rect2['height'] and rect1['y'] + rect1['height'] > rect2['y'])
    except Exception: return False

def is_inside_radius(pos_origen: Any, pos_destino: Any, radio: Any) -> bool:
    try:
        dx, dy = pos_origen[0] - pos_destino[0], pos_origen[1] - pos_destino[1]
        r = float(radio)
        return (dx * dx + dy * dy) <= (r * r)
    except Exception: return False

def get_distance(pos1: Any, pos2: Any) -> float:
    try: return float(math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1]))
    except (TypeError, IndexError): return 0.0


# =====================================================================
# 7. ENTRADA Y SALIDA / PERSISTENCIA LOCAL ADICIONAL #O el lugar mas inutil de la lib
# =====================================================================

def save_data(filename: str, datos: Any) -> bool:
    try:
        if not filename.endswith('.json'): filename += '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return True
    except Exception: return False

def load_data(filename: str, valor_defecto: Any = None) -> Any:
    try:
        if not filename.endswith('.json'): filename += '.json'
        with open(filename, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception: return valor_defecto


# =====================================================================
# 8. CLASES PROGRAMÁTICAS Y MOTORES DE CONTROL
# =====================================================================
#Solo use cooldown y steptracker, por que no se me ocurrio nada mas para poner aqui, pero bueno, por si acaso, aqui estan las clases
class Switch:
    def __init__(self, valor_a_evaluar: Any) -> None:
        self.valor: Any = valor_a_evaluar
        self.casos: List[Tuple[Any, Callable[..., Any]]] = []
        self.defecto: Optional[Callable[..., Any]] = None
        
    def case(self, condicion: Any, resultado_o_funcion: Callable[..., Any]) -> 'Switch':
        self.casos.append((condicion, resultado_o_funcion))
        return self
        
    def default(self, resultado_o_funcion: Callable[..., Any]) -> 'Switch':
        self.defecto = resultado_o_funcion
        return self
        
    def run(self) -> Any:
        for condicion, resultado in self.casos:
            coincide = False
            if callable(condicion):
                try: coincide = bool(condicion(self.valor))
                except Exception: coincide = False
            elif isinstance(condicion, list): coincide = self.valor in condicion
            else: coincide = self.valor == condicion
            
            if coincide: 
                return resultado() if callable(resultado) else resultado
        return self.defecto() if callable(self.defecto) else self.defecto    
import time
from typing import Optional, Union

class Cooldown:
    def __init__(self, duracion: Union[float, int], invertido: bool = False) -> None:
        try:
            self.duracion: float = float(duracion)
            if self.duracion < 0:
                raise ValueError
            self.invertido: bool = bool(invertido)
        except (ValueError, TypeError):
            self.duracion = 1.0
            self.invertido = False
        
        self.tiempo_inicio: Optional[float] = None
        self.tiempo_pausado: Optional[float] = None
        self.activo: bool = False

    def start(self) -> None:
        try:
            self.tiempo_inicio = time.time()
            self.tiempo_pausado = None
            self.activo = True
        except Exception:
            self.activo = False

    def reset(self) -> None:
        self.tiempo_inicio = None
        self.tiempo_pausado = None
        self.activo = False

    def pause(self) -> None:
        try:
            if self.activo and self.tiempo_pausado is None and self.tiempo_inicio is not None:
                self.tiempo_pausado = time.time()
        except Exception:
            pass

    def resume(self) -> None:
        try:
            if self.activo and self.tiempo_pausado is not None and self.tiempo_inicio is not None:
                tiempo_en_pausa: float = time.time() - self.tiempo_pausado
                self.tiempo_inicio += tiempo_en_pausa
                self.tiempo_pausado = None
        except Exception:
            pass

    def tiempo_restante(self) -> float:
        try:
            if not self.activo or self.tiempo_inicio is None:
                return self.duracion
            
            if self.tiempo_pausado is not None:
                pasado: float = self.tiempo_pausado - self.tiempo_inicio
            else:
                pasado = time.time() - self.tiempo_inicio
                
            restante: float = self.duracion - pasado
            
            if restante < 0.0:
                return 0.0
            return restante
        except Exception:
            return 0.0

    def is_ready(self) -> bool:
        try:
            if not self.activo:
                return False
            
            restante: float = self.tiempo_restante()
            finalizado: bool = restante <= 0.0
            
            if self.invertido:
                return not finalizado
            return finalizado
        except Exception:
            return False

    def progress(self) -> float:
        try:
            if not self.activo or self.duracion == 0:
                return 0.0
                
            restante: float = self.tiempo_restante()
            pasado: float = self.duracion - restante
            porcentaje: float = pasado / self.duracion
            
            if porcentaje > 1.0:
                return 1.0
            elif porcentaje < 0.0:
                return 0.0
            return porcentaje
        except ZeroDivisionError:
            return 1.0
        except Exception:
            return 0.0
class StepTracker:
    def __init__(self, paso_inicial: int = 1) -> None: 
        self.paso_actual: int = paso_inicial
        
    def is_current_step(self, paso_a_comprobar: int) -> bool: 
        return self.paso_actual == paso_a_comprobar
        
    def advance(self) -> None: 
        self.paso_actual += 1
        
    def reset(self, paso_destino: int = 1) -> None: 
        self.paso_actual = paso_destino

class FrameTimer:
    def __init__(self, cuadros_espera: int) -> None:
        self.cuadros_espera: int = max(1, cuadros_espera)
        self.contador: int = 0
        
    def check(self) -> bool:
        self.contador += 1
        if self.contador >= self.cuadros_espera:
            self.contador = 0
            return True
        return False

class AutoResetToggle:
    def __init__(self, estado_inicial: bool = False) -> None: 
        self.estado: bool = bool(estado_inicial)
        
    def trigger(self) -> None: 
        self.estado = True
        
    def check_and_reset(self) -> bool:
        if self.estado:
            self.estado = False
            return True
        return False

class RetryCounter:
    def __init__(self, max_intentos: int = 3) -> None:
        self.max_intentos: int = max_intentos
        self.intentos_realizados: int = 0
        
    def fail_and_check(self) -> bool:
        self.intentos_realizados += 1
        return self.intentos_realizados < self.max_intentos
        
    def reset(self) -> None: 
        self.intentos_realizados = 0

class CircuitBreaker:
    def __init__(self, umbral_fallos: int = 3, tiempo_recuperacion: float = 5.0) -> None:
        self.umbral_fallos: int = umbral_fallos
        self.tiempo_recuperacion: float = tiempo_recuperacion
        self.contador_fallos: int = 0
        self.estado: str = "CERRADO"
        self.timestamp_bloqueo: float = 0.0
        
    def is_allowed(self) -> bool:
        if self.estado == "ABIERTO":
            if time.time() - self.timestamp_bloqueo > self.tiempo_recuperacion:
                self.estado = "MEDIO_ABIERTO"
                return True
            return False
        return True
        
    def record_failure(self) -> None:
        self.contador_fallos += 1
        if self.contador_fallos >= self.umbral_fallos:
            self.estado = "ABIERTO"
            self.timestamp_bloqueo = time.time()
            
    def record_success(self) -> None:
        self.contador_fallos = 0
        self.estado = "CERRADO"    


# =====================================================================
# 9. EXPORTACIÓN DINÁMICA DE LA SUITE (Para __init__.py)
# =====================================================================
__all__ = [name for name in dir() if not name.startswith("_")]