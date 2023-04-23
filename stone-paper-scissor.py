from os import system
from sys import platform as ptfm
from random import choice
from time import sleep
from pyngrok import ngrok
from socket import socket

maxround =2
round, wins, draws, loses =1, 0, 0, 0
moves =['Stone', 'Paper', 'Scissor']

def createTunnel():
    ngrok.set_auth_token('2OLoyviHU2LQT99KyyAFQQwTLFM_6uEBdpzDg47qZrzqS5JgH')
    conn =ngrok.connect(50, 'tcp')
    host, port =conn.public_url.split('/')[-1].split(':')
    return host, port

def createConn():
    server =socket()
    server.bind(('127.0.0.1', 50))
    server.listen(1)
    conn, addr =server.accept()
    return conn

def connect(host, port):
    conn =socket()
    conn.connect((host, port))
    return conn

def gameplay(conn, connType):
    global round, wins, draws, loses
    system('cls') if ptfm.startswith('win') else system('clear')
    print(f'''    
    Round:{round}/{maxround} Wins:{wins} Draws:{draws} Loses:{loses}

    Choose Anyone From:

        1. Stone
        2. Paper
        3. Scissor

        4. Random
    ''')
    move =int(input('Choice: '))
    if move==4: move =choice(moves)
    else: move =moves[move-1]
    if connType=='Server':
        omove =conn.recv(1024).decode()
        conn.sendall(move.encode())
    elif connType=='Client':
        conn.sendall(move.encode())
        omove =conn.recv(1024).decode()
    system('cls') if ptfm.startswith('win') else system('clear')
    round +=1
    if move=='Stone' and omove=='Scissor' or move=='Paper' and omove=='Stone' or move=='Scissor' and omove=='Paper':
        message ='Your Win'
        wins +=1
    elif move==omove:
        message ='Match Draw'
        draws +=1
    else:
        message ='Your Lose'
        loses +=1
    print(f'''

    {move} Vs {omove}
    
    {message}

    ''')

    sleep(3)

print('''
    Select Option:

        1. Create and Listion
        2. Join
''')
option =int(input('Select: '))
system('cls') if ptfm.startswith('win') else system('clear')
if option==1:
    host, port =createTunnel()
    print('\nHost:', host, '\nPort:', port, '\n\nWaiting Connection..')
    conn =createConn()
    type ='Server'
elif option==2:
    conn =connect(input('\nEnter Host: '), int(input('Enter Port: ')))
    type ='Client'
while round <= maxround:
    gameplay(conn, type)

if wins>loses:
    message ='Your Winner Of The Game'
elif wins<loses:
    message ='Your Loser Of The Game'
else:
    message ='Game Draw'

system('cls') if ptfm.startswith('win') else system('clear')
print(f'''
    Your Score: {wins}  Vs   Opponant Score: {loses}
    
    {message}
''')
sleep(5)