from sqlalchemy import create_engine, text
import pandas as pd

# Configuração do banco de dados
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306"

# Criar engine inicial sem especificar o banco (para criar SoftwareDB)
engine = create_engine(DATABASE_URL)

# Comandos para criar o banco e tabelas
sql_script = """
DROP DATABASE IF EXISTS SoftwareDB;
CREATE DATABASE SoftwareDB;
USE SoftwareDB;

CREATE TABLE Funcionario (
    CPF VARCHAR(14) PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Idade INT,
    Cargo VARCHAR(50) NOT NULL,
    Salario DECIMAL(10,2)
);

CREATE TABLE Designer (
    CPF VARCHAR(14) PRIMARY KEY,
    Biblioteca_Designs TEXT,
    FOREIGN KEY (CPF) REFERENCES Funcionario(CPF) ON DELETE CASCADE
);

CREATE TABLE DesenvolvedorSoftware (
    CPF VARCHAR(14) PRIMARY KEY,
    Stack TEXT,
    FOREIGN KEY (CPF) REFERENCES Funcionario(CPF) ON DELETE CASCADE
);

CREATE TABLE Comercial (
    CPF VARCHAR(14) PRIMARY KEY,
    Nivel_Persuasao INT,
    FOREIGN KEY (CPF) REFERENCES Funcionario(CPF) ON DELETE CASCADE
);

CREATE TABLE Cliente (
    CNPJ VARCHAR(18) PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Setor_Atuacao VARCHAR(100)
);

CREATE TABLE Software (
    Codigo INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Stack_Tecnologias TEXT,
    Data_Inicio DATE,
    Data_Entrega DATE,
    Funcionalidades TEXT,
    Comercial_CPF VARCHAR(14),
    Cliente_CNPJ VARCHAR(18),
    FOREIGN KEY (Comercial_CPF) REFERENCES Comercial(CPF) ON DELETE SET NULL,
    FOREIGN KEY (Cliente_CNPJ) REFERENCES Cliente(CNPJ) ON DELETE CASCADE
);

CREATE TABLE DesenvolvimentoSoftware (
    Desenvolvedor_CPF VARCHAR(14),
    Software_Codigo INT,
    PRIMARY KEY (Desenvolvedor_CPF, Software_Codigo),
    FOREIGN KEY (Desenvolvedor_CPF) REFERENCES DesenvolvedorSoftware(CPF) ON DELETE CASCADE,
    FOREIGN KEY (Software_Codigo) REFERENCES Software(Codigo) ON DELETE CASCADE
);

CREATE TABLE IdealizacaoSoftware (
    Designer_CPF VARCHAR(14),
    Software_Codigo INT,
    PRIMARY KEY (Designer_CPF, Software_Codigo),
    FOREIGN KEY (Designer_CPF) REFERENCES Designer(CPF) ON DELETE CASCADE,
    FOREIGN KEY (Software_Codigo) REFERENCES Software(Codigo) ON DELETE CASCADE
);
"""

# Criar o banco e tabelas
with engine.connect() as connection:
    for statement in sql_script.split(";"):
        if statement.strip():
            connection.execute(text(statement))

# Atualizar a conexão para usar o banco criado
engine = create_engine(DATABASE_URL + "/softwaredb")

# Consulta para testar a conexão
query = "SELECT * FROM softwaredb.funcionario;"
try:
    df = pd.read_sql(query, con=engine)
    print(df)
except Exception as e:
    print(f"Erro na consulta: {e}")
