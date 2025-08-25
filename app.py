import streamlit as st # type: ignore
import pandas as pd #type: ignore
from automato import (
    ESTADO_INICIAL,
    ESTADO_FINAL,
    proximo_estado,
    verificar_cadeia_completa
)
from utils import xor
# --- Interface Gráfica com Streamlit ---

st.set_page_config(page_title="Travessia do Rio AFD", page_icon="🚢", layout="wide")

st.title("🚢 Problema da Travesia")
st.markdown("Use o jogo interativo ou o verificador de cadeias para resolver o problema.")

tab_jogo, tab_verificador = st.tabs(["▶️ Jogo Interativo", "🔍 Verificador de Cadeia"])

with tab_jogo:
    # Inicialização do estado da sessão para o jogo interativo
    if 'estado_jogo' not in st.session_state:
        st.session_state.estado_jogo = ESTADO_INICIAL
        st.session_state.game_over = False
        st.session_state.vitoria = False
        st.session_state.mensagem_final = ""
        st.session_state.historico_jogo = [("Início", ESTADO_INICIAL)]

    def reiniciar_jogo():
        st.session_state.estado_jogo = ESTADO_INICIAL
        st.session_state.game_over = False
        st.session_state.vitoria = False
        st.session_state.mensagem_final = ""
        st.session_state.historico_jogo = [("Início", ESTADO_INICIAL)]

    col_jogo, col_historico = st.columns([2, 1])

    with col_jogo:
        # --- Seção do Jogo Interativo ---
        margem_esquerda, margem_direita = [], []
        entidades = {
            "👨‍🌾‍": st.session_state.estado_jogo[0],
            "🐺": st.session_state.estado_jogo[1],
            "🐐": st.session_state.estado_jogo[2],
            "🥬": st.session_state.estado_jogo[3],
        }
        for emoji, margem in entidades.items():
            (margem_esquerda if margem == 0 else margem_direita).append(emoji)

        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.subheader("Margem Esquerda")
            st.markdown(f"<p style='font-size: 48px;'>{'<br>'.join(margem_esquerda)}</p>", unsafe_allow_html=True)
        with col2:
            st.subheader("Rio")
            st.markdown("<p style='font-size: 48px;'>⛵</p>", unsafe_allow_html=True)
        with col3:
            st.subheader("Margem Direita")
            st.markdown(f"<p style='font-size: 48px;'>{'<br>'.join(margem_direita)}</p>", unsafe_allow_html=True)

        st.write("")

        if st.session_state.vitoria:
            st.success("🎉 Parabéns! Você resolveu o problema!")
            st.balloons()
        elif st.session_state.game_over:
            st.error(f"❌ Fim de jogo! {st.session_state.mensagem_final}")

        if st.session_state.vitoria or st.session_state.game_over:
            if st.button("Jogar Novamente"):
                reiniciar_jogo()
                st.rerun()
        else:
            st.subheader("O que o fazendeiro deve fazer?")
            botoes_col1, botoes_col2 = st.columns(2)
            botoes = {"Levar o Lobo 🐺": "l", "Levar a Cabra 🐐": "c",
                    "Levar a alface 🥬": "a", "Atravessar Sozinho 👨‍🌾": "f"}

            item_clicado = None
            with botoes_col1:
                if st.button("Levar o Lobo 🐺", use_container_width=True, key = "lobo", disabled = (xor(st.session_state.estado_jogo[1], st.session_state.estado_jogo[0]))): item_clicado = "l"
                if st.button("Levar a alface 🥬", use_container_width=True, key = "alface", disabled = (xor(st.session_state.estado_jogo[3], st.session_state.estado_jogo[0]))): item_clicado = "a"
            with botoes_col2:
                if st.button("Levar a Cabra 🐐", use_container_width=True, key = "cabra", disabled = (xor(st.session_state.estado_jogo[2], st.session_state.estado_jogo[0]))): item_clicado = "c"
                if st.button("Atravessar Sozinho 👨‍🌾", use_container_width=True, key = "ninguem"): item_clicado = "f"

            if item_clicado:
                novo_estado, eh_valido, mensagem = proximo_estado(st.session_state.estado_jogo, item_clicado)
                
                if not eh_valido and "Movimento impossível" in mensagem:
                    st.toast(mensagem)
                else:
                    st.session_state.estado_jogo = novo_estado
                    operador = "sozinho" if item_clicado.lower() == "f" else "com " + "lobo" if item_clicado.lower() == "l" else "com cabra" if item_clicado.lower() == "c" else "com alface"
                    acao_desc = f"Atravessar {operador.capitalize()}" if item_clicado.lower() != "ninguem" else "Atravessar Sozinho"
                    st.session_state.historico_jogo.append((acao_desc, novo_estado))

                    if not eh_valido:
                        st.session_state.game_over = True
                        st.session_state.mensagem_final = mensagem.replace("❌ FALHA: ", "")
                    elif novo_estado == ESTADO_FINAL:
                        st.session_state.vitoria = True
                    st.rerun()

    with col_historico:

        if len(st.session_state.historico_jogo) > 1:
            st.subheader("Histórico de Movimentos")
            historico_df = pd.DataFrame(st.session_state.historico_jogo, columns=["Ação", "Estado"])
            st.dataframe(historico_df)
        else:
            st.subheader("Histórico de Movimentos")
            st.info("Nenhum movimento registrado ainda. Jogue para começar!")
        
with tab_verificador:

# --- Seção do Verificador de Cadeias ---

    st.header("🔍 Verifique uma Sequência Completa")
    st.markdown("Insira os movimentos separados por vírgula (ex: `c(cabra), f(fazendeiro), l(lobo), ...`) e o autômato validará a sequência inteira.")


    if 'cadeia_exemplo' in st.session_state:
        if st.session_state.get('last_example') != st.session_state.cadeia_exemplo:
            st.session_state.last_example = st.session_state.cadeia_exemplo
            st.session_state.cadeia_para_verificar = st.session_state.cadeia_exemplo
        else:
            del st.session_state.last_example
            del st.session_state.cadeia_exemplo

    cadeia_usuario = st.text_input(
        "Sequência de movimentos:",
        key="cadeia_para_verificar",
        placeholder="c, f, l, c, a, f, c"
    )

    col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
    with col_btn1:
        if st.button("Verificar Cadeia", type="primary", use_container_width=True):
            if not cadeia_usuario:
                st.warning("Por favor, insira uma cadeia de movimentos.")
            else:
                movimentos = [m.strip() for m in cadeia_usuario.split(',')]
                with st.status("Analisando a cadeia...", expanded=True) as status:
                    historico, sucesso = verificar_cadeia_completa(movimentos)
                    
                    for i, (acao, estado, msg) in enumerate(historico):
                        m_esq = [e for e, m in {"👨‍🌾": estado[0], "🐺": estado[1], "🐐": estado[2], "🥬": estado[3]}.items() if m == 0]
                        m_dir = [e for e, m in {"👨‍🌾": estado[0], "🐺": estado[1], "🐐": estado[2], "🥬": estado[3]}.items() if m == 1]
                        st.write(f"**Passo {i}: {acao}**")
                        st.text(f"Margem Esquerda: {' '.join(m_esq):<10} | Margem Direita: {' '.join(m_dir)}")
                        st.caption(f"Resultado: {msg}")
                    
                    if sucesso:
                        status.update(label="Análise Concluída: Solução Válida!", state="complete", expanded=True)
                        st.success("A cadeia fornecida é uma solução válida!")
                        st.balloons()
                    else:
                        status.update(label="Análise Concluída: Solução Inválida!", state="error", expanded=True)
                        st.error("A cadeia fornecida não é uma solução válida.")

    with col_btn2:
        if st.button("Ver Exemplo Positivo", use_container_width=True):
            st.session_state.cadeia_exemplo = "c, f, l, c, a, f, c"
            st.rerun()

    with col_btn3:
        if st.button("Ver Exemplo Negativo", use_container_width=True):
            st.session_state.cadeia_exemplo = "l, f, a"
            st.rerun()