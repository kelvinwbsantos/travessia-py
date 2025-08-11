# 🚢 Travessia do Rio: Fazendeiro, Lobo, Cabra e Couve

Este projeto é uma aplicação web interativa desenvolvida com **Streamlit** que simula o famoso problema lógico do fazendeiro, do lobo, da cabra e da couve. O objetivo é ajudar o fazendeiro a atravessar todos os itens para a outra margem do rio sem que o lobo coma a cabra, ou a cabra coma a couve.

O projeto foi modelado como um **Autômato Finito Determinístico (AFD)**, onde cada estado representa a posição dos personagens e cada transição é um movimento do fazendeiro.

## 🚀 Funcionalidades

A aplicação oferece duas maneiras de interagir com o problema:

1.  **Jogo Interativo**: Jogue passo a passo, clicando nos botões para mover o fazendeiro e um dos itens. A interface visual mostra a posição de todos os personagens e exibe o histórico de movimentos.
2.  **Verificador de Cadeias**: Teste uma sequência de movimentos completa para ver se ela é uma solução válida para o problema. O autômato irá validar cada passo e mostrar onde a sequência falha, se for o caso.

## 📁 Estrutura do Projeto

O código está organizado em dois arquivos principais para maior clareza e separação de responsabilidades:

-   `automato.py`: Contém toda a lógica do autômato, incluindo a definição dos estados, as regras de validação e as funções de transição. É o "motor" do jogo.
-   `app.py`: Contém a interface de usuário criada com Streamlit. Ele importa as funções do `automato.py` para renderizar o jogo e o verificador.

## ⚙️ Como Rodar o Projeto

Siga estas instruções para executar a aplicação na sua máquina local.

### Pré-requisitos

Certifique-se de ter o Python instalado. O projeto usa as seguintes bibliotecas:

-   `streamlit`
-   `pandas`

Você pode instalá-las usando `pip`:

```bash
pip install streamlit pandas
```

### Sirva a aplicação
No seu terminal:

```bash
pip streamlit run app.py