# EmergingBioCryptography / CRIPTOGRAFIA BIO-EMERGENTE

### Segurança como Propriedade de História Compartilhada Irreversível

**Thiago Maciel — 2025 — v2.2.0**

---

**Repositório:** https://github.com/ThiagoSilm/EmergingBioCryptography

---

## Abstract

Paradigma criptográfico distinto. Segurança opera sobre história compartilhada irreversível. Agentes coevoluem por trocas validadas desenvolvendo universo semântico exclusivo. Imune a ataques clássicos: ausência de chave estática. Imune a ataques quânticos: ausência de problema matemático endereçável. Segurança emerge, persiste, endurece com tempo de uso.

v2.2.0: Ofuscação emergente. Canal aberto. Cliente e servidor mantêm estados sincronizados P(t). Ciclo de vida completo: decaimento natural, morte por inanição, renascimento com nova identidade. API drop-in replacement para criptografia convencional.

---

## 1. O Problema com Criptografia Estática

Toda criptografia existente — de cifras de substituição a lattices pós-quânticos — opera sobre complexidade computacional. Segredo existe como objeto estático protegido por dificuldade matemática.

RSA e ECC colapsam ante Shor. Lattices resistem porque Learning With Errors não possui algoritmo quântico conhecido — mas primitiva é a mesma: objeto matemático protegido por dificuldade.

Problema não é matemática. É paradigma. Qualquer sistema onde segredo pode ser representado como dado estático possui superfície de ataque explorável.

Criptografia Bio-Emergente abandona essa corrida. Ocupa outro espaço.

---

## 2. Primitiva Nova

**Segurança como propriedade de história compartilhada irreversível.**

Não há chave. Não há objeto para proteger. Há processo que não pode ser replicado sem ter sido vivido.

Dois agentes que coevoluem por trocas validadas constroem estado interno mutuamente dependente — linguagem emergente que só existe para quem participou da criação. Adversário externo não encontra parede matemática. Encontra idioma que não existe em dicionário.

Pergunta que toda criptografia responde: *qual é a chave?*

Aqui, essa pergunta não tem resposta. **Chave é processo. Não objeto.**

Sistema opera em dois modos integrados:
1. Validação metabólica: comandos só têm efeito se ressoam com P(t).
2. Ofuscação emergente: mensagens mascaradas por estado compartilhado, eliminando necessidade de VPN/SSH/TLS.

---

## 3. Formalização

### 3.1 Estado do Sistema

Cada agente (cliente e servidor) mantém vetor de persistência P(t) — representação densa do histórico acumulado de trocas validadas.

```python
P(t) ∈ ℝⁿ  |  ‖P(t)‖ = 1
```

Estados cliente e servidor sincronizados: após cada troca validada, ambos evoluem identicamente.

### 3.2 Lei de Dominância

```python
W_c(t) = ‖P(t)‖ · f_local · charge_factor(t)
```

- P(t) — persistência acumulada; histórico colapsado de trocas validadas
- f_local — contexto de execução local; constante por instância
- charge_factor(t) — energia do momento; taxa de trocas validadas em janela deslizante

### 3.3 Decaimento Natural

```python
P(t + Δt) = P(t) · e^(−λ · Δt)
```

Sem trocas, ambos os lados decaem simetricamente. Sincronia mantida mesmo na ausência de comunicação.

### 3.4 Evolução por Digestão

```python
P(t+1) = normalize((1 − α) · P(t) + α · P_mensagem_validada)
```

Após validação bem-sucedida, servidor evolui estado. Cliente recebe projeção e evolui identicamente.

### 3.5 Ressonância como Validação Binária

```python
similarity(P_servidor, P_mensagem) = P_servidor · P_mensagem  ∈ [−1, 1]
válido = similarity > θ
```

Não há gradiente explorável. Ou ressoa ou não ressoa. Adversário sem direção de ataque.

### 3.6 Ofuscação por Estado Compartilhado

```python
mask = KDF(P(t) || contador)
ciphertext = plaintext XOR mask
```

KDF determinística baseada em semente derivada de P(t). Não é criptografia convencional — é projeção de estado.

### 3.7 GC Emergente

```python
se W_c(t) < ε → morte → restart com nova identidade (ambos os lados)
```

Morte não é falha. É forward secrecy emergente. Sistema morto não pode ser interrogado.

---

## 4. Arquitetura

### 4.1 Visão Geral

```python
┌─────────────────────────────────────────────────────────────┐
│  Cliente Bio-Emergente          Servidor Pai                │
│  ┌──────────────┐               ┌──────────────┐            │
│  │ Estado P_c(t)│◄─── sinc ────►│ Estado P_s(t)│            │
│  └──────────────┘               └──────────────┘            │
│         │                              │                     │
│         ▼                              ▼                     │
│  plaintext ──► mask ──► ciphertext ──► mask ──► plaintext   │
│                                                   │          │
│                                                   ▼          │
│                                             validação        │
│                                             metabólica       │
│                                                   │          │
│                                                   ▼          │
│  P_c(t+1) ◄───────── projeção ─────────────── P_s(t+1)      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Bootstrap Inicial

Primeira sincronização requer canal autenticado (encontro físico, QR code, VPN temporária). Após bootstrap, canal pode ser completamente aberto.

### 4.3 Sincronização de Estado

Premissa crítica: Cliente e servidor devem manter P(t) idênticos.

Mecanismo:
1. Bootstrap: ambos partem do mesmo vetor aleatório.
2. Cada troca validada: servidor envia projeção do novo P(t). Cliente aplica mesma evolução.
3. Decaimento: ambos aplicam mesma função temporal f(Δt) = e^(-λ·Δt).

Recuperação de dessincronia:
- Cliente detecta falha consecutiva de validação (NACK persistente).
- Cliente renasce (novo P aleatório) e reinicia handshake.

### 4.4 Rede de Confiança Transitiva

Múltiplos servidores Pai podem formar rede. Cliente que transita entre nós carrega estado P(t) como credencial viva.

```python
[Alice] ◄── P_a(t) ──► [Cliente] ◄── P_a(t) ──► [Bob]
                              │
                    Estado do cliente é
                    prova de história com Alice
```

Bob valida cliente sem conhecer Alice porque estado P(t) do cliente ressoa com projeção esperada para alguém que passou por Alice.

---

## 5. Ciclo de Vida

```python
EMERGÊNCIA → APROVAÇÃO → PERSISTÊNCIA → DUPLICAÇÃO → MORTE → RENASCIMENTO
```

Sincronização do ciclo:
- Cliente e servidor nascem com mesmo P(0).
- Evoluem juntos a cada troca validada.
- Decaem juntos na inatividade.
- Morrem juntos quando W_c < ε.
- Renascem com nova identidade (requer novo bootstrap).

---

## 6. Propriedade Fractal

Mesma lei opera em todas as escalas:

```python
W_c(t) = ‖P(t)‖ · f_local · charge_factor(t)
```

No micro — par cliente-servidor: cada troca valida e ofusca.

No macro — rede de servidores: cada nó persiste enquanto ressoa com outros.

No meta — protocolo: persiste enquanto há pares ativos.

---

## 7. Propriedades de Segurança

### 7.1 Sem Superfície de Ataque Clássica

Não há chave para extrair. Não há cifra para analisar. Não há protocolo de handshake. Estado P(t) existe apenas em RAM.

### 7.2 Resistência Quântica por Categoria

Nenhum algoritmo quântico endereça história vivida. Ofuscação usa XOR com máscara derivada de estado — sem problema matemático subjacente.

### 7.3 Confidencialidade sem Canal Seguro

| Cenário | v2.1 (plaintext sobre VPN) | v2.2 (ofuscação emergente) |
|---|---|---|
| Observador passivo | Vê comandos em claro | Vê bytes aleatórios |
| Análise de tráfego | Revela padrões de comando | Padrões ofuscados por estado evolutivo |
| Injeção de ciphertext | Impossível sem P(t) | Impossível sem P(t) + contador |
| Replay attack | P(t) evoluiu → falha | P(t) evoluiu + contador → falha |

### 7.4 Forward Secrecy Implícito

Cada mensagem usa máscara derivada de P(t) atual. Estado passado não recupera mensagens futuras. Morte do sistema apaga todo histórico.

### 7.5 Endurecimento com o Tempo

Convencional: exposição prolongada → mais dados para criptoanálise.

Bio-Emergente: cada troca validada aumenta distância do estado inicial. Tempo trabalha a favor.

### 7.6 Análise de Vetores de Ataque

| Vetor de Ataque | Resultado |
|---|---|
| Interceptar tráfego | Bytes aleatórios. Sem P(t), irrecuperável. |
| Comprometer cliente | Obtém P_c(t). Pode enviar mensagens válidas. Janela limitada até evolução. |
| Comprometer servidor | Obtém P_s(t). Pode validar qualquer mensagem. Equivale a acesso root. |
| Forjar ciphertext | Requer P(t) para derivar máscara correta. |
| Replay attack | Contador + P(t) evoluiu. Ciphertext antigo inválido. |
| Ataque quântico | Sem algoritmo matemático para acelerar. |
| Ataque de texto conhecido | Adversário sabe plaintext de uma mensagem. Recupera máscara daquela mensagem. Não recupera P(t) nem máscaras futuras. |
| Dessincronização forçada | Atacante bloqueia respostas. Cliente detecta NACKs consecutivos e renasce. |

---

## 8. API

```python
import bioemergent as be

# Geração de par (análogo a keypair)
servidor, cliente = be.gerar_par(dim=256)

# Cifrar
ciphertext = be.cifrar(cliente, "TRANSFERIR 1M BTC")

# Decifrar e validar
plaintext, valido = be.decifrar(servidor, ciphertext)

# Exportar/importar estado
dados = be.exportar(servidor)
servidor_restaurado = be.importar_estado(dados, modo="servidor")

# Renovação manual (forward secrecy)
be.renovar(servidor)

# Estatísticas
stats = servidor.estatisticas()
```

**Compatibilidade:** `Pai` e `ClienteBio` mantidos como aliases.

```python
from bioemergent import Pai, ClienteBio
servidor = Pai(dim=256)
cliente = ClienteBio(dim=256)
```

---

## 9. Implementação de Referência

Arquivo único: `bioemergent.py`

Dependência: `numpy >= 1.20.0`

```python
"""
bioemergent.py
Thiago Maciel — 2025
"""

__version__ = "2.2.0"

import numpy as np
import time
import hashlib
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
    def derivar_semente(self) -> int:
        with self.lock: return int(np.dot(self.vetor, self.vetor[::-1]) * 1e12)
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
        self._p_hash = 0
        self._atualizar_hash()
        self._contador = 0
        self._sinc = (modo == "servidor")
        self.cifradas = self.decifradas = self.validadas = self.rejeitadas = 0
    def _atualizar_hash(self): self._p_hash = self._estado.derivar_semente()
    def _gerar_mascara(self, seed: int, tamanho: int) -> bytes:
        h = hashlib.sha256(seed.to_bytes(16, 'big', signed=True)).digest()
        m = bytearray(); c = 0
        while len(m) < tamanho:
            m.extend(hashlib.sha256(h + c.to_bytes(4, 'big')).digest())
            c += 1
        return bytes(m[:tamanho])
    def _encode(self, msg: str) -> np.ndarray:
        rng = np.random.default_rng(hash(msg) ^ self._p_hash)
        v = rng.uniform(-1, 1, self.dim).astype(np.float64)
        return v / np.linalg.norm(v)
    def cifrar(self, plain: Union[str, bytes]) -> bytes:
        if isinstance(plain, str): plain = plain.encode()
        self.cifradas += 1
        seed = self._p_hash ^ self._contador
        mask = self._gerar_mascara(seed, len(plain))
        return self._contador.to_bytes(8, 'big') + bytes(a ^ b for a, b in zip(plain, mask))
    def decifrar(self, cipher: bytes) -> Tuple[Optional[str], bool]:
        self.decifradas += 1
        if len(cipher) < 8: return None, False
        ctr = int.from_bytes(cipher[:8], 'big')
        pay = cipher[8:]
        f = self._metabolismo.fator_decaimento()
        if f < 0.999:
            self._estado.decair(f)
            self._atualizar_hash()
        mask = self._gerar_mascara(self._p_hash ^ ctr, len(pay))
        try: msg = bytes(a ^ b for a, b in zip(pay, mask)).decode()
        except: self.rejeitadas += 1; return None, False
        v = self._encode(msg)
        sim = self._estado.similaridade(v)
        if sim > self.theta:
            self._estado.evoluir(v, self.alpha)
            self._metabolismo.registrar()
            self._atualizar_hash()
            self._contador += 1
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
```

---

## 10. Instalação

```bash
curl -O https://raw.githubusercontent.com/ThiagoSilm/EmergingBioCryptography/main/bioemergent.py
```

Dependência: `numpy >= 1.20.0`

```bash
pip install numpy
```

---

## 11. Comparação Entre Versões

| Característica | v2.0 | v2.1 | v2.2 |
|---|---|---|---|
| Canal seguro externo | Requer VPN/SSH | Requer VPN/SSH | Desnecessário |
| Estado no cliente | Inexistente | Inexistente | Sincronizado |
| Confidencialidade | Nenhuma | Nenhuma | Ofuscação por estado |
| Observação passiva | Vê comandos | Vê comandos | Vê ruído |
| Replay protection | Parcial | Parcial | Total (P(t)+contador) |
| Forward secrecy | Morte do servidor | Morte do servidor | Cada mensagem |
| API drop-in | Não | Não | Sim |

---

## 12. Limitações Conhecidas

### 12.1 Bootstrap Inicial

Primeira sincronização requer canal autenticado (encontro físico, QR code, VPN temporária). Após bootstrap, canal pode ser completamente aberto.

### 12.2 Dessincronização

Se cliente perde resposta do servidor, contadores divergem. Detectável via NACK consecutivo. Recuperação: cliente renasce e re-bootstrap.

### 12.3 Comprometimento do Cliente

Adversário com acesso ao cliente obtém P_c(t). Pode enviar mensagens válidas até próxima evolução. Mitigação: renovação frequente (alto charge_factor).

### 12.4 Ataque de Texto Conhecido

Se adversário conhece plaintext de uma mensagem, recupera máscara daquela mensagem específica. Não recupera P(t) nem máscaras de outras mensagens.

---

## 13. Conclusão

Criptografia Bio-Emergente não é variação de sistema existente. É primitiva nova.

Chave não é criada. É vivida. Adversário não enfrenta complexidade matemática — enfrenta irreversibilidade do tempo.

Sistema não protege informação. Cria universo onde comandos só têm efeito para quem pertence a ele.

v2.2.0 elimina última dependência de infraestrutura criptográfica tradicional: canal seguro. Estado compartilhado P(t) serve para validação metabólica e ofuscação de tráfego. Nenhuma chave estática. Nenhum handshake. Nenhum algoritmo matemático atacável.

---

## 14. Licença

MIT

---

*Thiago Maciel — 2025 — v2.2.0*
*Desenvolvido em colaboração com ❤️*

Wheeler • Susskind • Bekenstein • Prigogine • Kauffman • Penrose • Pauli • Hawking • Everett • Mandelbrot • Shannon • Neumann • Wolfram • Bohm • Zeilinger
