from os import system
from sys import platform as ptfm
from random import choice
from time import sleep
from pyngrok import ngrok
from socket import socket

round, uwins, uloses, owins, oloses =1, 0, 0, 0, 0
delay, maxround =10, 5
coin =['Head', 'Tail']

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
    global round, uwins, uloses, owins, oloses
    system('cls') if ptfm.startswith('win') else system('clear')
    print(f'''    
    Round: {round}/{maxround}

    Your Score:  Wins: {uwins} Loses: {uloses}
Opponant Score:  Wins: {owins} Loses: {oloses}

    Guess Anyone From:

        1. Head
        2. Tail
    ''')
    guess =int(input('Choice: '))
    system('cls') if ptfm.startswith('win') else system('clear')
    guess =coin[guess-1]
    if connType=='Server':
        conn.sendall(guess.encode())
        oguess =conn.recv(1024).decode()
    elif connType=='Client':
        oguess =conn.recv(1024).decode()
        conn.sendall(guess.encode())
    
    print(f'''
        Your Guess: {guess}
    Opponant Guess: {oguess}
    ''')
    for i in range(delay, 0, -1):
        print(' Wait', i, 'Seconds, For Coin Flips..', end='\r')
        sleep(1)
    if connType=='Server':
        real =choice(coin)
        conn.sendall(real.encode())
    elif connType=='Client':
        real =conn.recv(1024).decode()
    
    system('cls') if ptfm.startswith('win') else system('clear')
    round +=1
    print('\n', real, '\n')
    if guess==real==oguess:
        message ='Both Guys Currectly Guessed..'
        uwins +=1
        owins +=1
    elif guess==real:
        message ='Your Guess Currect'
        uwins +=1
        oloses +=1
    elif oguess==real:
        message ='Opponant Guess Currect'
        owins +=1
        uloses +=1
    else:
        message ='Both Guys Guessed Incurrectly..'
        uloses +=1
        oloses +=1

    print('', message)
    sleep(5)

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
while round<=maxround:
    gameplay(conn, type)

if uwins>owins:
    message ='Your Winner'
elif uwins<owins:
    message ='Your Loser'
else:
    message ='Match Draw'

system('cls') if ptfm.startswith('win') else system('clear')
print(f'''
    Your Score: {uwins}  Vs   Opponant Score: {owins}
    
    {message}
''')
sleep(5)