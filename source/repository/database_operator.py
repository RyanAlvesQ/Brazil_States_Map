class DatabaseOperations:
    def create_tables(self,connection):
        """
        Cria as tabelas necessárias no banco de dados
        """
        try:
            cursor = connection.cursor()

            # Criando o schema MAP, caso não exista
            create_schema_query = "CREATE SCHEMA IF NOT EXISTS MAP;"
            cursor.execute(create_schema_query)

            # Criando a tabela Map_infos no schema MAP
            create_table_query = """
            CREATE TABLE IF NOT EXISTS MAP.Map_infos (
                id SERIAL PRIMARY KEY,
                nome_usuario CHARACTER VARYING(255) NOT NULL,
                mapa_selecionado CHARACTER VARYING(255) NOT NULL
            );
            """
            cursor.execute(create_table_query)
            connection.commit()

            cursor.close()
            return "Tabelas criadas com sucesso!"
        except Exception as error:
            print(f"Erro ao criar tabelas: {error}")
            return "Erro ao criar tabelas."

    def insert_data(self,connection, nome_usuario, mapa_selecionado):
        """
        Insere os dados de nome do usuário e mapa selecionado na tabela Map_infos
        """
        try:
            cursor = connection.cursor()

            # Inserindo os dados na tabela Map_infos
            insert_query = "INSERT INTO MAP.Map_infos (nome_usuario, mapa_selecionado) VALUES (%s, %s)"
            cursor.execute(insert_query, (nome_usuario, mapa_selecionado))
            connection.commit()

            cursor.close()
            return "Dados inseridos com sucesso!"
        except Exception as error:
            print(f"Erro ao inserir dados: {error}")
            return "Erro ao inserir dados."
