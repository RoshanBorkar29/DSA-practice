class TextEditor:

    def __init__(self):
        self.text = ""
        self.undo_stack = []
        self.redo_stack = []

    def write(self, word):
        self.undo_stack.append(self.text)
        self.text+=word
        self.redo_stack.clear()
        

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.text)
            self.text=self.undo_stack.pop()
        

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.text)
            self.text=self.redo_stack.pop()
        

    def show(self):

        print(self.text)


editor = TextEditor()

editor.write("Hello")

editor.write(" World")

editor.show()

editor.undo()

editor.show()

editor.redo()

editor.show()