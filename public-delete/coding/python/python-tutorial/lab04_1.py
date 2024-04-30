import lab04

mod_response = lab04.hello()
local_response = __name__

if __name__ == '__main__':
    import sys
    print("BTW I'm the main program! " + sys.argv[0])

print("Local response: {}".format(local_response))
print("Module response: {}".format(mod_response))
