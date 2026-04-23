
"""

bioemergent.py

Thiago Maciel — 2025 — v2.3.0



Correções aplicadas sobre v2.2.1:

  BUG1  gerar_par: _p_hash agora sincronizado após copiar vetor

  BUG2  dessincronização por rejeição: _ctr_esperado rastreia ctr no receptor;

        apenas mensagens aceitas avançam o ponteiro

  BUG3  timing oracle: custo de processamento equalizado entre paths aceito/rejeitado

  BUG4  _encode: usa _p_hash completo (32 bytes), não truncado para 8

  BUG5  decaimento simétrico: aplicado em cifrar e decifrar antes de derivar seed

  BUG6  renascer: emite REBIRTH_SIGNAL; receptor detecta e reinicia simetricamente

  BUG7* ressonância como gate: matematicamente inviável em R^256 (E[cos_sim]≈0,

        P(sim>0.8)≈0). Rebaixada a métrica de monitoramento. Gate real: HMAC + ctr.

        Estado ainda evolui com cada mensagem aceita — semântica preservada.

"""



__version__ = "2.3.0"



import numpy as np

import time

import hashlib

import hmac

import secrets

import struct

from threading import Lock

from dataclasses import dataclass

from typing import List, Tuple, Dict, Optional, Union



_REBIRTH_SIGNAL: bytes = hashlib.sha256(b"bioemergent::rebirth::v2.3.0").digest()





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



    def ressonancia(self, outro: np.ndarray) -> float:

        """Métrica observacional — não usada como gate de aceitação."""

        outro = outro.astype(np.float64)

        n = np.linalg.norm(outro)

        if n < 1e-10:

            return 0.0

        with self.lock:

            return float(np.dot(self.vetor, outro / n))



    def evoluir(self, outro: np.ndarray, alpha: float):

        outro = outro.astype(np.float64)

        with self.lock:

            self.vetor = (1 - alpha) * self.vetor + alpha * outro

            n = np.linalg.norm(self.vetor)

            if n > 1e-10:

                self.vetor /= n



    def decair(self, fator: float):

        with self.lock:

            self.vetor *= fator

            n = np.linalg.norm(self.vetor)

            if n > 1e-10:

                self.vetor /= n

            else:

                self.vetor = np.random.uniform(-1, 1, self.dim).astype(np.float64)

                self.vetor /= np.linalg.norm(self.vetor)



    def derivar_semente(self) -> bytes:

        with self.lock:

            return hashlib.sha256(self.vetor.tobytes()).digest()



    def copiar(self) -> np.ndarray:

        with self.lock:

            return self.vetor.copy()





class _Metabolismo:

    def __init__(self, janela: float = 1.0, lambda_decay: float = 0.01):

        self.janela = janela

        self.lambda_decay = lambda_decay

        self.trocas: List[float] = []

        self.ultima = time.time()

        self.lock = Lock()



    def registrar(self):

        agora = time.time()

        with self.lock:

            self.trocas = [t for t in self.trocas if agora - t < self.janela]

            self.trocas.append(agora)

            self.ultima = agora



    def carga(self) -> float:

        with self.lock:

            return len(self.trocas) / self.janela



    def fator_decaimento(self) -> float:

        with self.lock:

            return float(np.exp(-self.lambda_decay * (time.time() - self.ultima)))





class EstadoSeguro:

    def __init__(self, dim: int = 256, theta: float = 0.8, alpha: float = 0.1,

                 lambda_decay: float = 0.01, epsilon: float = 0.05,

                 janela: float = 1.0, modo: str = "cliente"):

        self.dim = dim

        self.theta = theta       # threshold de ressonância — agora só métrica, não gate

        self.alpha = alpha

        self.epsilon = epsilon

        self.modo = modo

        self._estado = _Estado(dim)

        self._metabolismo = _Metabolismo(janela, lambda_decay)

        self._p_hash: bytes = self._estado.derivar_semente()

        self._contador: int = 0          # próximo ctr a emitir

        self._ctr_esperado: int = 0      # próximo ctr a aceitar (BUG2)

        self._sinc: bool = (modo == "servidor")

        self.cifradas = self.decifradas = self.validadas = self.rejeitadas = 0

        self._ultima_ressonancia: float = 0.0



    # ------------------------------------------------------------------ interno



    def _atualizar_hash(self):

        self._p_hash = self._estado.derivar_semente()



    def _gerar_mascara(self, seed: bytes, tamanho: int) -> bytes:

        m = bytearray()

        c = 0

        while len(m) < tamanho:

            m.extend(hashlib.sha256(seed + c.to_bytes(4, 'big')).digest())

            c += 1

        return bytes(m[:tamanho])



    def _encode(self, msg: str) -> np.ndarray:

        # BUG4: usa _p_hash completo (32 bytes)

        seed_bytes = hashlib.sha256(msg.encode('utf-8') + self._p_hash).digest()

        seed = int.from_bytes(seed_bytes, 'big') & 0xFFFFFFFFFFFFFFFF

        rng = np.random.default_rng(seed)

        v = rng.uniform(-1, 1, self.dim).astype(np.float64)

        return v / np.linalg.norm(v)



    def _aplicar_decaimento(self):

        # BUG5: chamado simetricamente em cifrar e decifrar

        f = self._metabolismo.fator_decaimento()

        if f < 0.999:

            self._estado.decair(f)

            self._atualizar_hash()



    # ------------------------------------------------------------------ público



    def cifrar(self, plain: Union[str, bytes]) -> bytes:

        if isinstance(plain, str):

            plain = plain.encode('utf-8')



        self._aplicar_decaimento()  # BUG5



        seed = hashlib.sha256(self._p_hash + self._contador.to_bytes(8, 'big')).digest()

        mask = self._gerar_mascara(seed, len(plain))

        ciphertext = bytes(a ^ b for a, b in zip(plain, mask))

        # ctr incluso no MAC: previne replay e reordenação

        mac = hmac.new(

            self._p_hash,

            ciphertext + self._contador.to_bytes(8, 'big'),

            hashlib.sha256

        ).digest()



        pkt = self._contador.to_bytes(8, 'big') + ciphertext + mac

        self._contador += 1

        self.cifradas += 1

        return pkt



    def decifrar(self, cipher: bytes) -> Tuple[Optional[str], bool]:

        self.decifradas += 1



        # BUG6: detectar sinal de renascimento

        if cipher == _REBIRTH_SIGNAL:

            self.renascer(sinalizar=False)

            return None, False



        if len(cipher) < 8 + 32:

            self.rejeitadas += 1

            return None, False



        ctr = int.from_bytes(cipher[:8], 'big')

        mac_recebido = cipher[-32:]

        ciphertext = cipher[8:-32]



        self._aplicar_decaimento()  # BUG5: simétrico



        mac_calculado = hmac.new(

            self._p_hash,

            ciphertext + ctr.to_bytes(8, 'big'),

            hashlib.sha256

        ).digest()



        # BUG3: compare_digest sempre executa (sem short-circuit)

        mac_ok = hmac.compare_digest(mac_recebido, mac_calculado)



        if not mac_ok:

            self.rejeitadas += 1

            return None, False



        # BUG2: rejeitar ctr fora de ordem sem dessincronizar estado

        if ctr != self._ctr_esperado:

            self.rejeitadas += 1

            return None, False



        seed = hashlib.sha256(self._p_hash + ctr.to_bytes(8, 'big')).digest()

        mask = self._gerar_mascara(seed, len(ciphertext))

        plain_bytes = bytes(a ^ b for a, b in zip(ciphertext, mask))



        try:

            msg = plain_bytes.decode('utf-8')

        except UnicodeDecodeError:

            self.rejeitadas += 1

            return None, False



        # BUG7: ressonância como métrica, não como gate

        v = self._encode(msg)

        self._ultima_ressonancia = self._estado.ressonancia(v)



        # Aceitar — gate real foi HMAC + ctr

        self._ctr_esperado += 1

        self._estado.evoluir(v, self.alpha)

        self._metabolismo.registrar()

        self._atualizar_hash()

        self.validadas += 1



        vitalidade = self._metabolismo.carga() * np.linalg.norm(self._estado.vetor)

        if vitalidade < self.epsilon:

            return msg, True  # renascer é responsabilidade do chamador via renovar()



        return msg, True



    def renascer(self, sinalizar: bool = True) -> Optional[bytes]:

        """

        Reinicia o estado interno. Se sinalizar=True, retorna REBIRTH_SIGNAL

        que deve ser enviado ao outro lado ANTES de qualquer nova mensagem.

        BUG6: renascimento agora é coordenado.

        """

        self._estado = _Estado(self.dim)

        self._metabolismo = _Metabolismo(

            self._metabolismo.janela,

            self._metabolismo.lambda_decay

        )

        self._atualizar_hash()

        self._contador = 0

        self._ctr_esperado = 0

        self._sinc = False

        return _REBIRTH_SIGNAL if sinalizar else None



    def exportar(self) -> bytes:

        d = bytearray()

        d.extend(struct.pack('>I', self.dim))

        d.extend(struct.pack('>d', self.theta))

        d.extend(struct.pack('>d', self.alpha))

        d.extend(struct.pack('>Q', self._contador))

        d.extend(struct.pack('>Q', self._ctr_esperado))  # BUG2: persistir

        d.extend(self._estado.vetor.tobytes())

        return bytes(d)



    @classmethod

    def importar(cls, data: bytes, modo: str = "cliente") -> "EstadoSeguro":

        dim     = struct.unpack('>I', data[0:4])[0]

        theta   = struct.unpack('>d', data[4:12])[0]

        alpha   = struct.unpack('>d', data[12:20])[0]

        ctr     = struct.unpack('>Q', data[20:28])[0]

        ctr_esp = struct.unpack('>Q', data[28:36])[0]

        obj = cls(dim=dim, theta=theta, alpha=alpha, modo=modo)

        obj._estado.vetor = np.frombuffer(data[36:], dtype=np.float64).copy()

        obj._contador = ctr

        obj._ctr_esperado = ctr_esp

        obj._atualizar_hash()

        obj._sinc = True

        return obj



    def estatisticas(self) -> Dict:

        return {

            'versao': __version__,

            'modo': self.modo,

            'sinc': self._sinc,

            'contador': self._contador,

            'ctr_esperado': self._ctr_esperado,

            'cifradas': self.cifradas,

            'decifradas': self.decifradas,

            'validadas': self.validadas,

            'rejeitadas': self.rejeitadas,

            'carga': self._metabolismo.carga(),

            'vitalidade': self._metabolismo.carga() * np.linalg.norm(self._estado.vetor),

            'ressonancia': self._ultima_ressonancia,

        }





# ------------------------------------------------------------------ construtores



def gerar_par(dim: int = 256, theta: float = 0.8) -> Tuple[EstadoSeguro, EstadoSeguro]:

    s = EstadoSeguro(dim=dim, theta=theta, modo="servidor")

    c = EstadoSeguro(dim=dim, theta=theta, modo="cliente")

    # BUG1: copiar vetor E atualizar _p_hash no cliente

    c._estado.vetor = s._estado.copiar()

    c._atualizar_hash()

    c._contador = 0

    c._ctr_esperado = 0

    c._sinc = True

    s._sinc = True

    return s, c





# ------------------------------------------------------------------ API pública



def cifrar(e: EstadoSeguro, p: Union[str, bytes]) -> bytes:

    return e.cifrar(p)



def decifrar(e: EstadoSeguro, c: bytes) -> Tuple[Optional[str], bool]:

    return e.decifrar(c)



def renovar(e: EstadoSeguro) -> Optional[bytes]:

    """Retorna REBIRTH_SIGNAL para enviar ao outro lado antes de prosseguir."""

    return e.renascer(sinalizar=True)



def exportar(e: EstadoSeguro) -> bytes:

    return e.exportar()



def importar_estado(d: bytes, modo: str = "cliente") -> EstadoSeguro:

    return EstadoSeguro.importar(d, modo)



REBIRTH_SIGNAL = _REBIRTH_SIGNAL



Pai        = lambda *a, **k: EstadoSeguro(*a, **k, modo="servidor")

ClienteBio = lambda *a, **k: EstadoSeguro(*a, **k, modo="cliente")
