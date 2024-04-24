import Pyro4
@Pyro4.expose
class stringconcatenator:
    def concatenate(self,str1,str2):
        return str1+str2

daemon=Pyro4.Daemon()
uri=daemon.register(stringconcatenator)
print(uri)
daemon.requestLoop()

import Pyro4

uri=input("enter uri of server")
concatenator=Pyro4.Proxy(uri)
str1=input("enter string 1")
str2=input("enter string 2")
result=concatenator.concatenate(str1,str2)
print(result)
