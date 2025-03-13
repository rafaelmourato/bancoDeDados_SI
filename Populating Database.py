from faker import Faker
import random
from sqlalchemy import create_engine
import pandas as pd

# Database connection URL
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/softwaredb"

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

fake = Faker("pt_BR")

# Define possible roles
roles = ["Comercial", "Designer", "Desenvolvedor de Software"]

# Possible stacks for developers
developer_stacks = [
    "Python, Django, PostgreSQL",
    "JavaScript, React, Node.js",
    "Java, Spring Boot, MySQL",
    "C#, .NET, SQL Server",
    "Ruby on Rails, PostgreSQL",
    "PHP, Laravel, MariaDB",
    "Swift, iOS, Firebase",
    "Kotlin, Android, MongoDB"
]

# Possible design libraries
design_libraries = [
    "Figma, Adobe XD",
    "Sketch, InVision",
    "Canva, CorelDRAW",
    "Photoshop, Illustrator"
]

# Generate individuals
individuals = []
developers_dict = []
comerciais_dict = []
designers_dict = []

for _ in range(100):
    role = random.choice(roles)
    cpf = fake.cpf()

    person = {
        "Nome": fake.name(),
        "CPF": cpf,
        "Cargo": role,
        "Idade": random.randint(20, 70),
        "Salario": random.randint(3000, 13000)
    }

    if role == "Desenvolvedor de Software":
        developers_dict.append({"CPF": cpf, "Stack": random.choice(developer_stacks)})

    elif role == "Comercial":
        comerciais_dict.append({"CPF": cpf, "Nivel_Persuasao": random.randint(1, 10)})

    elif role == "Designer":
        designers_dict.append({"CPF": cpf, "Biblioteca_Designs": random.choice(design_libraries)})

    individuals.append(person)

# Generate companies
sectors = ["Alimentício", "Tecnologia", "Financeiro", "Varejo", "Saúde", "Educação", "Construção", "Automotivo"]
companies = [
    {"Nome": fake.company(), "CNPJ": fake.cnpj(), "Setor_Atuacao": random.choice(sectors)}
    for _ in range(100)
]

# Generate software projects
software_projects = [{"Codigo": i, "Nome": fake.bs().title()} for i in range(1, 1001)]

# Generate functionalities
functionalities_list = [
    "Autenticação de usuários", "Integração com APIs", "Dashboard", "CRUD", "Upload de arquivos",
    "Processamento de pagamentos", "Notificações", "Controle de acesso", "Sistema de busca",
    "Geração de relatórios", "Chat/mensagens", "Suporte a múltiplos idiomas"
]

projects = []
for project in software_projects:
    dev = random.choice(developers_dict) if developers_dict else None
    comercial = random.choice(comerciais_dict) if comerciais_dict else None

    projects.append({
        "Nome": project["Nome"],
        "Stack_Tecnologias": dev["Stack"] if dev else None,
        "Data_Inicio": fake.date_between(start_date="-2y", end_date="today"),
        "Data_Entrega": fake.date_between(start_date="today", end_date="+1y"),
        "Funcionalidades": ", ".join(random.sample(functionalities_list, k=random.randint(2, 5))),
        "Comercial_CPF": comercial["CPF"] if comercial else None,
        "Cliente_CNPJ": random.choice(companies)["CNPJ"]
    })

# Print samples
print("Individuals Sample:", individuals[:5])
print("Developers Dictionary Sample:", developers_dict[:5])
print("Comerciais Dictionary Sample:", comerciais_dict[:5])
print("Designers Dictionary Sample:", designers_dict[:5])
print("Projects Sample:", projects[:5])

# Convert individuals to DataFrame
df_funcionario = pd.DataFrame(individuals)

# Convert designers, developers, and commercials to separate DataFrames
df_designers = pd.DataFrame(designers_dict)
df_developers = pd.DataFrame(developers_dict)
df_comerciais = pd.DataFrame(comerciais_dict)

# Convert companies and projects to DataFrames
df_cliente = pd.DataFrame(companies)
df_software = pd.DataFrame(projects)

# Insert into MySQL (if_exists="append" ensures it won't overwrite)
df_funcionario.to_sql("funcionario", con=engine, if_exists="append", index=False)
df_designers.to_sql("designer", con=engine, if_exists="append", index=False)
df_developers.to_sql("desenvolvedorsoftware", con=engine, if_exists="append", index=False)
df_comerciais.to_sql("comercial", con=engine, if_exists="append", index=False)
df_cliente.to_sql("cliente", con=engine, if_exists="append", index=False)
df_software.to_sql("software", con=engine, if_exists="append", index=False)

# Define your SQL query
query = "SELECT * FROM softwaredb.software;"

# Execute query and convert to DataFrame
df_softwaredb_software = pd.read_sql(query, con=engine)  # Pass the engine instead of a connection

dict_query_software = df_softwaredb_software.to_dict(orient='records')

# Generate many-to-many relationships
desenvolvimento_software_dict = []
idealizacao_software_dict = []

for _ in range(500):  # Generate 500 random relationships
    dev = random.choice(developers_dict) if developers_dict else None
    designer = random.choice(designers_dict) if designers_dict else None
    software = random.choice(dict_query_software)

    if dev:
        desenvolvimento_software_dict.append({"Desenvolvedor_CPF": dev["CPF"], "Software_Codigo": software["Codigo"]})

    if designer:
        idealizacao_software_dict.append({"Designer_CPF": designer["CPF"], "Software_Codigo": software["Codigo"]})

# Convert relationships to DataFrames
df_desenvolvimento_software = pd.DataFrame(desenvolvimento_software_dict)
df_desenvolvimento_software.drop_duplicates(inplace=True)
df_idealizacao_software = pd.DataFrame(idealizacao_software_dict)
df_idealizacao_software.drop_duplicates(inplace=True)

print("Desenvolvimento Software Sample:", desenvolvimento_software_dict[:5])
print("Idealizacao Software Sample:", idealizacao_software_dict[:5])

df_desenvolvimento_software.to_sql("desenvolvimentosoftware", con=engine, if_exists="append", index=False)
df_idealizacao_software.to_sql("idealizacaosoftware", con=engine, if_exists="append", index=False)

print("Data successfully inserted into MySQL!")
