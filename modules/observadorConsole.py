from modules.observador import Observador
from modules.eventoJogo import EventoJogo, TipoEvento

class ObservadorConsole(Observador):
    """
    Implementação de Observador que exibe eventos do jogo no console
    """

    def notificar(self, evento: EventoJogo) -> None:
        """
        Recebe notificação de eventos e exibe no console

        espera:
            evento: EventoJogo - evento ocorrido
        retorna:
            None
        """
        tipo = evento.tipo
        dados = evento.dados

        if tipo == TipoEvento.TURNO_INICIADO:
            jogador = dados['jogador']
            print(f"\n{'=' * 60}")
            print(f"TURNO {dados['turno']} - {jogador.getNome()}")
            print(f"Saldo: R$ {jogador.getSaldo()} | Posição: {jogador.getPosicao()}")
            print(f"{'=' * 60}")

        elif tipo == TipoEvento.DADOS_LANCADOS:
            jogador = dados['jogador']
            resultado = dados['dados']
            soma = dados['soma']
            print(f"\n{jogador.getNome()} lançou os dados: {resultado[0]} + {resultado[1]} = {soma}")

        elif tipo == TipoEvento.DUPLA_LANCADA:
            jogador = dados['jogador']
            contador = dados['contador_duplas']
            print(f"DUPLA! ({contador}ª dupla consecutiva)")

        elif tipo == TipoEvento.JOGADOR_MOVEU:
            jogador = dados['jogador']
            pos_nova = dados['posicao_nova']
            espaco = dados.get('espaco', '')
            print(f"{jogador.getNome()} moveu para a posição {pos_nova}")

        elif tipo == TipoEvento.PASSOU_INICIO:
            jogador = dados['jogador']
            valor = dados['valor']
            print(f"{jogador.getNome()} passou pelo Início! +R$ {valor}")

        elif tipo == TipoEvento.PROPRIEDADE_COMPRADA:
            jogador = dados['jogador']
            propriedade = dados['propriedade']
            valor = dados['valor']
            nome_prop = propriedade.getNome() if hasattr(propriedade, 'getNome') else str(propriedade)
            print(f"{jogador.getNome()} comprou {nome_prop} por R$ {valor}")

        elif tipo == TipoEvento.ALUGUEL_PAGO:
            pagador = dados['pagador']
            recebedor = dados['recebedor']
            propriedade = dados['propriedade']
            valor = dados['valor']
            nome_prop = propriedade.getNome() if hasattr(propriedade, 'getNome') else str(propriedade)
            print(f"{pagador.getNome()} pagou R$ {valor} de aluguel para {recebedor.getNome()} ({nome_prop})")

        elif tipo == TipoEvento.JOGADOR_PRESO:
            jogador = dados['jogador']
            motivo = dados.get('motivo', 'desconhecido')
            print(f"{jogador.getNome()} foi preso! Motivo: {motivo}")

        elif tipo == TipoEvento.SAIU_CADEIA:
            jogador = dados['jogador']
            metodo = dados.get('metodo', 'desconhecido')
            print(f"{jogador.getNome()} saiu da cadeia! Método: {metodo}")

        elif tipo == TipoEvento.JOGADOR_FALIU:
            jogador = dados.get('jogador')
            if jogador:
                print(f"{jogador.getNome()} FALIU!")

        elif tipo == TipoEvento.TURNO_FINALIZADO:
            pass
