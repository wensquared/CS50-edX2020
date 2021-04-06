import cs50

text = cs50.get_string("Text: ")
sent = 0
abc = 0
word = 1

for c in range(len(text)):
    if text[c] == "." or text[c] == "?" or text[c] == "!":
        sent += 1
    elif text[c] == " ":
        word += 1
    elif text[c].isalpha():
        abc += 1

print(f"words = {word}, sentences: {sent}, letters: {abc}")

l = (abc / word) * 100
s = (sent / word) * 100

j = (0.0588 * l) - (0.296 * s) - 15.8

grade = round(j)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print("Grade " + str(grade))

