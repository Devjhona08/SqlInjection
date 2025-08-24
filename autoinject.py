import nmap
import os
import socket
import datetime
import pyfiglet

# ====== Colores ======
AMARILLO = "\033[93m"
BLANCO = "\033[97m"
CYAN = "\033[96m"
VERDE = "\033[92m"
ROJO = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


# ====== Cabecera ======
def cabecera():
    banner = pyfiglet.figlet_format("Sql Injector")
    print(ROJO + banner + RESET)
    print(CYAN + " Offensive Security & Audit Tool       by < devjhonatan >" + RESET)
    print(VERDE + " github: https://github.com/Devjhona08")
    print("------------------------------------------------------------")


cabecera()


# ====== Escaneo de Puertos ======
def escanear_puertos(ip, output_file=None):
    nm = nmap.PortScanner()
    print(VERDE + f"[*] Escaneando puertos en {ip} ..." + RESET)
    try:
        nm.scan(ip, arguments="-sS -T4")
        results = []
        for host in nm.all_hosts():
            host_info = (
                f"Host: {host} ({nm[host].hostname()}) - Estado: {nm[host].state()}"
            )
            print(AMARILLO + host_info + RESET)
            results.append(host_info)
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in sorted(lport):
                    port_info = (
                        f"Puerto {port}/{proto} - {nm[host][proto][port]['state']}"
                    )
                    color = VERDE if nm[host][proto][port]["state"] == "open" else ROJO
                    print(color + port_info + RESET)
                    results.append(port_info)
        if output_file:
            save_results(results, output_file)
    except Exception as e:
        print(ROJO + f"[!] Error: {str(e)}" + RESET)


# ====== Escaneo de Servicios ======
def escanear_servicios(ip, output_file=None):
    print(VERDE + f"[*] Escaneando servicios en {ip} ..." + RESET)
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments="-sV -T4")
        results = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]["state"]
                    name = nm[host][proto][port]["name"]
                    service_info = f"Puerto {port}/{proto} - {name} - {state}"
                    print(AMARILLO + service_info + RESET)
                    results.append(service_info)
        if output_file:
            save_results(results, output_file)
    except Exception as e:
        print(ROJO + f"[!] Error: {str(e)}" + RESET)


# ====== Inyección SQL (sqlmap wrapper) ======
def inyeccion_sql(url, output_file=None):
    print(VERDE + f"[*] Probando SQL Injection en {url} ..." + RESET)
    try:
        command = f"sqlmap -u {url} --batch --level=2 --risk=2 --random-agent"
        os.system(command)
        if output_file:
            save_results([f"SQLMap ejecutado sobre {url}"], output_file)
    except Exception as e:
        print(ROJO + f"[!] Error: {str(e)}" + RESET)


# ====== Guardar resultados ======
def save_results(results, filename):
    with open(filename, "a") as f:
        f.write("\n".join(results) + "\n")
    print(MAGENTA + f"[+] Resultados guardados en {filename}" + RESET)


# ====== Main ======
def main():
    while True:
        print(CYAN + "\n[+] Menú de Auditoría" + RESET)
        print("1. Escanear Puertos")
        print("2. Escanear Servicios")
        print("3. Pruebas de Inyección SQL")
        print("4. Salir")

        opcion = input(VERDE + "> " + RESET)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"report_{timestamp}.txt"

        if opcion == "1":
            ip = input(CYAN + "[*] Ingrese la IP o dominio a escanear: " + RESET)
            escanear_puertos(ip, output_file)
        elif opcion == "2":
            ip = input(CYAN + "[*] Ingrese la IP o dominio a escanear: " + RESET)
            escanear_servicios(ip, output_file)
        elif opcion == "3":
            url = input(CYAN + "[*] Ingrese la URL: " + RESET)
            inyeccion_sql(url, output_file)
        elif opcion == "4":
            print(ROJO + "[*] Saliendo..." + RESET)
            break
        else:
            print(ROJO + "[!] Opción inválida" + RESET)


if _name_ == "_main_":
    main()
