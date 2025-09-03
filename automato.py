# Representação do estado: (Fazendeiro, Lobo, Cabra, Alface)
# 0 = Margem Esquerda, 1 = Margem Direita
ESTADO_INICIAL = (0, 0, 0, 0)
ESTADO_FINAL = (1, 1, 1, 1)
dicionario = {"a": "alface", "l" : "lobo", "f": "fazendeiro", "c" : "cabra"}
# Mapeamento de nomes (em minúsculas para facilitar a entrada do usuário) para índices
ITENS_MAP = {
    'l': 1,
    'c': 2,
    'a': 3,
    'f': 0 # Representa o fazendeiro atravessando sozinho
}

# --- Funções do Autômato ---
# procedimento
def estado_eh_invalido(estado):
    """ 
    Verifica se o Estado é válido.
    Retorna (True, mensagem) se inválido.
    """
    fazendeiro, lobo, cabra, alface = estado
    if lobo == cabra and fazendeiro != lobo:
        return True, "❌ FALHA: O lobo comeu a cabra!"
    if cabra == alface and fazendeiro != cabra:
        return True, "❌ FALHA: A cabra comeu a alface!"
    return False, ""

# Controle
def proximo_estado(estado_atual, item_movido_str):
    """
    Calcula o próximo estado com base na ação. (Matriz de transição)
    Retorna uma tupla: (novo_estado, eh_valido, mensagem)
    """
    fazendeiro = estado_atual[0]
    item_movido_str_lower = item_movido_str.lower()
    
    if item_movido_str_lower not in ITENS_MAP:
        return estado_atual, False, "Movimento desconhecido."

    item_movido_idx = ITENS_MAP[item_movido_str_lower]

    # Validação: o fazendeiro só pode levar algo que está na mesma margem que ele
    if item_movido_idx != 0 and estado_atual[item_movido_idx] != fazendeiro:
        return estado_atual, False, f"⚠️ Movimento impossível: O(a) {dicionario[item_movido_str]} não está com o fazendeiro."

    novo_estado = list(estado_atual)
    # O fazendeiro sempre muda de margem
    novo_estado[0] = 1 - fazendeiro
    
    # Se um item foi movido, ele também muda de margem
    if item_movido_idx != 0:
        novo_estado[item_movido_idx] = 1 - novo_estado[item_movido_idx]
    
    novo_estado_tupla = tuple(novo_estado)
    
    # Verifica se o estado resultante é uma derrota
    invalido, msg_derrota = estado_eh_invalido(novo_estado_tupla)
    if invalido:
        return novo_estado_tupla, False, msg_derrota

    return novo_estado_tupla, True, "Movimento válido."


def verificar_cadeia_completa(cadeia_de_movimentos):
    """
    Processa uma cadeia e verifica se ela é valida.
    Retorna o histórico da verificação e um booleano de sucesso.
    """
    estado_atual = ESTADO_INICIAL
    historico = [("Início", estado_atual, "Estado inicial.")]
    # Cabeçote == movimento
    # cadeia_de_movimentos == fita
    # proximo_estado == controle
    for movimento in cadeia_de_movimentos:
        movimento_limpo = movimento.strip()
        if not movimento_limpo: continue

        estado_seguinte, eh_valido, mensagem = proximo_estado(estado_atual, movimento_limpo)
        operador = "sozinho" if movimento_limpo.lower() == "f" else "com " + "lobo" if movimento_limpo.lower() == "l" else "com cabra" if movimento_limpo.lower() == "c" else "com alface"
        acao_desc = f"Atravessar {operador.capitalize()}" if movimento_limpo.lower() != "ninguem" else "Atravessar Sozinho"
        historico.append((acao_desc, estado_seguinte, mensagem))

        if not eh_valido:
            return historico, False # A cadeia falhou
        
        estado_atual = estado_seguinte

    # Após todos os movimentos, verifica se atingiu o estado final
    if estado_atual == ESTADO_FINAL:
        historico.append(("Fim", estado_atual, "🎉 SUCESSO: Todos atravessaram em segurança! Estado final."))
        return historico, True
    else:
        historico.append(("Fim", estado_atual, "❌ FALHA: A cadeia terminou, mas o problema não foi resolvido. Não é estado final."))
        return historico, False