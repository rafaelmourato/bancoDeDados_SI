import pymysql
from datetime import datetime, timedelta


class SoftwareDBManager:
    def __init__(self, host='localhost', user='root', password='password', database='SoftwareDB'):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    # =============================================
    # CRUD Operations (Create, Read, Update, Delete)
    # =============================================

    # 1. Add new software to the database
    def adicionar_software(self, nome, stack_tecnologias, data_inicio, data_entrega,
                           funcionalidades, comercial_cpf, cliente_cnpj):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO Software (Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, 
                                     Funcionalidades, Comercial_CPF, Cliente_CNPJ)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (nome, stack_tecnologias, data_inicio, data_entrega,
                                     funcionalidades, comercial_cpf, cliente_cnpj))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao adicionar software: {str(e)}")

    # 2. Register a new employee
    def registrar_funcionario(self, cpf, nome, idade, cargo, salario, atributos_especificos):
        try:
            with self.connection.cursor() as cursor:
                # Insert into base employee table
                sql_funcionario = """
                INSERT INTO Funcionario (CPF, Nome, Idade, Cargo, Salario)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_funcionario, (cpf, nome, idade, cargo, salario))

                # Insert into specific role table based on cargo
                if cargo.lower() == 'designer':
                    sql_especifico = """
                    INSERT INTO Designer (CPF, Biblioteca_Designs)
                    VALUES (%s, %s)
                    """
                    cursor.execute(sql_especifico, (cpf, atributos_especificos.get('biblioteca_designs', '')))

                elif cargo.lower() == 'desenvolvedor':
                    sql_especifico = """
                    INSERT INTO DesenvolvedorSoftware (CPF, Stack)
                    VALUES (%s, %s)
                    """
                    cursor.execute(sql_especifico, (cpf, atributos_especificos.get('stack', '')))

                elif cargo.lower() == 'comercial':
                    sql_especifico = """
                    INSERT INTO Comercial (CPF, Nivel_Persuasao)
                    VALUES (%s, %s)
                    """
                    cursor.execute(sql_especifico, (cpf, atributos_especificos.get('nivel_persuasao', 0)))

                self.connection.commit()
                return cpf
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao registrar funcionário: {str(e)}")

    # 3. Register a new client
    def cadastrar_cliente(self, cnpj, nome, setor_atuacao):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO Cliente (CNPJ, Nome, Setor_Atuacao)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (cnpj, nome, setor_atuacao))
                self.connection.commit()
                return cnpj
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao cadastrar cliente: {str(e)}")

    # 4. Update software information
    def atualizar_software(self, codigo, nome=None, stack_tecnologias=None,
                           data_inicio=None, data_entrega=None, funcionalidades=None):
        try:
            with self.connection.cursor() as cursor:
                updates = []
                params = []

                if nome is not None:
                    updates.append("Nome = %s")
                    params.append(nome)
                if stack_tecnologias is not None:
                    updates.append("Stack_Tecnologias = %s")
                    params.append(stack_tecnologias)
                if data_inicio is not None:
                    updates.append("Data_Inicio = %s")
                    params.append(data_inicio)
                if data_entrega is not None:
                    updates.append("Data_Entrega = %s")
                    params.append(data_entrega)
                if funcionalidades is not None:
                    updates.append("Funcionalidades = %s")
                    params.append(funcionalidades)

                if not updates:
                    return False

                sql = f"UPDATE Software SET {', '.join(updates)} WHERE Codigo = %s"
                params.append(codigo)

                cursor.execute(sql, params)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao atualizar software: {str(e)}")

    # 5. Update employee data
    def atualizar_funcionario(self, cpf, salario=None, cargo=None, atributos_especificos=None):
        try:
            with self.connection.cursor() as cursor:
                # Update base employee table
                updates = []
                params = []

                if salario is not None:
                    updates.append("Salario = %s")
                    params.append(salario)
                if cargo is not None:
                    updates.append("Cargo = %s")
                    params.append(cargo)

                if updates:
                    sql_funcionario = f"UPDATE Funcionario SET {', '.join(updates)} WHERE CPF = %s"
                    params.append(cpf)
                    cursor.execute(sql_funcionario, params)

                # Update specific role attributes if provided
                if atributos_especificos:
                    # First, determine the current role
                    sql_cargo = "SELECT Cargo FROM Funcionario WHERE CPF = %s"
                    cursor.execute(sql_cargo, (cpf,))
                    result = cursor.fetchone()

                    if not result:
                        raise Exception(f"Funcionário com CPF {cpf} não encontrado")

                    current_cargo = cargo or result['Cargo']

                    if current_cargo.lower() == 'designer' and 'biblioteca_designs' in atributos_especificos:
                        sql_especifico = """
                        UPDATE Designer SET Biblioteca_Designs = %s WHERE CPF = %s
                        """
                        cursor.execute(sql_especifico, (atributos_especificos['biblioteca_designs'], cpf))

                    elif current_cargo.lower() == 'desenvolvedor' and 'stack' in atributos_especificos:
                        sql_especifico = """
                        UPDATE DesenvolvedorSoftware SET Stack = %s WHERE CPF = %s
                        """
                        cursor.execute(sql_especifico, (atributos_especificos['stack'], cpf))

                    elif current_cargo.lower() == 'comercial' and 'nivel_persuasao' in atributos_especificos:
                        sql_especifico = """
                        UPDATE Comercial SET Nivel_Persuasao = %s WHERE CPF = %s
                        """
                        cursor.execute(sql_especifico, (atributos_especificos['nivel_persuasao'], cpf))

                self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao atualizar funcionário: {str(e)}")

    # 6. Delete a software
    def excluir_software(self, codigo):
        try:
            with self.connection.cursor() as cursor:
                # Check if software exists
                check_sql = "SELECT Codigo FROM Software WHERE Codigo = %s"
                cursor.execute(check_sql, (codigo,))
                if not cursor.fetchone():
                    return False

                # Delete the software (other tables with foreign keys will be handled by ON DELETE constraints)
                sql = "DELETE FROM Software WHERE Codigo = %s"
                cursor.execute(sql, (codigo,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao excluir software: {str(e)}")

    # 7. Delete an employee
    def excluir_funcionario(self, cpf):
        try:
            with self.connection.cursor() as cursor:
                # Check if employee exists
                check_sql = "SELECT CPF FROM Funcionario WHERE CPF = %s"
                cursor.execute(check_sql, (cpf,))
                if not cursor.fetchone():
                    return False

                # Delete the employee (cascade will handle child tables)
                sql = "DELETE FROM Funcionario WHERE CPF = %s"
                cursor.execute(sql, (cpf,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao excluir funcionário: {str(e)}")

    # 8. Delete a client and all associated software
    def excluir_cliente(self, cnpj):
        try:
            with self.connection.cursor() as cursor:
                # Check if client exists
                check_sql = "SELECT CNPJ FROM Cliente WHERE CNPJ = %s"
                cursor.execute(check_sql, (cnpj,))
                if not cursor.fetchone():
                    return False

                # Delete the client (ON DELETE CASCADE will handle related software)
                sql = "DELETE FROM Cliente WHERE CNPJ = %s"
                cursor.execute(sql, (cnpj,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao excluir cliente: {str(e)}")

    # =============================================
    # Informative Queries
    # =============================================

    # 9. List all software developed for a specific client
    def listar_softwares_por_cliente(self, cliente_cnpj):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT s.Codigo, s.Nome, s.Stack_Tecnologias, s.Data_Inicio, s.Data_Entrega, 
                       s.Funcionalidades, c.Nome as Cliente_Nome
                FROM Software s
                JOIN Cliente c ON s.Cliente_CNPJ = c.CNPJ
                WHERE s.Cliente_CNPJ = %s
                """
                cursor.execute(sql, (cliente_cnpj,))
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao listar softwares por cliente: {str(e)}")

    # 10. List software under development by each employee
    def listar_softwares_por_desenvolvedor(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT ds.Desenvolvedor_CPF, f.Nome as Desenvolvedor_Nome, 
                       s.Codigo as Software_Codigo, s.Nome as Software_Nome
                FROM DesenvolvimentoSoftware ds
                JOIN DesenvolvedorSoftware d ON ds.Desenvolvedor_CPF = d.CPF
                JOIN Funcionario f ON d.CPF = f.CPF
                JOIN Software s ON ds.Software_Codigo = s.Codigo
                ORDER BY ds.Desenvolvedor_CPF
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao listar softwares por desenvolvedor: {str(e)}")

    # 11. List employees involved in the development of a specific software
    def listar_funcionarios_por_software(self, software_codigo):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                (SELECT f.CPF, f.Nome, f.Cargo, 'Desenvolvedor' as Tipo_Envolvimento
                 FROM Funcionario f
                 JOIN DesenvolvedorSoftware d ON f.CPF = d.CPF
                 JOIN DesenvolvimentoSoftware ds ON d.CPF = ds.Desenvolvedor_CPF
                 WHERE ds.Software_Codigo = %s)
                UNION
                (SELECT f.CPF, f.Nome, f.Cargo, 'Designer' as Tipo_Envolvimento
                 FROM Funcionario f
                 JOIN Designer des ON f.CPF = des.CPF
                 JOIN IdealizacaoSoftware i ON des.CPF = i.Designer_CPF
                 WHERE i.Software_Codigo = %s)
                """
                cursor.execute(sql, (software_codigo, software_codigo))
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao listar funcionários por software: {str(e)}")

    # 12. Query all software sold by a sales employee
    def consultar_softwares_por_comercial(self, comercial_cpf):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT s.Codigo, s.Nome, s.Data_Inicio, s.Data_Entrega, 
                       c.Nome as Cliente_Nome, c.CNPJ as Cliente_CNPJ
                FROM Software s
                JOIN Cliente c ON s.Cliente_CNPJ = c.CNPJ
                WHERE s.Comercial_CPF = %s
                """
                cursor.execute(sql, (comercial_cpf,))
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao consultar softwares por comercial: {str(e)}")

    # 13. Get the technology stack needed for software development
    def obter_stack_tecnologias(self, software_codigo):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT Stack_Tecnologias FROM Software WHERE Codigo = %s"
                cursor.execute(sql, (software_codigo,))
                result = cursor.fetchone()
                return result['Stack_Tecnologias'] if result else None
        except Exception as e:
            raise Exception(f"Erro ao obter stack de tecnologias: {str(e)}")

    # 14. List clients by business sector
    def listar_clientes_por_setor(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT Setor_Atuacao, GROUP_CONCAT(CNPJ) as CNPJs, 
                           GROUP_CONCAT(Nome) as Nomes, COUNT(*) as Total
                    FROM Cliente
                    GROUP BY Setor_Atuacao
                    """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao listar clientes por setor: {str(e)}")

    # 15. List all designers or developers with more than one software designed/developed
    def listar_funcionarios_multiplos_projetos(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                (SELECT f.CPF, f.Nome, f.Cargo, COUNT(ds.Software_Codigo) as Quantidade_Projetos
                 FROM Funcionario f
                 JOIN DesenvolvedorSoftware d ON f.CPF = d.CPF
                 JOIN DesenvolvimentoSoftware ds ON d.CPF = ds.Desenvolvedor_CPF
                 GROUP BY f.CPF
                 HAVING COUNT(ds.Software_Codigo) > 1)
                UNION
                (SELECT f.CPF, f.Nome, f.Cargo, COUNT(i.Software_Codigo) as Quantidade_Projetos
                 FROM Funcionario f
                 JOIN Designer des ON f.CPF = des.CPF
                 JOIN IdealizacaoSoftware i ON des.CPF = i.Designer_CPF
                 GROUP BY f.CPF
                 HAVING COUNT(i.Software_Codigo) > 1)
                ORDER BY Quantidade_Projetos DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao listar funcionários com múltiplos projetos: {str(e)}")

    # 16. Query the design library of a specific designer
    def consultar_biblioteca_designs(self, designer_cpf):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT d.Biblioteca_Designs, f.Nome 
                FROM Designer d
                JOIN Funcionario f ON d.CPF = f.CPF
                WHERE d.CPF = %s
                """
                cursor.execute(sql, (designer_cpf,))
                return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Erro ao consultar biblioteca de designs: {str(e)}")

    # 17. Identify sales employees with high persuasion level
    def identificar_comerciais_persuasivos(self, nivel_minimo=7):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT c.CPF, f.Nome, c.Nivel_Persuasao
                FROM Comercial c
                JOIN Funcionario f ON c.CPF = f.CPF
                WHERE c.Nivel_Persuasao >= %s
                ORDER BY c.Nivel_Persuasao DESC
                """
                cursor.execute(sql, (nivel_minimo,))
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao identificar comerciais persuasivos: {str(e)}")

    # 18. Get the list of features of a software
    def obter_funcionalidades_software(self, software_codigo):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT Funcionalidades FROM Software WHERE Codigo = %s"
                cursor.execute(sql, (software_codigo,))
                result = cursor.fetchone()
                return result['Funcionalidades'] if result else None
        except Exception as e:
            raise Exception(f"Erro ao obter funcionalidades do software: {str(e)}")

    # =============================================
    # Report Queries
    # =============================================

    # 19. Generate a project report by client
    def gerar_relatorio_projetos_por_cliente(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT c.CNPJ, c.Nome as Cliente_Nome, c.Setor_Atuacao, 
                       s.Codigo as Software_Codigo, s.Nome as Software_Nome,
                       s.Data_Inicio, s.Data_Entrega,
                       CASE 
                           WHEN CURDATE() > s.Data_Entrega THEN 'Atrasado'
                           WHEN s.Data_Entrega IS NULL THEN 'Em Definição'
                           WHEN CURDATE() = s.Data_Entrega THEN 'Entrega Hoje'
                           ELSE 'Em Andamento' 
                       END as Status,
                       com.CPF as Comercial_CPF,
                       (SELECT GROUP_CONCAT(f.Nome) 
                        FROM Funcionario f 
                        JOIN DesenvolvedorSoftware d ON f.CPF = d.CPF
                        JOIN DesenvolvimentoSoftware ds ON d.CPF = ds.Desenvolvedor_CPF
                        WHERE ds.Software_Codigo = s.Codigo) as Desenvolvedores,
                       (SELECT GROUP_CONCAT(f.Nome) 
                        FROM Funcionario f 
                        JOIN Designer des ON f.CPF = des.CPF
                        JOIN IdealizacaoSoftware i ON des.CPF = i.Designer_CPF
                        WHERE i.Software_Codigo = s.Codigo) as Designers
                FROM Cliente c
                LEFT JOIN Software s ON c.CNPJ = s.Cliente_CNPJ
                LEFT JOIN Comercial com ON s.Comercial_CPF = com.CPF
                ORDER BY c.Nome, s.Nome
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao gerar relatório de projetos por cliente: {str(e)}")

    # 20. Report on delays in software delivery
    def relatorio_atrasos_entrega(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT s.Codigo, s.Nome as Software_Nome, 
                       s.Data_Inicio, s.Data_Entrega,
                       DATEDIFF(CURDATE(), s.Data_Entrega) as Dias_Atraso,
                       c.Nome as Cliente_Nome, c.CNPJ,
                       fc.Nome as Comercial_Nome,
                       (SELECT GROUP_CONCAT(f.Nome) 
                        FROM Funcionario f 
                        JOIN DesenvolvedorSoftware d ON f.CPF = d.CPF
                        JOIN DesenvolvimentoSoftware ds ON d.CPF = ds.Desenvolvedor_CPF
                        WHERE ds.Software_Codigo = s.Codigo) as Desenvolvedores
                FROM Software s
                JOIN Cliente c ON s.Cliente_CNPJ = c.CNPJ
                LEFT JOIN Comercial com ON s.Comercial_CPF = com.CPF
                LEFT JOIN Funcionario fc ON com.CPF = fc.CPF
                WHERE s.Data_Entrega < CURDATE()
                ORDER BY Dias_Atraso DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao gerar relatório de atrasos na entrega: {str(e)}")

    # 21. Get the number of software by technology stack
    def qtd_softwares_por_stack(self):
        try:
            with self.connection.cursor() as cursor:
                # This query assumes stack technologies are separated by commas
                sql = """
                SELECT 
                    SUBSTRING_INDEX(SUBSTRING_INDEX(t.Stack_Item, ',', n.n), ',', -1) as Tecnologia,
                    COUNT(*) as Quantidade
                FROM 
                    Software,
                    (SELECT 1 n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
                     UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) n,
                    (SELECT Codigo, CONCAT(Stack_Tecnologias, ',') as Stack_Item FROM Software) t
                WHERE 
                    n.n <= 1 + LENGTH(t.Stack_Item) - LENGTH(REPLACE(t.Stack_Item, ',', ''))
                    AND Stack_Tecnologias IS NOT NULL
                GROUP BY Tecnologia
                ORDER BY Quantidade DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao obter quantidade de softwares por stack: {str(e)}")

    # 22. Project team salary report
    def relatorio_salarios_por_projeto(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT s.Codigo, s.Nome as Software_Nome,
                       (SELECT SUM(f.Salario)
                        FROM Funcionario f
                        WHERE f.CPF IN (
                            SELECT ds.Desenvolvedor_CPF
                            FROM DesenvolvimentoSoftware ds
                            WHERE ds.Software_Codigo = s.Codigo
                        ) OR f.CPF IN (
                            SELECT i.Designer_CPF
                            FROM IdealizacaoSoftware i
                            WHERE i.Software_Codigo = s.Codigo
                        ) OR f.CPF = s.Comercial_CPF
                       ) as Custo_Total_Salarios,
                       (SELECT COUNT(*)
                        FROM (
                            SELECT ds.Desenvolvedor_CPF as CPF
                            FROM DesenvolvimentoSoftware ds
                            WHERE ds.Software_Codigo = s.Codigo
                            UNION
                            SELECT i.Designer_CPF as CPF
                            FROM IdealizacaoSoftware i
                            WHERE i.Software_Codigo = s.Codigo
                            UNION
                            SELECT s.Comercial_CPF as CPF
                            WHERE s.Comercial_CPF IS NOT NULL
                        ) as Funcionarios
                       ) as Total_Funcionarios
                FROM Software s
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao gerar relatório de salários por projeto: {str(e)}")

    # 23. List clients with more than one contracted software
    def listar_clientes_multiplos_softwares(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT c.CNPJ, c.Nome, c.Setor_Atuacao, COUNT(s.Codigo) as Quantidade_Softwares
                FROM Cliente c
                JOIN Software s ON c.CNPJ = s.Cliente_CNPJ
                GROUP BY c.CNPJ
                HAVING COUNT(s.Codigo) > 1
                ORDER BY Quantidade_Softwares DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao listar clientes com múltiplos softwares: {str(e)}")

    # 24. Report on use of technologies by developers
    def relatorio_uso_tecnologias_desenvolvedores(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT ds.Desenvolvedor_CPF, f.Nome as Desenvolvedor_Nome, d.Stack as Tecnologias_Dominadas,
                       GROUP_CONCAT(DISTINCT s.Codigo) as Codigos_Software,
                       GROUP_CONCAT(DISTINCT s.Nome) as Nomes_Software,
                       GROUP_CONCAT(DISTINCT s.Stack_Tecnologias) as Tecnologias_Projetos
                FROM DesenvolvimentoSoftware ds
                JOIN DesenvolvedorSoftware d ON ds.Desenvolvedor_CPF = d.CPF
                JOIN Funcionario f ON d.CPF = f.CPF
                JOIN Software s ON ds.Software_Codigo = s.Codigo
                GROUP BY ds.Desenvolvedor_CPF
                ORDER BY f.Nome
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao gerar relatório de uso de tecnologias: {str(e)}")

    # 25. Generate a list of software completed in the last 6 months
    def listar_softwares_concluidos_recentes(self, meses=6):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT s.Codigo, s.Nome, s.Data_Inicio, s.Data_Entrega,
                       DATEDIFF(s.Data_Entrega, s.Data_Inicio) as Dias_Desenvolvimento,
                       c.Nome as Cliente_Nome, c.Setor_Atuacao
                FROM Software s
                JOIN Cliente c ON s.Cliente_CNPJ = c.CNPJ
                WHERE s.Data_Entrega <= CURDATE() 
                  AND s.Data_Entrega >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
                ORDER BY s.Data_Entrega DESC
                """
                cursor.execute(sql, (meses,))
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao listar softwares concluídos recentes: {str(e)}")

    # =============================================
    # Analytical Queries
    # =============================================

    # 26. Analyze average development time by project type
    def analisar_tempo_medio_desenvolvimento(self):
        try:
            with self.connection.cursor() as cursor:
                # This query groups by technology stack (might need adjustment based on actual data format)
                sql = """
                SELECT 
                    Stack_Tecnologias,
                    COUNT(*) as Quantidade_Projetos,
                    AVG(DATEDIFF(Data_Entrega, Data_Inicio)) as Media_Dias_Desenvolvimento,
                    MIN(DATEDIFF(Data_Entrega, Data_Inicio)) as Min_Dias,
                    MAX(DATEDIFF(Data_Entrega, Data_Inicio)) as Max_Dias
                FROM Software
                WHERE Data_Inicio IS NOT NULL AND Data_Entrega IS NOT NULL
                GROUP BY Stack_Tecnologias
                ORDER BY Media_Dias_Desenvolvimento DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao analisar tempo médio de desenvolvimento: {str(e)}")

    # 27. Analyze developer productivity by software
    def analisar_produtividade_desenvolvedores(self):
        try:
            with self.connection.cursor() as cursor:
                # 27. (continued) Analyze developer productivity by software
                sql = """
                SELECT d.CPF, f.Nome, COUNT(ds.Software_Codigo) as Total_Projetos,
                       AVG(DATEDIFF(s.Data_Entrega, s.Data_Inicio)) as Media_Dias_Projeto,
                       SUM(CASE WHEN s.Data_Entrega < CURDATE() THEN 1 ELSE 0 END) as Projetos_Concluidos,
                       SUM(CASE WHEN s.Data_Entrega >= CURDATE() THEN 1 ELSE 0 END) as Projetos_Em_Andamento
                FROM DesenvolvedorSoftware d
                JOIN Funcionario f ON d.CPF = f.CPF
                JOIN DesenvolvimentoSoftware ds ON d.CPF = ds.Desenvolvedor_CPF
                JOIN Software s ON ds.Software_Codigo = s.Codigo
                WHERE s.Data_Inicio IS NOT NULL AND s.Data_Entrega IS NOT NULL
                GROUP BY d.CPF
                ORDER BY Total_Projetos DESC, Media_Dias_Projeto ASC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao analisar produtividade dos desenvolvedores: {str(e)}")

    # 28. Identify most used technology stacks
    def identificar_stacks_mais_utilizadas(self):
        try:
            with self.connection.cursor() as cursor:
                # Similar to query 21, but with more details
                sql = """
                SELECT 
                    SUBSTRING_INDEX(SUBSTRING_INDEX(t.Stack_Item, ',', n.n), ',', -1) as Tecnologia,
                    COUNT(*) as Quantidade,
                    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Software WHERE Stack_Tecnologias IS NOT NULL) as Porcentagem,
                    GROUP_CONCAT(DISTINCT t.Codigo ORDER BY t.Codigo SEPARATOR ', ') as Softwares
                FROM 
                    (SELECT 1 n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
                     UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) n,
                    (SELECT Codigo, CONCAT(Stack_Tecnologias, ',') as Stack_Item FROM Software) t
                WHERE 
                    n.n <= 1 + LENGTH(t.Stack_Item) - LENGTH(REPLACE(t.Stack_Item, ',', ''))
                    AND Stack_Item IS NOT NULL
                GROUP BY Tecnologia
                ORDER BY Quantidade DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao identificar stacks mais utilizadas: {str(e)}")

    # 29. Analyze sales performance by sales volume
    def analisar_desempenho_comerciais(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT c.CPF, f.Nome, c.Nivel_Persuasao,
                       COUNT(s.Codigo) as Total_Vendas,
                       COUNT(DISTINCT s.Cliente_CNPJ) as Total_Clientes_Distintos,
                       AVG(DATEDIFF(s.Data_Entrega, s.Data_Inicio)) as Media_Duracao_Projetos
                FROM Comercial c
                JOIN Funcionario f ON c.CPF = f.CPF
                LEFT JOIN Software s ON c.CPF = s.Comercial_CPF
                GROUP BY c.CPF
                ORDER BY Total_Vendas DESC, Nivel_Persuasao DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao analisar desempenho dos comerciais: {str(e)}")

    # 30. Identify most profitable client sectors
    def identificar_setores_lucrativos(self):
        try:
            with self.connection.cursor() as cursor:
                # This query assumes some way to calculate profit, using count as a proxy
                sql = """
                SELECT c.Setor_Atuacao, 
                       COUNT(s.Codigo) as Total_Softwares,
                       COUNT(DISTINCT c.CNPJ) as Total_Clientes,
                       AVG(DATEDIFF(s.Data_Entrega, s.Data_Inicio)) as Media_Duracao_Dias
                FROM Cliente c
                JOIN Software s ON c.CNPJ = s.Cliente_CNPJ
                GROUP BY c.Setor_Atuacao
                ORDER BY Total_Softwares DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao identificar setores mais lucrativos: {str(e)}")

    # =============================================
    # Control and Validation Queries
    # =============================================

    # 31. Validate if all software has at least one developer associated
    def validar_softwares_sem_desenvolvedores(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT s.Codigo, s.Nome, s.Data_Inicio, s.Data_Entrega, c.Nome as Cliente_Nome
                FROM Software s
                JOIN Cliente c ON s.Cliente_CNPJ = c.CNPJ
                LEFT JOIN DesenvolvimentoSoftware ds ON s.Codigo = ds.Software_Codigo
                WHERE ds.Desenvolvedor_CPF IS NULL
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao validar softwares sem desenvolvedores: {str(e)}")

    # 32. Check if all clients have registered software
    def verificar_clientes_sem_softwares(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT c.CNPJ, c.Nome, c.Setor_Atuacao
                FROM Cliente c
                LEFT JOIN Software s ON c.CNPJ = s.Cliente_CNPJ
                WHERE s.Codigo IS NULL
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao verificar clientes sem softwares: {str(e)}")

    # 33. Identify employees with no associated projects
    def identificar_funcionarios_sem_projetos(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT f.CPF, f.Nome, f.Cargo
                FROM Funcionario f
                LEFT JOIN (
                    SELECT ds.Desenvolvedor_CPF as CPF
                    FROM DesenvolvimentoSoftware ds
                    UNION
                    SELECT i.Designer_CPF as CPF
                    FROM IdealizacaoSoftware i
                    UNION
                    SELECT s.Comercial_CPF as CPF
                    FROM Software s
                    WHERE s.Comercial_CPF IS NOT NULL
                ) as Projetos ON f.CPF = Projetos.CPF
                WHERE Projetos.CPF IS NULL
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao identificar funcionários sem projetos: {str(e)}")

    # 34. Check the integrity of relationships between entities
    def verificar_integridade_relacionamentos(self):
        try:
            with self.connection.cursor() as cursor:
                # Check software without clients or sales staff
                sql_software = """
                SELECT s.Codigo, s.Nome, 
                       CASE WHEN s.Cliente_CNPJ IS NULL THEN 'Sem Cliente' ELSE 'OK' END as Status_Cliente,
                       CASE WHEN s.Comercial_CPF IS NULL THEN 'Sem Comercial' ELSE 'OK' END as Status_Comercial
                FROM Software s
                WHERE s.Cliente_CNPJ IS NULL OR s.Comercial_CPF IS NULL
                """
                cursor.execute(sql_software)
                softwares_problematicos = cursor.fetchall()

                # Check for orphaned records in relationship tables
                sql_dev = """
                SELECT ds.Desenvolvedor_CPF, ds.Software_Codigo
                FROM DesenvolvimentoSoftware ds
                LEFT JOIN DesenvolvedorSoftware d ON ds.Desenvolvedor_CPF = d.CPF
                LEFT JOIN Software s ON ds.Software_Codigo = s.Codigo
                WHERE d.CPF IS NULL OR s.Codigo IS NULL
                """
                cursor.execute(sql_dev)
                desenvolvedores_problematicos = cursor.fetchall()

                sql_designer = """
                SELECT i.Designer_CPF, i.Software_Codigo
                FROM IdealizacaoSoftware i
                LEFT JOIN Designer d ON i.Designer_CPF = d.CPF
                LEFT JOIN Software s ON i.Software_Codigo = s.Codigo
                WHERE d.CPF IS NULL OR s.Codigo IS NULL
                """
                cursor.execute(sql_designer)
                designers_problematicos = cursor.fetchall()

                return {
                    'softwares_problematicos': softwares_problematicos,
                    'desenvolvedores_problematicos': desenvolvedores_problematicos,
                    'designers_problematicos': designers_problematicos
                }
        except Exception as e:
            raise Exception(f"Erro ao verificar integridade dos relacionamentos: {str(e)}")

    # 35. Query the current status of all projects
    def consultar_status_projetos(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT s.Codigo, s.Nome, s.Data_Inicio, s.Data_Entrega,
                       c.Nome as Cliente_Nome,
                       CASE 
                           WHEN s.Data_Inicio IS NULL THEN 'Não Iniciado'
                           WHEN s.Data_Entrega IS NULL THEN 'Em Definição'
                           WHEN s.Data_Entrega < CURDATE() THEN 'Concluído'
                           WHEN DATEDIFF(s.Data_Entrega, CURDATE()) <= 7 THEN 'Entrega Próxima'
                           ELSE 'Em Andamento' 
                       END as Status,
                       CASE
                           WHEN s.Data_Inicio IS NULL OR s.Data_Entrega IS NULL THEN 0
                           WHEN s.Data_Entrega < CURDATE() THEN 100
                           ELSE ROUND(
                               (DATEDIFF(CURDATE(), s.Data_Inicio) * 100.0) / 
                               NULLIF(DATEDIFF(s.Data_Entrega, s.Data_Inicio), 0)
                           )
                       END as Porcentagem_Conclusao
                FROM Software s
                JOIN Cliente c ON s.Cliente_CNPJ = c.CNPJ
                ORDER BY 
                    CASE 
                        WHEN s.Data_Entrega < CURDATE() THEN 3
                        WHEN DATEDIFF(s.Data_Entrega, CURDATE()) <= 7 THEN 1
                        WHEN s.Data_Inicio IS NULL THEN 4
                        ELSE 2
                    END,
                    s.Data_Entrega
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Erro ao consultar status dos projetos: {str(e)}")

    # =============================================
    # Helper methods for connecting software with employees
    # =============================================

    # Associate a developer with a software
    def associar_desenvolvedor_software(self, desenvolvedor_cpf, software_codigo):
        try:
            with self.connection.cursor() as cursor:
                # Check if developer exists
                check_dev = "SELECT CPF FROM DesenvolvedorSoftware WHERE CPF = %s"
                cursor.execute(check_dev, (desenvolvedor_cpf,))
                if not cursor.fetchone():
                    raise Exception(f"Desenvolvedor com CPF {desenvolvedor_cpf} não encontrado")

                # Check if software exists
                check_sw = "SELECT Codigo FROM Software WHERE Codigo = %s"
                cursor.execute(check_sw, (software_codigo,))
                if not cursor.fetchone():
                    raise Exception(f"Software com Código {software_codigo} não encontrado")

                # Create association
                sql = """
                INSERT INTO DesenvolvimentoSoftware (Desenvolvedor_CPF, Software_Codigo)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (desenvolvedor_cpf, software_codigo))
                self.connection.commit()
                return True
        except pymysql.err.IntegrityError:
            # Association already exists
            return False
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao associar desenvolvedor ao software: {str(e)}")

    # Associate a designer with a software
    def associar_designer_software(self, designer_cpf, software_codigo):
        try:
            with self.connection.cursor() as cursor:
                # Check if designer exists
                check_des = "SELECT CPF FROM Designer WHERE CPF = %s"
                cursor.execute(check_des, (designer_cpf,))
                if not cursor.fetchone():
                    raise Exception(f"Designer com CPF {designer_cpf} não encontrado")

                # Check if software exists
                check_sw = "SELECT Codigo FROM Software WHERE Codigo = %s"
                cursor.execute(check_sw, (software_codigo,))
                if not cursor.fetchone():
                    raise Exception(f"Software com Código {software_codigo} não encontrado")

                # Create association
                sql = """
                INSERT INTO IdealizacaoSoftware (Designer_CPF, Software_Codigo)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (designer_cpf, software_codigo))
                self.connection.commit()
                return True
        except pymysql.err.IntegrityError:
            # Association already exists
            return False
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao associar designer ao software: {str(e)}")

    # Remove association between developer and software
    def remover_desenvolvedor_software(self, desenvolvedor_cpf, software_codigo):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                DELETE FROM DesenvolvimentoSoftware 
                WHERE Desenvolvedor_CPF = %s AND Software_Codigo = %s
                """
                cursor.execute(sql, (desenvolvedor_cpf, software_codigo))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao remover desenvolvedor do software: {str(e)}")

    # Remove association between designer and software
    def remover_designer_software(self, designer_cpf, software_codigo):
        # Remove association between designer and software (continued)
        try:
            with self.connection.cursor() as cursor:
                sql = """
                            DELETE FROM IdealizacaoSoftware 
                            WHERE Designer_CPF = %s AND Software_Codigo = %s
                            """
                cursor.execute(sql, (designer_cpf, software_codigo))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao remover designer do software: {str(e)}")

    # Example usage


if __name__ == "__main__":
    try:
        # Create an instance of the database manager
        db = SoftwareDBManager(host='localhost', user='root', password='password', database='SoftwareDB')

        # Example of adding a client
        cnpj = "12.345.678/0001-99"
        db.cadastrar_cliente(cnpj, "Empresa XYZ", "Tecnologia")

        # Example of adding an employee
        cpf = "123.456.789-00"
        db.registrar_funcionario(
            cpf, "João Silva", 30, "desenvolvedor",
            5000.00, {"stack": "Python, JavaScript, SQL"}
        )

        # Example of adding a software
        software_id = db.adicionar_software(
            "Sistema ERP",
            "Python, Django, React",
            "2025-01-15",
            "2025-06-30",
            "Gestão financeira, Controle de estoque, RH",
            None,  # comercial_cpf
            cnpj
        )

        # Associate developer with software
        db.associar_desenvolvedor_software(cpf, software_id)

        # Query all software for a client
        softwares = db.listar_softwares_por_cliente(cnpj)
        for sw in softwares:
            print(f"Software: {sw['Nome']}, Início: {sw['Data_Inicio']}, Entrega: {sw['Data_Entrega']}")

        # Generate a report of project status
        status = db.consultar_status_projetos()
        for projeto in status:
            print(f"Projeto: {projeto['Nome']}, Status: {projeto['Status']}, "
                  f"Conclusão: {projeto['Porcentagem_Conclusao']}%")

        print("Database operations completed successfully!")

    except Exception as e:
        print(f"Error: {str(e)}")
