# EmergingBioCryptography / CRIPTOGRAFIA BIO-EMERGENTE

### Segurança como Propriedade de História Compartilhada Irreversível

**Thiago Maciel — 2025 — v2.2.1**

---

**Repositório:** https://github.com/ThiagoSilm/EmergingBioCryptography

---

## Abstract

Paradigma criptográfico distinto. Segurança opera sobre história compartilhada irreversível. Agentes coevoluem por trocas validadas desenvolvendo universo semântico exclusivo. Imune a ataques clássicos: ausência de chave estática. Imune a ataques quânticos: ausência de problema matemático endereçável. Segurança emerge, persiste, endurece com tempo de uso.

v2.2.1: Correções de segurança. HMAC-SHA256 para autenticação. Contador incrementa em `cifrar()` (nonce reuse corrigido). `hashlib.sha256` substitui `hash()` (determinismo entre processos). `derivar_semente()` usa SHA-256 sobre `vetor.tobytes()` (entropia 256 bits).

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

Sistema opera em dois modos integrados:
1. Validação metabólica: comandos só têm efeito se ressoam com P(t).
2. Ofuscação emergente: mensagens mascaradas por estado compartilhado + HMAC.

---

## 3. Formalização

### 3.1 Estado do Sistema

P(t) ∈ ℝⁿ | ‖P(t)‖ = 1. Cliente e servidor sincronizados.

### 3.2 Lei de Dominância

W_c(t) = ‖P(t)‖ · f_local · charge_factor(t)

### 3.3 Decaimento Natural

P(t + Δt) = P(t) · e^(−λ · Δt)

### 3.4 Evolução por Digestão

P(t+1) = normalize((1 − α) · P(t) + α · P_msg_validada)

### 3.5 Ressonância como Validação Binária

similarity = P · Q ∈ [−1, 1]. válido ⇔ similarity > θ.

### 3.6 Ofuscação Autenticada

mask = SHA-256(P(t) ‖ contador)
ciphertext = plaintext XOR mask
MAC = HMAC-SHA256(P(t), ciphertext)
formato = contador(8) ‖ ciphertext ‖ MAC(32)

### 3.7 GC Emergente

W_c(t) < ε → renascer()

---

## 4. Arquitetura

```text
┌──────────────────────────────────────────────────────────────────┐
│  Cliente Bio-Emergente               Servidor Pai                │
│  ┌──────────────┐                    ┌──────────────┐            │
│  │ Estado P_c(t)│◄──── sinc ────────►│ Estado P_s(t)│            │
│  └──────────────┘                    └──────────────┘            │
│         │                                   │                     │
│         ▼                                   ▼                     │
│  plaintext ──► mask ──► ciphertext+MAC ──► valida MAC            │
│                                              │                    │
│                                              ▼                    │
│                                        mask ──► plaintext        │
│                                              │                    │
│                                              ▼                    │
│                                         validação                │
│                                         metabólica               │
│                                              │                    │
│                                              ▼                    │
│  P_c(t+1) ◄────────── projeção ──────── P_s(t+1)                │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Bootstrap Inicial

Primeira sincronização requer canal autenticado (QR code, VPN temporária). Após bootstrap, canal pode ser aberto.

### 4.3 Sincronização de Estado

Bootstrap: P(0) idêntico. Cada troca validada: ambos evoluem. Decaimento simétrico.

---

## 5. Ciclo de Vida

EMERGÊNCIA → APROVAÇÃO → PERSISTÊNCIA → DUPLICAÇÃO → MORTE → RENASCIMENTO

---

## 6. Propriedade Fractal

W_c(t) = ‖P(t)‖ · f_local · charge_factor(t)

Micro: par cliente-servidor. Macro: rede de servidores. Meta: protocolo.

---

## 7. Propriedades de Segurança

### 7.1 Sem Superfície de Ataque Clássica

Sem chave estática. Sem handshake. P(t) apenas em RAM.

### 7.2 Resistência Quântica por Categoria

Sem problema matemático subjacente. HMAC e SHA-256 usados como KDF, não como primitiva de segurança pública.

### 7.3 Confidencialidade e Autenticação

| Cenário | v2.2.0 | v2.2.1 |
|---|---|---|
| Nonce reuse | Vulnerável | Corrigido |
| Bit-flipping | Possível | Detectado (HMAC) |
| Hash determinístico | `hash()` não criptográfico | SHA-256 |
| Entropia de seed | ~40 bits | 256 bits |

### 7.4 Forward Secrecy Implícito

Cada mensagem usa máscara de P(t) atual. Morte apaga histórico.

### 7.5 Análise de Vetores de Ataque

| Vetor | Resultado |
|---|---|
| Interceptar tráfego | Bytes aleatórios + MAC. Sem P(t): irrecuperável. |
| Replay | Contador + MAC. Inválido. |
| Forjar ciphertext | Requer P(t) para máscara e HMAC. |
| Quântico | Sem algoritmo aplicável. |
| Texto conhecido | Recupera máscara daquela mensagem. Não recupera P(t). |

---

## 8. API

```python
import bioemergent as be

servidor, cliente = be.gerar_par(dim=256)
ciphertext = be.cifrar(cliente, "TRANSFERIR 1M BTC")
plaintext, valido = be.decifrar(servidor, ciphertext)
```

---

## 9. Instalação

```bash
curl -O https://raw.githubusercontent.com/ThiagoSilm/EmergingBioCryptography/main/bioemergent.py
pip install numpy
```

---

## 10. Comparação Entre Versões

| Característica | v2.2.0 | v2.2.1 |
|---|---|---|
| Nonce reuse | Vulnerável | Corrigido |
| Autenticação | Ausente | HMAC-SHA256 |
| Hash | `hash()` | SHA-256 |
| Entropia seed | ~40 bits | 256 bits |
| Formato | contador + ciphertext | contador + ciphertext + MAC |

---

## 11. Limitações Conhecidas

Bootstrap inicial requer canal autenticado. Comprometimento do cliente dá janela de oportunidade. Exportar() serializa estado em plaintext (uso local).

---

## 12. Licença

MIT

---

*Thiago Maciel — 2025 — v2.2.1*
