import streamlit as st
import pandas as pd
from components.auth import check_user, create_user, hash_password
import os
from glob import glob
import plotly.express as px 
from datetime import date, datetime
from components.registro import (
    registrar_recebimento, registrar_gasto,
    registrar_gasto_fixo, pagar_gasto_fixo
)
    

st.set_page_config(page_title="Gerenciador de Finanças", page_icon="💰")
st.title("Gerenciador de Finanças")

# Inicializa a sessão
if "logado" not in st.session_state:
    st.session_state.logado = False

# === TELA DE LOGIN ===
if not st.session_state.logado:
    st.subheader("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if check_user(usuario, senha):
            st.success("Login realizado com sucesso!")
            st.session_state.logado = True
            st.session_state.usuario = usuario
        else:
            st.error("Usuário ou senha incorretos.")

    st.markdown("---")
    st.subheader("Criar nova conta")
    novo_usuario = st.text_input("Novo usuário")
    nova_senha = st.text_input("Nova senha", type="password")
    if st.button("Criar conta"):
        if create_user(novo_usuario, nova_senha):
            st.success("Conta criada com sucesso!")
        else:
            st.error("Usuário já existe.")

# === TELA PRINCIPAL APÓS LOGIN ===
else:
    st.success(f"Bem-vinda, {st.session_state.usuario} 👋")

    aba = st.tabs(["➕ Registrar", "📊 Visualizar"])

    # ======= ABA DE REGISTRO =======
    with aba[0]:
        st.subheader("➕ Registrar movimentação")

        opcao = st.radio("Escolha uma ação:", [
            "Registrar recebimento", 
            "Registrar gasto", 
            "Registrar gasto fixo", 
            "Pagar gasto fixo"
        ], horizontal=True)

        if opcao == "Registrar recebimento":
            registrar_recebimento(st.session_state.usuario)

        elif opcao == "Registrar gasto":
            registrar_gasto(st.session_state.usuario)

        elif opcao == "Registrar gasto fixo":
            registrar_gasto_fixo(st.session_state.usuario)

        elif opcao == "Pagar gasto fixo":
            pagar_gasto_fixo(st.session_state.usuario)




    # ======= ABA DE VISUALIZAÇÃO ========
    with aba[1]:
        st.subheader("📋 Registros do mês atual")
        hoje = date.today()
        #nome_arquivo = f"dados/{hoje.year}-{str(hoje.month).zfill(2)}.csv"
        nome_arquivo = f"dados/{hoje.year}-06.csv"


        if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 0:
            df = pd.read_csv(nome_arquivo)
            df = df[df["Usuário"] == st.session_state.usuario]

            tipos = st.multiselect("Filtrar por tipo", df["Tipo"].unique(), default=list(df["Tipo"].unique()))
            categorias = st.multiselect("Filtrar por categoria", df["Categoria"].unique(), default=list(df["Categoria"].unique()))

            df_filtrado = df[(df["Tipo"].isin(tipos)) & (df["Categoria"].isin(categorias))]

            st.dataframe(df_filtrado, use_container_width=True)

            # Totais
            gastos_debito = df_filtrado[(df_filtrado["Tipo"] == "Gasto") & (df_filtrado["Forma de Pagamento"] == "Débito")]["Valor"].sum()
            gastos_credito = df_filtrado[(df_filtrado["Tipo"] == "Gasto") & (df_filtrado["Forma de Pagamento"].isin(["Nubank", "BB"]))]["Valor"].sum()
            recebimentos = df_filtrado[df_filtrado["Tipo"] == "Recebimento"]["Valor"].sum()

            saldo_real = recebimentos - gastos_debito

            st.metric("💸 Gastos (Débito)", f"R$ {gastos_debito:.2f}")
            st.metric("💳 Gastos (Crédito)", f"R$ {gastos_credito:.2f}")
            st.metric("🟢 Recebimentos", f"R$ {recebimentos:.2f}")
            st.metric("📊 Saldo do Mês (real)", f"R$ {saldo_real:.2f}", delta=saldo_real)

            # Botão para baixar CSV filtrado
            csv_download = df_filtrado.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Baixar CSV filtrado", data=csv_download, file_name="registros_filtrados.csv", mime="text/csv")

        else:
            st.info("Nenhum registro encontrado para este mês.")
