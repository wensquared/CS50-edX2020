import cs50

def main():
    h = get_height() + 1
    k = h - 2
    
    for i in range(1,h):
        for j in range(k):
            print(" ", end = "")
        
        for g in range(i):
            print("#", end = "")
        k -= 1
        print()

def get_height():
    while True:
        n = cs50.get_int("Height: ")
        
        if n > 0 and n < 9:
            break
    return n    
    
main()    