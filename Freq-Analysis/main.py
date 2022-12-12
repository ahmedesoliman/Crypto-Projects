
#open text file in read mode
text_file = open("cipherText.txt", "r")
 
#read whole file to a string
str = text_file.read()
 
#close file
text_file.close()

str = str.replace(' ', '')  #removing empty spaces from the string
str = str.replace('\n', '')  #cleaning new lines from the string

count = len(str)  #counting total numbers of characters.

#Given english alphabet letters frequency
given_dictionary = {
  "A": 0.0817, "B" : 0.0150, "C" : 0.0278, "D" :0.0425, 
  "E": 0.1270, "F": 0.0223, "G": 0.0202, "H": 0.0609, 
  "I": 0.0697, "J": 0.0015, "K": 0.0077, "L": 0.0403, 
  "M": 0.0241, "N": 0.0675, "O": 0.0751, "P": 0.0193, 
  "Q": 0.0010, "R": 0.0599, "S": 0.0633, "T": 0.0906, 
  "U": 0.0276, "V": 0.0098, "W": 0.0236, "X": 0.0015, 
  "Y": 0.0197, "Z": 0.0007,
}
  
sorted_givenDic = sorted(given_dictionary.items(), key=lambda x: x[1] , reverse=True)

# print ("\nSorted english letters frequency")
# for alpha, num in sorted_givenDic :
#   print(alpha, " = ", num)

dictionary = dict()  #creating empty dictionary to keep track of frequency

#creating the dictionary with letter occurences in the cipher text.
for i in str:
    if i in dictionary:
        dictionary[i] = dictionary[i] + 1
    else:
        dictionary[i] = 0

#Chnaging values of dictinoary to the frequecy based on the cipher text
for i in dictionary:
  dictionary[i] = round((dictionary[i] / count), 4)

#creating a new dictionary with sorted letter frequecy
sorted_dic = sorted(dictionary.items(), key=lambda x: x[1] , reverse=True)

# print ("\nSorted cipher letters frequency")
# for alpha, num in sorted_dic:
#   print (alpha, "=", num)


#printing the frequency in a tabular format.
print("\nGiven-Freq  --  Text-Freq\n")
for l, r in zip(sorted_dic, sorted_givenDic):
  print (l, "-", r)

  
#mapping letters based on frequency
def build_key():
  buildKey = [(a[0], b[0]) for a, b in zip(sorted_dic ,sorted_givenDic)]
  buildKey.append(("z", "Z")) #added Z because it was never mentioned in the cipher text
  return buildKey
  
# for x in build_key():
#   print (x)

def decoder(ciphertext, key):
    for x, y in key:
        ciphertext = ciphertext.replace(x, y)
    return ciphertext

def get_key():
 
    return [
        ('r', 'E'), ('b', 'T'), ('m', 'A'),
        ('k', 'N'), ('j', 'O'), ('w', 'I'),
        ('i', 'S'), ('p', 'H'), ('u', 'R'),
        ('d', 'D'), ('h', 'L'), ('v', 'C'),
        ('x', 'F'), ('y', 'M'), ('n', 'U'),
        ('s', 'P'), ('t', 'Y'), ('l', 'B'),
        ('o', 'G'), ('q', 'K'), ('a', 'X'),
        ('c', 'W'), ('e', 'V'), ('g', 'Z'),
        ('f', 'Q'), ('z', 'J')
    ]

manual_key = get_key()
auto_key = build_key()

#open text file in read mode
text_file = open("cipherText.txt", "r")
 
#read whole file to a string
data = text_file.read()
 
#close file
text_file.close()

print("\n Auto Try:\n",decoder(data, auto_key))
print("\n Manual Try:\n",decoder(data, manual_key))