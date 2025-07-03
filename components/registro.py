import streamlit as st
from datetime import date
import pandas as pd
import os

categorias_list = ['Alimentação', 'Transporte', 'Educação', 'Saúde', 'Lazer', 'Shopping', 'Comida Faculdade', 'Restaurantes', 'Contas', 'Assinaturas', 'Despesas Eventuais', 'Outros']
formas_pgto_list = ['Débito', 'Nubank', 'BB']

# Função auxiliar para salvar em CSV
def salvar_em_csv(nome_arquivo, registro):
    if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 0:
        df = pd.read_csv(nome_arquivo)
        df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
    else:
        df = pd.DataFrame([registro])
    df.to_csv(nome_arquivo, index=False)

# -----------------------------------------
# 1. REGISTRAR RECEBIMENTO
# -----------------------------------------
def registrar_recebimento(usuario):
    st.subheader("Registrar recebimento")

    with st.form("form_recebimento"):
        data = st.date_input("Data", value=date.today())
        valor = st.number_input("Valor (R$)", step=0.01, format="%.2f")
        categoria = st.selectbox("Categoria", ["Salário", "Extra", "Outros"])
        forma_pgto = st.selectbox("Forma de pagamento", ["Débito", "Nubank", "BB"])
        descricao = st.text_input("Descrição")
        enviar = st.form_submit_button("Salvar")

    if enviar:
        registro = {
            "Data": data.strftime("%Y-%m-%d"),
            "Tipo": "Recebimento",
            "Valor": valor,
            "Categoria": categoria,
            "Forma de Pagamento": forma_pgto,
            "Descrição": descricao,
            "Usuário": usuario
        }
        nome_arquivo = f"dados/{data.year}-{str(data.month).zfill(2)}.csv"
        salvar_em_csv(nome_arquivo, registro)
        st.success("Recebimento salvo com sucesso!")

# -----------------------------------------
# 2. REGISTRAR GASTO
# -----------------------------------------
def registrar_gasto(usuario):
    st.subheader("Registrar gasto")

    with st.form("form_gasto"):
        data = st.date_input("Data", value=date.today())
        valor = st.number_input("Valor (R$)", step=0.01, format="%.2f")
        categoria = st.selectbox("Categoria", categorias_list)
        forma_pgto = st.selectbox("Forma de pagamento", formas_pgto_list)
        descricao = st.text_input("Descrição")
        enviar = st.form_submit_button("Salvar")

    if enviar:
        registro = {
            "Data": data.strftime("%Y-%m-%d"),
            "Tipo": "Gasto",
            "Valor": valor,
            "Categoria": categoria,
            "Forma de Pagamento": forma_pgto,
            "Descrição": descricao,
            "Usuário": usuario
        }
        nome_arquivo = f"dados/{data.year}-{str(data.month).zfill(2)}.csv"
        salvar_em_csv(nome_arquivo, registro)
        st.success("Gasto salvo com sucesso!")

# -----------------------------------------
# 3. REGISTRAR GASTO FIXO
# -----------------------------------------
def registrar_gasto_fixo(usuario):
    st.subheader("Registrar gasto fixo")

    with st.form("form_gasto_fixo"):
        nome = st.text_input("Nome do gasto fixo")
        vencimento = st.number_input("Dia do vencimento", min_value=1, max_value=31, step=1)
        valor = st.number_input("Valor previsto (R$)", step=0.01, format="%.2f")
        categoria = st.selectbox("Categoria", categorias_list)
        forma_pgto = st.selectbox("Forma de pagamento", formas_pgto_list)
        descricao = st.text_input("Descrição")
        enviar = st.form_submit_button("Salvar gasto fixo")

    if enviar:
        registro = {
            "Nome": nome,
            "Vencimento": vencimento,
            "Valor Previsto": valor,
            "Categoria": categoria,
            "Forma de Pagamento": forma_pgto,
            "Descrição": descricao,
            "Status": "Não pago",
            "Usuário": usuario
        }
        salvar_em_csv("gastos_fixos.csv", registro)
        st.success("Gasto fixo cadastrado com sucesso!")

# -----------------------------------------
# 4. PAGAR GASTO FIXO
# -----------------------------------------
def pagar_gasto_fixo(usuario):
    st.subheader("Pagar gasto fixo")

    if not os.path.exists("gastos_fixos.csv"):
        st.info("Nenhum gasto fixo cadastrado ainda.")
        return

    df = pd.read_csv("gastos_fixos.csv")
    df = df[(df["Usuário"] == usuario) & (df["Status"] == "Não pago")]

    if df.empty:
        st.info("Todos os gastos fixos já foram pagos.")
        return

    selecionado = st.selectbox("Selecione o gasto a pagar", df["Nome"].tolist())

    gasto = df[df["Nome"] == selecionado].iloc[0]
    valor_real = st.number_input("Valor pago", value=gasto["Valor Previsto"], step=0.01, format="%.2f")
    confirmar = st.button("Confirmar pagamento")

    if confirmar:
        # 1. Salvar no mês atual como gasto normal
        hoje = date.today()
        registro = {
            "Data": hoje.strftime("%Y-%m-%d"),
            "Tipo": "Gasto",
            "Valor": valor_real,
            "Categoria": gasto["Categoria"],
            "Forma de Pagamento": gasto["Forma de Pagamento"],
            "Descrição": f"{gasto['Nome']} (fixo)",
            "Usuário": usuario
        }
        nome_arquivo = f"dados/{hoje.year}-{str(hoje.month).zfill(2)}.csv"
        salvar_em_csv(nome_arquivo, registro)

        # 2. Atualizar o status no CSV de gastos fixos
        df.loc[df["Nome"] == selecionado, "Status"] = "Pago"
        df.to_csv("gastos_fixos.csv", index=False)

        st.success("Gasto fixo pago e registrado com sucesso!")
