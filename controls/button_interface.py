import time

class Button_interface(object):

    def __init__(self, view):
        print("initialize button interface")
        self.v = view

    def check_buttons(self):
        response = raw_input("- ")
        print("Key pressed", response)

        before = time.time()
        self.v.feedback_flashing()

        if(response == "s"):
            print("start Song!")
        elif(response == "p"):
            print("pause Song!")
        elif(response == "p"):
            print("pause Song!")
        elif(response == "q"):
            print("Exit program!")
            return False
        after = time.time()
        difference = after - before
        print("it took", difference)
        return True
