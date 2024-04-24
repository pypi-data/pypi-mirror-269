import Pyro4
@Pyro4.expose
class PalindromeChecker(object):
    def is_palindrome(self, text):
        text = text.lower().replace(" ", "")
        return text == text[::-1]

daemon=Pyro4.Daemon()
uri=daemon.register(PalindromeChecker)
print(uri)
daemon.requestLoop()

import Pyro4

def main():
    uri = input("enter server uri:")
    checker = Pyro4.Proxy(uri)
    text = input("Enter a string to check if it's a palindrome: ")
    is_palindrome = checker.is_palindrome(text)
    
    if is_palindrome:
        print(f"'{text}' is a palindrome.")
    else:
        print(f"'{text}' is not a palindrome.")
if __name__ == "__main__":
    main()
