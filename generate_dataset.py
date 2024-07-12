from lib2to3.pgen2.tokenize import tokenize
import random 
from string import ascii_letters, punctuation, digits
import re
import os
from tqdm import tqdm
import sys
import argparse
import unidecode
import numpy as np


def is_number(s):
    try:
        float(s)  # Thử chuyển chuỗi thành số thực
        return True
    except ValueError:
        return False
    
def delete_characters(text, prob=0.005):
    idx = []
    words = text.split()  
    for i in range(len(words)):
        if words[i] in punctuation or is_number(words[i]):
            continue
        modifyed_line = [] 
        temp = []
        for char in words[i]:
            if random.random() > prob or char in digits:
                modifyed_line.append(char)
            else:
                temp.append(i)

        if len(modifyed_line): 
            words[i] = "".join(modifyed_line)
            idx.extend(set(temp))
    return " ".join(words), idx

def insert_characters(text, prob=0.005):
    idx = []
    words = text.split()  
    for i in range(len(words)):
        if words[i] in punctuation or is_number(words[i]):
            continue
        modifyed_line = [] 
        temp = []
        if random.random() < prob:
            modifyed_line.append(random.choice(ascii_letters))
            temp.append(i)

        for char in words[i]:
            modifyed_line.append(char)
            if random.random() < prob or char in digits:
                modifyed_line.append(random.choice(ascii_letters))
                temp.append(i)

        words[i] = "".join(modifyed_line)
        idx.extend(set(temp))
    return " ".join(words), idx

def replace_characters(text, prob=0.005):
    idx = []
    words = text.split() 
    for i in range(len(words)):
        if words[i] in punctuation or is_number(words[i]):
            continue
        modifyed_line = []  
        for char in words[i]:
            if random.random() <= prob and char not in digits: 
                c = random.choice(ascii_letters)
                modifyed_line.append(c)
                if c != char:
                    idx.append(i)

            else:
                modifyed_line.append(char)
        words[i] = "".join(modifyed_line)

    return " ".join(words), list(set(idx))

def swap_characters_case(text, prob=0.005):
    idx = []  
    words = text.split()
    for i in range(len(words)):
        if words[i] in punctuation or is_number(words[i]):
            continue
        modifyed_word = []
        for char in words[i]:
            if random.random() <= prob:            
                char = char.swapcase()
                idx.append(i)
            modifyed_word.append(char)
        words[i] = "".join(modifyed_word)
    return " ".join(words), idx

def lower_case_words(text, prob=0.025):
    idx = []
    modifyed_line = []   
    for i, word in enumerate(text.split()):
        if word[0].islower() == False and random.random() <= prob:            
            word = word.lower()
            idx.append(i)
        modifyed_line.append(word)
    return " ".join(modifyed_line), idx


clean_chars = re.compile(r'[^A-Za-zöäüÖÄÜß,.!?’\'$%€0-9\(\)\- ]', re.MULTILINE)
def cleanup(text):    
    text = clean_chars.sub('', text)
    #print("bug: somehow all numbers are removed - this is might be due to this regex")
    #exit()
    #text = text.replace("\n", "")
    #text = text.replace('"','\\"')
    return text

#=========================================================================
chars_regrex = '[aàảãáạăằẳẵắặâầẩẫấậAÀẢÃÁẠĂẰẲẴẮẶÂẦẨẪẤẬoòỏõóọôồổỗốộơờởỡớợOÒỎÕÓỌÔỒỔỖỐỘƠỜỞỠỚỢeèẻẽéẹêềểễếệEÈẺẼÉẸÊỀỂỄẾỆuùủũúụưừửữứựUÙỦŨÚỤƯỪỬỮỨỰiìỉĩíịIÌỈĨÍỊyỳỷỹýỵYỲỶỸÝỴnNvVmMCG]'
same_chars = {
    'a': ['á', 'à', 'ả', 'ã', 'ạ', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ'],
    'A': ['Á','À','Ả','Ã','Ạ','Ấ','Ầ','Ẩ','Ẫ','Ậ','Ắ','Ằ','Ẳ','Ẵ','Ặ'],
    'O': ['Ó','Ò','Ỏ','Õ','Ọ','Ô','Ố','Ồ','Ổ','Ỗ','Ộ','Ơ','Ớ','Ờ','Ở','Ỡ','Ợ','Q'],
    'o': ['ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ','ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'q'],
    'e': ['é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'ê'],
    'E': ['É', 'È', 'Ẻ', 'Ẽ', 'Ẹ', 'Ế', 'Ề', 'Ể', 'Ễ', 'Ệ', 'Ê'],
    'u': ['ú', 'ù', 'ủ', 'ũ', 'ụ', 'ứ', 'ừ', 'ử', 'ữ', 'ự', 'ư'],
    'U': ['Ú', 'Ù', 'Ủ', 'Ũ', 'Ụ', 'Ứ', 'Ừ', 'Ử', 'Ữ', 'Ự', 'Ư'],
    'i': ['í', 'ì', 'ỉ', 'ĩ', 'ị'],
    'I': ['Í', 'Ì', 'Ỉ', 'Ĩ', 'Ị'],
    'y': ['ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ', 'v'],
    'Y': ['Ý', 'Ỳ', 'Ỷ', 'Ỹ', 'Ỵ', 'V'],
    'n': ['m'],
    'N': ['N'],
    'v': ['y'],
    'V': ['Y'],
    'm': ['n'],
    'M': ['N'],
    'C': ['G'],
    'G': ['C']
}
def _char_regrex(text):
    match_chars = re.findall(chars_regrex, text)
    return match_chars

def _random_replace(text, match_chars):
    replace_char = match_chars[np.random.randint(low=0, high=len(match_chars), size=1)[0]]
    insert_chars = same_chars[unidecode.unidecode(replace_char)]
    insert_char = insert_chars[np.random.randint(low=0, high=len(insert_chars), size=1)[0]]
    text = text.replace(replace_char, insert_char, 1)

    return text

def change(text):
    match_chars = _char_regrex(text)
    if len(match_chars) == 0:
        return text

    text = _random_replace(text, match_chars)

    return text

def replace_accent_chars(text, prob=0.025):
    idx = []
    words = text.split()
    mask = np.random.random(size=len(words)) < prob

    for i in range(len(words)):
        if words[i] in punctuation or is_number(words[i]):
            continue
        if mask[i]:
            word = change(words[i])
            if words[i] != word:
                idx.append(i)
                words[i] = word

    return ' '.join(words), idx

def remove_random_accent(text, prob=0.025):
    idx = []
    words = text.split()
    mask = np.random.random(size=len(words)) < prob
    
    for i in range(len(words)):
        if words[i] in punctuation or is_number(words[i]):
            continue
        if mask[i]:
            word = unidecode.unidecode(words[i])
            if words[i] != word:
                idx.append(i)
                words[i] = word

    return ' '.join(words), idx

# Space between words
def remove_random_space(text, prob=0.025):
    '''
    - xóa space giữa 2 từ i và i + 1 (không phải dấu câu hoặc số)
    - Không có trường hợp xóa space giữa 3 từ
    '''
    idxs = []
    words = text.split()
    num_words = len(words)
    out = text
    for i in range(num_words):
        if i + 2 >= len(words): break
        if words[i] in punctuation or is_number(words[i]):
            continue
        if words[i + 1] in punctuation or is_number(words[i + 1]):
            continue
        if random.random() < prob:
            out = ' '.join(words[:i])  + ' ' + ''.join(words[i:i + 2]) + ' ' + ' '.join(words[i + 2:])
            words = out.split()
            idxs.append(i)
    return out.strip(), idxs