from turtle import done


class Fond(object):
    
    fond_list = []
    total = 0

    def __init__(self, name, perc, sum):
        self.name = name
        self.perc = perc
        self.sum = sum
        Fond.fond_list.append(self)
        Fond.total += sum
    
    def addMoney(x):
        for tmp in Fond.fond_list:
            tmp.sum += tmp.perc * x
        Fond.total += x
        return True, f"ВНЕСЕНО: {x}\n"

    def takeMoney(name, sum):
        for index, item in enumerate(Fond.fond_list):
            if item.name == name:
                if Fond.fond_list[index].sum >= sum:
                    Fond.fond_list[index].sum -= sum
                    Fond.total -= sum
                    return True, f"СПИСАНО: {sum} из {name}\n"
                else: return False, "Недостаточно средств"
                
        
    