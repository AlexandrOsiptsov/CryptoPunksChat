from cmath import e
import random
from flask import Flask, request, jsonify, session, render_template, url_for
import uuid
import sympy
import math
from .credential import *
first_primes_list = []  

exponent = None
modulus = None
s_key = None

#Решето Эратосфена
def SieveOfEratosthenes(n):
    global first_primes_list  

    prime = [True for i in range(n + 1)]
    p = 2
    count = 0  # Счетчик найденных простых чисел
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1

    for p in range(2, n + 1):
        if prime[p]:
            first_primes_list.append(p)  
            count += 1
            if count == 250: 
                break

#Поиск первых 500 простых чисел
def fillPrimeList():
    n = 500 
    print("Finding the first 500 prime numbers...")
    SieveOfEratosthenes(n)
    print("Finding the first 500 prime numbers is finished")

#Get random n-bit value
def nBitRandom(n):
    return(random.randrange(2**(n-1)+1, 2**n-1))

#Получить n-битное число кандидата на простоту
def getLowLevelPrime(n)->int:
    global first_primes_list 
    
    while True: 
        prime_candidate = nBitRandom(n) 
   
        for divisor in first_primes_list: 
            if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                break
            else: 
                return prime_candidate

    return 0

#Идентификатор прохождения теста Миллера-Рабина
def isMillerRabinPassed(miller_rabin_candidate):
   
    maxDivisionsByTwo = 0
    evenComponent = miller_rabin_candidate-1
   
    while evenComponent % 2 == 0:
        evenComponent >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * evenComponent == miller_rabin_candidate-1)
   
    def trialComposite(round_tester):
        if pow(round_tester, evenComponent, 
               miller_rabin_candidate) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * evenComponent,
                   miller_rabin_candidate) == miller_rabin_candidate-1:
                return False
        return True
   
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2,
                       miller_rabin_candidate)
        if trialComposite(round_tester):
            return False
    return True

#Возвращает n-битное простое число
def  doItPrime(bit_len)-> int:
    print(f"Getting prime {bit_len} bit number...")
    while True:
        prime_candidate = getLowLevelPrime(bit_len)
        if (not prime_candidate) or (not isMillerRabinPassed(prime_candidate)):
            continue
        else:
            break
    print(f"Getting prime {bit_len} bit number is finished")
    return prime_candidate

#Расширенный алгоритм Евклида
def extended_euclidean_algorithm(a, b):

    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_euclidean_algorithm(b % a, a)
        return g, x - (b // a) * y, y

#Поиск обратного
def modular_inverse(e, t):
    print(f"Getting secret RSA key...")
    g, x, y = extended_euclidean_algorithm(e, t)
    print(f"Getting secret RSA key is finished")
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % t

#Инициализирует все переменные
def preSet():
    global exponent
    global modulus
    global s_key
    fillPrimeList()
    p=doItPrime(1024)
    q=doItPrime(1024)
    k = 2
    modulus=p*q
    phi=(p-1)*(q-1)
    exponent=7
    while(exponent<phi):
        if (math.gcd(exponent, phi) == 1):
         break
        else:
         exponent += 2
    s_key = round(modular_inverse(exponent, phi))

    return modulus, exponent, s_key
