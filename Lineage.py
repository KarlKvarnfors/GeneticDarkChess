from genetics import Population

class Lineage:
    def __init__(self, populations = [], name = ''):
        self.populations = populations
        self.name = name


    def __repr__(self):
        str = 'LINEAGE {}\n\n'.format(self.name)
        str += '\n\n'.join(repr(pop) for pop in self.populations)
        return str

    def fromStr(str):
        Str = str.split('\n\n')
        name = Str.pop(0).split(' ')[1]
        pops = [Population.fromStr(s) for s in Str]
        return Lineage(pops, name)

    def toFile(self, filename = "a.lineage"):
        f = open(filename, 'w')
        f.write(repr(self))
        return f.close()

    def fromFile(filename):
        f = open(filename,'r')
        lin = Lineage.fromStr(f.read())
        f.close()
        return lin
