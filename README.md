# EmergingBioCryptography / CRIPTOGRAFIA BIO-EMERGENTE

### Segurança como Propriedade de História Compartilhada Irreversível

**Thiago Maciel — 2026 — v2.4.0**

---

**Repositório:** https://github.com/ThiagoSilm/EmergingBioCryptography

---

## Abstract

Paradigma criptográfico distinto. Segurança opera sobre história compartilhada irreversível. Agentes coevoluem por trocas validadas desenvolvendo universo semântico exclusivo. Imune a ataques clássicos: ausência de chave estática. Imune a ataques quânticos: ausência de problema matemático endereçável. Segurança emerge, persiste, endurece com tempo de uso. v2.4.0 introduz ofuscação de tráfego: padding determinístico-aleatório, timing jitter, e REBIRTH_SIGNAL autenticado e camuflado.

---

## 1. O Problema com Criptografia Estática

Toda criptografia existente — de cifras de substituição a lattices pós-quânticos — opera sobre complexidade computacional. Segredo existe como objeto estático protegido por dificuldade matemática.

RSA e ECC colapsam ante Shor. Lattices resistem porque Learning With Errors não possui algoritmo quântico conhecido — mas primitiva é a mesma: objeto matemático protegido por dificuldade.

Problema não é matemática. É paradigma. Qualquer sistema onde segredo pode ser representado como dado estático possui superfície de ataque explorável.

Criptografia Bio-Emergente abandona essa corrida. Ocupa outro espaço.

---

## 2. Primitiva Nova

**Segurança como propriedade de história compartilhada irreversível.**

Não há chave estática. Há processo que não pode ser replicado sem ter sido vivido.

Dois agentes que coevoluem por trocas validadas constroem estado interno mutuamente dependente — linguagem emergente que só existe para quem participou da criação. Adversário externo não encontra parede matemática. Encontra idioma que não existe em dicionário.

Sistema opera em três camadas integradas:
1. **Validação criptográfica:** HMAC-SHA256 + contador monotônico como gate de aceitação.
2. **Evolução de estado:** Vetor de alta dimensionalidade evolui com cada mensagem aceita.
3. **Ofuscação de tráfego:** Padding determinístico-aleatório, tamanho de pacote constante, timing jitter.

---

## 3. Formalização

### 3.1 Estado do Sistema

P(t) ∈ ℝⁿ | ‖P(t)‖ = 1. Cliente e servidor sincronizados. n = 256 por padrão.

### 3.2 Lei de Vitalidade

V(t) = carga(t) · ‖P(t)‖

`carga(t)` = número de trocas na janela temporal ÷ janela.

### 3.3 Decaimento por Mensagem

fator = e^(−λ · contador_trocas)

P_new = normalize(P · fator)

Decaimento baseado no contador de mensagens trocadas, não no relógio local. Elimina dependência de sincronização temporal entre nós.

### 3.4 Evolução por Digestão

P(t+1) = normalize((1 − α) · P(t) + α · P_msg)

Onde P_msg = encode(mensagem, P(t)) — vetor unitário derivado deterministicamente do conteúdo da mensagem e do estado atual.

### 3.5 Ressonância como Métrica Observacional

similarity = P · Q ∈ [−1, 1]

Ressonância é métrica de monitoramento, não gate de aceitação. Em R²⁵⁶, E[cos_sim] ≈ 0, P(sim > 0.8) ≈ 0. Gate real é HMAC + contador.

### 3.6 Criptografia Autenticada

```
seed     = SHA-256(P_hash ‖ contador)
mask     = SHA-256(seed + 0) ‖ SHA-256(seed + 1) ‖ ...
cipher   = plaintext XOR mask[:len(plaintext)]
MAC      = HMAC-SHA-256(P_hash, cipher ‖ contador)
```

### 3.7 Ofuscação de Pacote

```
payload  = contador(8 bytes) ‖ ciphertext ‖ MAC(32 bytes)
padding  = PRNG(seed = SHA-256(P_hash ‖ contador ‖ "pad"))
pacote   = payload ‖ padding  → tamanho constante (512 bytes padrão)
```

Todos os pacotes têm tamanho idêntico. Padding é deterministicamente aleatório — derivado do estado, reproduzível pelo receptor, indistinguível de ruído para observador externo.

### 3.8 Timing Jitter

Antes de cada `cifrar()`, delay aleatório entre 0 e `jitter_max` segundos. Inibe análise de tempo entre mensagens.

### 3.9 REBIRTH_SIGNAL Autenticado

```
REBIRTH_SIGNAL = HMAC-SHA-256(P_hash, constante_rebirth)
```

Sinal de renascimento é ofuscado como pacote comum (ctr=0, payload=vazio, MAC=REBIRTH_SIGNAL) com padding até tamanho constante. Indistinguível de mensagem normal. Apenas portador do P_hash atual pode gerar ou verificar.

### 3.10 Colapso e Renascimento

V(t) < ε → `renascer()`. Emite REBIRTH_SIGNAL autenticado. Ambos lados reiniciam vetor com entropia fresca, preservando parâmetros estruturais (dimensão, α, λ, pacote_tamanho, jitter_max).

Se vetor colapsa para norma zero (decaimento extremo ou erro numérico), `DessincronizacaoCritica` é lançada. Não há reset unilateral — renascimento deve ser coordenado.

---

## 4. Arquitetura

```
┌──────────────────────────────────────────────────────────────────┐
│  Cliente Bio-Emergente               Servidor Pai                │
│  ┌──────────────┐                    ┌──────────────┐            │
│  │ Estado P_c(t)│◄──── sinc ────────►│ Estado P_s(t)│            │
│  └──────────────┘                    └──────────────┘            │
│         │                                   │                     │
│         ▼                                   ▼                     │
│  plaintext ──► mask ──► cipher+MAC ──► valida MAC                │
│         │                                   │                     │
│         ▼                                   ▼                     │
│  + padding ──► pacote 512B ──► extrai ciphertext                 │
│  + jitter                             + verifica ctr             │
│                                            │                      │
│                                            ▼                      │
│                                       mask ──► plaintext         │
│                                            │                      │
│                                            ▼                      │
│                                       ressonância                 │
│                                       (métrica)                  │
│                                            │                      │
│                                            ▼                      │
│  P_c(t+1) ◄────────── evolução ────── P_s(t+1)                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.1 Formato do Pacote (v2.4.0)

```
┌────────────┬──────────────────┬──────────────────┬──────────────────┐
│ contador   │ ciphertext       │ MAC              │ padding          │
│ 8 bytes    │ variável         │ 32 bytes         │ até pacote_tam   │
└────────────┴──────────────────┴──────────────────┴──────────────────┘
```

Tamanho total: `pacote_tamanho` bytes (padrão: 512).

### 4.2 Bootstrap Inicial

`gerar_par()` copia vetor inicial e verifica integridade via HMAC. Primeira sincronização requer canal autenticado (QR code, VPN temporária, encontro físico). Após bootstrap, canal pode ser público.

### 4.3 Sincronização de Estado

Bootstrap: P(0) idêntico. Cada troca com HMAC válido e contador correto: ambos evoluem com mesma mensagem. Decaimento simétrico baseado em contador de trocas.

---

## 5. Ciclo de Vida

EMERGÊNCIA → VALIDAÇÃO → PERSISTÊNCIA → DECAIMENTO → COLAPSO → RENASCIMENTO

---

## 6. Propriedade Fractal

V(t) = carga(t) · ‖P(t)‖

Micro: par cliente-servidor. Macro: rede de servidores. Meta: protocolo.

---

## 7. Propriedades de Segurança

### 7.1 Sem Superfície de Ataque Clássica

Sem chave estática. Sem handshake. P(t) apenas em RAM. Nada para roubar de disco ou memória persistente.

### 7.2 Resistência Quântica por Categoria

Sem problema matemático subjacente (fatoração, logaritmo discreto, lattices, códigos). HMAC e SHA-256 usados apenas como KDF e autenticador — resistentes a Grover (2^128 segurança).

### 7.3 Confidencialidade, Integridade e Autenticação

| Propriedade | Mecanismo |
|---|---|
| Confidencialidade | XOR com máscara derivada de P_hash + contador |
| Integridade | HMAC-SHA256 sobre ciphertext + contador |
| Autenticação | HMAC verificado com P_hash compartilhado |
| Anti-replay | Contador monotônico; mensagens fora de ordem rejeitadas |
| Anti-análise | Padding constante, timing jitter, REBIRTH_SIGNAL camuflado |

### 7.4 Forward Secrecy Implícito

Cada evolução sobrescreve P(t). Operação não é bijetiva — múltiplos pares (P_anterior, msg) produzem mesmo P_novo. Atacante com P_atual não pode reconstruir P_anterior unicamente. Mensagens passadas são information-theoretic irrecuperáveis.

### 7.5 Invisibilidade de Tráfego

Pacotes têm tamanho constante (512 bytes). Padding é deterministicamente aleatório — indistinguível de ruído. REBIRTH_SIGNAL é pacote comum (ctr=0, ciphertext=vazio). Observador externo vê fluxo uniforme de bytes aleatórios sem estrutura discernível.

### 7.6 Análise de Vetores de Ataque

| Vetor | Resultado |
|---|---|
| Interceptar tráfego | Pacotes de tamanho fixo com padding. Sem estrutura visível. |
| Replay | Contador monotônico. Mensagem repetida tem ctr incorreto → rejeitada. |
| Forjar ciphertext | Requer P_hash para máscara e HMAC. |
| Forjar REBIRTH_SIGNAL | Requer P_hash para HMAC. Sem P_hash, sinal rejeitado. |
| Análise de tempo | Jitter aleatório mascara padrões de cadência. |
| Análise de tamanho | Todos os pacotes têm tamanho constante. |
| Quântico (Shor) | Sem estrutura de grupo cíclico para atacar. |
| Quântico (Grover) | SHA-256 mantém 2^128 segurança. |
| Texto conhecido | Recupera máscara daquela mensagem específica. Não recupera P_hash nem P(t). |
| Ataque de dicionário | P(t) ∈ ℝ²⁵⁶ contínuo. Espaço de busca não enumerável. |

---

## 8. API

```python
import bioemergent as be

# Geração de par sincronizado com parâmetros de ofuscação
servidor, cliente = be.gerar_par(
    dim=256,
    theta=0.8,
    pacote_tamanho=512,   # todos os pacotes têm 512 bytes
    jitter_max=0.05       # até 50ms de delay aleatório
)

# Cifrar (adiciona padding + aplica jitter)
ciphertext = be.cifrar(cliente, "TRANSFERIR 1M BTC")

# Decifrar (remove padding, verifica HMAC e contador)
plaintext, valido = be.decifrar(servidor, ciphertext)

# Renascimento coordenado
sinal = be.renovar(cliente)              # gera REBIRTH_SIGNAL ofuscado
be.decifrar(servidor, sinal)             # receptor detecta e renasce

# Exportar/Importar estado
dados = be.exportar(servidor)
novo_servidor = be.importar_estado(dados, modo="servidor")

# Estatísticas
stats = servidor.estatisticas()
# {'versao': '2.4.0', 'cifradas': 42, 'validadas': 42, 'rejeitadas': 0,
#  'carga': 5.0, 'vitalidade': 5.0, 'ressonancia': 0.73,
#  'pacote_tamanho': 512, 'jitter_max': 0.05}
```

---

## 9. Instalação

```bash
pip install numpy
curl -O https://raw.githubusercontent.com/ThiagoSilm/EmergingBioCryptography/main/bioemergent.py
```

Dependência única: `numpy`.

---

## 10. Histórico de Versões

| Versão | Data | Mudanças |
|---|---|---|
| 2.2.0 | 2026 | Versão inicial pública. |
| 2.2.1 | 2026 | HMAC-SHA256. Contador em `cifrar()`. SHA-256 determinístico. Entropia 256 bits. |
| 2.3.0 | 2026 | Ressonância rebaixada a métrica. Gate real: HMAC + ctr. |
| 2.3.1 | 2026 | REBIRTH_SIGNAL autenticado. Decaimento por contador. Verificação de cópia inicial. Overflow de contador com wrapar. Colapso de vetor gera exceção. Importar valida vetor. |
| 2.4.0 | 2026 | Ofuscação de tráfego: padding determinístico-aleatório, tamanho de pacote configurável, timing jitter. REBIRTH_SIGNAL camuflado como pacote comum. |

---

## 11. Breaking Changes

| De | Para | Mudança |
|---|---|---|
| 2.2.x | 2.3.x | Formato do pacote: adicionado MAC (8 bytes adicionais). `decifrar` retorna `Tuple[Optional[str], bool]`. |
| 2.3.0 | 2.3.1 | `renovar()` retorna HMAC autenticado, não constante nua. `exportar()` inclui `ctr_esperado`. |
| 2.3.x | 2.4.0 | `exportar()` inclui `pacote_tamanho` (4 bytes) e `jitter_max` (8 bytes). Formato de pacote inclui padding. `gerar_par()` aceita `pacote_tamanho` e `jitter_max`. `__init__()` requer `pacote_tamanho` e `jitter_max`. |

---

## 12. Limitações Conhecidas

1. **Bootstrap inicial:** Requer canal autenticado para primeira cópia do vetor. Não resolve distribuição de chaves — é protocolo de manutenção de sessão, não de estabelecimento.
2. **Sem tolerância a perda de pacotes:** Contador monotônico estrito. Pacote perdido = canal travado até renascimento.
3. **Comprometimento do cliente:** Acesso à RAM do cliente expõe P(t) atual. Mensagens futuras (não passadas) são decifráveis até próxima evolução.
4. **Exportar estado:** Serializa P(t) em plaintext. Uso apenas local seguro. Não é substituto para acordo de chaves.
5. **Sem prova formal de não-invertibilidade:** Forward secrecy é empírica (renormalização destrói informação). Prova matemática pendente.
6. **Dependência de numpy:** Float64, operações de norma, RNG determinístico. Portabilidade para hardware restrito requer reimplementação.

---

## 13. Licença

MIT

---

*Thiago Maciel — 2026 — v2.4.0*
