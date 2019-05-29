from abc import ABC, abstractmethod
import math


class Base(ABC):
    def __init__(self, data, result):
        self.data = data
        self.result = result

    def get_answer(self):
        return [int(x >= 0.5) for x in self.data]

    def get_score(self):
        ans = self.get_answer()
        return sum([int(x == y) for (x, y) in zip(ans, self.result)]) / len(ans)

    @abstractmethod
    def get_loss(self):
        pass


class A(Base):

    def get_loss(self):
        return sum([(x - y) * (x - y) for (x, y) in zip(self.data, self.result)])


class B(Base):

    def get_loss(self):
        return -sum([y * math.log(x) + (1 - y) * math.log(1 - x) for (x, y) in zip(self.data, self.result)])

    def get_pre(self):
        ans = self.get_answer()
        res = [int(x == 1 and y == 1) for (x, y) in zip(ans, self.result)]
        return sum(res) / sum(ans)

    def get_rec(self):
        ans = self.get_answer()
        res = [int(x == 1 and y == 1) for (x, y) in zip(ans, self.result)]
        return sum(res) / sum(self.result)

    def get_score(self):
        pre = self.get_pre()
        rec = self.get_rec()
        return 2 * pre * rec / (pre + rec)


class C(Base):

    def get_loss(self):
        return sum([abs(x - y) for (x, y) in zip(self.data, self.result)])


if __name__ == "__main__":
    print('Base:\t', list(filter(lambda x: x[0] != '_' and x[1] != '_', dir(Base))))
    print('A:\t\t', list(filter(lambda x: x[0] != '_' and x[1] != '_', dir(A))))
    print('B:\t\t', list(filter(lambda x: x[0] != '_' and x[1] != '_', dir(B))))
    print('C:\t\t', list(filter(lambda x: x[0] != '_' and x[1] != '_', dir(C))))
