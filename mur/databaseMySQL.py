
# Credentials
import user_config


def consulta_data_banco(table, filter = None):
    """Short summary.
    -----------------
    Realiza consulta na tabela especificada em table, buscando a data mais recente de dado;

    Caso haja necessidade de fazer um filtro na consulta para obter a data em realação
    à algum parâmetro, preencher filter = "código sql para o filtro", por exemplo:



    Parameters
    ----------
    table : string
        Tabela em que será realizada a consulta.
    filter : string (Opcional)
        Realiza consulta de data baseado em algum outros parâmetro/coluna
        ex:
        filter = "coluna = A"

        A query final será - SELECT max(datahora) WHERE coluna = A -

    Returns
    -------
    data = data de último registro da tabela especifica, de acordo com o especificado.
    """

    import mysql.connector as MySQL



    try:
        cnx = MySQL.connect(host = user_config.host,
                            user = user_config.username,
                            password = user_config.password,
                            database = user_config.database)

    except MySQL.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('MySQL: Usuário ou senha incorreta')
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("MySQL: Não existe database")
            return
        else:
            print('Error na conexão MySQL: ', err)
            return


    if cnx.is_connected():

        if filter:
            consulta_data = 'SELECT max(datahora) FROM %s WHERE %s' % (table, filter)

        else:
            consulta_data = 'SELECT max(datahora) FROM %s' % table



        cur = cnx.cursor()
        cur.execute(consulta_data)
        data_max = cur.fetchall()
        data_max = data_max[0][0]

        cur.close()
        cnx.close()

        return data_max



    else:
        return




#######################################################################################



def deleta_dado(table, condition):
    """Short summary.

    Deleta dados do banco de dados
    Parameters
    ----------
    table : string
        tabela em que serão deletados os dados
    condition : string
        string, em SQL, em que declara a condição
        para deletar o dado, por exemplo:

        'WHERE datahora >= xxxxxx'
        *** sempre verificar o padrão do atributo/varíavel
        que será usada na condição, usando o mesmo formato que
        está presente no banco.

    Returns
    -------
    None

    """

    import mysql.connector as MySQL
    import pandas as pd


    try:
        cnx = MySQL.connect(host = user_config.host,
                            user = user_config.username,
                            password = user_config.password,
                            database = user_config.database)

    except MySQL.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('MySQL: Usuário ou senha incorreta')
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("MySQL: Não existe database")
            return
        else:
            print('Error na conexão MySQL: ', err)
            return


    query_del = 'DELETE FROM %s %s' % (table, condition)

    cur = cnx.cursor()
    cur.execute(query_del)

    # commit
    cnx.commit()

    cur.close()
    cnx.close()




def insere_dado_banco(table, dados):
    """Short summary.
    Insere dados no banco de dados.

    Parameters
    ----------
    table : string
        Nome da tabela no banco de dados.
    dados : pandas dataframe
        Dataframe com os dados que serão inseridos. Os nomes das colunas
        deste dataframe devem ser os mesmos nomes que estão nas colunas
        da tabela. Apenas os dados das colunas em comum serão inseridas.

    Returns
    -------
    None

    """
    import mysql.connector as MySQL
    import pandas as pd
    import sqlalchemy
    from sqlalchemy.engine.reflection import Inspector
    #

    try:

        con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(user_config.username,
                                                    user_config.password,
                                                    user_config.host,
                                                    user_config.database))

    except MySQL.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('MySQL: Usuário ou senha incorreta')
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("MySQL: Não existe database")
            return
        else:
            print('Error na conexão MySQL: ', err)
            return



    inspector = Inspector.from_engine(con)
    if table in inspector.get_table_names():

        dados = dados.set_index('datahora')
        print(dados)

        try:
            dados.to_sql(con=con, name= table, if_exists='append')
        except Exception as erro_insere:
            print("Erro na inserção de dados.")
            print(erro_insere)
        else:
            print("Dados inseridos com sucesso!")

        return

    else:
        print("Tabela não existe no banco.")
