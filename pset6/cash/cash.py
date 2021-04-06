import cs50

def main():
    
    n = change_owed()
    coins = 0
    
    while n > 0:
        if n >= 25:
            coins = coins + int(n / 25)
            n = n % 25
        elif n < 25 and n >= 10 and n > 5:
            coins = coins + int(n / 10)
            n = n % 10
        elif n < 25 and n < 10 and n > 1:
            coins = coins + int(n / 5)
            n = n % 5
        else:
            coins +=n
            n = n % 1
    
    print(coins)
            
        
    
def change_owed():
    
    while True:
        n = cs50.get_float("Changed owed: ")
        
        if n > 0:
            break
    
    
    return round(n * 100)
    
main()