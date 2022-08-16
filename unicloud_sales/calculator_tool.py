from math import floor
class Calculator:

    def __init__(self, unit_hour, memory, cpu):
        self.hours_month = unit_hour
        self.memory = memory
        self.cpu = cpu

    def calc_compute(self, mem, cpu):
        result = {}
        subtotal = 0
        if mem/cpu == 2:
            result['informal'] = ((self.hours_month * 0.1541804) * cpu)
            result['eleven_month_agreement'] = (((self.hours_month * 0.1541804) * cpu)/100)*65
            result['thirtysix_month_agreement'] = (((self.hours_month * 0.1541804) * cpu)/100)*40
        if mem/cpu == 4:
            result['informal'] = ((self.hours_month * 0.3060596) * cpu)
            result['eleven_month_agreement'] = (((self.hours_month * 0.3060596) * cpu)/100)*65
            result['thirtysix_month_agreement'] = (((self.hours_month * 0.3060596) * cpu)/100)*40
        if mem/cpu == 8:
            result['informal'] = ((self.hours_month * 0.4625412) * cpu)
            result['eleven_month_agreement'] = (((self.hours_month * 0.4625412) * cpu)/100)*65
            result['thirtysix_month_agreement'] = (((self.hours_month * 0.4625412) * cpu)/100)*65

        return result

    def calc_ssd(self, ammount):
        return 0.92048*ammount

    def calc_hdd(self, ammount):
        return 0.46024*ammount

    def calc_object_storage(self, ammount):
        return 0.143825*ammount

    def get_ratio(self):
        return self.memory/self.cpu

    def get_one_for_two(self, mem, cpu):
        unit_hour = 0.1541804
        quotation = self.hours_month*self.cpu*unit_hour
        return {'cpu': self.cpu, 'memory': self.cpu*2, 'price': round(quotation, 2)}

    def get_one_for_four(self):
        unit_hour = 0.3060596
        quotation = self.hours_month*self.cpu*unit_hour
        return {'cpu': self.cpu, 'memory': self.cpu*4, 'price': round(quotation, 2)}

    def get_one_for_eight(self):
        unit_hour = 0.4625412
        quotation = self.hours_month*self.cpu*unit_hour
        return {'cpu': self.cpu, 'memory': self.cpu*8, 'price': quotation}

    def calculate(self):
        if self.get_ratio() <= 2:
            print(self.get_one_for_two())
        elif self.get_ratio() <= 4:
            if self.get_ratio() != 4:
                print('quebrado')
                print(self.get_one_for_four())
                x = floor((self.get_one_for_four()['memory']-self.memory)/2)
                print(x)
                first_cpu_option = self.memory-x
                second_cpu_oprion = x
                first_quotation = get
            else:
                print(self.get_one_for_four())
        elif self.get_ratio() <= 8:
            if self.get_ratio() != 8:
                print('quebrado')
            else:
                print('menor que 8')


if __name__ == "__main__":
    calculator = Calculator(730, 196, 84)
    calculator.calculate()