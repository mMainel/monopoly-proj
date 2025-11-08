# Ingração com o front

E.T

Pra ajudar na integração de vcs, backend->front

---

## Inicialização do Jogo

Criar uma instância do jogo e configurar jogadores (humanos e IA)

```python
from modules.jogo import Jogo
from modules.peca import Peca

jogo = Jogo()

# Configurar jogadores: lista de tuplas (nome, peca)
jogadores_config = [
    ("Alice", Peca.BIOLOGIA),
    ("Bob", Peca.COMPUTACAO),
    ("IA", Peca.MEDICINA)  # IA detectada pelo nome "IA"
]

jogo.iniciar_jogo(jogadores_config)
```

---

## Sistema de Eventos (Observer)

Registrar observadores para receber notificações de eventos do jogo

```python
from modules.observador import Observador
from modules.eventoJogo import TipoEvento

class InterfaceObservador(Observador):
    def notificar(self, evento):
        tipo = evento.getTipo()
        dados = evento.getDados()

        if tipo == TipoEvento.DADOS_LANCADOS:
            print(f"Dados: {dados['dados']}, Soma: {dados['soma']}")
        elif tipo == TipoEvento.PROPRIEDADE_COMPRADA:
            print(f"{dados['jogador'].nome} comprou {dados['propriedade'].nome}")
        # ... coloquem aq o que vcs acharem necessario

observador = InterfaceObservador()
jogo.adicionar_observador(observador)
```

**Eventos disponíveis:**
- `TURNO_INICIADO`, `TURNO_FINALIZADO`
- `DADOS_LANCADOS`, `DUPLA_LANCADA`
- `JOGADOR_MOVEU`, `PASSOU_INICIO`
- `PROPRIEDADE_COMPRADA`, `ALUGUEL_PAGO`
- `JOGADOR_PRESO`, `SAIU_CADEIA`
- `LEILAO_INICIADO`, `LEILAO_FINALIZADO`
- `CONSTRUCAO_FEITA`, `JOGADOR_FALIU`

---

## Fluxo de um Turno

Executar turno completo (lançar dados, mover, processar ação da casa)

```python
# Turno automático (dados + movimento + ação)
jogo.executar_turno()

# Avançar para próximo jogador
jogo.proximo_turno()

# Verificar vencedor
vencedor = jogo.verificar_vencedor()
if vencedor:
    print(f"Vencedor: {vencedor.nome}")
```

---

## Compra de Propriedades

Processar decisão de compra quando jogador cai em propriedade disponível

```python
# Método 1: Compra direta
jogador = jogo.jogadorAtual
propriedade = jogo.propriedade_disponivel_compra

sucesso = jogo.tratarCompraPropriedade(jogador, propriedade)

# Método 2: Com callback de decisão
def callback_decisao_compra(jogador, propriedade):
    if isinstance(jogador, JogadorIA):
        return jogador.decidir_comprar_propriedade(propriedade)
    else:
        # Perguntar ao jogador humano via interface
        return interface.perguntar_compra(propriedade)

jogo.solicitarDecisaoCompra(jogador, propriedade, callback_decisao_compra)
```

---

## Sistema de Leilão

Iniciar e gerenciar leilão quando propriedade não é comprada

```python
# Iniciar leilão
leilao = jogo.iniciarLeilao(propriedade)

# Fazer lance
jogador = jogo.jogadores[0]
valor_lance = 100
sucesso = leilao.fazerLance(jogador, valor_lance)

# Jogador desiste
leilao.desistir(jogador)

# Finalizar leilão
vencedor, valor_final = leilao.finalizarLeilao(jogo)
jogo.notificarLeilaoFinalizado(vencedor, valor_final)

# Verificar leilão ativo
leilao_ativo = jogo.getLeilaoAtivo()
```

---

## Construção de Casas e Hotéis

Construir ou vender casas/hotéis em propriedades com monopólio

```python
# Verificar monopólio
tem_monopolio = jogador.possuiMonopolio("Marrom")

# Construir casa
propriedade = jogador.getPropriedades()[0]
sucesso = jogo.construirCasa(propriedade, jogador)

# Construir hotel (requer 4 casas)
sucesso = jogo.construirHotel(propriedade, jogador)

# Vender casa
sucesso = jogo.venderCasa(propriedade, jogador)

# Vender hotel
sucesso = jogo.venderHotel(propriedade, jogador)

# Callback para escolher onde construir
def callback_construcao(jogador, propriedades_construiveis):
    if isinstance(jogador, JogadorIA):
        return jogador.escolher_propriedade_construir(propriedades_construiveis)
    else:
        return interface.escolher_propriedade(propriedades_construiveis)

jogo.solicitarDecisaoConstrucao(jogador, callback_construcao)
```

---

## Sistema de Cadeia

Gerenciar entrada, permanência e saída da cadeia

```python
# Enviar para cadeia
jogo.tratarCadeia(jogador)

# Verificar se está preso
esta_preso = jogador.estaEmCadeia()
turnos_preso = jogador.getTurnosCadeia()

# Opções de saída
opcao = "carta"  # ou "fianca" ou "dupla"
saiu = jogo.processarOpcoesCadeia(jogador, opcao)

# IA escolhe automaticamente
if isinstance(jogador, JogadorIA):
    opcao = jogador.escolher_opcao_cadeia()
    saiu = jogo.processarOpcoesCadeia(jogador, opcao)
```

---

## Gestão Financeira

Hipotecar, deshipotecar e gerenciar finanças

```python
# Hipotecar propriedade
valor_recebido = jogo.hipotecarPropriedade(propriedade, jogador)

# Deshipotecar propriedade
sucesso = jogo.deshipotecarPropriedade(propriedade, jogador)

# Verificar saldo
saldo = jogador.getSaldo()

# Verificar patrimônio total
patrimonio = jogador.calcularPatrimonio()

# Propriedades hipotecáveis
hipotecaveis = jogador.obterPropriedadesHipotecaveis()

# Propriedades com construções
com_construcoes = jogador.obterPropriedadesComConstrucoes()
```

---

## Sistema de Falência

Tratamento de falência com transferência de propriedades

```python
# Jogador declara falência
credor = outro_jogador  # ou None para banco
jogador.declararFalencia(credor)

# Verificar se está falido
esta_falido = jogador.verificarFalencia()

# Tentar levantar fundos antes de falir
valor_necessario = 500
conseguiu = jogador.tentarLevantarFundos(valor_necessario)
```

---

## Integração com IA

Usar métodos de decisão do JogadorIA.

```python
from modules.jogadorIA import JogadorIA

# Verificar se é IA
if isinstance(jogador, JogadorIA):
    # Decisões automáticas
    comprar = jogador.decidir_comprar_propriedade(propriedade)
    construir = jogador.decidir_construir_casa(propriedade)
    lance = jogador.decidir_dar_lance(propriedade, lance_atual)

    # Opções de cadeia
    opcao_cadeia = jogador.escolher_opcao_cadeia()

    # Escolher propriedade para construir
    props_disponiveis = [...]
    escolha = jogador.escolher_propriedade_construir(props_disponiveis)
```

---

## Consultar Estado do Jogo

Obter informações sobre o estado atual do jogo

```python
# Jogador atual
jogador_atual = jogo.jogadorAtual

# Turno atual
turno = jogo.turno

# Todos os jogadores
jogadores = jogo.jogadores

# Jogadores ativos (não falidos)
ativos = [j for j in jogo.jogadores if not j.verificarFalencia()]

# Tabuleiro
tabuleiro = jogo.tabuleiro
espaco = tabuleiro.obterEspaco(15)

# Dados
dados = jogo.dados
resultado = dados.lancar()
soma = dados.soma_dados()
dupla = dados.isDupla()

# Verificar se jogo está ativo
ativo = jogo.esta_ativo()
```

---

## Consultar Estado do Jogador

Acessar informações de um jogador específico

```python
# Dados básicos
nome = jogador.getNome()
peca = jogador.getPeca()
posicao = jogador.getPosicao()
saldo = jogador.getSaldo()

# Propriedades
propriedades = jogador.getPropriedades()
total_casas = jogador.getTotalCasas()
total_hoteis = jogador.getTotalHoteis()

# Status de cadeia
em_cadeia = jogador.estaEmCadeia()
turnos_cadeia = jogador.getTurnosCadeia()
cartas_sair = jogador.getCartasSairCadeia()

# Status financeiro
falido = jogador.verificarFalencia()
patrimonio = jogador.calcularPatrimonio()
```

---

## Tipos de Propriedades

Identificar e trabalhar com diferentes tipos de títulos

```python
from modules.tituloPropriedade import TituloPropriedade
from modules.tituloEstacao import TituloEstacao
from modules.tituloCompanhia import TituloCompanhia

# Verificar tipo
if isinstance(propriedade, TituloPropriedade):
    # Propriedade colorida (pode construir)
    cor = propriedade.getCor()
    casas = propriedade.getNumCasas()
    hotel = propriedade.temHotel()
    custo_casa = propriedade.getCustoCasa()

elif isinstance(propriedade, TituloEstacao):
    # Estação (aluguel baseado em quantidade)
    num_estacoes = propriedade.contarEstacoesProprietario()

elif isinstance(propriedade, TituloCompanhia):
    # Companhia (aluguel baseado em dados)
    multiplicador = propriedade.getMultiplicador()

# Propriedades gerais
nome = propriedade.getNome()
preco = propriedade.getPreco()
proprietario = propriedade.getProprietario()
hipotecada = propriedade.estaHipotecada()
aluguel = propriedade.calcularAluguel()
```

---

## Regras e Validações

Consultar regras e validar ações

```python
from modules.regras import Regras

regras = Regras()

# Constantes
dinheiro_inicial = Regras.DINHEIRO_INICIAL  # 1500
salario = Regras.SALARIO_VOLTA  # 200
fianca = Regras.FIANCA_CADEIA  # 50
max_casas = Regras.MAX_CASAS  # 4
max_duplas = Regras.MAX_DUPLAS  # 3

# Validações
pode_comprar = regras.validar_compra(jogador, propriedade)
pode_construir = regras.validar_construcao(jogador, propriedade)

# Cálculo de aluguel
aluguel = regras.calcular_aluguel(propriedade, dados)
```

---

## Exemplo de Fluxo Completo

```python
# 1. Verificar se jogador está na cadeia
if jogador.estaEmCadeia():
    if isinstance(jogador, JogadorIA):
        opcao = jogador.escolher_opcao_cadeia()
    else:
        opcao = interface.perguntar_opcao_cadeia()

    saiu = jogo.processarOpcoesCadeia(jogador, opcao)
    if not saiu:
        jogo.proximo_turno()
        return

# 2. Executar turno (dados + movimento + ação)
jogo.executar_turno()

# 3. Processar ação baseada no tipo de espaço
espaco = jogo.tabuleiro.obterEspaco(jogador.posicao)

# Se caiu em propriedade disponível
if jogo.propriedade_disponivel_compra:
    prop = jogo.propriedade_disponivel_compra

    if isinstance(jogador, JogadorIA):
        decisao = jogador.decidir_comprar_propriedade(prop)
    else:
        decisao = interface.perguntar_compra(prop)

    if decisao:
        jogo.tratarCompraPropriedade(jogador, prop)
    else:
        # Iniciar leilão
        leilao = jogo.iniciarLeilao(prop)
        # ... gerenciar leilão

# 4. Oferecer construção se tiver monopólio
def callback_construcao(j, props):
    if isinstance(j, JogadorIA):
        return j.escolher_propriedade_construir(props)
    return interface.escolher_propriedade(props)

jogo.solicitarDecisaoConstrucao(jogador, callback_construcao)

# 5. Verificar fim de jogo
vencedor = jogo.verificar_vencedor()
if vencedor:
    jogo.finalizar_jogo()
```

---

## Tratamento de Erros

Exceções que podem ser lançadas durante o jogo

```python
try:
    jogo.executar_turno()
except RuntimeError as e:
    # Jogo não foi iniciado
    print(f"Erro: {e}")

try:
    jogo.iniciar_jogo(jogadores_config)
except ValueError as e:
    # Número inválido de jogadores
    print(f"Erro: {e}")
```

---

## Notas Importantes

**Sistema de Falência:**
Quando um jogador falir, suas propriedades são transferidas ao credor (se faliu por dívida a jogador) ou devolvidas ao banco (se faliu por taxa). Construções são removidas quando devolvidas ao banco

**Validação de Duplas:**
Jogador vai para cadeia após 3 duplas consecutivas (MAX_DUPLAS = 3)

**Passagem pelo Início:**
Jogador recebe R$200 automaticamente ao passar ou cair no Início
