import numpy as np
import time
from threading import Lock, Thread
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Estado:
    dim: int
    vetor: np.ndarray = None
    lock: Lock = None
    
    def __post_init__(self):
        self.vetor = np.random.uniform(-1, 1, self.dim)
        self.vetor /= np.linalg.norm(self.vetor)
        self.lock = Lock()
    
    def similaridade(self, outro: np.ndarray) -> float:
        outro = outro / np.linalg.norm(outro)
        with self.lock:
            return float(np.dot(self.vetor, outro))
    
    def evoluir(self, outro: np.ndarray, alpha: float):
        with self.lock:
            self.vetor = (1 - alpha) * self.vetor + alpha * outro
            self.vetor /= np.linalg.norm(self.vetor)
    
    def decair(self, fator: float):
        with self.lock:
            self.vetor *= fator
            self.vetor /= np.linalg.norm(self.vetor)

class Metabolismo:
    def __init__(self, janela: float = 1.0, lambda_decay: float = 0.01):
        self.janela = janela
        self.lambda_decay = lambda_decay
        self.trocas: List[float] = []
        self.ultima_atividade = time.time()
    
    def registrar(self):
        agora = time.time()
        self.trocas = [t for t in self.trocas if agora - t < self.janela]
        self.trocas.append(agora)
        self.ultima_atividade = agora
    
    def carga(self) -> float:
        return len(self.trocas) / self.janela
    
    def fator_decaimento(self) -> float:
        delta = time.time() - self.ultima_atividade
        return np.exp(-self.lambda_decay * delta)

class Pai:
    def __init__(self, dim: int, theta: float = 0.8, alpha: float = 0.1,
                 lambda_decay: float = 0.01, epsilon: float = 0.05, janela: float = 1.0):
        self.dim = dim
        self.theta = theta
        self.alpha = alpha
        self.epsilon = epsilon
        self.estado = Estado(dim)
        self.metabolismo = Metabolismo(janela, lambda_decay)
        self._p_hash = 0
        self._atualizar_hash()
    
    def _atualizar_hash(self):
        with self.estado.lock:
            self._p_hash = int(np.dot(self.estado.vetor, self.estado.vetor[::-1]) * 1e6)
    
    def encode(self, mensagem: str) -> np.ndarray:
        seed = hash(mensagem) ^ self._p_hash
        rng = np.random.default_rng(seed)
        vetor = rng.uniform(-1, 1, self.dim)
        return vetor / np.linalg.norm(vetor)
    
    def digest(self, vetor_filho: np.ndarray) -> Tuple[bool, float]:
        fator = self.metabolismo.fator_decaimento()
        if fator < 1.0:
            self.estado.decair(fator)
            self._atualizar_hash()
        
        sim = self.estado.similaridade(vetor_filho)
        if sim > self.theta:
            self.estado.evoluir(vetor_filho, self.alpha)
            self.metabolismo.registrar()
            self._atualizar_hash()
            
            if self.metabolismo.carga() * np.linalg.norm(self.estado.vetor) < self.epsilon:
                self.renascer()
            
            return True, sim
        return False, sim
    
    def renascer(self):
        self.estado = Estado(self.dim)
        self.metabolismo = Metabolismo(self.metabolismo.janela, self.metabolismo.lambda_decay)
        self._atualizar_hash()

class Filho:
    def __init__(self, pai: Pai, alpha: float = 0.1):
        self.pai = pai
        self.alpha = alpha
        self.estado = Estado(pai.dim)
    
    def processar_mensagem(self, mensagem: str) -> Tuple[bool, float]:
        vetor_msg = self.pai.encode(mensagem)
        aceito, sim = self.pai.digest(vetor_msg)
        if aceito:
            with self.pai.estado.lock:
                proj = self.pai.estado.vetor.copy()
            self.estado.evoluir(proj, self.alpha)
        return aceito, sim
