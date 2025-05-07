import pandas as pd
import streamlit as st
from datetime import date, datetime, timedelta

caminho_datasets = "datasets"

df_compras = pd.read_csv(f"{caminho_datasets}/compras.csv", sep=";", decimal=",", index_col=0, parse_dates=True)
df_lojas = pd.read_csv(f"{caminho_datasets}/lojas.csv", sep=";", decimal=",", index_col=0)
df_produtos = pd.read_csv(f"{caminho_datasets}/produtos.csv", sep=";", decimal=",", index_col=0)

df_produtos = df_produtos.rename(columns={"nome": "produto"})
print(df_produtos)

df_compras = df_compras.reset_index()
df_compras = pd.merge(left=df_compras,
                      right=df_produtos[["preco", "produto"]],
                      on="produto",
                      how="left"
                     )

df_compras = df_compras.set_index("data")

df_compras["comissao"] = df_compras["preco"] * 0.08
print(df_compras)

data_default = df_compras.index.date.max()
data_inicio = st.sidebar.date_input("Data Inicial", data_default - timedelta(days=6))
data_final = st.sidebar.date_input("Data Final", data_default + timedelta(days=1))

df_compras_filter = df_compras[
    (df_compras.index.date >= data_inicio) & 
    (df_compras.index.date < data_final + timedelta(days=1))
]

st.markdown("# Números Gerais")
col1, col2 = st.columns(2)

valor_compras = df_compras_filter["preco"].sum()
valor_compras = f"R$ {valor_compras:.2f}"
col1.metric("Valor de compras no período", valor_compras)
col2.metric("Quantidade de compras no período", df_compras_filter["preco"].count())
