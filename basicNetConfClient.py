from ncclient import manager
import xml.dom.minidom
from ncclient.transport.errors import SSHError, AuthenticationError
from ncclient.operations.rpc import RPCError
import socket

host = input("Add meg a NETCONF szerver IP címét vagy host nevét: ")
username = input("Add meg a Felhasználóneved a NETCONF szerverhez: ")
password = input("Add meg a jelszavad: ")
try:
    with manager.connect(
        host=host,
        port=830,
        username=username,
        password=password,
        hostkey_verify=False
    ) as m:
        print("""Sikeresen csatlakoztál a NETCONF szerverhez!\nA lehetséges parancsokért írd be a 'help'-et.""")
        while True:  
            try:
                cmd = input(">>> ").split()
                if len(cmd) == 0:
                    print("Nem adott meg parancsot, próbálja újra.")
                    continue
                elif cmd[0] == "help":
                    help_text = """
                    ********** NETCONF TERMINÁL SEGÉDLET **********

                    Elérhető parancsok:

                    help
                        Kiírja ezt a segítséget, a parancsok rövid leírásával.

                    exit
                        Kilép a terminálból.

                    get_running_config
                        Lekérdezi a NETCONF szerverről a futó (running) konfigurációt és kiírja a konzolra.

                    get_startup_config
                        Lekérdezi a NETCONF szerverről a mentett (startup) konfigurációt és kiírja a konzolra.

                    save_running_config <filename>
                        Lekérdezi a NETCONF szerverről a futó (running) konfigurációt és elmenti a megadott nevű fájlba.

                    save_startup_config <filename>
                        Lekérdezi a NETCONF szerverről a mentett (startup) konfigurációt és elmenti a megadott nevű fájlba.

                    delete_running_config
                        Törli a NETCONF szerverről a futó (running) konfigurációt.
                    
                    delete_startup_config
                        Törli a NETCONF szerverről a mentett (startup) konfigurációt.

                    ********** Használati tippek **********
                    - A parancsok szóközzel elválasztott argumentumokat is kaphatnak, pl.:
                        save_running_config backup.xml
                    - Ismeretlen parancs esetén próbáld újra vagy használd a 'help' parancsot.

                    *******************************************
                    """
                    print(help_text)
                elif cmd[0] == "exit":
                    break
                elif cmd[0]=="get_running_config":
                    config = m.get_config(source="running")
                    xml_str = xml.dom.minidom.parseString(config.xml).toprettyxml()
                    print(xml_str)
                elif cmd[0]=="get_startup_config":
                    config = m.get_config(source="startup")
                    xml_str = xml.dom.minidom.parseString(config.xml).toprettyxml()
                    print(xml_str)
                elif cmd[0]=="save_running_config":
                    if len(cmd)<2:
                        print("Adjon meg elérési útvonalat a mentéshez: 'save_running_config <filename>'")
                        continue
                    config = m.get_config(source="running")
                    xml_str = xml.dom.minidom.parseString(config.xml).toprettyxml()
                    with open(cmd[1], "w", encoding="utf-8") as f:
                        f.write(xml_str)
                    print("Letöltés befejeződött")
                elif cmd[0]=="save_startup_config":
                    if len(cmd)<2:
                        print("Adjon meg elérési útvonalat a mentéshez: 'save_startup_config <filename>'")
                        continue
                    config = m.get_config(source="startup")
                    xml_str = xml.dom.minidom.parseString(config.xml).toprettyxml()
                    with open(cmd[1], "w", encoding="utf-8") as f:
                        f.write(xml_str)
                    print("Letöltés befejeződött")
                elif cmd[0]=="delete_running_config":
                    m.delete_config(target="running")
                    print("A running konfiguráció törölve.")
                elif cmd[0]=="delete_startup_config":
                    m.delete_config(target="startup")
                    print("A startup konfiguráció törölve.")
                else:
                    print("Ismeretlen vagy hibás parancsot adott meg. Próbálja meg újra vagy a 'help' parancs segítségével megnézheti milyen parancsok vannak.")
            except RPCError as e:
                print("Hiba a parancs végrehajtásakor:", e)
            except FileNotFoundError:
                print("Hiba: a megadott elérési út nem létezik.")
            except PermissionError:
                print("Hiba: nincs jogosultság a fájl írásához.")
            except OSError as e:
                print("Fájlműveleti hiba történt:", e)
except AuthenticationError:
    print("Hibás felhasználónév/jelszó")
except SSHError as e:
    print("SSH hiba:", e)
except socket.gaierror:
    print("Host nem elérhető")
except Exception as e:
    print("Más hiba történt:", e)