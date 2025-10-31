
def sIndex(indexable, index, default):
    if index >= len(indexable):
        return default 
    else:
        return indexable[index]

class LetNum:
    def __init__(self, character = "", count = 1):
        self.character = character
        self.count = count

    def __str__(self):
        return self.character + str(self.count)

class CompressedString:
    def __init__(self, string_in):
        new = []
        for letter in string_in:
            if len(new) == 0:
                new.append(LetNum(letter))
            elif new[-1].character != letter:
                new.append(LetNum(letter))
            elif new[-1].character == letter:
                new[-1].count += 1
        self.string = new

    def __str__(self, normal = False):
        if not normal:
            accumil = ""
            for letter in self.string:
                accumil += letter.character + str(letter.count)+" "
            return accumil
        else:
            accumil = ""
            for letter in self.string:
                accumil += letter.character * letter.count
            return accumil


    def compare(self, other):
        if not isinstance(other, CompressedString):
            other = CompressedString(other)
        if len(self.string) < len(other.string):
            self,other = other,self
        i = 0
        score = 0
        for let1 in self.string:
            let2 = sIndex(other.string,i,LetNum('\0',1))
            if let1.character != let2.character:
                score += 1 
            score += abs(let1.count - let2.count)
            i += 1
        return score


def compare(str1,str2):
    return CompressedString(str1).compare(CompressedString(str2))
