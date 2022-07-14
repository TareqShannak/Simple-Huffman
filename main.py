import math

import docx2txt

codes = dict()


class Character:
    def __init__(self, symbol, probability: int, left=None, right=None):
        self.symbol = symbol
        self.probability = probability
        self.left = left
        self.right = right
        self.code = ''


def calculate_code(char, value=''):
    temp = value + str(char.code)

    if char.left:
        calculate_code(char.left, temp)
    if char.right:
        calculate_code(char.right, temp)

    if not char.left and not char.right:
        codes[char.symbol] = temp

    return codes


def output_encoded(data, coding):
    encoding_output = []
    for c in data:
        # print(coding[c], end='')
        encoding_output.append(coding[c])
    string = ''.join([str(item) for item in encoding_output])
    return string


def encoding(symbols_list, frequency):
    nodes = []
    for element in symbols_list:
        nodes.append(Character(element, int(frequency[symbols_list.index(element)])))

    # for node in nodes:
    #     if node.symbol == '\n':
    #         print("'\\n' " + str(node.probability))
    #     else:
    #         print("'" + node.symbol + "' " + str(node.probability))

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.probability)

        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        new_node = Character(left.symbol + right.symbol, left.probability + right.probability, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)

    huffman_encoding = calculate_code(nodes[0])
    # print(huffman_encoding)
    return output_encoded(symbols_list, huffman_encoding)


my_text = docx2txt.process("Shooting+an+elephant+by+George+Orwell+recovered.docx")
# print(my_text)
list_of_symbols = []
count = []
sum_of_characters = 0
for i in my_text:
    sum_of_characters += 1
    if i.upper() not in list_of_symbols:
        list_of_symbols.append(i.upper())
        count.append(1)
    else:
        count[list_of_symbols.index(i.upper())] += 1
ascii_bits = sum_of_characters * 8
average = 0
entropy = 0
encoded_output = encoding(list_of_symbols, count)

for j in list_of_symbols:
    p = count[list_of_symbols.index(j)] / sum_of_characters
    average += p * len(codes[j])
    entropy += - p * math.log(p, 2)

print("\nAverage = " + str(round(average, 3)) + " Bits/Character")
print("Entropy = " + str(round(entropy, 3)) + " Bits/Character")
# print(len(list_of_symbols))


print("For ASCII coding,   # of bits = " + str(ascii_bits))
huffman_bits = 0
for i in encoded_output:
    huffman_bits += 1
print("For Huffman coding, # of bits = " + str(huffman_bits))

print("Percentage of Compression = " + str(round((huffman_bits / ascii_bits) * 100, 3)) + "%")

print("Symbol\tProbability\tLength Of Codeword\tCodeword")
list_selected_symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' ', '.']
for j in list_selected_symbols:
    p = count[list_of_symbols.index(j)] / sum_of_characters
    print("'" + j + "'\t\t\t" + str(round(p, 3)) + "\t\t\t" + str(len(codes[j])) + "\t\t\t" + codes[j])
