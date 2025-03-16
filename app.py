import streamlit as st
import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "SoftwareDB")
DB_PORT = int(os.getenv("DB_PORT", 3306))

# Função para conectar ao MySQL
def get_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
    except pymysql.MySQLError as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None  # Retorna None se a conexão falhar

# Função para obter tabelas do banco
def get_tables(conn):
    query = "SHOW TABLES;"
    df = pd.read_sql(query, conn)
    return df.iloc[:, 0].tolist()

# Função para executar consultas SQL
def execute_query(query, conn):
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        return str(e)

# Interface no Streamlit
st.title("Consulta Interativa ao Banco de Dados (MySQL)")

# Tentar conectar ao banco
conn = get_connection()

if conn:
    tables = get_tables(conn)
    st.markdown("🟢 **Conectado ao banco de dados!**")
else:
    st.markdown("🔴 **Erro ao conectar ao banco de dados.**")
    tables = []

# Exibir as tabelas disponíveis
if conn and tables:
    selected_table = st.selectbox("Escolha uma tabela para visualizar", tables)

    if selected_table:
        st.subheader(f"Visualizando dados da tabela: {selected_table}")
        query = f"SELECT * FROM {selected_table} LIMIT 100;"
        df = execute_query(query, conn)

        if isinstance(df, pd.DataFrame):
            columns = df.columns.tolist()
            filter_col = st.selectbox("Escolha uma coluna para filtrar", ["Nenhum"] + columns)
            if filter_col != "Nenhum":
                filter_value = st.text_input(f"Digite um valor para filtrar na coluna {filter_col}")
                if filter_value:
                    query = f"SELECT * FROM {selected_table} WHERE {filter_col} LIKE '%{filter_value}%' LIMIT 100;"
                    df = execute_query(query, conn)

        st.dataframe(df)

# Permitir consultas SQL personalizadas somente se a conexão estiver ativa
if conn:
    st.subheader("Consulta SQL personalizada")
    custom_query = st.text_area("Digite sua consulta SQL", "SELECT * FROM Funcionario;")
    if st.button("Executar Consulta"):
        result = execute_query(custom_query, conn)
        if isinstance(result, str):
            st.error(f"Erro na consulta: {result}")
        else:
            st.dataframe(result)

    # Fechar conexão ao final
    conn.close()
