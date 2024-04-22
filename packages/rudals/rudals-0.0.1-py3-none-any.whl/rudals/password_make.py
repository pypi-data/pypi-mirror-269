import random
import re

def generate_random_password(length):
    """
    무작위 비밀번호 생성 함수
    :param length: 생성할 비밀번호의 길이
    :return: 생성된 비밀번호
    """
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@$%^&*()."
    password = ''.join(random.sample(characters, length))
    return password

def evaluate_password_strength(password):
    """
    비밀번호 강도 평가 및 안전 여부 검증 함수
    :param password: 평가할 비밀번호
    :return: 비밀번호 강도와 안전 여부를 포함한 메시지
    """
    length = len(password)
    uppercase = any(char.isupper() for char in password)
    lowercase = any(char.islower() for char in password)
    digit = any(char.isdigit() for char in password)
    special_char = re.match(r'^[\w\d]*$', password) is None

    # 강도 평가
    strength = 0
    if length >= 8:
        strength += 1
    if uppercase:
        strength += 1
    if lowercase:
        strength += 1
    if digit:
        strength += 1
    if special_char:
        strength += 1

    # 안전 여부 검증
    if strength >= 4:
        message = "안전한 비밀번호입니다."
    else:
        message = "비밀번호 강도가 낮습니다. 더 강력한 비밀번호를 사용해주세요."

    return f"비밀번호 강도: {strength}/5, {message}"

if __name__ == "__main__":
    # 무작위 비밀번호 생성
    password = generate_random_password(10)
    print("Generated password:", password)

    # 비밀번호 강도 평가
    result = evaluate_password_strength(password)
    print(result)
