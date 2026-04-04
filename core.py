import numpy as np
import time
from threading import Lock, Thread

class Pai:
    def __init__(self, dim, theta=0.8, alpha=0.1, janela=1.0):
        self.dim = dim
        self.theta = theta
        self.alpha = alpha
        self.P = np.random.uniform(-1, 1, dim)
        self.P /= np.linalg.norm(self.P)
        self.lock = Lock()
        self.janela = janela
        self.trocas_recentes = []

    def encode(self, mensagem):
        seed = int(sum(ord(c) for c in str(mensagem))) ^ int(np.dot(self.P, self.P[::-1]) * 1e6)
        rng = np.random.default_rng(seed)
        vetor = rng.uniform(-1, 1, self.dim)
        vetor /= np.linalg.norm(vetor)
        return vetor

    def similarity(self, vetor):
        vetor /= np.linalg.norm(vetor)
        return np.dot(self.P, vetor)

    def registrar_troca(self):
        agora = time.time()
        self.trocas_recentes = [t for t in self.trocas_recentes if agora - t < self.janela]
        self.trocas_recentes.append(agora)

    def charge_factor(self):
        return len(self.trocas_recentes) / self.janela

    def digest(self, P_filho):
        with self.lock:
            res = self.similarity(P_filho)
            if res > self.theta:
                self.P = (1 - self.alpha) * self.P + self.alpha * P_filho
                self.P /= np.linalg.norm(self.P)
                self.registrar_troca()
                return True, res
            return False, res

class Filho:
    def __init__(self, pai, alpha=0.1):
        self.pai = pai
        self.alpha = alpha
        self.P = np.random.uniform(-1, 1, pai.dim)
        self.P /= np.linalg.norm(self.P)

    def processar_mensagem(self, mensagem):
        P_msg = self.pai.encode(mensagem)
        aceito, res = self.pai.digest(P_msg)
        if aceito:
            proj = self.pai.P.copy()
            self.P = (1 - self.alpha) * self.P + self.alpha * proj
            self.P /= np.linalg.norm(self.P)
        return aceito, res

def loop_continuo(pai, filhos, mensagens, running_flag):
    def filho_loop(filho):
        while running_flag["ativo"]:
            for msg in mensagens:
                aceito, res = filho.processar_mensagem(msg)
                # Pode incluir sleep se precisar controlar taxa
                time.sleep(0.01)
    
    threads = [Thread(target=filho_loop, args=(f,), daemon=True) for f in filhos]
    for t in threads:
        t.start()
    return threads

# Exemplo de uso
pai = Pai(dim=64)
filhos = [Filho(pai) for _ in range(5)]
mensagens = ["mensagem1", "mensagem2", "mensagem3"]
running_flag = {"ativo": True}
threads = loop_continuo(pai, filhos, mensagens, running_flag)

# Para encerrar o loop depois de algum tempo
time.sleep(5)
running_flag["ativo"] = False
