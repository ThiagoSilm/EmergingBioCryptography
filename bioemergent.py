"""
bioemergent.py
Thiago Maciel — 2025 — v2.2.1
"""

__version__ = "2.2.1"

import numpy as np
import time
import hashlib
import hmac
import secrets
from threading import Lock
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Union

@dataclass
class _Estado:
    dim: int
    vetor: Optional[np.ndarray] = None
    lock: Optional[Lock] = None
    def __post_init__(self):
        s = secrets.token_bytes(32)
        rng = np.random.default_rng(int.from_bytes(s, 'big'))
        self.vetor = rng.uniform(-1, 1, self.dim).astype(np.float64)
        self.vetor /= np.linalg.norm(self.vetor)
        self.lock = Lock()
    def similaridade(self, outro: np.ndarray) -> float:
        outro = outro.astype(np.float64) / np.linalg.norm(outro)
        with self.lock: return float(np.dot(self.vetor, outro))
    def evoluir(self, outro: np.ndarray, alpha: float):
        outro = outro.astype(np.float64)
        with self.lock:
            self.vetor = (1 - alpha) * self.vetor + alpha * outro
            self.vetor /= np.linalg.norm(self.vetor)
    def decair(self, fator: float):
        with self.lock:
            self.vetor *= fator
            n = np.linalg.norm(self.vetor)
            if n > 1e-10: self.vetor /= n
            else:
                self.vetor = np.random.uniform(-1, 1, self.dim)
                self.vetor /= np.linalg.norm(self.vetor)
    def derivar_semente(self) -> bytes:
        with self.lock: return hashlib.sha256(self.vetor.tobytes()).digest()
    def copiar(self) -> np.ndarray:
        with self.lock: return self.vetor.copy()

class _Metabolismo:
    def __init__(self, janela: float = 1.0, lambda_decay: float = 0.01):
        self.janela = janela
        self.lambda_decay = lambda_decay
        self.trocas: List[float] = []
        self.ultima = time.time()
        self.lock = Lock()
    def registrar(self):
        a = time.time()
        with self.lock:
            self.trocas = [t for t in self.trocas if a - t < self.janela]
            self.trocas.append(a)
            self.ultima = a
    def carga(self) -> float:
        with self.lock: return len(self.trocas) / self.janela
    def fator_decaimento(self) -> float:
        with self.lock: return np.exp(-self.lambda_decay * (time.time() - self.ultima))

class EstadoSeguro:
    def __init__(self, dim: int = 256, theta: float = 0.8, alpha: float = 0.1,
                 lambda_decay: float = 0.01, epsilon: float = 0.05, janela: float = 1.0,
                 modo: str = "cliente"):
        self.dim, self.theta, self.alpha, self.epsilon, self.modo = dim, theta, alpha, epsilon, modo
        self._estado = _Estado(dim)
        self._metabolismo = _Metabolismo(janela, lambda_decay)
        self._p_hash = hashlib.sha256(self._estado.vetor.tobytes()).digest()
        self._contador = 0
        self._sinc = (modo == "servidor")
        self.cifradas = self.decifradas = self.validadas = self.rejeitadas = 0
    def _atualizar_hash(self): self._p_hash = self._estado.derivar_semente()
    def _gerar_mascara(self, seed: bytes, tamanho: int) -> bytes:
        m = bytearray(); c = 0
        while len(m) < tamanho:
            m.extend(hashlib.sha256(seed + c.to_bytes(4, 'big')).digest())
            c += 1
        return bytes(m[:tamanho])
    def _encode(self, msg: str) -> np.ndarray:
        seed = int.from_bytes(hashlib.sha256(msg.encode()).digest()[:8], 'big')
        seed ^= int.from_bytes(self._p_hash[:8], 'big')
        rng = np.random.default_rng(seed)
        v = rng.uniform(-1, 1, self.dim).astype(np.float64)
        return v / np.linalg.norm(v)
    def cifrar(self, plain: Union[str, bytes]) -> bytes:
        if isinstance(plain, str): plain = plain.encode()
        self.cifradas += 1
        seed = hashlib.sha256(self._p_hash + self._contador.to_bytes(8, 'big')).digest()
        mask = self._gerar_mascara(seed, len(plain))
        ciphertext = bytes(a ^ b for a, b in zip(plain, mask))
        mac = hmac.new(self._p_hash, ciphertext, hashlib.sha256).digest()
        self._contador += 1
        return self._contador.to_bytes(8, 'big') + ciphertext + mac
    def decifrar(self, cipher: bytes) -> Tuple[Optional[str], bool]:
        self.decifradas += 1
        if len(cipher) < 40: return None, False
        ctr = int.from_bytes(cipher[:8], 'big')
        mac_recebido = cipher[-32:]
        ciphertext = cipher[8:-32]
        mac_calculado = hmac.new(self._p_hash, ciphertext, hashlib.sha256).digest()
        if not hmac.compare_digest(mac_recebido, mac_calculado):
            self.rejeitadas += 1
            return None, False
        f = self._metabolismo.fator_decaimento()
        if f < 0.999:
            self._estado.decair(f)
            self._atualizar_hash()
        seed = hashlib.sha256(self._p_hash + ctr.to_bytes(8, 'big')).digest()
        mask = self._gerar_mascara(seed, len(ciphertext))
        plain_bytes = bytes(a ^ b for a, b in zip(ciphertext, mask))
        try:
            msg = plain_bytes.decode('utf-8')
        except UnicodeDecodeError:
            self.rejeitadas += 1
            return None, False
        v = self._encode(msg)
        sim = self._estado.similaridade(v)
        if sim > self.theta:
            self._estado.evoluir(v, self.alpha)
            self._metabolismo.registrar()
            self._atualizar_hash()
            self.validadas += 1
            if self._metabolismo.carga() * np.linalg.norm(self._estado.vetor) < self.epsilon:
                self.renascer()
            return msg, True
        self.rejeitadas += 1
        return None, False
    def renascer(self):
        self._estado = _Estado(self.dim)
        self._metabolismo = _Metabolismo(self._metabolismo.janela, self._metabolismo.lambda_decay)
        self._atualizar_hash()
        self._contador = 0
        self._sinc = False
    def exportar(self) -> bytes:
        import struct
        d = bytearray()
        d.extend(struct.pack('>I', self.dim))
        d.extend(struct.pack('>d', self.theta))
        d.extend(struct.pack('>d', self.alpha))
        d.extend(struct.pack('>Q', self._contador))
        d.extend(self._estado.vetor.tobytes())
        return bytes(d)
    @classmethod
    def importar(cls, data: bytes, modo: str = "cliente"):
        import struct
        dim = struct.unpack('>I', data[0:4])[0]
        theta = struct.unpack('>d', data[4:12])[0]
        alpha = struct.unpack('>d', data[12:20])[0]
        ctr = struct.unpack('>Q', data[20:28])[0]
        obj = cls(dim=dim, theta=theta, alpha=alpha, modo=modo)
        obj._estado.vetor = np.frombuffer(data[28:], dtype=np.float64).copy()
        obj._contador = ctr
        obj._atualizar_hash()
        obj._sinc = True
        return obj
    def estatisticas(self) -> Dict:
        return {
            'modo': self.modo, 'sinc': self._sinc, 'contador': self._contador,
            'cifradas': self.cifradas, 'decifradas': self.decifradas,
            'validadas': self.validadas, 'rejeitadas': self.rejeitadas,
            'carga': self._metabolismo.carga(),
            'vitalidade': self._metabolismo.carga() * np.linalg.norm(self._estado.vetor)
        }

def gerar_par(dim: int = 256, theta: float = 0.8) -> Tuple[EstadoSeguro, EstadoSeguro]:
    s = EstadoSeguro(dim=dim, theta=theta, modo="servidor")
    c = EstadoSeguro(dim=dim, theta=theta, modo="cliente")
    c._estado.vetor = s._estado.copiar()
    c._contador = 0
    c._sinc = True
    return s, c

def cifrar(e: EstadoSeguro, p: Union[str, bytes]) -> bytes: return e.cifrar(p)
def decifrar(e: EstadoSeguro, c: bytes) -> Tuple[Optional[str], bool]: return e.decifrar(c)
def renovar(e: EstadoSeguro): e.renascer()
def exportar(e: EstadoSeguro) -> bytes: return e.exportar()
def importar_estado(d: bytes, modo: str = "cliente") -> EstadoSeguro: return EstadoSeguro.importar(d, modo)

Pai = lambda *a, **k: EstadoSeguro(*a, **k, modo="servidor")
ClienteBio = lambda *a, **k: EstadoSeguro(*a, **k, modo="cliente")
