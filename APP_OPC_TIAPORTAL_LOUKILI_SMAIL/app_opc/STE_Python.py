import sys
import time
from opcua import Client, ua

def write_value_bool(node_id, value):
    client_node = client.get_node(node_id)
    client_node_dv = ua.DataValue(ua.Variant(value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)

def read_input_value(node_id):
    client_node = client.get_node(node_id)
    client_node_value = client_node.get_value()
    return client_node_value

# Ajout du Serveur OPC serveur
client = Client("opc.tcp://127.0.0.1:49320")

try:
    # Connexion au serveur
    client.connect()
    print("Connected to OPCUA SERVER")
    
    # ID des noeuds: définition des noeuds
    nodeid_niveau = "ns=2;s=S7_Ethernet.S7_1500.niveau"
    nodeid_aru = "ns=2;s=S7_Ethernet.S7_1500.ARU"
    nodeid_rea = "ns=2;s=S7_Ethernet.S7_1500.REA"
    nodeid_aut = "ns=2;s=S7_Ethernet.S7_1500.aut"
    nodeid_marche = "ns=2;s=S7_Ethernet.S7_1500.marche"
    nodeid_arret = "ns=2;s=S7_Ethernet.S7_1500.arret"
    nodeid_BPpompe = "ns=2;s=S7_Ethernet.S7_1500.BPpompe"
    nodeid_BPvanne = "ns=2;s=S7_Ethernet.S7_1500.BPvanne"
    nodeid_pompe = "ns=2;s=S7_Ethernet.S7_1500.pompe"
    nodeid_vanne = "ns=2;s=S7_Ethernet.S7_1500.vanne"
    
    while True:
        choix1 = input("Choix du fonctionnement  MAN --> 1; AUT --> 2: ")
        
        if choix1 in ['1', '2']:
            if choix1 == '2':
                # Mode automatique
                write_value_bool(nodeid_aut, True)
                time.sleep(0.2)
                
                write_value_bool(nodeid_marche, True)
                time.sleep(0.2)
                write_value_bool(nodeid_marche, False)
                time.sleep(0.2)
                
                choix2 = input("Arrêt du fonctionnement automatique: (O) ")
                if choix2.upper() == 'O':
                    write_value_bool(nodeid_arret, True)
                    time.sleep(0.2)
                    write_value_bool(nodeid_arret, False)
                    time.sleep(0.2)
            else:
                # Mode manuel
                while True:
                    choix3 = input("Commandes manuelles: Pompe ON --> P1; Pompe OFF --> P0; Vanne ON --> V1; Vanne OFF --> V0; Quitter --> Q: ")
                    if choix3.upper() == 'Q':
                        break
                    elif choix3 == 'P1':
                        write_value_bool(nodeid_BPpompe, True)
                    elif choix3 == 'P0':
                        write_value_bool(nodeid_BPpompe, False)
                    elif choix3 == 'V1':
                        write_value_bool(nodeid_BPvanne, True)
                    elif choix3 == 'V0':
                        write_value_bool(nodeid_BPvanne, False)
                    else:
                        print("Commande non reconnue. Réessayez.")
                        
except Exception as err:
    print("Erreur:", err)
    sys.exit(1)
        
finally:
    time.sleep(2)
    client.disconnect()
