class ArrayStack :
    def __init__( self, capacity ):
        self.capacity = capacity
        self.array = [None]*self.capacity
        self.top = -1

    def isEmpty( self ) :
       return self.top == -1

    def isFull( self ) :
       return self.top == self.capacity-1

    def push( self, item ):
        if not self.isFull() :
            self.top += 1
            self.array[self.top] = item
        else: pass
    def pop( self ):
        if not self.isEmpty():
            self.top -= 1
            return self.array[self.top+1]
        else: pass

    def peek( self ):
        if not self.isEmpty():
            return self.array[self.top]
        else: pass

    def __str__(self ) :
        return str(self.array[0:self.top+1][::-1])

    def size( self ) : return self.top+1

def checkBrackets(statement):
    stack = ArrayStack(100)
    for ch in statement:
        # if ch in ('{', '[', '('):
        # if ch in '{[(':
        if ch=='{' or ch=='[' or ch=='(' :
            stack.push(ch)
        # elif ch in ('}', ']', ')'):
        # elif ch in '}])':
        elif ch=='}' or ch==']' or ch==')' :
            if stack.isEmpty() :
                return False
            else :
                left = stack.pop()
                if (ch == "}" and left != "{") or \
                   (ch == "]" and left != "[") or \
                   (ch == ")" and left != "(") :
                    return False

    return stack.isEmpty()

s1 = " 입력 "
print(s1, " ---> ", checkBrackets(s1))
