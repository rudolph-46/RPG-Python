import socket

socket = socket.socket()
host = '127.0.0.1'
port = 1234
start = 1

print('Waiting for connection')
try:
    socket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = socket.recv(102400)
while True:
    if start == 1:
        socket.send(str.encode("START#null"))
        start = 0

    response = socket.recv(1024)
    dataS = str(response.decode('utf-8')).split("#")
    action = dataS[0]
    dataF = dataS[1]
    if action == "START":
        print(dataF)
    elif action == "STARTED":
        print("Créer votre personnage :")
        perso_name = input("Nom : ")
        perso_sexe = ""
        while perso_sexe != "M" and perso_sexe != "F":
            perso_sexe = input('Sexe Masculin (M) ou Féminin (F): ')

        perso_classe = input("Sélectionnez votre classe : guerrier, mage ou archer\n")
        verif = False
        personnage = "START"
        while verif == False:
            if perso_classe == "guerrier":
                personnage = "CREATE#" + perso_name + ";" + str(perso_sexe) + ";" + str(40) + ";" + str(10)
                verif = True
            elif perso_classe == "mage":
                personnage = "CREATE#" + perso_name + ";" + str(perso_sexe) + ";" + str(25) + ";" + str(16)
                verif = True
            elif perso_classe == "archer":
                perso_name + ";" + str(perso_sexe) + ";" + str(35) + ";" + str(13)
                personnage = "CREATE#" + perso_name + ";" + str(perso_sexe) + ";" + str(35) + ";" + str(13)
                verif = True
            else:
                perso_classe = input("Sélectionnez votre classe : guerrier, mage ou archer\n")

        socket.send(personnage.encode())
    elif action == "CREATED" or action == "PLAYED":
        socket.send(("PLAY-1#null").encode())
    elif action == "PLAYED-1":
        c = input(dataF)
        socket.send(("PLAY-2#" + c).encode())
    elif action == "PLAYED-2":
        c = input(dataF)
        socket.send(("PLAY-2-A#" + c).encode())
    elif action == "MSG":
        print(dataF)
    elif action == "PLAYED-2-P":
        print(dataF)

    else:
        print(dataF)
socket.close()
