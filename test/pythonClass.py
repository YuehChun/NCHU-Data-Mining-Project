class Demo:
    i = 9527
     
    def hello(self):
        print("hello")

d = Demo()
# print(d.i)
# # print(d.i) result:
# # 9527


# d.hello()
# # d.hello() result:
# # hello

     
# print(dir(Demo)) 
# # print(dir(Demo)) result:
# # ['__doc__', '__module__', 'hello', 'i']



# help(Demo)
# # help(Demo) result:
# # class Demo
# #  |  Methods defined here:
# #  |  
# #  |  hello(self)
# #  |  
# #  |  ----------------------------------------------------------------------
# #  |  Data and other attributes defined here:
# #  |  
# #  |  i = 9527