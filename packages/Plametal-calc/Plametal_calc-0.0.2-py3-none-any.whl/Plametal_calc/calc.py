
def capitalize_first_letter(sentence):
    
    words = sentence.split()  # 문장을 단어 단위로 분리
    capitalized_words = [word.capitalize() for word in words]  # 각 단어의 첫 글자를 대문자로 변환
    return ' '.join(capitalized_words)  # 변환된 단어들을 다시 조합하여 문장으로 반환

# 사용 예시
    sentence = input()
    result = capitalize_first_letter(sentence)
    print(result)  # 출력: "Hello World"



def remove_duplicates(lst):
    return list(set(lst))


    my_list = input().split()  
    result = remove_duplicates(my_list)
    print(result)

