import streamlit as st
import datetime
import pandas as pd
from CRUD import SoftwareDBManager


class DatabaseApp:
    def __init__(self):
        st.set_page_config(page_title="Software Database Management", layout="wide")
        st.title("Software Database Management System")

        # Initialize database directly
        self.db = SoftwareDBManager(host="localhost", user="root", password="password", database="SoftwareDB")

        # Main content - display function selector right away
        self.display_function_selector()


    def display_function_selector(self):
        # Group functions by category for better organization
        function_categories = {
            "Software Management": [
                "adicionar_software",
                "atualizar_software",
                "excluir_software",
                "obter_stack_tecnologias",
                "obter_funcionalidades_software",
                "listar_softwares_concluidos_recentes",
                "consultar_status_projetos"
            ],
            "Employee Management": [
                "registrar_funcionario",
                "atualizar_funcionario",
                "excluir_funcionario",
                "listar_funcionarios_por_software",
                "listar_funcionarios_multiplos_projetos",
                "identificar_funcionarios_sem_projetos"
            ],
            "Client Management": [
                "cadastrar_cliente",
                "excluir_cliente",
                "listar_clientes_por_setor",
                "listar_clientes_multiplos_softwares",
                "verificar_clientes_sem_softwares"
            ],
            "Reports and Analysis": [
                "listar_softwares_por_cliente",
                "listar_softwares_por_desenvolvedor",
                "consultar_softwares_por_comercial",
                "consultar_biblioteca_designs",
                "identificar_comerciais_persuasivos",
                "gerar_relatorio_projetos_por_cliente",
                "relatorio_atrasos_entrega",
                "qtd_softwares_por_stack",
                "relatorio_salarios_por_projeto",
                "relatorio_uso_tecnologias_desenvolvedores",
                "analisar_tempo_medio_desenvolvimento",
                "analisar_produtividade_desenvolvedores",
                "identificar_stacks_mais_utilizadas",
                "analisar_desempenho_comerciais",
                "identificar_setores_lucrativos",
                "validar_softwares_sem_desenvolvedores",
                "verificar_integridade_relacionamentos",
            ],
            "Associations": [
                "associar_desenvolvedor_software",
                "associar_designer_software",
                "remover_desenvolvedor_software",
                "remover_designer_software"
            ]
        }

        # Create tabs for each category
        tab_names = list(function_categories.keys())
        tabs = st.tabs(tab_names)

        for i, tab_name in enumerate(tab_names):
            with tabs[i]:
                st.subheader(f"{tab_name} Functions")
                functions = function_categories[tab_name]
                selected_function = st.selectbox(
                    "Select a function",
                    functions,
                    key=f"function_select_{tab_name}"
                )

                st.divider()
                self.display_function_form(selected_function)

    def display_function_form(self, function_name):
        st.subheader(f"Form: {function_name}")

        if function_name == "adicionar_software":
            with st.form("add_software_form"):
                nome = st.text_input("Nome do Software")
                stack_tecnologias = st.text_area("Stack de Tecnologias (separadas por vírgula)")
                data_inicio = st.date_input("Data de Início")
                data_entrega = st.date_input("Data de Entrega")
                funcionalidades = st.text_area("Funcionalidades (separadas por vírgula)")
                comercial_cpf = st.text_input("CPF do Comercial")
                cliente_cnpj = st.text_input("CNPJ do Cliente")

                submit = st.form_submit_button("Adicionar Software")
                if submit:
                    try:
                        result = self.db.adicionar_software(
                            nome,
                            stack_tecnologias,
                            data_inicio,
                            data_entrega,
                            funcionalidades,
                            comercial_cpf,
                            cliente_cnpj
                        )
                        st.success("Software adicionado com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "registrar_funcionario":
            with st.form("register_employee_form"):
                cpf = st.text_input("CPF")
                nome = st.text_input("Nome")
                idade = st.number_input("Idade", min_value=18, max_value=100)
                cargo = st.selectbox("Cargo", ["Desenvolvedor", "Designer", "Comercial", "Gerente"])
                salario = st.number_input("Salário", min_value=0.0)

                # Different attributes based on role
                if cargo == "Desenvolvedor":
                    atributos = st.text_area("Linguagens de Programação (separadas por vírgula)")
                elif cargo == "Designer":
                    atributos = st.text_area("Ferramentas de Design (separadas por vírgula)")
                elif cargo == "Comercial":
                    atributos = st.number_input("Nível de Persuasão (1-10)", min_value=1, max_value=10)
                else:
                    atributos = st.text_area("Especialidades (separadas por vírgula)")

                submit = st.form_submit_button("Registrar Funcionário")
                if submit:
                    try:
                        result = self.db.registrar_funcionario(cpf, nome, idade, cargo, salario, atributos)
                        st.success("Funcionário registrado com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "cadastrar_cliente":
            with st.form("register_client_form"):
                cnpj = st.text_input("CNPJ")
                nome = st.text_input("Nome")
                setor_atuacao = st.text_input("Setor de Atuação")

                submit = st.form_submit_button("Cadastrar Cliente")
                if submit:
                    try:
                        result = self.db.cadastrar_cliente(cnpj, nome, setor_atuacao)
                        st.success("Cliente cadastrado com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "atualizar_software":
            with st.form("update_software_form"):
                codigo = st.text_input("Código do Software")
                nome = st.text_input("Nome do Software (deixe em branco para não alterar)")
                stack_tecnologias = st.text_area("Stack de Tecnologias (deixe em branco para não alterar)")
                data_inicio = st.date_input("Data de Início", value=None)
                data_entrega = st.date_input("Data de Entrega", value=None)
                funcionalidades = st.text_area("Funcionalidades (deixe em branco para não alterar)")

                submit = st.form_submit_button("Atualizar Software")
                if submit:
                    try:
                        # Convert empty strings to None
                        nome = None if nome == "" else nome
                        stack_tecnologias = None if stack_tecnologias == "" else stack_tecnologias
                        funcionalidades = None if funcionalidades == "" else funcionalidades

                        result = self.db.atualizar_software(
                            codigo, nome, stack_tecnologias, data_inicio, data_entrega, funcionalidades
                        )
                        st.success("Software atualizado com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "atualizar_funcionario":
            with st.form("update_employee_form"):
                cpf = st.text_input("CPF do Funcionário")
                salario = st.number_input("Novo Salário (deixe 0 para não alterar)", min_value=0.0)
                cargo = st.text_input("Novo Cargo (deixe em branco para não alterar)")
                atributos_especificos = st.text_area("Novos Atributos Específicos (deixe em branco para não alterar)")

                submit = st.form_submit_button("Atualizar Funcionário")
                if submit:
                    try:
                        # Convert empty values to None
                        salario = None if salario == 0 else salario
                        cargo = None if cargo == "" else cargo
                        atributos_especificos = None if atributos_especificos == "" else atributos_especificos

                        result = self.db.atualizar_funcionario(cpf, salario, cargo, atributos_especificos)
                        st.success("Funcionário atualizado com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "excluir_software":
            with st.form("delete_software_form"):
                codigo = st.text_input("Código do Software")

                submit = st.form_submit_button("Excluir Software")
                if submit:
                    try:
                        result = self.db.excluir_software(codigo)
                        st.success("Software excluído com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "excluir_funcionario":
            with st.form("delete_employee_form"):
                cpf = st.text_input("CPF do Funcionário")

                submit = st.form_submit_button("Excluir Funcionário")
                if submit:
                    try:
                        result = self.db.excluir_funcionario(cpf)
                        st.success("Funcionário excluído com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "excluir_cliente":
            with st.form("delete_client_form"):
                cnpj = st.text_input("CNPJ do Cliente")

                submit = st.form_submit_button("Excluir Cliente")
                if submit:
                    try:
                        result = self.db.excluir_cliente(cnpj)
                        st.success("Cliente excluído com sucesso!")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "listar_softwares_por_cliente":
            with st.form("list_software_by_client_form"):
                cliente_cnpj = st.text_input("CNPJ do Cliente")

                submit = st.form_submit_button("Listar Softwares")
                if submit:
                    try:
                        result = self.db.listar_softwares_por_cliente(cliente_cnpj)
                        st.write("Softwares do Cliente:")
                        st.write(pd.DataFrame(result))
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "listar_softwares_por_desenvolvedor":
            with st.form("list_software_by_dev_form"):
                submit = st.form_submit_button("Listar Softwares por Desenvolvedor")
                if submit:
                    try:
                        result = self.db.listar_softwares_por_desenvolvedor()
                        st.write("Softwares por Desenvolvedor:")
                        st.write(pd.DataFrame(result))
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "listar_funcionarios_por_software":
            with st.form("list_employees_by_software_form"):
                software_codigo = st.text_input("Código do Software")

                submit = st.form_submit_button("Listar Funcionários")
                if submit:
                    try:
                        result = self.db.listar_funcionarios_por_software(software_codigo)
                        st.write("Funcionários do Software:")
                        st.write(pd.DataFrame(result))
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "consultar_softwares_por_comercial":
            with st.form("software_by_commercial_form"):
                comercial_cpf = st.text_input("CPF do Comercial")

                submit = st.form_submit_button("Consultar Softwares")
                if submit:
                    try:
                        result = self.db.consultar_softwares_por_comercial(comercial_cpf)
                        st.write("Softwares do Comercial:")
                        st.write(pd.DataFrame(result))
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "obter_stack_tecnologias":
            with st.form("get_tech_stack_form"):
                software_codigo = st.text_input("Código do Software")

                submit = st.form_submit_button("Obter Stack")
                if submit:
                    try:
                        result = self.db.obter_stack_tecnologias(software_codigo)
                        st.write("Stack de Tecnologias:")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

        elif function_name == "listar_clientes_por_setor":
            with st.form("list_clients_by_sector_form"):
                # Add a hidden input or a visible one that doesn't affect functionality
                st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                submit = st.form_submit_button("Listar Clientes por Setor")
                if submit:
                    try:
                        result = self.db.listar_clientes_por_setor()
                        st.write("Clientes por Setor:")
                        st.write(pd.DataFrame(result))
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

                elif function_name == "listar_funcionarios_multiplos_projetos":
                    with st.form("list_employees_multiple_projects_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Listar Funcionários com Múltiplos Projetos")
                        if submit:
                            try:
                                result = self.db.listar_funcionarios_multiplos_projetos()
                                st.write("Funcionários com Múltiplos Projetos:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "consultar_biblioteca_designs":
                    with st.form("consult_design_library_form"):
                        designer_cpf = st.text_input("CPF do Designer")

                        submit = st.form_submit_button("Consultar Biblioteca de Designs")
                        if submit:
                            try:
                                result = self.db.consultar_biblioteca_designs(designer_cpf)
                                st.write("Biblioteca de Designs:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "identificar_comerciais_persuasivos":
                    with st.form("identify_persuasive_commercials_form"):
                        nivel_minimo = st.number_input("Nível Mínimo de Persuasão", min_value=1, max_value=10, value=7)

                        submit = st.form_submit_button("Identificar Comerciais Persuasivos")
                        if submit:
                            try:
                                result = self.db.identificar_comerciais_persuasivos(nivel_minimo)
                                st.write("Comerciais Persuasivos:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "obter_funcionalidades_software":
                    with st.form("get_software_features_form"):
                        software_codigo = st.text_input("Código do Software")

                        submit = st.form_submit_button("Obter Funcionalidades")
                        if submit:
                            try:
                                result = self.db.obter_funcionalidades_software(software_codigo)
                                st.write("Funcionalidades do Software:")
                                st.write(result)
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "gerar_relatorio_projetos_por_cliente":
                    with st.form("report_projects_by_client_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Gerar Relatório")
                        if submit:
                            try:
                                result = self.db.gerar_relatorio_projetos_por_cliente()
                                st.write("Relatório de Projetos por Cliente:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "relatorio_atrasos_entrega":
                    with st.form("report_delivery_delays_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Gerar Relatório de Atrasos")
                        if submit:
                            try:
                                result = self.db.relatorio_atrasos_entrega()
                                st.write("Relatório de Atrasos na Entrega:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "qtd_softwares_por_stack":
                    with st.form("qty_software_by_stack_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Gerar Relatório")
                        if submit:
                            try:
                                result = self.db.qtd_softwares_por_stack()
                                st.write("Quantidade de Softwares por Stack:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "relatorio_salarios_por_projeto":
                    with st.form("report_salaries_by_project_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Gerar Relatório de Salários")
                        if submit:
                            try:
                                result = self.db.relatorio_salarios_por_projeto()
                                st.write("Relatório de Salários por Projeto:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "listar_clientes_multiplos_softwares":
                    with st.form("list_clients_multiple_software_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Listar Clientes com Múltiplos Softwares")
                        if submit:
                            try:
                                result = self.db.listar_clientes_multiplos_softwares()
                                st.write("Clientes com Múltiplos Softwares:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "relatorio_uso_tecnologias_desenvolvedores":
                    with st.form("report_tech_usage_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Gerar Relatório")
                        if submit:
                            try:
                                result = self.db.relatorio_uso_tecnologias_desenvolvedores()
                                st.write("Relatório de Uso de Tecnologias por Desenvolvedores:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "listar_softwares_concluidos_recentes":
                    st.write("Debug: Function matched")
                    with st.form("list_recent_completed_software_form"):
                        st.write("Debug: Function matched")
                        meses = st.number_input("Número de Meses", min_value=1, max_value=36, value=6)

                        submit = st.form_submit_button("Listar Softwares Concluídos")
                        if submit:
                            try:
                                result = self.db.listar_softwares_concluidos_recentes(meses)
                                st.write("Softwares Concluídos Recentemente:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "analisar_tempo_medio_desenvolvimento":
                    with st.form("analyze_avg_development_time_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Analisar Tempo Médio")
                        if submit:
                            try:
                                result = self.db.analisar_tempo_medio_desenvolvimento()
                                st.write("Análise de Tempo Médio de Desenvolvimento:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "analisar_produtividade_desenvolvedores":
                    with st.form("analyze_developer_productivity_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Analisar Produtividade")
                        if submit:
                            try:
                                result = self.db.analisar_produtividade_desenvolvedores()
                                st.write("Análise de Produtividade dos Desenvolvedores:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "identificar_stacks_mais_utilizadas":
                    with st.form("identify_most_used_stacks_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Identificar Stacks Mais Utilizadas")
                        if submit:
                            try:
                                result = self.db.identificar_stacks_mais_utilizadas()
                                st.write("Stacks Mais Utilizadas:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "analisar_desempenho_comerciais":
                    with st.form("analyze_commercial_performance_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Analisar Desempenho")
                        if submit:
                            try:
                                result = self.db.analisar_desempenho_comerciais()
                                st.write("Análise de Desempenho dos Comerciais:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "identificar_setores_lucrativos":
                    with st.form("identify_profitable_sectors_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Identificar Setores Lucrativos")
                        if submit:
                            try:
                                result = self.db.identificar_setores_lucrativos()
                                st.write("Setores Lucrativos:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "validar_softwares_sem_desenvolvedores":
                    with st.form("validate_software_no_developers_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Validar Softwares")
                        if submit:
                            try:
                                result = self.db.validar_softwares_sem_desenvolvedores()
                                st.write("Softwares sem Desenvolvedores:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "verificar_clientes_sem_softwares":
                    with st.form("verify_clients_no_software_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Verificar Clientes")
                        if submit:
                            try:
                                result = self.db.verificar_clientes_sem_softwares()
                                st.write("Clientes sem Softwares:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "identificar_funcionarios_sem_projetos":
                    with st.form("identify_employees_no_projects_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Identificar Funcionários")
                        if submit:
                            try:
                                result = self.db.identificar_funcionarios_sem_projetos()
                                st.write("Funcionários sem Projetos:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "verificar_integridade_relacionamentos":
                    with st.form("verify_relationship_integrity_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Verificar Integridade")
                        if submit:
                            try:
                                result = self.db.verificar_integridade_relacionamentos()
                                st.write("Relatório de Integridade dos Relacionamentos:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "consultar_status_projetos":
                    with st.form("consult_project_status_form"):
                        # Add a hidden input or a visible one that doesn't affect functionality
                        st.text_input("", "", key="hidden_input", label_visibility="collapsed")

                        submit = st.form_submit_button("Consultar Status")
                        if submit:
                            try:
                                result = self.db.consultar_status_projetos()
                                st.write("Status dos Projetos:")
                                st.write(pd.DataFrame(result))
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "associar_desenvolvedor_software":
                    with st.form("associate_developer_software_form"):
                        desenvolvedor_cpf = st.text_input("CPF do Desenvolvedor")
                        software_codigo = st.text_input("Código do Software")

                        submit = st.form_submit_button("Associar Desenvolvedor")
                        if submit:
                            try:
                                result = self.db.associar_desenvolvedor_software(desenvolvedor_cpf, software_codigo)
                                st.success("Desenvolvedor associado com sucesso!")
                                st.write(result)
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "associar_designer_software":
                    with st.form("associate_designer_software_form"):
                        designer_cpf = st.text_input("CPF do Designer")
                        software_codigo = st.text_input("Código do Software")

                        submit = st.form_submit_button("Associar Designer")
                        if submit:
                            try:
                                result = self.db.associar_designer_software(designer_cpf, software_codigo)
                                st.success("Designer associado com sucesso!")
                                st.write(result)
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "remover_desenvolvedor_software":
                    with st.form("remove_developer_software_form"):
                        desenvolvedor_cpf = st.text_input("CPF do Desenvolvedor")
                        software_codigo = st.text_input("Código do Software")

                        submit = st.form_submit_button("Remover Desenvolvedor")
                        if submit:
                            try:
                                result = self.db.remover_desenvolvedor_software(desenvolvedor_cpf, software_codigo)
                                st.success("Desenvolvedor removido com sucesso!")
                                st.write(result)
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                elif function_name == "remover_designer_software":
                    with st.form("remove_designer_software_form"):
                        designer_cpf = st.text_input("CPF do Designer")
                        software_codigo = st.text_input("Código do Software")

                        submit = st.form_submit_button("Remover Designer")
                        if submit:
                            try:
                                result = self.db.remover_designer_software(designer_cpf, software_codigo)
                                st.success("Designer removido com sucesso!")
                                st.write(result)
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                # Database simulation class - replace with your actual database implementation


# Run the app
if __name__ == "__main__":
    app = DatabaseApp()
