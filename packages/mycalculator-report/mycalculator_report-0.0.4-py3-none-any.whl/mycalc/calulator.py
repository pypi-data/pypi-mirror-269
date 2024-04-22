
# 닉네임과 비밀번호를 랜덤으로 만들어 추천하기 때문에 이 라이브러리가 필요하다
import random
import string

#자음과 모음을 조합해서 간단한 닉네임을 만들어주는 코드
def nicknamemake():

    consonants = 'bcdfghjklmnpqrstvwxyz'
    vowels = 'aeiou'

    nickname = ''

    for _ in range(2):
        nickname += random.choice(consonants).lower()
        nickname += random.choice(vowels).lower()

    return nickname

#총 8자리의 비밀번호를 만들어주는 함수 / 1자리=>영어 대문자, 2~4자리=>영어 소문자, 5~6자리=>숫자, 7~8자리=> 특정 특수기호
def passwordmake():

    first_letter = random.choice(string.ascii_uppercase)
    rest_letters = ''.join(random.choice(string.ascii_lowercase) for i in range(3))

    digits = ''.join(str(random.randint(0, 9)) for i in range(2))

    special_chars = ''.join(random.choice("~!^*") for i in range(2))

    password = first_letter+ rest_letters+ digits + special_chars

    return password
