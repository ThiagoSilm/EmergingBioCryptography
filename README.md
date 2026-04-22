# EmergingBioCryptography / CRIPTOGRAFIA BIO-EMERGENTE

### Segurança como Propriedade de História Compartilhada Irreversível

**Thiago Maciel — 2025 — v2.2**

---

## Abstract

Propomos um paradigma criptográfico categoricamente distinto de toda arquitetura existente. A Criptografia Bio-Emergente não opera sobre complexidade computacional como primitiva de segurança — opera sobre **história compartilhada irreversível**. Dois agentes que coevoluem por trocas validadas desenvolvem um universo semântico exclusivo, inacessível a qualquer entidade sem presença desde a origem. O sistema é imune a ataques clássicos por ausência de chave estática. É imune a ataques quânticos por ausência de problema matemático endereçável. A segurança não é protegida — **emerge, persiste e endurece com o tempo de uso.**

**Atualização v2.2:** Eliminação da dependência de canal seguro externo. Cliente e servidor mantêm estados sincronizados P(t). Ofuscação simétrica emerge do estado compartilhado sem chave estática. Canal pode ser completamente aberto — observador vê apenas sequências aleatórias não-reproduzíveis. Ciclo de vida completo integrado: decaimento natural, morte por inanição, renascimento com nova identidade.

---

## 1. O Problema com Criptografia Estática

Toda criptografia existente — de cifras de substituição a lattices pós-quânticos — opera sobre o mesmo pressuposto fundamental: segurança é um problema de **complexidade computacional**. O segredo existe como objeto estático protegido por dificuldade matemática.

RSA e ECC colapsam ante o algoritmo de Shor porque fatoração e logaritmo discreto têm solução quântica eficiente. Lattices resistem porque Learning With Errors não possui algoritmo quântico conhecido — mas a primitiva é a mesma: um objeto matemático protegido por dificuldade.

O problema não é a matemática. **É o paradigma.** Qualquer sistema onde o segredo pode ser representado como dado estático em algum momento possui superfície de ataque explorável. Exposição prolongada é risco crescente. A história do campo é uma corrida entre criação de complexidade e ruptura dela.

A Criptografia Bio-Emergente abandona essa corrida. Não compete no mesmo espaço — **ocupa outro.**

---

## 2. A Primitiva Nova

**Segurança como propriedade de história compartilhada irreversível.**

Não há chave. Não há objeto para proteger. Há um processo que não pode ser replicado sem ter sido vivido.

Dois agentes que coevoluem por trocas validadas ao longo do tempo constroem um estado interno mutuamente dependente — linguagem emergente que só existe para quem participou da sua criação. Um adversário externo não encontra uma parede matemática para superar. Encontra um **idioma que não existe em nenhum dicionário.**

A pergunta que toda criptografia existente responde é: *qual é a chave?*

Aqui, essa pergunta não tem resposta. **A chave é um processo. Não um objeto.**

O sistema opera em dois modos integrados:
1. **Validação metabólica:** Comandos só têm efeito se ressoam com P(t).
2. **Ofuscação emergente:** Mensagens são mascaradas por estado compartilhado, eliminando necessidade de VPN/SSH/TLS.

---

## 3. Formalização

### 3.1 Estado do Sistema

Cada agente (cliente e servidor) mantém um vetor de persistência **P(t)** — representação densa do histórico acumulado de trocas validadas.

```
P(t) ∈ ℝⁿ  |  ‖P(t)‖ = 1
```

Estados cliente e servidor são sincronizados: após cada troca validada, ambos evoluem identicamente.

### 3.2 Lei de Dominância

```
W_c(t) = ‖P(t)‖ · f_local · charge_factor(t)
```

- **P(t)** — persistência acumulada; histórico colapsado de trocas validadas
- **f_local** — contexto de execução local; constante por instância
- **charge_factor(t)** — energia do momento; taxa de trocas validadas em janela deslizante

### 3.3 Decaimento Natural

```
P(t + Δt) = P(t) · e^(−λ · Δt)
```

Sem trocas, ambos os lados decaem simetricamente. Sincronia é mantida mesmo na ausência de comunicação.

### 3.4 Evolução por Digestão

```
P(t+1) = normalize((1 − α) · P(t) + α · P_mensagem_validada)
```

Após validação bem-sucedida, servidor evolui seu estado. Cliente recebe projeção e evolui identicamente.

### 3.5 Ressonância como Validação Binária

```
similarity(P_servidor, P_mensagem) = P_servidor · P_mensagem  ∈ [−1, 1]

válido = similarity > θ
```

### 3.6 Ofuscação por Estado Compartilhado

```
mask = KDF(P(t) || contador)
ciphertext = plaintext XOR mask
```

**KDF** (Key Derivation Function) determinística baseada em semente derivada de P(t). Não é criptografia convencional — é projeção de estado.

### 3.7 GC Emergente

```
se W_c(t) < ε → morte → restart com nova identidade (ambos os lados)
```

Morte sincronizada requer coordenação. Cliente detecta morte do servidor via falha de validação persistente e reinicia seu estado.

---

## 4. Arquitetura

### 4.1 Visão Geral

```
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

### 4.2 O Cliente Bio-Emergente

**Novo componente (v2.2).** Mantém estado local sincronizado com servidor.

```python
class ClienteBio:
    def __init__(self, dim=256):
        self.estado = Estado(dim)      # P_c(t)
        self.contador = 0
    
    def enviar(self, mensagem: str) -> bytes:
        # Deriva máscara do estado atual + contador
        seed = self._derivar_semente() ^ self.contador
        mask = self._gerar_mascara(seed, len(mensagem))
        
        # Ofusca
        msg_bytes = mensagem.encode()
        ciphertext = bytes(a ^ b for a, b in zip(msg_bytes, mask))
        
        # Contador em claro + payload ofuscado
        return self.contador.to_bytes(8, 'big') + ciphertext
    
    def receber(self, resposta: dict):
        if resposta['aceito']:
            # Sincroniza estado com projeção do servidor
            proj = np.array(resposta['projecao'])
            self.estado.evoluir(proj, alpha=0.1)
            self.contador += 1
```

**Propriedades:**
- Estado local nunca é transmitido.
- Máscara é função determinística de P(t) + contador.
- Após cada mensagem aceita, estado evolui em ambos os lados.

### 4.3 O Servidor Pai (Modificado)

```python
class Pai:
    # ... estado, metabolismo, encode, digest ...
    
    def processar_ciphertext(self, ciphertext: bytes) -> Tuple[bool, dict]:
        # Extrai contador
        contador = int.from_bytes(ciphertext[:8], 'big')
        payload = ciphertext[8:]
        
        # Deriva máscara com estado atual
        seed = self._derivar_semente() ^ contador
        mask = self._gerar_mascara(seed, len(payload))
        
        # Recupera plaintext
        plaintext_bytes = bytes(a ^ b for a, b in zip(payload, mask))
        mensagem = plaintext_bytes.decode()
        
        # Validação metabólica
        vetor_msg = self.encode(mensagem)
        aceito, sim = self.digest(vetor_msg)
        
        if aceito:
            return True, {
                'status': 'OK',
                'projecao': self.estado.vetor.tolist(),
                'similaridade': sim
            }
        return False, {'status': 'NACK'}
```

### 4.4 Os Filhos (Inalterados)

Filhos permanecem como threads locais do Pai. Processam mensagens já decodificadas. Não interagem diretamente com ofuscação — camada é transparente.

### 4.5 Sincronização de Estado

**Premissa crítica:** Cliente e servidor devem manter P(t) idênticos.

**Mecanismo:**
1. Bootstrap inicial: ambos partem do mesmo vetor aleatório (transmitido uma única vez por canal autenticado).
2. Cada troca validada: servidor envia projeção do novo P(t). Cliente aplica mesma evolução.
3. Decaimento: ambos aplicam mesma função temporal f(Δt) = e^(-λ·Δt).

**Recuperação de dessincronia:**
- Cliente detecta falha consecutiva de validação (NACK persistente).
- Cliente solicita ressincronização enviando vetor nulo.
- Servidor responde com P(t) atual (apenas se canal for considerado seguro neste momento).
- Alternativa: cliente simplesmente renasce (novo P aleatório) e reinicia handshake.

### 4.6 Rede de Confiança Transitiva

Múltiplos servidores Pai podem formar rede. Cliente que transita entre nós carrega estado P(t) como credencial viva.

```
[Alice] ◄── P_a(t) ──► [Cliente] ◄── P_a(t) ──► [Bob]
                              │
                    Estado do cliente é
                    prova de história com Alice
```

Bob valida cliente sem conhecer Alice porque o estado P(t) do cliente ressoa com projeção esperada para alguém que passou por Alice.

---

## 5. Ciclo de Vida

```
EMERGÊNCIA → APROVAÇÃO → PERSISTÊNCIA → DUPLICAÇÃO → MORTE → RENASCIMENTO
```

**Sincronização do ciclo:**
- Cliente e servidor nascem com mesmo P(0).
- Evoluem juntos a cada troca validada.
- Decaem juntos na inatividade.
- Morrem juntos quando W_c < ε.
- Renascem com nova identidade (requer novo bootstrap).

---

## 6. Propriedades de Segurança

### 6.1 Sem Superfície de Ataque Clássica

Não há chave para extrair. Não há cifra para analisar. Não há protocolo de handshake. Estado P(t) existe apenas em RAM.

### 6.2 Resistência Quântica por Categoria

Nenhum algoritmo quântico endereça história vivida. A ofuscação usa XOR com máscara derivada de estado — sem problema matemático subjacente.

### 6.3 Confidencialidade sem Canal Seguro

| Cenário | v2.1 (plaintext sobre VPN) | v2.2 (ofuscação emergente) |
|---|---|---|
| Observador passivo | Vê comandos em claro | Vê bytes aleatórios |
| Análise de tráfego | Revela padrões de comando | Padrões ofuscados por estado evolutivo |
| Injecão de ciphertext | Impossível sem P(t) | Impossível sem P(t) + contador |
| Replay attack | P(t) evoluiu → falha | P(t) evoluiu + contador → falha |

### 6.4 Forward Secrecy Implícito

Cada mensagem usa máscara derivada de P(t) atual. Estado passado não recupera mensagens futuras. Morte do sistema apaga todo histórico.

### 6.5 Endurecimento com o Tempo

Convencional: exposição prolongada → mais dados para criptoanálise.

Bio-Emergente: cada troca validada aumenta distância do estado inicial. Tempo trabalha a favor.

### 6.6 Análise de Vetores de Ataque

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

## 7. Propriedade Fractal

A mesma lei opera em todas as escalas:

```
W_c(t) = ‖P(t)‖ · f_local · charge_factor(t)
```

**No micro** — par cliente-servidor: cada troca valida e ofusca.

**No macro** — rede de servidores: cada nó persiste enquanto ressoa com outros.

**No meta** — o protocolo: persiste enquanto há pares ativos.

---

## 8. Implementação de Referência (v2.2)

### 8.1 Núcleo Compartilhado

```python
import numpy as np
import time
from threading import Lock
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Estado:
    """Vetor de persistência e operações atômicas."""
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
    
    def derivar_semente(self) -> int:
        with self.lock:
            return int(np.dot(self.vetor, self.vetor[::-1]) * 1e6)

class Metabolismo:
    """Gerencia taxa de trocas e decaimento temporal."""
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
```

### 8.2 Servidor Pai

```python
class Pai:
    """Servidor soberano. Mantém estado mestre e valida mensagens."""
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
        self._p_hash = self.estado.derivar_semente()
    
    def _gerar_mascara(self, seed: int, tamanho: int) -> bytes:
        rng = np.random.default_rng(seed)
        return rng.bytes(tamanho)
    
    def encode(self, mensagem: str) -> np.ndarray:
        seed = hash(mensagem) ^ self._p_hash
        rng = np.random.default_rng(seed)
        vetor = rng.uniform(-1, 1, self.dim)
        return vetor / np.linalg.norm(vetor)
    
    def digest(self, vetor_msg: np.ndarray) -> Tuple[bool, float]:
        fator = self.metabolismo.fator_decaimento()
        if fator < 1.0:
            self.estado.decair(fator)
            self._atualizar_hash()
        
        sim = self.estado.similaridade(vetor_msg)
        if sim > self.theta:
            self.estado.evoluir(vetor_msg, self.alpha)
            self.metabolismo.registrar()
            self._atualizar_hash()
            
            if self.metabolismo.carga() * np.linalg.norm(self.estado.vetor) < self.epsilon:
                self.renascer()
            
            return True, sim
        return False, sim
    
    def processar_ciphertext(self, ciphertext: bytes) -> Tuple[bool, dict]:
        if len(ciphertext) < 8:
            return False, {'status': 'ERROR', 'motivo': 'payload muito curto'}
        
        contador = int.from_bytes(ciphertext[:8], 'big')
        payload = ciphertext[8:]
        
        seed = self._p_hash ^ contador
        mask = self._gerar_mascara(seed, len(payload))
        
        plaintext_bytes = bytes(a ^ b for a, b in zip(payload, mask))
        
        try:
            mensagem = plaintext_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return False, {'status': 'NACK', 'motivo': 'decode falhou'}
        
        vetor_msg = self.encode(mensagem)
        aceito, sim = self.digest(vetor_msg)
        
        if aceito:
            return True, {
                'status': 'OK',
                'projecao': self.estado.vetor.tolist(),
                'similaridade': sim
            }
        return False, {'status': 'NACK', 'similaridade': sim}
    
    def renascer(self):
        self.estado = Estado(self.dim)
        self.metabolismo = Metabolismo(self.metabolismo.janela, self.metabolismo.lambda_decay)
        self._atualizar_hash()
```

### 8.3 Cliente Bio-Emergente

```python
class ClienteBio:
    """Cliente com estado sincronizado e ofuscação emergente."""
    def __init__(self, dim: int, alpha: float = 0.1):
        self.dim = dim
        self.alpha = alpha
        self.estado = Estado(dim)
        self.contador = 0
    
    def _derivar_semente(self) -> int:
        return self.estado.derivar_semente()
    
    def _gerar_mascara(self, seed: int, tamanho: int) -> bytes:
        rng = np.random.default_rng(seed)
        return rng.bytes(tamanho)
    
    def enviar(self, mensagem: str) -> bytes:
        seed = self._derivar_semente() ^ self.contador
        mask = self._gerar_mascara(seed, len(mensagem.encode()))
        
        msg_bytes = mensagem.encode()
        ciphertext = bytes(a ^ b for a, b in zip(msg_bytes, mask))
        
        return self.contador.to_bytes(8, 'big') + ciphertext
    
    def receber(self, resposta: dict) -> bool:
        if resposta.get('status') == 'OK':
            proj = np.array(resposta['projecao'])
            self.estado.evoluir(proj, self.alpha)
            self.contador += 1
            return True
        return False
    
    def inicializar(self, vetor_inicial: np.ndarray):
        """Bootstrap: recebe P(0) do servidor por canal autenticado."""
        self.estado.vetor = vetor_inicial.copy()
        self.estado.vetor /= np.linalg.norm(self.estado.vetor)
        self.contador = 0
```

### 8.4 Filho (Inalterado)

```python
class Filho:
    """Thread local do Pai. Processa mensagens já decodificadas."""
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
```

### 8.5 Exemplo de Uso

```python
# Bootstrap inicial (canal autenticado único)
dim = 256
servidor = Pai(dim=dim)
cliente = ClienteBio(dim=dim)
cliente.inicializar(servidor.estado.vetor.copy())

# Comunicação normal (canal aberto)
mensagem = "TRANSFERIR 1M BTC"
ciphertext = cliente.enviar(mensagem)

# Servidor processa
aceito, resposta = servidor.processar_ciphertext(ciphertext)

# Cliente sincroniza
if aceito:
    cliente.receber(resposta)
    print(f"Comando executado. Similaridade: {resposta['similaridade']:.4f}")
else:
    print(f"Comando rejeitado.")
```

---

## 9. Comparação Entre Versões

| Característica | v2.0 (Conceito) | v2.1 (Implementação) | v2.2 (Ofuscação Emergente) |
|---|---|---|---|
| Canal seguro externo | Requer VPN/SSH | Requer VPN/SSH | **Desnecessário** |
| Estado no cliente | Inexistente | Inexistente | **Sincronizado** |
| Confidencialidade | Nenhuma | Nenhuma | **Ofuscação por estado** |
| Observação passiva | Vê comandos | Vê comandos | **Vê ruído** |
| Replay protec
