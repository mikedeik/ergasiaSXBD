strs = "“A few hours after the shot my left arm was VERY sore"

def create_ngrams(text,num):
    text = text.lower()
    count = 0
    word = ""
    words_list = []

    for ch in text:
        if is_letter(ch):
            word += ch
        else:
            if ch == " ":
                if is_not_stopword(word):
                    count+=1
                    word += ch
                    if count==num:
                        words_list.append(word)
                        word= ""
                        count = 0
                else:
                    word =""
    if word:
        words_list.append(word)

    return words_list


def is_letter(char):
    return ("A" <= char <= "Z") or ("a" <= char <= "z")

def is_not_stopword(string):
    stopwords = {"this","is","at","the"}
    if string in stopwords:
        return False
    else:
        return True

if __name__ == '__main__':
    print(create_ngrams(strs,1))