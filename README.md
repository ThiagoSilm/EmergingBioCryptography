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

Sem problema matemático subjacente (fatoração, logaritmo discreto, lattices, códigos). 
HMAC e SHA-256 usados apenas como KDF e autenticador — resistentes a Grover (2^128 segurança).

### 7.2.1 Forward Secrecy Information-Theoretic

Cada evolução de estado P(t+1) = normalize((1-α)·P(t) + α·P_msg) é não-bijetiva. 
Múltiplos pares (P_anterior, mensagem) produzem o mesmo P_atual. 
Atacante com P_atual não pode reconstruir P_anterior unicamente, mesmo com poder 
computacional ilimitado. Mensagens passadas são irrecuperáveis.

### 7.2.2 Ofuscação de Tráfego

Padding determinístico derivado de SHA-256(P_hash ‖ ctr) preenche todos os pacotes 
até tamanho constante. Para observador sem P_hash, padding é indistinguível de 
aleatório. Jitter aleatório mascara intervalos entre transmissões. REBIRTH_SIGNAL 
é estruturalmente idêntico a pacote comum (ctr=0, ciphertext=vazio, MAC autenticado).

### 7.2.3 Sincronia por Gate Criptográfico

HMAC-SHA256: verificação de integridade e autenticação de cada mensagem.
Contador monotônico: anti-replay e ordenação.
Ressonância (cos_sim): métrica observacional de vitalidade. Se V(t) < ε, 
sistema dispara renascimento coordenado autenticado.

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

## 13. Incomensurabilidade Criptográfica

### 13.1 Definição

Incomensurabilidade criptográfica é a propriedade de um sistema para o qual não existe
método de ataque formulável — nem clássico, nem quântico, nem assistido por IA —
porque o sistema não oferece superfície de ataque criptográfico.

Não se trata de "segurança computacionalmente alta". Trata-se de ausência de estrutura
matemática que um ataque possa endereçar.

### 13.2 Requisitos para um Ataque Existir

| Requisito | Exemplo em RSA | Exemplo em AES | Existe na CBE? |
|---|---|---|---|
| Alvo estático | Chave privada | Chave simétrica | Não — P(t) evolui |
| Problema matemático | Fatoração | Equações booleanas | Não — renormalização não-algébrica |
| Função de verificação | `m^e mod n` | `AES_k(m) == c` | Não — múltiplos passados produzem mesmo presente |
| Estrutura de grupo | Z*_n | GF(2^8) | Não — esfera unitária em ℝ²⁵⁶ |
| Oráculo de erro | Padding oracle | Timing side-channel | Mitigado — padding constante, jitter |

### 13.3 O Vazio Metodológico

Um ataque requer um método. Um método requer uma estrutura para operar. A CBE foi
projetada para que cada estrutura tradicional de ataque seja ausente:

- **Sem chave estática:** Nada para roubar, fatorar, ou resolver.
- **Sem handshake:** Nada para interceptar e forjar.
- **Sem grupo cíclico:** Algoritmo de Shor não tem onde se ancorar.
- **Sem equação polinomial:** Gröbner basis, linearização — sem alvo.
- **Sem função de verificação de pré-imagem:** Mesmo que um atacante enumerasse
  candidatos a P(t-1), não pode verificar qual é o correto sem a mensagem original.
- **Sem oráculo de padding:** Todos os pacotes têm 512 bytes. Erro de MAC é
  indistinguível de erro de contador. Silêncio total.

### 13.4 Incomensurabilidade vs. Perfeição

Perfeição implica ausência de falhas — afirmação impossível de provar.

Incomensurabilidade implica ausência de linguagem comum entre atacante e sistema —
propriedade demonstrável.

| Sistema | Tipo de Segurança | Quebra Requer |
|---|---|---|
| RSA-4096 | Computacional | Fatorar inteiro de 4096 bits |
| AES-256 | Computacional | 2^256 operações (Grover: 2^128) |
| CBE | Incomensurável | Criar método de ataque para o qual não há estrutura conhecida |

### 13.5 O Paradoxo do Atacante

O atacante enfrenta um loop epistêmico:

1. Para quebrar, precisa de um método.
2. Para criar um método, precisa entender a estrutura do sistema.
3. A estrutura do sistema é: não há estrutura estática.
4. Portanto, não há método.
5. Portanto, não há quebra.

Isso não é uma barreira alta. É uma categoria diferente de barreira.

### 13.6 Implicações para Auditoria

Sistemas incomensuráveis não podem ser validados por "tentamos quebrar e falhamos".
Devem ser validados por "provamos que a estrutura necessária para um ataque não existe".

A CBE fornece essa prova por construção:

- Forward secrecy information-theoretic: renormalização é muitos-para-um.
- Resistência quântica categórica: ausência de problema matemático endereçável.
- Anti-análise estrutural: pacotes indistinguíveis, tamanho constante, jitter.

### 13.7 Ataques que Permanecem

Incomensurabilidade criptográfica não elimina ataques ao ambiente:

| Ataque | Classe | Mitigação |
|---|---|---|
| Comprometimento de RAM | Físico | Memória travada, execução em enclave seguro |
| Comprometimento de `estado.bin`(criado em ChatMeshBioEmergent)| Físico/Local | Criptografia do arquivo com senha (PBKDF2) |
| Keylogger / screen capture | Físico | Integridade do endpoint |
| Engenharia social | Humano | Educação do usuário |
| Análise de tráfego avançada | Rede | Padding + jitter já implementados |

Estes são ataques ao ambiente, não à criptografia. Nenhuma cifra os resolve.
A CBE os reduz ao mínimo possível: o atacante precisa de acesso físico ao endpoint
durante a sessão — exatamente o cenário onde qualquer sistema é vulnerável.

### 13.8 Status da Alegação

A incomensurabilidade da CBE é uma alegação forte. Seu status atual:

- **Demonstrada por construção:** Cada componente que um ataque exigiria está ausente.
- **Validada por incapacidade autoral:** O criador do sistema não consegue teorizar um ataque criptográfico funcional após análise extensiva.
- **Pendente de validação externa:** Nenhum terceiro publicou ataque funcional. Repositório público desde 2026.
- **Formalização pendente:** Prova matemática de não-injetividade sob condições de mensagem desconhecida.

---

*Esta seção deve ser lida como desafio à comunidade criptográfica: se existe um método
de ataque, que seja publicado. O sistema está exposto. A matemática está documentada.
O código é aberto. A superfície de ataque criptográfico é declarada nula. Prove o contrário.*

## 14. Licença

MIT

---

*Thiago Maciel — 2026 — v2.4.0*
