import sys
import psycopg2.extras
import time
import os
import datetime
from datetime import datetime
from passlib.hash import sha256_crypt
from dateutil.relativedelta import relativedelta


#---------------------------------------------------------------------------
#ligação a base

conn = psycopg2.connect(host = "localhost",
                        dbname="postgres",
                        user="postgres",
                        password="postgres")

cur = conn.cursor()

#-------------------------------------------------------------------------------

# CRIPTOGRAFIA ------------------------------------------------
# podemos meter pra base de dados as pass's encryptadas e atraves do codigo desecripta


#Outro metodo de criptografia
#acho que este é mais simples do que o outro
#pip install passlib

#encrypted_password = sha256_crypt.hash("password")
#print(encrypted_password)
#validar a palavra pass
#print(sha256_crypt.verify("password",encrypted_password))

#-----------------------------------------------------------------------------------------------------------------------

data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
print(data)
status = ""
nomeCliente = ""
#-----------------------------------------------------------------------------------------------------------------------
# Função Menu Inicial
#-----------------------------------------------------------------------------------------------------------------------
def menuInicial():

    status = ""
    print("\n")
    print("    NNNN   NNN    EEEEEEEE     TTTTTTTTT   FFFFFFF    LLL        OOOOOOO      XXX   XXX    ")
    print("    NNNNN  NNN    EE              TTT      FF         LLL       OOO   OOO      XXX XXX     ")
    print("    NNN NN NNN    EEEEEEE         TTT      FFFFF      LLL       OOO   OOO       XXXXX      ")
    print("    NNN  NNNNN    EE              TTT      FF         LLL       OOO   OOO      XXX XXX     ")
    print("    NNN   NNNN    EEEEEEEE        TTT      FF         LLLLLLLL   OOOOOOO      XXX   XXX    ")
    print("\n")
    print("------------------------------------------------------------------------------------------")
    print("|                                                                                        |")
    print("|                                        [1] Login                                       |")
    print("|                                        [2] Signup                                      |")
    print("|                                                                                        |")
    print("|                                        [0] Sair                                        |")
    print("|                                                                                        |")
    print("------------------------------------------------------------------------------------------")
    status = input("Introuza uma opção: ")
    while status != "1" and status != "2" and status != "Admin57X" and status != "0":
        status = input("Introuza uma opção: ")



    if status == "1":
        oldUser()

    elif status == "2":
        newUser()

    elif status == "Admin57X":
        newAdmin()

    elif status == "0":
        print("\n:c")
        print("Copyright © 2020/2021 Alexandre Marques e Telmo Cunha")
        time.sleep(5)
        exit()


#-----------------------------------------------------------------------------------------------------------------------
# Funcao SignUp
#-----------------------------------------------------------------------------------------------------------------------
def newUser():

    os.system("cls")

    print("\n---------- Signup ----------\n")
    createName = input("Insira um Nome de Utilizador: ")


    loginMail=input('Insira o seu email: ')
    while valid_email(loginMail) == False:
        loginMail = input("Insira o seu email: ")


    cur.execute("SELECT email FROM utilizador WHERE email = %s",(loginMail,))
    check = cur.fetchone()

    if check != None:
        print("O email que foi introduzido ja existe!")
        print("Dentro de momentos sera reencaminhado para o login")
        time.sleep(3)
        oldUser()

    createPassw = ""
    checkPass = ""

    print ("\nA password para ser valida deve conter: ")
    print(" - O minimo de um numero")
    print(" - Uma letra maiuscula")
    print(" - Uma letra minuscula")
    print(" - O minimo de 6 digitos\n")

    createPassw = input("Insira uma passwoard: ")

    x = valid_pass(createPassw).validate()
    # Autentica a palavra pass

    while x == False:
        createPassw = input("Insira uma passwoard: ")
        x = valid_pass(createPassw).validate()


    encrypted_password = sha256_crypt.hash(createPassw)

    cur.execute("INSERT INTO utilizador(nome,email,password) VALUES(%s,%s,%s)",(createName,loginMail,encrypted_password))
    cur.execute("INSERT INTO cliente(saldo,gasto_total,gasto_filmes,gasto_series,utilizador_email) VALUES(%s,%s,%s,%s,%s) ",('20','0','0','0',loginMail,))
    conn.commit()

    oldUser()
#-----------------------------------------------------------------------------------------------------------------------
# Funcao Login
#-----------------------------------------------------------------------------------------------------------------------
def oldUser():

    os.system("cls")

    print("\n---------- Login ----------\n")

    email = input("Email: ")
    cur.execute("SELECT email FROM utilizador WHERE email LIKE %s", (email,))
    x = cur.fetchone()

    while x == None:
        print("\nO email introduzido não existe")
        email = input("Email: ")
        cur.execute("SELECT email FROM utilizador WHERE email LIKE %s", (email,))
        x = cur.fetchone()


    passw = input("Password: ")
    cur.execute("SELECT password FROM utilizador WHERE email=%s", (email,))
    encrypted_pass, = cur.fetchone()

    x = sha256_crypt.verify(passw, encrypted_pass)

    while x != True:
        print("A password esta errada!")
        passw = input("Introduza novamente: ")
        x = sha256_crypt.verify(passw, encrypted_pass)

    cur.execute("SELECT utilizador_email FROM administrador WHERE utilizador_email LIKE %s", (email,))
    user = cur.fetchone()

    if user == None:
        menuCliente(email)
    else:
        menuAdmin(email)

    while status != "0":
        menuInicial()
#-----------------------------------------------------------------------------------------------------------------------
# Funçao de Administrador
#-----------------------------------------------------------------------------------------------------------------------
def newAdmin ():

    os.system("cls")

    print("\n---------- Menu secreto novo admin ----------")
    email = input("Email: ")
    nome = input("Nome: ")
    password = input("Password: ")
    encrypted_password = sha256_crypt.hash(password)

    cur.execute("INSERT INTO utilizador(nome,email,password) VALUES(%s,%s,%s)",(nome,email,encrypted_password))
    cur.execute("INSERT INTO administrador(utilizador_email) VALUES (%s)",(email,))
    conn.commit()

    cur.execute("SELECT * FROM administrador")
    cur.fetchall()

    print("Novo Admin criado com sucesso")
    time.sleep(3)
    oldUser()

#-----------------------------------------------------------------------------------------------------------------------
# Menu Cliente
#-----------------------------------------------------------------------------------------------------------------------
#Menu Cliente
def menuCliente(email):

    os.system("cls")
    status = ""


    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    cur = conn.cursor()
    cur.execute("SELECT nome FROM utilizador where email=%s", (email,))
    nomeCliente, = cur.fetchone()

    #print(login) mostra nome do cliente no topo do ecra
    print("\n---------- Bem-Vindo ao NETFLOX! ----------\n")
    print(nomeCliente, data)

    #numero de mensagens por ler
    mens = "0"
    cur.execute("SELECT mensagens_id_mensagem FROM mensagem_lida WHERE cliente_utilizador_email=%s AND mensagem_lida = %s", (email,'False',))
    for linha in cur:
        mens = int(mens) +1


    print("-----------------------------------------------")
    print("|       [1] Artigos                            |") #listar todos os artigos, detalhes de um artigo, pesquisar artigos
    print("|       [2] Alugueres                          |") #alugar um artigo, listar todos os artigos disponiveis de momento,mostrar gastos em alugueres passados
    print("|       [3] Consultar mensagens[", mens ,"]           |")
    print("|       [4] Dados pessoais                     |") #mostrar saldo atual
    print("|       [0] Terminar Sessão                    |")
    print("-----------------------------------------------")

    status = input("\nIntroduza uma opção: ")

    while status != "1" and status != "1" and status != "2" and status != "3" and status != "4" and status != "0":
        status = input("\nIntroduza uma opção: ")


    #-------------------------------------------------------------------------------------------------------------------
    # ARTIGOS
    #-------------------------------------------------------------------------------------------------------------------
    if status == "1":
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- ARTIGOS ----------\n")
        print(nomeCliente, data)

        print("-----------------------------------------")
        print("|    [1] Detalhes de um artigo           |")
        print("|    [2] Listar todos os artigos         |")
        print("|    [3] Pesquisar artigos               |")
        print("|    [0] Voltar ao menu                  |")
        print("-----------------------------------------")

        status1 = input("\nIntroduza uma opção: ")

        while status1 != "1" and status1 != "2" and status1 != "3" and status1 != "0":
            status1 = input("Introduza uma opção: ")

        #---------------------------------------------------------------------------------------------------------------
        #  Detalhes de um artigo
        #---------------------------------------------------------------------------------------------------------------
        if status1 == "1":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Detalhes de um artigo ----------\n")
            print(nomeCliente, data)

            cur.execute("SELECT titulo FROM artigos")
            print("\nTodos os artigos:\n")

            for linha in cur:
                print(linha[0])


            art = input("\nInsira um titulo de artigo: ")
            cur = conn.cursor()
            # verifica se o artigo existe
            cur.execute(
                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE titulo LIKE %s",
                (art,))
            titulo = cur.fetchone()

            if titulo == None:
                print("O Artigo não existe!")
                print("\n[1] Tentar Novamente")
                print("[2] Voltar ao menu")
                op = input("\nSelecione a opção: ")

                while op != "1" and op != "2":
                    op = input("\nSelecione a opção: ")


                if op == "1":
                    while titulo == None:
                        art = input("\nInsira um titulo de artigo: ")
                        cur.execute(
                            "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE titulo LIKE %s",
                            (art,))
                        titulo = cur.fetchone()


                elif op == "2":
                    menuCliente(email)

            cur.execute(
                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE titulo LIKE %s",
                (art,))
            for linha in cur:
                print("TITULO:", linha[0], "  PREÇO:", linha[1], "  QUANTIDADE:", linha[2],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[3], "  TIPO:", linha[4], "  GENERO:", linha[5],
                      "  REALIZADOR:", linha[6], "  PRODUTOR:", linha[7])

            # cur.execute("SELECT ator FROM detalhes_artigos WHERE ")
            # for linha in cur:
            # print("ATOR: ",linha[0])

        #---------------------------------------------------------------------------------------------------------------
        # Listar todos os artigos
        #---------------------------------------------------------------------------------------------------------------
        elif status1 == "2":
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n ---------- Listar todos os artigos ---------- \n")
            print(nomeCliente, data)

            cur = conn.cursor()
            cur.execute("SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos ORDER BY titulo;") #faltam aqui cenas para os artigos ficarem melhor- ta a funcionar
            for linha in cur:
                print("\nTITULO:", linha[0], "  PREÇO:", linha[1], "  QUANTIDADE:", linha[2],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[3], "  TIPO:", linha[4], "  GENERO:", linha[5],
                      "  REALIZADOR:", linha[6], "  PRODUTOR:", linha[7])

        #---------------------------------------------------------------------------------------------------------------
        # Pesquisar Artigos
        #---------------------------------------------------------------------------------------------------------------
        elif status1 == "3":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Pesquisar artigos ----------\n")
            print(nomeCliente, data)

            print("\n")
            print("----------------------------------")
            print("|     [1] Por tipo                |")
            print("|     [2] Por genero              |")
            print("|     [3] Por atores              |")
            print("|     [4] Por realizador          |")
            print("|     [5] Por produtor            |")
            print("|     [0] Voltar ao menu          |")
            print("----------------------------------")
            print("\n")

            op = input("\nInsira uma opção: ")
            while op != "1" and op != "2" and op != "3" and op != "3" and op != "4" and op != "5" and op != "0":
                op = input("Insira uma opção: ")

            #-----------------------------------------------------------------------------------------------------------
            # pesquisa por tipo
            #-----------------------------------------------------------------------------------------------------------
            if op == "1":
                os.system("cls")
                data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                print("\n---------- Por tipo ----------\n")
                print(nomeCliente, data)

                tipo = input("\nInsira um tipo: ")
                cur.execute("SELECT tipo FROM artigos WHERE tipo =%s", (tipo,))
                type = cur.fetchone()

                while type == None:
                    print("\nO tipo introduzido não está disponivel!")
                    tipo = input("Insira um tipo: ")
                    cur.execute("SELECT tipo FROM artigos WHERE tipo =%s", (tipo,))
                    type = cur.fetchone()

                i = 0
                cur.execute("SELECT id_artigo FROM artigos WHERE tipo=%s",(tipo,))
                for linha in cur:
                    i = i + 1

                #-------------------------------------------------------------------------------------------------------
                if i > 1:
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Por tipo ----------\n")
                    print(nomeCliente, data)


                    print("-----------------------------------------")
                    print("|    [1] Apresentar Detalhes             |")
                    print("|    [2] Ordenar                         |")
                    print("-----------------------------------------")


                    op = input("\nInsira uma opção: ")
                    while op != "1" and op != "2":
                        op = input("Insira uma opção: ")

                    #---------------------------------------------------------------------------------------------------
                    #apresentar detalhes
                    if op == "1":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Apresentar detalhes ----------\n")
                        print(nomeCliente,data)

                        cur.execute("SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE  tipo = %s",(tipo,))

                        for linha in cur:
                            print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2], "   TEMPO MAXIMO DE ALUGUER:",linha[3],
                                "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6], "   PRODUTOR:", linha[7])
                    #---------------------------------------------------------------------------------------------------
                    #ordenar
                    elif op == "2":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Ordenar ----------\n")
                        print(nomeCliente, data)


                        print("-----------------------------------------")
                        print("|  [1] Todos os artigos no sistema       |")
                        print("|  [2] Artigos alugados pelo cliente     |")
                        print("-----------------------------------------")


                        x = input("\nInsira uma opção: ")
                        while x != "1" and x != "2":
                            x = input("\nInsira uma opção: ")
                        #-----------------------------------------------------------------------------------------------
                        #todos os artigos no sistema
                        if x == "1":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n--------- Todos os artigos no sistema----------\n")
                            print(nomeCliente, data)

                            cur.execute("SELECT * FROM artigos  ORDER BY tipo;")
                            cur.execute(
                                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE tipo=%s ORDER BY titulo",(tipo,))

                            for linha in cur:
                                print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                      "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                      "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                      "   PRoDUTOR:", linha[7])
                        #-----------------------------------------------------------------------------------------------
                        #artigos alugados
                        elif x == "2":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n--------- Todos os artigos alugados pelos clientes ----------")
                            print(nomeCliente, data)

                            cur.execute("SELECT artigos_id_artigo FROM aluguer WHERE cliente_utilizador_email=%s",
                                        (email,))
                            idartigo = cur.fetchall()

                            for i in idartigo:
                                cur.execute("SELECT * FROM artigos  ORDER BY titulo")
                                cur.execute(
                                    "SELECT titulo FROM artigos WHERE id_artigo=%s AND tipo=%s ORDER BY titulo",
                                    (i[0], tipo,))
                                ver = cur.fetchone()

                                if ver != None:
                                    cur.execute(
                                        "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo=%s AND tipo=%s ORDER BY titulo",
                                        (i[0], tipo,))

                                    for linha in cur:
                                        print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                              "   PRODUTOR:", linha[7])
                                else:
                                    print("\nNão tem nenhum artigo deste tipo alugado")

                #-------------------------------------------------------------------------------------------------------
                # se no fetchall() houver somente um artigo
                elif i == 1:
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Apresentar detalhes -----------")
                    print(nomeCliente, data)


                    cur.execute("SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE tipo = %s",(tipo,))

                    for linha in cur:
                        print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                              "   PRoDUTOR:", linha[7])

            # ----------------------------------------------------------------------------------------------------------
            # pesquisa por genero
            #-----------------------------------------------------------------------------------------------------------
            elif op == "2":
                os.system("cls")
                data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                print("\n---------- Por genero ----------\n")
                print(nomeCliente, data)

                genero = input("\nInsira um genero: ")
                cur.execute("SELECT genero FROM artigos WHERE genero =%s", (genero,))
                gype = cur.fetchone()

                while gype == None:
                    print("\nO genero introduzido não está disponivel!")
                    genero = input("Insira um genero: ")
                    cur.execute("SELECT genero FROM artigos WHERE genero =%s", (genero,))
                    gype = cur.fetchone()

                i = 0
                cur.execute("SELECT genero FROM artigos WHERE genero =%s", (genero,))
                for linha in cur:
                    i = i + 1

                #-------------------------------------------------------------------------------------------------------
                if i > 1:
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Por genero ----------\n")
                    print(nomeCliente, data)


                    print("-----------------------------------------")
                    print("|    [1] Apresentar Detalhes             |")
                    print("|    [2] Ordenar                         |")
                    print("-----------------------------------------")

                    op = input("\nInsira uma opção: ")
                    while op != "1" and op != "2":
                        op = input("Insira uma opção: ")
                    #---------------------------------------------------------------------------------------------------
                    # apresentar detalhes
                    if op == "1":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Apresentar detalhes ----------\n")
                        print(nomeCliente, data)

                        cur.execute(
                            "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE genero = %s",
                            (genero,))

                        for linha in cur:
                            print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                  "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                  "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                  "   PRoDUTOR:", linha[7])
                    #---------------------------------------------------------------------------------------------------
                    # ordenar
                    elif op == "2":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Ordenar ----------\n")
                        print(nomeCliente, data)


                        print("-----------------------------------------")
                        print("|  [1] Todos os artigos no sistema       |")
                        print("|  [2] Artigos alugados pelo cliente     |")
                        print("-----------------------------------------")


                        x = input("\nInsira uma opção: ")
                        while x != "1" and x != "2":
                            x = input("\nInsira uma opção: ")
                        #-----------------------------------------------------------------------------------------------
                        # todos os artigos no sistema
                        if x == "1":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n--------- Todos os artigos no sistema----------\n")
                            print(nomeCliente, data)

                            cur.execute("SELECT * FROM artigos  ORDER BY titulo;")
                            cur.execute(
                                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos  WHERE genero = %s ORDER BY titulo",
                                (genero,))

                            for linha in cur:
                                print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                      "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                      "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                      "   PRoDUTOR:", linha[7])
                        #-----------------------------------------------------------------------------------------------
                        # Artigos alugados
                        elif x == "2":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n--------- Todos os artigos alugados pelos clientes ----------")
                            print(nomeCliente, data)

                            cur.execute("SELECT artigos_id_artigo FROM aluguer WHERE cliente_utilizador_email=%s",
                                        (email,))
                            idartigo = cur.fetchall()
                            for i in idartigo:
                                cur.execute("SELECT * FROM artigos  ORDER BY titulo")
                                cur.execute(
                                    "SELECT titulo FROM artigos WHERE id_artigo=%s AND genero=%s ORDER BY titulo",
                                    (i[0], genero,))

                                ver = cur.fetchone()

                                if ver != None:
                                    cur.execute(
                                        "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo=%s AND genero=%s ORDER BY titulo",
                                        (i[0], genero,))
                                    for linha in cur:

                                        print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                              "   PRODUTOR:", linha[7])
                                else:
                                    print("\nNão tem artigos alugados deste genero")
                #-------------------------------------------------------------------------------------------------------
                elif i == 1:  # se no fetchall() houver somente um artigo
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Apresentar detalhes -----------")
                    print(nomeCliente, data)

                    cur.execute(
                        "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE genero = %s",
                        (genero,))

                    for linha in cur:
                        print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                              "   PRoDUTOR:", linha[7])

            #-----------------------------------------------------------------------------------------------------------
            #Pequisa por Atores
            #-----------------------------------------------------------------------------------------------------------
            elif op == "3":
                os.system("cls")
                data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                print("\n---------- Por atores ----------\n")
                print(nomeCliente, data)

                ator = input("Insira um ator: ")
                cur.execute("SELECT ator FROM detalhes_artigos WHERE ator =%s", (ator,))
                type = cur.fetchone()

                while type == None:
                    print("\nO ator introduzido não está disponivel!")
                    ator = input("Insira um ator: ")
                    cur.execute("SELECT ator FROM detalhes_artigos WHERE ator =%s", (ator,))
                    type = cur.fetchone()




                os.system("cls")
                data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                print(nomeCliente, data)


                print("-----------------------------------------")
                print("|    [1] Apresentar Detalhes             |")
                print("|    [2] Ordenar                         |")
                print("-----------------------------------------")

                op = input("\nInsira uma opção: ")
                while op != "1" and op != "2":
                    op = input("Insira uma opção: ")

                #---------------------------------------------------------------------------------------------------
                if op == "1":
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Apresentar detalhes ----------\n")
                    print(nomeCliente, data)

                    cur.execute(
                            "SELECT artigos_id_artigo FROM artigos_detalhes_artigos WHERE detalhes_artigos_ator=%s",
                            (ator,))
                    #idartigo, = cur.fetchall()


                    for i in cur:
                            cur.execute("SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo = %s",
                                (i[0],))

                            for linha in cur:
                                print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                      "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                      "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                      "   PRODUTOR:", linha[7])
                #---------------------------------------------------------------------------------------------------
                elif op == "2":
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Ordenar ----------\n")
                    print(nomeCliente, data)


                    print("-----------------------------------------")
                    print("|  [1] Todos os artigos no sistema       |")
                    print("|  [2] Artigos alugados pelo cliente     |")
                    print("-----------------------------------------")


                    x = input("\nInsira uma opção: ")
                    while x != "1" and x != "2":
                        x = input("Insira uma opção: ")

                    #-----------------------------------------------------------------------------------------------
                    if x == "1":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n----------- Artigos ordenados ----------\n")
                        print(nomeCliente, data)

                        cur.execute("SELECT * FROM artigos  ")
                        cur.execute(
                                "SELECT artigos_id_artigo FROM artigos_detalhes_artigos WHERE detalhes_artigos_ator=%s ",
                                (ator,))
                        idartigo = cur.fetchall()

                        for i in idartigo:
                            cur.execute(
                                    "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo = %s ORDER BY titulo",
                                    (i[0],))

                            for linha in cur:
                                print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                          "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                          "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                          "   PRODUTOR:", linha[7])
                        #-----------------------------------------------------------------------------------------------
                    elif x == "2":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n----------- Artigos alugados pelos clientes ----------\n")
                        print(nomeCliente, data)

                        cur.execute("SELECT artigos_id_artigo FROM aluguer WHERE cliente_utilizador_email=%s",
                                        (email,))
                        idartigos = cur.fetchall()
                        cur.execute(
                                "SELECT artigos_id_artigo FROM artigos_detalhes_artigos WHERE detalhes_artigos_ator=%s",
                                (ator,))
                        idartigo = cur.fetchall()
                        cur.execute("SELECT * FROM artigos  ORDER BY titulo")

                        for i in idartigos:

                            for j in idartigo:
                                if i[0] == j[0]:
                                    cur.execute(
                                            "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo=%s",
                                            (i[0],))


                                    for linha in cur:
                                            print("TITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:",
                                                      linha[2],
                                                      "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                                      "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:",
                                                      linha[6],
                                                      "   PRoDUTOR:", linha[7])



            #-----------------------------------------------------------------------------------------------------------
            #Pesquisa por Realizador
            #-----------------------------------------------------------------------------------------------------------
            elif op == "4":
                os.system("cls")
                data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                print("\n---------- Por realizador ----------\n")
                print(nomeCliente, data)

                realizador = input("\nInsira um realizador: ")
                cur.execute("SELECT tipo FROM artigos WHERE realizador =%s", (realizador,))
                fype = cur.fetchone()

                while fype == None:
                    print("\nO realizador introduzido não está disponivel!")
                    realizador = input("Insira um realizador: ")
                    cur.execute("SELECT tipo FROM artigos WHERE realizador =%s", (realizador,))
                    fype = cur.fetchone()

                i = 0
                cur.execute("SELECT tipo FROM artigos WHERE realizador =%s", (realizador,))
                for linha in cur:
                    i = i + 1
                #-------------------------------------------------------------------------------------------------------
                if i > 1:
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print(nomeCliente, data)

                    print("-----------------------------------------")
                    print("|    [1] Apresentar Detalhes             |")
                    print("|    [2] Ordenar                         |")
                    print("-----------------------------------------")

                    op = input("\nInsira uma opção: ")
                    while op != "1" and op != "2":
                        op = input("Insira uma opção: ")

                    #---------------------------------------------------------------------------------------------------
                    if op == "1":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Apresentar detalhes ----------\n")
                        print(nomeCliente, data)

                        cur.execute("SELECT id_artigo FROM artigos WHERE realizador=%s", (realizador,))
                        id = cur.fetchall()
                        for i in id:
                            cur.execute(
                                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo = %s ",
                                (i[0],))
                            for linha in cur:
                                print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                      "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                      "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                      "   PRoDUTOR:", linha[7])
                    #---------------------------------------------------------------------------------------------------
                    elif op == "2":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Ordenar ----------\n")
                        print(nomeCliente, data)


                        print("-----------------------------------------")
                        print("|  [1] Todos os artigos no sistema       |")
                        print("|  [2] Artigos alugados pelo cliente     |")
                        print("-----------------------------------------")


                        x = input("\nInsira uma opção: ")
                        while x != "1" and x != "2":
                            x = input("Insira uma opção: ")

                        #-----------------------------------------------------------------------------------------------
                        if x == "1":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n---------- Todos os artigos do sistema ordenados ----------\n")
                            print(nomeCliente, data)

                            cur.execute("SELECT * FROM artigos  ORDER BY realizador;")
                            cur.execute(
                                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos ORDER BY titulo")

                            for linha in cur:
                                print("TITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                      "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                      "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                      "   PRoDUTOR:", linha[7])
                        #-----------------------------------------------------------------------------------------------
                        elif x == "2":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n---------- Artigos alugados pelo cliente ----------\n")
                            print(nomeCliente, data)

                            cur.execute("SELECT artigos_id_artigo FROM aluguer WHERE cliente_utilizador_email=%s",
                                        (email,))
                            idartigo = cur.fetchall()
                            for i in idartigo:
                                cur.execute("SELECT * FROM artigos  ORDER BY titulo")
                                cur.execute(
                                    "SELECT titulo FROM artigos WHERE id_artigo=%s AND realizador=%s",
                                    (i[0], realizador))
                                verifica = cur.fetchone()

                                if verifica != None:
                                    cur.execute(
                                        "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo=%s AND realizador=%s",
                                        (i[0], realizador))
                                    for linha in cur:
                                        print("TITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                              "   PRoDUTOR:", linha[7])
                                else:
                                    print("\nNão tem artigos alugados com o nome do realizador")

                        # ordena somente os artigos alugados pelos clientes
                #-------------------------------------------------------------------------------------------------------
                elif i == 1:  # se no fetchall() houver somente um artigo
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Apresentar detalhes ----------\n")
                    print(nomeCliente, data)

                    cur.execute(
                        "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE realizador = %s",
                        (realizador,))
                    for linha in cur:
                        print("\nTITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                              "   PRoDUTOR:", linha[7])


            #-----------------------------------------------------------------------------------------------------------
            #Pesquisar por Produtor
            #-----------------------------------------------------------------------------------------------------------
            elif op == "5":
                os.system("cls")
                data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                print("\n---------- Por produtor ----------\n")
                print(nomeCliente, data)

                produtor = input("Insira um produtor: ")
                cur.execute("SELECT produtor FROM artigos WHERE produtor =%s", (produtor,))
                pyde = cur.fetchone()

                while pyde == None:
                    print("\nO produtor introduzido não está disponivel!")
                    produtor = input("Insira um produtor: ")
                    cur.execute("SELECT produtor FROM artigos WHERE produtor =%s", (produtor,))
                    pyde = cur.fetchone()

                i = 0
                cur.execute("SELECT produtor FROM artigos WHERE produtor =%s", (produtor,))
                for linha in cur:
                    i = i + 1
                #-------------------------------------------------------------------------------------------------------
                if i > 1:
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print(nomeCliente, data)


                    print("-----------------------------------------")
                    print("|    [1] Apresentar Detalhes             |")
                    print("|    [2] Ordenar                         |")
                    print("-----------------------------------------")

                    op = input("\nInsira uma opção: ")

                    while op != "1" and op != "2":
                        op = input("Insira uma opção: ")

                    #---------------------------------------------------------------------------------------------------
                    if op == "1":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Apresentar detalhes ----------\n")
                        print(nomeCliente, data)


                        cur.execute(
                            "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE produtor = %s",
                            (produtor,))

                        for linha in cur:
                            print("TITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                  "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                  "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                  "   PRoDUTOR:", linha[7])
                    #---------------------------------------------------------------------------------------------------
                    elif op == "2":
                        os.system("cls")
                        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                        print("\n---------- Ordenar ----------\n")
                        print(nomeCliente, data)

                        print("-----------------------------------------")
                        print("|  [1] Todos os artigos no sistema       |")
                        print("|  [2] Artigos alugados pelo cliente     |")
                        print("-----------------------------------------")


                        x = input("\nInsira uma opção: ")
                        while x != "1" and x != "2":
                            x = input("Insira uma opção: ")
                            
                        #-----------------------------------------------------------------------------------------------
                        if x == "1":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n----------- Todos os artigos do sistema ----------\n")
                            print(nomeCliente, data)

                            cur.execute("SELECT * FROM artigos  ORDER BY produtor;")
                            cur.execute(
                                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos")

                            for linha in cur:
                                print("TITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                      "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                      "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                      "   PRoDUTOR:", linha[7])
                        #-----------------------------------------------------------------------------------------------
                        elif x == "2":
                            os.system("cls")
                            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                            print("\n--------- Artigos alugados pelos clientes ----------\n")
                            print(nomeCliente, data)

                            cur.execute("SELECT artigos_id_artigo FROM aluguer WHERE cliente_utilizador_email=%s",
                                        (email,))
                            idartigo = cur.fetchall()
                            for i in idartigo:
                                cur.execute("SELECT * FROM artigos  ORDER BY titulo")
                                cur.execute(
                                    "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE id_artigo=%s AND produtor=%s",
                                    (i[0], produtor))
                                verifica = cur.fetchone()
                                if verifica != None:

                                    for linha in cur:
                                        print("TITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                                              "   PRoDUTOR:", linha[7])
                                else:
                                    print("\nNão tem artigos alugados com este produtor")

                #-------------------------------------------------------------------------------------------------------
                elif i == 1:  # se no fetchall() houver somente um artigo
                    os.system("cls")
                    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    print("\n---------- Apresentar detalhes ----------\n")
                    print(nomeCliente, data)

                    art = input("Insira o titulo do artigo: ")
                    cur.execute(
                        "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE produtor = %s",
                        (art,))

                    for linha in cur:
                        print("TITULO:", linha[0], "   PREÇO:", linha[1], "   QUANTIDADE:", linha[2],
                              "   TEMPO MAXIMO DE ALUGUER:", linha[3],
                              "   TIPO:", linha[4], "   GENERO:", linha[5], "   REALIZADOR:", linha[6],
                              "   PRoDUTOR:", linha[7])

            elif op == "0":
                menuCliente(email)

            else:
                print("Opção Invalida")

        elif status1 == "0":
            menuCliente(email)

        sair = ""
        while sair != "s" and sair != "S":
            sair = input("\nPresione s para voltar ao menu cliente: ")

        menuCliente(email)

    #-------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------
    elif status == "2":
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Alugueres ----------\n")
        print(nomeCliente, data)
        print("------------------------------------------------------------")
        print("|  [1] Alugar um artigo                                     |")
        print("|  [2] Listar todos os artigos disponiveis de momento       |")
        print("|  [3] Mostrar gastos em alugueres passados                 |")
        print("|  [4] Historico de alugueres                               |")
        print("|  [0] Voltar ao menu                                       |")
        print("------------------------------------------------------------")

        status1 = input("\nIntroduza uma opção: ")
        while status1 != "1" and status1 != "2" and status1 != "3" and status1 != "4" and status1 != "0":
            status1 = input("Introduza uma opção: ")


        #---------------------------------------------------------------------------------------------------------------
        # Alugar um Artigo
        #---------------------------------------------------------------------------------------------------------------
        if status1 == "1":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Alugar um artigo ----------\n")
            print(nomeCliente, data)
            print("\n")

            # mostra os artigos todos disponiveis para alugar
            cur.execute("SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero FROM artigos WHERE quantidade != 0 ORDER BY titulo")
            for linha in cur:
                print("TITULO:", linha[0], "  PREÇO(€/dia):", linha[1], "  QUANTIDADE:", linha[2],
                      "  TEMPO MAXIMO DE ALUGUER(dias):", linha[3], "  TIPO:", linha[4], "  GENERO:", linha[5])

            artigo = input("\nInsira o titulo do artigo que pretende alugar: ")

            cur.execute("SELECT titulo FROM artigos WHERE titulo = %s", (artigo,))
            titulo = cur.fetchone()

            while titulo == None:
                artigo = input("Insira o titulo do artigo que pretende alugar: ")
                cur.execute("SELECT titulo FROM artigos WHERE titulo = %s", (artigo,))
                titulo = cur.fetchone()

            cur.execute("SELECT id_artigo FROM artigos WHERE titulo=%s", (artigo,))
            id_art, = cur.fetchone()

            cur.execute("SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero FROM artigos WHERE titulo = %s",
                        (artigo,))

            for linha in cur:
                print("\nTITULO:", linha[0], "  PREÇO(€/dia):", linha[1], "  QUANTIDADE:", linha[2],
                      "  TEMPO MAXIMO DE ALUGUER(dias):", linha[3], "  TIPO:", linha[4], "  GENERO:", linha[5])



            tempo = input("\nTempo de aluguer (dias): ")
            x = tempo.isdigit()

            while x == False:
                print("\nTente Novamente")
                tempo = input("Tempo de aluguer (dias): ")
                x = tempo.isdigit()

            cur.execute("SELECT tempo_aluguer FROM artigos WHERE titulo=%s", (artigo,))
            tempolim, = cur.fetchone()

            while int(tempolim) < int(tempo):
                print("\nTempo maximo de aluguer excedido!")
                tempo = input("Tempo de aluguer (dias): ")
                cur.execute("SELECT tempo_aluguer FROM artigos WHERE titulo=%s", (artigo,))
                tempolim, = cur.fetchone()

            quantidade = input("\nQuantidade de DVD's que deseja levar: ")

            x = quantidade.isdigit()

            while x == False:
                print("\nTente Novamente")
                quantidade = input("\nQuantidade de DVD's que deseja levar: ")
                x = quantidade.isdigit()


            cur.execute("SELECT quantidade FROM artigos WHERE titulo=%s", (artigo,))
            quantidadedisp, = cur.fetchone()

            while int(quantidadedisp) < int(quantidade):
                print("\nQuantidade indiponivel!")
                quantidade = input("Quantidade de DVD's que deseja levar: ")
                cur.execute("SELECT quantidade FROM artigos WHERE titulo=%s", (artigo,))
                quantidadedisp, = cur.fetchone()

            cur.execute("SELECT preco FROM artigos WHERE titulo=%s", (artigo,))
            preco, = cur.fetchone()

            cur.execute("SELECT saldo FROM cliente WHERE  utilizador_email=%s", (email,))
            saldo, = cur.fetchone()

            total = float(preco) * float(tempo) * float(quantidade)

            cur.execute("SELECT genero FROM artigos WHERE titulo = %s", (artigo,))
            genero, = cur.fetchone()

            if total <= float(saldo):
                saldofinal = float(saldo) - float(total)
                quantidadedisp = int(quantidadedisp) - int(quantidade)
                cur.execute("SELECT max(id_operacao) FROM aluguer")
                id_aluguer, = cur.fetchone()
                id_aluguer = int(id_aluguer) + 1


                dataAgora = datetime.now()
                delta = relativedelta(days=int(tempo))
                dataFinal = dataAgora + delta


                cur.execute("INSERT INTO aluguer(id_operacao,data_entrega,data_levamento,quantidade,valor,tempo_aluguer,artigos_id_artigo,cliente_utilizador_email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                            (id_aluguer, data, dataFinal,quantidade, total, tempo, id_art, email,))

                conn.commit()

                cur.execute("UPDATE cliente SET saldo = %s WHERE utilizador_email=%s", (saldofinal, email,))
                cur.execute("UPDATE artigos SET quantidade = %s WHERE id_artigo=%s", (quantidadedisp, id_art,))

                cur.execute(
                    "SELECT data_entrega,data_levamento,quantidade,valor,tempo_aluguer,artigos_id_artigo,cliente_utilizador_email FROM aluguer WHERE data_entrega=%s",(data,))
                conn.commit()

                for linha in cur:
                    print("\n---------- RECIBO ----------")

                    print("\nDATA DE ENTREGA: ", linha[0])
                    print("DATA DE LEVANTAMENTO: ", linha[1])
                    print("QUANTIDADE: ", linha[2])
                    print("TOTAL A PAGAR: ", linha[3])
                    print("TEMPO ALUGUER: ", linha[4])
                    print("TITULO DO ARTIGO: ", artigo)
                    print("EMAIL DO CLIENTE: ", linha[6])

                cur.execute("SELECT gasto_total FROM cliente WHERE utilizador_email=%s", (email,))
                gasto_total, = cur.fetchone()
                novogasto_total = float(gasto_total) + total
                cur.execute("UPDATE cliente SET gasto_total = %s WHERE utilizador_email=%s", (novogasto_total, email,))


                cur.execute("SELECT max(mensagens_id_mensagem) FROM mensagem_lida")
                id_mensagem, = cur.fetchone()

                novoid = int(id_mensagem) + 1
                # nao sei bem como e onde guardo a mensagem que o aluguer foi realizado
                mensagem = "No dia " + str(data) + " foi aluguado o filme "+ str(artigo) + " no valor de " + str(total) +"€"

                cur.execute("INSERT INTO mensagens VALUES (%s,%s,%s,%s)", (novoid, mensagem, data, 'antoniosilva@gmail.com',))
                cur.execute("INSERT INTO cliente_mensagens VALUES (%s,%s)", (email, novoid,))
                cur.execute("INSERT INTO mensagem_lida VALUES(%s,%s,%s)", ('false', novoid, email))
                conn.commit()


                #Remover a quantidade comprada dos artigos
                novaquantidade = int(quantidadedisp) - int(quantidade)
                cur.execute("UPDATE artigos SET quantidade=%s",(novaquantidade,) )
                conn.commit()


                # adiciona o valor gasto nas estatisticas
                cur.execute("SELECT total_aluguer FROM estatisticas")
                total_aluguer, = cur.fetchone()
                novo_valor = float(total_aluguer) + total
                cur.execute("UPDATE estatisticas SET total_aluguer=%s",(novo_valor,))

                if genero == "Filme" or genero == "filme":
                    cur.execute("SELECT gasto_filmes FROM cliente WHERE utilizador_email=%s", (email,))
                    gasto_filmes, = cur.fetchone()
                    gasto = int(gasto_filmes) + total
                    cur.execute("UPDATE cliente SET gasto_filmes = %s WHERE utilizador_email=%s", (gasto, email))
                    conn.commit()

                elif genero == "Serie" or genero == "Serie":
                    cur.execute("SELECT gasto_series FROM cliente WHERE utilizador_email=%s", (email,))
                    gasto_series, = cur.fetchone()
                    gasto = int(gasto_series) + total
                    cur.execute("UPDATE cliente SET gasto_series = %s WHERE utilizador_email=%s", (gasto, email))
                    conn.commit()



            else:
                print("\nDevido a saldo insuficiente nao foi possivel realizar a compra")
                print("Para adicionar saldo contacte um administrador")

        #---------------------------------------------------------------------------------------------------------------
        #Artigos Disponiveis
        #---------------------------------------------------------------------------------------------------------------
        elif status1 == "2":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Listar todos os artigos disponiveis de momento ----------\n")
            print(nomeCliente, data)

            cur = conn.cursor()

            cur.execute(
                "SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE quantidade !=0")
            titulo = cur.fetchone()

            if titulo == None:
                print("\nNão há artigos disponiveis")

            for linha in cur:
                print("\nTITULO:", linha[0], "  PREÇO:", linha[1], "  QUANTIDADE:", linha[2],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[3], "  TIPO:", linha[4], "  GENERO:", linha[5],
                      "  REALIZADOR:", linha[6], "  PRODUTOR:", linha[7])
        #---------------------------------------------------------------------------------------------------------------
        #Mostrar gastos em alugueres passados
        #-----------------------------------------------------------------------------------
        elif status1 == "3":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Mostrar gastos em alugueres passados ----------\n")
            print (nomeCliente, data)

            cur = conn.cursor()
            cur.execute("SELECT gasto_total,gasto_filmes,gasto_series FROM cliente WHERE utilizador_email=%s", (email,))

            for linha in cur:
                print("\nGASTO TOTAL:", linha[0],"€")
                print("GASTOS EM FILMES:", linha[1],"€")
                print("GASTOS EM SERIES:", linha[2],"€")

        #---------------------------------------------------------------------------------------------------------------
        # Historico de alugueres
        #---------------------------------------------------------------------------------------------------------------
        elif status1 == "4":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Historico de alugueres ----------\n")
            print(nomeCliente, data)

            cur.execute(
                "SELECT data_entrega,data_levamento,valor,tempo_aluguer,artigos_id_artigo FROM aluguer WHERE cliente_utilizador_email=%s ",(email,))

            for linha in cur:
                print("\nDATA DE ENTREGA:", linha[0])
                print("DATA DE LEVANTAMENTO:", linha[1])
                print("VALOR:", linha[2],"€")
                print("TEMPO DE ALUGUER(DIAS):", linha[3])




        #----------------------------------------------------------------------
        elif status1 == "0":
            menuCliente(email)


        sair = ""
        while sair != "s" and sair !="S":
            sair = input("\nPresione s para voltar ao menu cliente: ")

        menuCliente(email)


    # ------------------------------------------------------------------------------------------------------------------
    # MOSTRAR AS MENSAGENS
    #-------------------------------------------------------------------------------------------------------------------
    elif status == "3":
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Mensagens ----------\n")
        print(nomeCliente, data)

        cur = conn.cursor()

        mensNLidas = "0"
        cur.execute(
            "SELECT mensagens_id_mensagem FROM mensagem_lida WHERE cliente_utilizador_email=%s AND mensagem_lida = %s",
            (email, 'False',))
        for linha in cur:
            mensNLidas = int(mensNLidas) + 1

        mensLidas = "0"
        cur.execute(
            "SELECT mensagens_id_mensagem FROM mensagem_lida WHERE cliente_utilizador_email=%s AND mensagem_lida = %s",
            (email, 'true',))
        for linha in cur:
            mensLidas = int(mensLidas) + 1

        print("--------------------------------------------------")
        print("| [1] Mensagens lidas [", mensLidas ,"]                       |")
        print("| [2] Mensagens nao lidas [", mensNLidas ,"]                   |")
        print("| [0] Voltar ao menu                              |")
        print("---------------------------------------------------")
        print("\n")
        opcao=input("\nEscolha a opção:")

        while opcao != "1" and opcao != "2" and opcao != "0":
            opcao = input("Escolha a opção:")
        #---------------------------------------------------------------------------------------------------------------
        #Mensagens Lidas
        #---------------------------------------------------------------------------------------------------------------
        if opcao == "1":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Mensagens lidas ----------\n")
            print(nomeCliente, data)


            cur.execute(
                "SELECT cliente_mensagens.mensagens_id_mensagem,mensagem_lida FROM cliente_mensagens, mensagem_lida WHERE cliente_mensagens.mensagens_id_mensagem=mensagem_lida.mensagens_id_mensagem AND cliente_mensagens.cliente_utilizador_email= mensagem_lida.cliente_utilizador_email AND cliente_mensagens.cliente_utilizador_email=%s AND mensagem_lida is true",
                (email,))

            mensagem = cur.fetchall()
            if mensagem == None:
                print("\nNão á mensagens lidas")

            print("Mensagem                     Data")
            for i in mensagem:

                if i[1] == True:
                    cur.execute("SELECT mensagem,data FROM mensagens WHERE id_mensagem = %s", (i[0],))

                    print(cur.fetchone())
                    conn.commit()

                else:
                    print("\nNão há mensagens lidas")
        #---------------------------------------------------------------------------------------------------------------
        #Mensagens nao Lidas
        #---------------------------------------------------------------------------------------------------------------
        elif opcao == "2":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Mensagens nao lidas ----------\n")
            print(nomeCliente, data)

            cur.execute(
                "SELECT cliente_mensagens.mensagens_id_mensagem,mensagem_lida FROM cliente_mensagens, mensagem_lida WHERE cliente_mensagens.mensagens_id_mensagem=mensagem_lida.mensagens_id_mensagem AND cliente_mensagens.cliente_utilizador_email= mensagem_lida.cliente_utilizador_email AND cliente_mensagens.cliente_utilizador_email=%s AND mensagem_lida is false",
                (email,))

            mensagem = cur.fetchall()
            if mensagem == None:
                print("\nNão há mensagens por ler")


            for i in mensagem:
                if i[1] == False:
                    cur.execute("SELECT mensagem,data FROM mensagens WHERE id_mensagem = %s", (i[0],))
                    print(cur.fetchone())

                    cur.execute("UPDATE mensagem_lida SET mensagem_lida = %s WHERE cliente_utilizador_email=%s",
                            ('True', email))

                    conn.commit()

                else:
                    print("\nNão há mensagens por ler")


        elif opcao == "0":
            menuCliente(email)

        sair = " "
        while sair != "s" and sair != "S":
            sair = input("\nPresione s para voltar ao menu cliente: ")
            
        menuCliente(email)

    # ------------------------------------------------------------------------------------------------------------------
    # Dados Pessoais
    #-------------------------------------------------------------------------------------------------------------------

    elif status == "4":
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Dados Pessoais ----------\n")
        print(nomeCliente, data)

        cur.execute("SELECT saldo FROM cliente WHERE utilizador_email = %s",(email,))
        saldo, = cur.fetchone()
        cur.execute("SELECT nome, email FROM utilizador WHERE email = %s",(email,))

        for linha in cur:
            print("\nNome: ",linha[0])
            print("Email: ",linha[1])
            print("Saldo:",saldo,"€")

        sair = " "
        while sair != "s" and sair != "S":
            sair = input("\nPresione s para voltar ao menu cliente: ")

        menuCliente(email)

    # ------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------
    elif status == "0":
        os.system("cls")
        print("\nObrigado por usar a NETFLOX")
        print("Dentro de instantes irá terminar a sessão")
        print("Copyright © 2020/2021 Alexandre Marques e Telmo Cunha")
        conn.commit()
        cur.close()
        conn.close()
        time.sleep(3)
        exit()





#-----------------------------------------------------------------------------------------------------------------------
#  Menu Administrador
#-----------------------------------------------------------------------------------------------------------------------
def menuAdmin(email):


    os.system("cls")
    data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    print("\n---------- Bem-Vindo ao NETFLOX! ----------\n")
    print(data)

    #novo menu
    print("----------------------------------------------")
    print("| [1] Artigos                                |")# adicionar um novo artigo,remover um artigo, visualizar todos os artigos disponiveis
    print("| [2] Corrigir artigo                        |") #corrigir o preço de um artigo
    print("| [3] Enviar mensagem                        |") #a todos os clientes, a um cliente especifico
    print("| [4] Aumentar o saldo de um certo cliente   |")
    print("| [5] Estatisticas                           |")
    print("| [0] Terminar Sessão                        |")
    print("----------------------------------------------")

    status = input("\nIntroduza uma opção: ")
    while status != "1" and status != "2" and status != "3" and status != "4" and status != "5" and status != "0":
        status = input("\nIntroduza uma opção: ")


    #-------------------------------------------------------------------------------------------------------------------
    # ARTIGOS
    #-------------------------------------------------------------------------------------------------------------------
    if status == "1":
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Artigos ----------\n")
        print(data)

        print("------------------------------------")
        print("| [1] Adicionar um novo artigo     |")
        print("| [2] Remover um artigo            |")
        print("| [3] Visualizar todos os artigos  |")
        print("| [0] Voltar ao menu               |")
        print("------------------------------------")


        status1 = input("\nIntroduza uma opção: ")
        while status1 != "1" and status1 != "2" and status1 != "3" and status1 != "0":
            status1 = input("\nIntroduza uma opção: ")

        #---------------------------------------------------------------------------------------------------------------
        # ADICIONAR UM NOVO ARTIGO
        #---------------------------------------------------------------------------------------------------------------
        if status1 == "1":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Adicionar um novo artigo ----------\n")
            print(data)

            titulo = input("Titulo: ")
            preco = input("Preco: ")
            quantidade = input("Quantidade: ")
            tempo_aluguer = input("Tempo maximo aluguer: ")
            tipo = input("Tipo: ")
            genero = input("Genero: ")
            realizador = input("Realizador: ")
            produtor = input("Produtor: ")
            ator = input("Ator Principal: ")

            cur.execute("SELECT max(id_artigo) FROM artigos")
            maxid_artigo, = cur.fetchone()
            id_art = int(maxid_artigo) +1


            cur.execute("INSERT INTO artigos (id_artigo,titulo,preco,tempo_aluguer,tipo,genero,realizador,produtor,quantidade) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (id_art,titulo,preco,tempo_aluguer,tipo,genero,realizador,produtor,quantidade,))

            cur.execute("INSERT INTO detalhes_artigos(ator) VALUES(%s)", (ator,))
            print("O seu artigo foi adicionado com sucesso!")
            conn.commit()
        #---------------------------------------------------------------------------------------------------------------
        # REMOVER UM ARTIGO
        #---------------------------------------------------------------------------------------------------------------
        elif status1 == "2":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Remover um artigo ----------\n")
            print(data)

            print("\n")
            i = "0"


            cur.execute("SELECT titulo FROM artigos;")
            for linha in cur:
                print("TITULO:", linha[0])

            artigo = input("\nTitulo de artigo: ")

            cur.execute("SELECT titulo FROM artigos WHERE titulo=%s", (artigo,))
            titulo = cur.fetchone()

            while titulo == None:
                print("O artigo não existe!")
                print("Tente Novamente!")
                artigo = input("Titulo de artigo: ")
                cur.execute("SELECT titulo FROM artigos WHERE titulo=%s", (artigo,))
                titulo = cur.fetchone()

            #caso o artigo tenha quantidade =0
            cur.execute("SELECT quantidade FROM artigos WHERE titulo=%s",(artigo,))
            quantidade, = cur.fetchone()

            if int(quantidade) == "0":
                print("Não pode remover este artigo")
                #voltar ao inicio

            #caso do aluguer
            cur.execute("SELECT id_artigo FROM artigos WHERE titulo=%s",(artigo,))
            idartigo,=cur.fetchone()

            cur.execute("SELECT artigos_id_artigo FROM aluguer WHERE  artigos_id_artigo = %s",(idartigo,) )


            for linha in cur:
                if idartigo != None:
                    print("\nO artigo neste momento encontra-se alugado.Por esse motivo não pode eliminar este produto")

                else:
                    # remove o artigo
                    cur.execute("DELETE FROM artigos WHERE titulo=%s ", (artigo,))
                    conn.commit()

                    print("\nArtigo removido com sucesso!")

            sair = " "
            while sair != "s" and sair != "S":
                sair = input("\nPresione s para voltar ao menu administrador: ")

            menuAdmin(email)

        #---------------------------------------------------------------------------------------------------------------
        # VISUALIZAR DETALHES DE UM ARTIGO
        #---------------------------------------------------------------------------------------------------------------
        elif status1 == "3":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Visualizar detalhes de um artigo ----------\n")
            print(data)

            print("\n")

            cur.execute(
                "SELECT id_artigo,titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos WHERE quantidade != 0")

            for linha in cur:
                print("ID DO ARTIGO:",linha[0],"  TITULO:", linha[1], "  PREÇO:", linha[2], "  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])

            print("\n")
            cur.execute("SELECT novo_preco,data_alteracao,administrador_utilizador_email,artigos_id_artigo FROM precos")
            for linha in cur:
                print("NOVO PREÇO:",linha[0],"  DATA DE ALTERAÇÃO:",linha[1], " EMAIL DO ADMINISTRADOR QUE FEZ A ALTERAÇÃO:",linha[2]," ID DO ARTIGO ALTERADO: ",linha[3])


        elif status1 == "0":
            menuAdmin(email)


        sair = " "
        while sair != "s" and sair != "S":
            sair = input("\n\nPresione s para voltar ao menu administrador: ")

        menuAdmin(email)

    #-------------------------------------------------------------------------------------------------------------------
    # Corrigir Artigo
    #-------------------------------------------------------------------------------------------------------------------
    elif status == "2":
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Corrigir artigo ----------\n")
        print(data)

        print("------------------------------------")
        print("| [1] Titulo                       |")
        print("| [2] Tempo maximo de aluguer      |")
        print("| [3] Tipo                         |")
        print("| [4] Genero                       |")
        print("| [5] Realizador                   |")
        print("| [6] Produtor                     |")
        print("| [7] Quantidade                   |")
        print("| [8] Preço                        |")
        print("| [0] Voltar ao menu               |")
        print("------------------------------------")

        op = input("\nInsira uma opção: ")

        while op != "1" and op != "2" and op != "3" and op != "4" and op != "5" and op != "6" and op != "7" and op != "8" and op != "0":
            op = input("Insira uma opção: ")
        #---------------------------------------------------------------------------------------------------------------
        #Corrigir o Titulo
        #---------------------------------------------------------------------------------------------------------------
        if op == "1":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir titulo ----------\n")
            print(data)

            cur.execute("SELECT * FROM artigos ORDER BY id_artigo")
            for linha in cur:
                print("ID ARTIGO:", linha[0], "  TITULO:", linha[1], "  PREÇO:", linha[2], "  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])
            id = input("Insira o id do artigo que pretende corrigir: ")
            cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
            titulo = cur.fetchone()

            while titulo == None:
                print("O artigo não existe")
                print("Tente Novamente")
                id = input("Insira o id do artigo que pretende corrigir: ")
                cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
                titulo = cur.fetchone()
            novoTitulo = input("Insira o Novo Titulo: ")
            cur.execute("UPDATE artigos SET titulo = %s WHERE id_artigo=%s", (novoTitulo, id,))
            print("\nTitulo atualizado com sucesso!")
            conn.commit()
        #---------------------------------------------------------------------------------------------------------------
        # Corrigir o Tempo Maximo de Aluguer
        #---------------------------------------------------------------------------------------------------------------
        elif op == "2":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir o tempo maximo de aluguer ----------\n")
            print(data)

            cur.execute("SELECT * FROM artigos ORDER BY id_artigo")

            for linha in cur:
                print("ID ARTIGO:", linha[0], "  TITULO:", linha[1], "  PREÇO:", linha[2], "  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])

            id = input("Insira o id do artigo que pretende corrigir: ")

            cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
            titulo = cur.fetchone()

            while titulo == None:
                print("O artigo não existe")
                print("Tente Novamente")
                id = input("Insira o id do artigo que pretende corrigir: ")
                cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
                titulo = cur.fetchone()

            novoTempo_aluguer = input("Insira o novo tempo maximo de aluguer: ")
            cur.execute("UPDATE artigos SET tempo_aluguer = %s WHERE id_artigo=%s", (novoTempo_aluguer, id,))
            print("Tempo maximo de aluguer atualizado com sucesso!")
            conn.commit()
        #---------------------------------------------------------------------------------------------------------------
        #Corrigir o Tipo
        #---------------------------------------------------------------------------------------------------------------
        elif op == "3":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir tipo ----------\n")
            print(data)

            cur.execute("SELECT * FROM artigos ORDER BY id_artigo")
            for linha in cur:
                print("ID ARTIGO:", linha[0], "  TITULO:", linha[1], "  PREÇO:", linha[2], "  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])

            id = input("Insira o id do artigo que pretende corrigir: ")
            cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
            titulo = cur.fetchone()

            while titulo == None:
                print("O artigo não existe")
                print("Tente Novamente")
                id = input("Insira o id do artigo que pretende corrigir: ")
                cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
                titulo = cur.fetchone()

            novoTipo = input("Insira o Novo Tipo: ")
            cur.execute("UPDATE artigos SET tipo = %s WHERE id_artigo=%s", (novoTipo, id,))
            print("Tipo atualizado com sucesso!")
            conn.commit()

        #---------------------------------------------------------------------------------------------------------------
        #Corrigir o Genero
        #---------------------------------------------------------------------------------------------------------------
        elif op == "4":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir o genero ----------\n")
            print(data)

            cur.execute("SELECT * FROM artigos ORDER BY id_artigo")
            for linha in cur:
                print("ID ARTIGO:", linha[0], "  TITULO:", linha[1], "  PREÇO:", linha[2], "  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])
            id = input("\nInsira o id do artigo que pretende corrigir: ")
            cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
            titulo = cur.fetchone()
            while titulo == None:
                print("O artigo não existe")
                print("Tente Novamente")
                id = input("\nInsira o id do artigo que pretende corrigir: ")
                cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
                titulo = cur.fetchone()
            novoGenero = input("\nInsira o Novo Genero: ")
            cur.execute("UPDATE artigos SET genero = %s WHERE id_artigo=%s", (novoGenero, id,))
            print("Genero atualizado com sucesso!")
            conn.commit()

        #---------------------------------------------------------------------------------------------------------------
        #Corrigir o Realizador
        #---------------------------------------------------------------------------------------------------------------
        elif op == "5":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir o realizador ----------\n")
            print(data)

            cur.execute("SELECT * FROM artigos ORDER BY id_artigo")
            for linha in cur:
                print("ID ARTIGO:", linha[0], "  TITULO:", linha[1], "  PREÇO:", linha[2], "  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])
            id = input("Insira o id do artigo que pretende corrigir: ")

            cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
            titulo = cur.fetchone()

            while titulo == None:
                print("O artigo não existe")
                print("Tente Novamente")
                id = input("Insira o id do artigo que pretende corrigir: ")
                cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
                titulo = cur.fetchone()

            novoRealizador = input("Insira o Novo realizador: ")
            cur.execute("UPDATE artigos SET realizador = %s WHERE id_artigo=%s", (novoRealizador, id,))
            print("Realizador atualizado com sucesso!")
            conn.commit()

        #---------------------------------------------------------------------------------------------------------------
        #Corrigir o Produtor
        #---------------------------------------------------------------------------------------------------------------
        elif op == "6":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir o produtor ----------\n")
            print(data)

            cur.execute("SELECT * FROM artigos ORDER BY id_artigo")
            for linha in cur:
                print("ID ARTIGO:", linha[0], "  TITULO:", linha[1], "  PREÇO:", linha[2], "  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])

            id = input("Insira o id do artigo que pretende corrigir: ")
            cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
            titulo = cur.fetchone()

            while titulo == None:
                print("O artigo não existe")
                print("Tente Novamente")
                id = input("Insira o id do artigo que pretende corrigir: ")
                cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
                titulo = cur.fetchone()

            novoProdutor = input("Insira o Novo Produtor: ")
            cur.execute("UPDATE artigos SET produtor = %s WHERE id_artigo=%s", (novoProdutor, id,))
            print("Produtor atualizado com sucesso!")
            conn.commit()
        #---------------------------------------------------------------------------------------------------------------
        #Corrigir Quantidade
        #---------------------------------------------------------------------------------------------------------------
        elif op == "7":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir a quantidade ----------\n")
            print(data)

            cur.execute("SELECT * FROM artigos ORDER BY id_artigo")
            for linha in cur:
                print("ID ARTIGO:", linha[0], "  TITULO:", linha[1], "  PREÇO:", linha[2],"  QUANTIDADE:", linha[3],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[4], "  TIPO:", linha[5], "  GENERO:", linha[6],
                      "  REALIZADOR:", linha[7], "  PRODUTOR:", linha[8])
            id = input("Insira o id do artigo que pretende corrigir: ")

            cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
            titulo = cur.fetchone()

            while titulo == None:
                print("O artigo não existe")
                print("Tente Novamente")
                id = input("Insira o id do artigo que pretende corrigir: ")
                cur.execute("SELECT titulo FROM artigos WHERE id_artigo=%s", (id,))
                titulo = cur.fetchone()

            novoQuantidade = input("Insira a Novo Quantidade: ")
            cur.execute("UPDATE artigos SET quantidade = %s WHERE id_artigo=%s", (novoQuantidade, id,))
            print("Quantidade atualizada com sucesso!")
            conn.commit()
        #---------------------------------------------------------------------------------------------------------------
        #Corrigir Preço
        #---------------------------------------------------------------------------------------------------------------
        elif op =="8":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- Corrigir o Preço ----------\n")
            print(data)

            cur.execute("SELECT titulo,preco,quantidade,tempo_aluguer,tipo,genero,realizador,produtor FROM artigos;")
            for linha in cur:
                print("TITULO:", linha[0], "  PREÇO:", linha[1], "  QUANTIDADE:", linha[2],
                      "  TEMPO MAXIMO DE ALUGUER:", linha[3], "  TIPO:", linha[4], "  GENERO:", linha[5],
                      "  REALIZADOR:", linha[6], "  PRODUTOR:", linha[7])

            artigo = input("Escreva o titulo do artigo que deseja efetuar alteração: ")

            cur.execute("SELECT titulo FROM artigos WHERE titulo=%s", (artigo,))
            titulo = cur.fetchone()

            if titulo == None:
                print("O artigo não existe!")
                print("Tente Novamente")
                artigo = input("Escreva o titulo do artigo que deseja efetuar alteração: ")
                cur.execute("SELECT titulo FROM artigos WHERE titulo=%s", (artigo,))
                titulo=cur.fetchone()

            novoPreco = input("Novo preco: ")
            # verifica se é digito e se for retorna true
            x = novoPreco.isdigit()

            while x == False:
                print("Tente Novamente")
                novoPreco = input("Novo preco: ")
                x = novoPreco.isdigit()

            cur.execute("UPDATE artigos SET preco = %s WHERE titulo=%s", (novoPreco, artigo,))

            cur.execute("SELECT id_artigo FROM artigos WHERE titulo=%s", (artigo,))
            id_artigo, = cur.fetchone()

            cur.execute("SELECT max(id_alteracao) FROM precos")
            id_alt, = cur.fetchone()

            novoid = int(id_alt) + 1

            cur.execute(
                "INSERT INTO precos(id_alteracao, novo_preco, data_alteracao, administrador_utilizador_email , artigos_id_artigo) VALUES(%s,%s,%s,%s,%s)",
                (novoid, novoPreco, data, email, id_artigo,))

            cur.execute("SELECT novo_preco,data_alteracao FROM precos WHERE data_alteracao=%s", (data,))
            conn.commit()

            print("\nTITULO: ", artigo)
            for linha in cur:
                print("PREÇO:", linha[0])
                print("DATA:", linha[1])

            print("\nOperação realizada com sucesso!!")



        elif op == "0":
            menuAdmin(email)

        sair = ""
        while sair != "s" and sair !="S":
            sair = input("\n\nPresione s para voltar ao menu administrador: ")
        menuAdmin(email)


    #-----------------------------------------------------------------------------------------------------------------
    # mensagens
    #----------------------------------------------------------------------------------------------------------------------------
    elif status == "3":            #envia uma mensagem
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Enviar mensagens ----------\n")
        print(data)

        print("\n[1] A todos os clientes")
        print("[2] A um cliente especifico")
        print("[0] Voltar ao menu")
        status1 = input("\nInsira uma opção: ")

        while status1 != "1" and status1 != "2" and status1 != "0":
            status1 = input("Insira uma opção: ")

        #---------------------------------------------------------------------
        # envia mensagem  a todos os clientes
        #---------------------------------------------------------------------
        if status1 == "1":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- A todos os clientes ----------\n")
            print(data)

            mensagem = input("\nSua mensagem: ")



            cur.execute("SELECT utilizador_email FROM cliente")
            cur.execute("SELECT max(id_mensagem) FROM mensagens")
            idmensagem,=cur.fetchone()
            novoid=idmensagem+1

            cur.execute("INSERT INTO mensagens VALUES (%s,%s,%s,%s)",(novoid,mensagem,data,email,))
            cur.execute("SELECT utilizador_email FROM cliente;")
            clientes=cur.fetchall()

            for i in clientes:
                cur.execute("INSERT INTO cliente_mensagens VALUES (%s,%s)",(i[0],novoid,))
                cur.execute("INSERT INTO mensagem_lida VALUES(%s,%s,%s)",('false',novoid,i[0]))
                conn.commit()

            print("\nMensagem enviada com sucesso!")
            conn.commit()


        #-----------------------------------------------------------------------
        # envia mensagem a um cliente especifico
        #------------------------------------------------------------------------
        elif status1 == "2":
            os.system("cls")
            data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            print("\n---------- A um cliente especifico ----------\n")
            print(data)

            # dar print ao nome de todos os clientes
            cur.execute("SELECT utilizador_email FROM cliente")
            for linha in cur:
                print("Email:", linha[0])

            cliente = input("\nInsira o email do cliente: ")
            cur.execute("SELECT email FROM utilizador WHERE email LIKE %s", (cliente,))
            clienteEmail = cur.fetchone()

            while clienteEmail == None:
                cliente = input("Email do cliente: ")
                cur.execute("SELECT email FROM utilizador WHERE email LIKE %s", (cliente,))
                clienteEmail = cur.fetchone()

            mensagem = input("Sua mensagem: ")

            cur.execute("SELECT max(id_mensagem) FROM mensagens")
            idmensagem, = cur.fetchone()
            novoid = int(idmensagem) + 1

            cur.execute("INSERT INTO mensagens VALUES (%s,%s,%s,%s)", (novoid, mensagem, data, email,))
            cur.execute("INSERT INTO cliente_mensagens VALUES (%s,%s)", (clienteEmail, novoid,))
            cur.execute("INSERT INTO mensagem_lida VALUES(%s,%s,%s)", ('false', novoid, clienteEmail))
            conn.commit()

            print("\nMensagem enviada com sucesso!")
            conn.commit()

        elif status1 == "0":
            menuAdmin(email)


        sair = ""
        while sair != "s" and sair != "S":
            sair = input("\nPresione s para voltar ao menu administrador: ")
        menuAdmin(email)
    #-------------------------------------------------------------------------------------------------------------------
    # aumentar o saldo de um certo cliente
    #-------------------------------------------------------------------------------------------------------------------
    elif status == "4":                          #aumenta o saldo de um certo cliente
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Aumentar o saldo de um cliente ----------\n")
        print(data,"\n")

        cur.execute("SELECT utilizador_email,saldo FROM cliente ORDER BY utilizador_email")
        for linha in cur:
            print("EMAIL:", linha[0], "   SALDO:", linha[1])

        emailCliente = input("\nEmail do Cliente: ")
        cur.execute("SELECT utilizador_email FROM cliente WHERE utilizador_email=%s", (emailCliente,))
        cliente = cur.fetchone()

        if cliente == None:
            print("\nEmail incorreto ou cliente inexistente!")
            emailCliente = input("Email do Cliente: ")
            cur.execute("SELECT utilizador_email FROM cliente WHERE utilizador_email=%s", (emailCliente,))
            cliente = cur.fetchone()

        cur.execute("SELECT saldo FROM cliente WHERE utilizador_email=%s", (emailCliente,))
        saldoAtual, = cur.fetchone()

        saldo = input("\nValor a ser adicionado(€): ")
        saldoNovo = float(saldoAtual) + float(saldo)

        cur.execute("UPDATE cliente SET saldo = %s WHERE utilizador_email=%s", (saldoNovo, emailCliente,))
        conn.commit()

        print("\nSaldo atualizado com sucesso!")

        sair = ""
        while sair != "s" and sair != "S":
            sair = input("\nPresione s para voltar ao menu administrador: ")


        menuAdmin(email)
    #-------------------------------------------------------------------------------------------------------------------
    # Estatisticas
    #-------------------------------------------------------------------------------------------------------------------
    elif status == "5":                                        #ver estatisticas
        os.system("cls")
        data = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n---------- Estatisticas ----------\n")
        print(data)

        # novo id estatistica
        cur.execute("SELECT max(id_estatistica) FROM estatisticas")
        estatistica, = cur.fetchone()
        id_estatistica = int(estatistica) + 1

        # contagem de utilizadores
        cur.execute("SELECT utilizador_email FROM cliente")
        total_cliente = "0"
        for linha in cur:
            total_cliente = int(total_cliente) +1

        # contagem de artigos
        cur.execute("SELECT max(id_artigo) FROM artigos")
        total_artigos,= cur.fetchone()

        cur.execute("SELECT SUM(quantidade) FROM aluguer WHERE data_levamento > %s", (data,))
        valor_agora,= cur.fetchone()

        # total aluguer
        cur.execute("SELECT SUM(valor) FROM aluguer")
        valor,= cur.fetchone()

        # total gasto por filmes
        cur.execute("SELECT SUM(gasto_filmes) FROM cliente")
        total_filme,=cur.fetchone()

        #total gasto por series
        cur.execute("SELECT SUM(gasto_series) FROM cliente")
        total_serie,= cur.fetchone()

        # contagem total mensagens lidas
        cur.execute("SELECT mensagens_id_mensagem FROM mensagem_lida WHERE mensagem_lida = %s",('True',))
        total_mensagens_lidas = "0"
        for linha in cur:
            total_mensagens_lidas = int(total_mensagens_lidas) +1

        # contagem total de mensagens enviadas
        cur.execute("SELECT mensagens_id_mensagem FROM mensagem_lida ")
        total_mensagens_enviadas = "0"
        for linha in cur:
            total_mensagens_enviadas= int(total_mensagens_enviadas) + 1


        cur.execute("INSERT INTO estatisticas(id_estatistica,total_clientes,total_artigos,valor_total_artigos_alugados_agora,total_aluguer,total_mensagens_lidas,total_mensagens_enviadas,total_filmes,total_series) "
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (id_estatistica, total_cliente, total_artigos, valor_agora, valor, total_mensagens_lidas, total_mensagens_enviadas, total_filme, total_serie,))

        conn.commit()
        cur.execute("SELECT total_clientes, total_artigos, valor_total_artigos_alugados_agora, total_aluguer, total_mensagens_lidas, total_mensagens_enviadas,total_filmes,total_series "
                    "FROM estatisticas WHERE id_estatistica = %s;",(id_estatistica,))

        #nesta situaçao é importante ter uma legenda de valores
        for linha in cur:
            print("\nTOTAL CLIENTES:", linha[0])
            print("TOTAL ARTIGOS EM STOCK:",linha[1])
            print("VALOR TOTAL DE ARTIGOS ALUGADOS NO MOMENTO:",linha[2])
            print("LUCRO DE TODOS OS ALUGUERES:",linha[3],"€")
            print("TOTAL DE MENSAGENS LIDAS:",linha[4])
            print("TOTAL DE MENSAGENS ENVIADAS:",linha[5])
            print("VALOR GASTO EM FILMES:",linha[6],"€")
            print("VALOR GASTO EM SERIES:",linha[7],"€")

        sair = " "
        while sair != "s" and sair != "S":
            sair = input("\nPresione s para voltar ao menu administrador: ")

        menuAdmin(email)

    #---------------------------------------------------------------------------------
    elif status == "0":
        os.system("cls")

        print("\nObrigado por usar a NETFLOX")
        print("Dentro de instantes irá terminar a sessão")
        print("Copyright © 2020/2021 Alexandre Marques e Telmo Cunha")
        conn.commit()
        cur.close()
        conn.close()
        time.sleep(3)
        exit()


#----------------------------------------------------------------------------------------------------------------------------
#  Validação de palavra pass
#----------------------------------------------------------------------------------------------------------------------------
class valid_pass(object):
    def __init__(self, passW = ''):
        self.passW = passW

    def __lower(self):
        lower = any(c.islower() for c in self.passW)
        return lower

    def __upper(self):
        upper = any(c.isupper() for c in self.passW)
        return upper

    def __digit(self):
        digit = any(c.isdigit() for c in  self.passW)
        return digit

    def validate(self):
        lower = self.__lower()
        upper = self.__upper()
        digit = self.__digit()

        length = len(self.passW)

        report = lower and upper and digit and length >= 6

        if report:
            print("A password é valida e segura")
            return True

        elif not lower:
            print("Nao utilizou nenhuma letra minuscula")
            return False

        elif not upper:
            print("Nao utilizou nenhuma letra maiuscula")
            return False

        elif length <6:
            print("Inferior a 6 digitos")
            return False

        elif not digit:
            print("Nao utilizou um numero")
            return False
        else:
            pass

#-----------------------------------------------------------------------------------------------------
# Validação Email
#-----------------------------------------------------------------------------------------------------
def valid_email(string):

    pos = string.find("@")
    dot = string.rfind(".")

    if pos < 1:
        print("O email nao é valido")
        return False

    if dot < pos + 2:
        print("O email nao é valido")
        return False

    if dot + 2 >= len(string):
        print("O email nao é valido")
        return False
    return True


menuInicial()


#Torna permanente as alteraçoes feitas a base de dados
conn.commit()
# Fecha a ligação à base de dados
cur.close()
conn.close()