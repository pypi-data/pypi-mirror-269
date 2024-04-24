from xmlrpc.server import SimpleXMLRPCServer

def arithmetic(n1,n2,opp):
    if opp==1:
        return n1+n2
    elif opp==2:
        return n1-n2
    elif opp==3:
        return n1*n2
    elif opp==4:
        return n1/n2
    else:
        return("not an operator")
        
server=SimpleXMLRPCServer(('localhost',8000))
server.register_function(arithmetic,'calculate')
server.serve_forever()

import xmlrpc.client

def main():
    server = xmlrpc.client.ServerProxy('http://localhost:8000')
    
    while True:
        n1 = int(input("Enter the first number (or 0 to exit): "))
        
        if n1 == 0:
            print("Exiting the program.")
            break
        
        n2 = int(input("Enter the second number: "))
        opp = int(input("Enter 1 for addition, 2 for subtraction, 3 for multiplication, 4 for division (or 0 to exit): "))
        
        if opp == 0:
            print("Exiting the program.")
            break
        
        result = server.calculate(n1, n2, opp)
        print(f"Result: {result}")
if __name__ == '__main__':
    main()
