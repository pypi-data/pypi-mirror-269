# xor 암호화: xor 연산을 두번 실행하면 원본데이터로 돌아오는 원리를 이용한 암호화 
import random

def en_de(str, key):
    en_str = ""
    for i in range(len(str)):
        en_str = en_str + chr(ord(str[i]) ^ ord(key[i % len(key)]))
    return en_str

def rand_key():
  key = ''
  for i in range(random.randint(10, 30)):
    key += str(random.randint(0,9))
  return key
