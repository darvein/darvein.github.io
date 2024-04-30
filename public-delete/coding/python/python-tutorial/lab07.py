# global and nonlocal scopes
def ex01():
    def scope_test():
        def do_local():
            spam = "local spam"

        def do_nonlocal():
            nonlocal spam
            spam = "nonlocal spam"

        def do_global():
            global spam
            spam = "global spam"

        spam = "test spam"
        do_local()
        print("After local assignment:", spam)
        do_nonlocal()
        print("After nonlocal assignment:", spam)
        do_global()
        print("After global assignment:", spam)

    scope_test()
    print("In global scope:", spam)

# Basic Class definition
def ex02():
    class Singer:
        __is_millonarie = False # private var

        def __init__(self, name):
            self.name = name
            self.songs = []

        def add_song(self, song):
            self.songs.append(song)

        def is_millonaire(self):
            print("{} is a millionarie: {}".format(self.name, self.__is_millonarie))

    eminem = Singer("Eminem")
    tupac = Singer("2pac")
    eminem.add_song("Lose Yourself")
    eminem.add_song("The Real Slim Shady")
    tupac.add_song("Changes")
    print(eminem.is_millonaire())
    print(eminem.songs)
    print(tupac.songs)

#ex01()
#ex02()
