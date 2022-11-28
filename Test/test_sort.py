class C:
    def __init__(self, idn: int):
        self.id = idn


lis = []
for i in range(5):
    lis.append(C(i))
lis.sort(key=lambda x: x.id, reverse=True)
for c in lis:
    print(c.id)
