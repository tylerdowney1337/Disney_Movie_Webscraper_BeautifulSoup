### Convert dollar values and quantifiers into integers ###
import re

# Regular Expressions
amounts = r"thousand|million|billion"
number = r"\d+(,\d{3})*\.*\d*"

value_re = rf"\${number}"
word_re = fr"\${number}(-|\sto\s)?({number})?\s({amounts})"

# Convert word to value
def word_to_value(word):
    value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    return value_dict[word]

# Parse Value and word syntax function
def parse_value_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",", ""))
    return value

def parse_word_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",", ""))
    word = re.search(amounts, string, flags=re.I).group().lower()
    word_value = word_to_value(word)
    return value * word_value

# Money Conversion Function
def money_conversion(money):
    if money == "N/A":
        return None

    if isinstance(money, list):
        money = money[0]

    word_syntax = re.search(word_re, money, flags=re.I)
    value_syntax = re.search(value_re, money)

    if word_syntax:
        return parse_word_syntax(word_syntax.group())
    elif value_syntax:
        return parse_value_syntax(value_syntax.group())
    else:
        return None
