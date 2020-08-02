i = [0, 1, 2, 3, 4, 5]

# while(True):
#     continue
#     print "You won't see this"

# while(True):
#     pass
#     print "You will see this"
for x in i:
    try:
        if x == 3:
            raise AttributeError("ERROR")
    except AttributeError as e:
        print("we passed" + str(e))
    except Exception as e:
        print("HII")
    else:
        print(x)
      
