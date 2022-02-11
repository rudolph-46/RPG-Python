import socket
import os
import random
import time
from _thread import *


class Personnage():

    def __init__(self, nom, sexe, nbvie, attaque):
        self.nom = nom
        self.sexe = sexe
        self.nbvie = nbvie
        self.attaque = attaque
        self.msg = ''
        self.Potion = 1

        if self.attaque < 10:
            self.msg = "C'est le monstre " + self.nom + ", il a " + str(self.nbvie) + " points de vie et " + str(
                self.attaque) + " dégâts d'attaque"
        else:
            self.msg = "Bienvenue, " + self.nom + " Vous avez " + str(self.nbvie) + " de vie et " + str(
                self.attaque) + " de dégats."
        # On verifie si le fichier save.txt existe
        if os.path.exists("save.txt"):
            # print("Fichier existe deja")
            with open("save.txt", 'r') as f:
                if str(nom + "#") in f.read():
                    print("Personnage existe deja")
                else:
                    with open("save.txt", 'a+') as file:
                        file.write(nom + '#' + sexe + '#' + str(nbvie) + '#' + str(attaque) + "\n")
                    file.close()
            f.close()
        else:
            # print("File not found!")
            with open("save.txt", 'a+') as file:
                file.write(nom + '#' + sexe + '#' + str(nbvie) + '#' + str(attaque) + "\n")
            file.close()

    def coup(self, cible):
        self.msg = ">>" + self.nom + " attaque " + cible.nom + "\n"
        cible.nbvie = int(cible.nbvie) - int(self.attaque)
        if cible.nbvie <= 0:
            a = "Le personnage " + cible.nom + " est mort\n"
            cible.nbvie = 0
        else:
            a = cible.nom + " prend " + str(self.attaque) + " dégâts et il lui reste " + str(
                cible.nbvie) + " points de vie\n"

        self.msg = self.msg + a

    def potion(self):
        if self.Potion > 0:

            file = open("save.txt", "r+")
            content = file.read()
            content = content.split()
            positionPersonnage = content.index(
                self.nom + '#' + self.sexe + '#' + str(self.nbvie) + '#' + str(self.attaque))
            self.nbvie = self.nbvie + 15
            personnage = content[positionPersonnage].split('#')
            personnage[2] = str(self.nbvie)
            content[positionPersonnage] = "#".join(personnage)

            for i in range(0, len(content) + 4, 2):
                content.insert(i + 1, "\n")
            s = ''.join(content)
            file.close()

            file = open("save.txt", "w+")
            file.write(s)
            file.close()

        self.Potion -= 1

        print(self.nom + 'a utilisé sa potiion ')

    def message(self):
        return self.msg


ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1234
ThreadCount = 0
joueurs = []
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('En attente de connection ....')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    perso = ''
    while True:
        data = connection.recv(1024)
        dataS = str(data.decode('utf-8')).split("#")
        action = dataS[0]
        dataF = dataS[1]

        if len(dataF) > 1:
            data = dataF
        if action == "START":
            connection.sendall(str.encode("MSG#Début de la partie"))
            e1 = Personnage("Wario", "M", 50, 3)
            connection.sendall(str.encode("MSG#" + e1.message()))
            e2 = Personnage("Mrs. Smith", "F", 30, 7)
            connection.sendall(str.encode("MSG#" + e2.message()))
            e3 = Personnage("Voldemort", "M", 25, 9)
            connection.sendall(str.encode("MSG#" + e3.message()))
            file = open("save.txt", "r+")
            end_content = file.read()
            file.close()
            connection.sendall(str.encode("STARTED#null"))
        elif action == "CREATE":
            dataReceive = data.split(";")
            perso = Personnage(dataReceive[0], dataReceive[1], int(dataReceive[2]), int(dataReceive[3]))
            connection.sendall(str.encode("CREATED#" + perso.message()))

        elif action == "PLAY-1":
            connection.sendall(str.encode(
                "PLAYED-1#<<<< NOUVEAU TOUR >>>> \nIl vous reste " + str(perso.Potion) + " potion" + " et " + str(
                    perso.nbvie) + "\nQue voulez-vous faire: Attaquer (A) ou Utiliser une potion (P) \n"))
        elif action == "PLAY-2":
            choix = dataF
            if choix == "A":
                file = open("save.txt", "r+")
                content = file.read()
                content = content.split()
                ennemi1 = content[0]
                ennemi1 = ennemi1.split('#')
                ennemi2 = content[1]
                ennemi2 = ennemi2.split('#')
                ennemi3 = content[2]
                ennemi3 = ennemi3.split('#')
                file.close()

                msg = "Qui voulez-vous attaquer?\n"
                if int(ennemi1[2]) > 0:
                    msg = msg + "1 - " + e1.nom + " avec " + str(ennemi1[2]) + " points de vie\n"
                if int(ennemi2[2]) > 0:
                    msg = msg + "2 - " + e2.nom + " avec " + str(ennemi2[2]) + " points de vie\n"
                if int(ennemi3[2]) > 0:
                    msg = msg + "3 - " + e3.nom + " avec " + str(ennemi3[2]) + " points de vie\n"

                msg = msg + "Choisissez le numéro de l'ennemi "
                connection.sendall(str.encode("PLAYED-2#" + msg))
            elif choix == "P":
                perso.potion()
                connection.sendall(str.encode("PLAYED-1#!!!! Nouveau point de vies sont de " + str(
                    perso.nbvie) + " Et le nombre de potion " + str(perso.Potion) + str(
                    "\n<<<< NOUVEAU TOUR >>>> \nIl vous reste " + str(
                        perso.Potion) + " potion\nQue voulez-vous faire: Attaquer (A) ou Utiliser une potion (P) \n")))

        elif action == "PLAY-2-A":
            choix_ennemi = int(dataF)
            file = open("save.txt", "r+")
            content = file.read()
            content = content.split()
            ennemi = content[int(choix_ennemi) - 1].split('#')
            connection.sendall(str.encode("MSG#>>" + perso.nom + ' attaque ' + ennemi[0]))
            if choix_ennemi == 1:
                e1.msg = ''
                perso.coup(e1)
                p = content[0].split('#')
                p[2] = str(e1.nbvie)
                e1.nbvie = e1.nbvie
                content[0] = "#".join(p)
                connection.sendall(str.encode("MSG#" + e1.msg))
            elif choix_ennemi == 2:
                perso.coup(e2)
                p = content[1].split('#')
                p[2] = str(e2.nbvie)
                e2.nbvie = e2.nbvie
                content[1] = "#".join(p)
                connection.sendall(str.encode("MSG#" + e2.message()))
            elif choix_ennemi == 3:
                perso.coup(e3)
                p = content[2].split('#')
                p[2] = str(e3.nbvie)
                e3.nbvie = e3.nbvie
                content[2] = "#".join(p)
                connection.sendall(str.encode("MSG#" + e3.message()))
            for i in range(0, len(content) + 4, 2):
                content.insert(i + 1, "\n")

            s = ''.join(content)
            file.close()

            file = open("save.txt", "w+")
            file.write(s)
            file.close()

            tourEnnemi(connection, perso, e1, e2, e3)
            connection.sendall(str.encode("PLAYED#null"))
        if not data:
            break
    connection.close()


def reinitialiser():
    os.remove("save.txt")
    Personnage("Wario", "M", 50, 3)
    Personnage("Mrs. Smith", "F", 30, 7)
    Personnage("Voldemort", "M", 25, 9)


def tourEnnemi(connection: ServerSocket, perso: Personnage, e1: Personnage, e2: Personnage, e3: Personnage):
    file = open("save.txt", "r+")
    content = file.read()
    content = content.split()
    positionPersonnage = content.index(perso.nom + '#' + perso.sexe + '#' + str(perso.nbvie) + '#' + str(perso.attaque))

    msg = "MSG#<<<< TOUR DE L'ENNEMI >>>>\n"
    if e1.nbvie > 0:
        i = random.randint(1, 2)
        if i == 1:
            e1.coup(perso)
            msg = msg + e1.message()
            personnage = content[positionPersonnage].split('#')
            personnage[2] = str(perso.nbvie)
            content[positionPersonnage] = "#".join(personnage)
        elif i == 2:
            msg = msg + e1.nom + " passe son tour\n"

    if e2.nbvie > 0:
        i = random.randint(1, 2)
        if i == 1:
            e2.coup(perso)
            msg = msg + e2.message()
            personnage = content[positionPersonnage].split('#')
            personnage[2] = str(perso.nbvie)
            content[positionPersonnage] = "#".join(personnage)
        elif i == 2:
            msg = msg + e2.nom + " passe son tour\n"

    if e3.nbvie > 0:
        i = random.randint(1, 2)
        if i == 1:
            e3.coup(perso)
            msg = msg + e3.message()
            personnage = content[positionPersonnage].split('#')
            personnage[2] = str(perso.nbvie)
            content[positionPersonnage] = "#".join(personnage)
        elif i == 2:
            msg = msg + e3.nom + " passe son tour\n"

    connection.send(str.encode(msg))
    for i in range(0, len(content) + 4, 2):
        content.insert(i + 1, "\n")
    s = ''.join(content)
    file.close()
    if e1.nbvie <= 0 and e2.nbvie <= 0 and e3.nbvie <= 0:
        if perso.nbvie == 0:
            connection.send(str.encode("MSG#<<<< VOUS AVEZ PERDU, DOMMAGE >>>>"))
        else:
            connection.send(str.encode("MSG#\n\n<<<< BRAVO POUR LA VICTOIRE >>>>\nPARTIE TERMINE"))
            reinitialiser()
            exit()

    file = open("save.txt", "w+")
    file.write(s)
    file.close()


while True:
    Client, address = ServerSocket.accept()
    print('Nouveau joueur connecté ' + address[0] + ':' + str(address[1]))
    joueurs.append([threaded_client, (Client,)])
    tmp = joueurs
    print('Nombre de joueurs ' + str(len(joueurs)))
    if len(joueurs) >= 2:
        for joueur in joueurs:
            start_new_thread(joueur[0], joueur[1])
            time.sleep(1)

    else:
        print("En attente du 2e joueur")

ServerSocket.close()
