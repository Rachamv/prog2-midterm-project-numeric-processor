import json
import urllib.parse
import urllib.request

class NumericProcessor:
    def __init__(self, computations_list):
        self.computations_list = computations_list
        self.ans = 0

    def run_computations(self):
        for computation in self.computations_list:
            self.run_one_computation(computation)

    def run_one_computation(self, computation):
        operator = computation["operation"]
        operands = computation["values"]

        match operator:
            case "add":
                self.ans = self.add(operands)

            case "subtract":
                self.ans = self.subtract(operands)

            case "divide":
                self.ans = self.divide(operands)

            case "multiply":
                self.ans = self.multiply(operands)

            case "api-compute":
                self.ans = self.send_to_api(operands[0])

            case "display":
                print(self.ans)

    def add(self, operand):
        result = 0
        for value in operand:
            if value == "ANS":
                value = self.ans
            value = float(value)
            result += value
        return result

    def divide(self, operand):
        for index, value in enumerate(operand):
            if value == "ANS":
                operand[index] = self.ans
            if type(operand[index]) == str:
                operand[index] = float(value)
        return operand[0] / operand[1]

    def multiply(self, operand):
        for index, value in enumerate(operand):
            if value == "ANS":
                operand[index] = self.ans
            if type(operand[index]) == str:
                operand[index] = float(value)
        return operand[0] * operand[1]

    def subtract(self, operand):
        for index, value in enumerate(operand):
            if value == "ANS":
                operand[index] = self.ans
            if type(operand[index]) == str:
                operand[index] = float(value)
        return operand[0] - operand[1]

    def send_to_api(self, expr):
        url = get_mathjs_api_url(expr)
        response = urllib.request.urlopen(url)
        result = response.read().decode("utf-8")
        return float(result)


class OperationCounterNumericProcessor(NumericProcessor):
    def __init__(self, computations_list):
        super().__init__(computations_list)
        self.count_operations = {}

    def run_one_computation(self, computation):
        operator = computation["operation"]
        operands = computation["values"]

        if operator in self.count_operations:
            self.count_operations[operator] += 1
        else:
            self.count_operations[operator] = 1

        super().run_one_computation(computation)

    def show_statistics(self):
        for operation, count in self.count_operations.items():
            print(f"operation: {operation}, count: {count}")


def load_computations_list_from_file(filename):
    with open(filename, "r") as f:
        contents = json.load(f)
        return contents["computations"]


def get_mathjs_api_url(expression):
    expression = urllib.parse.quote(expression)
    url = "http://api.mathjs.org/v4/?expr=" + expression
    return url


if __name__ == "__main__":
    computations = load_computations_list_from_file("example_api.json")

    processor = NumericProcessor(computations)
    processor.run_computations()

    counter_processor = OperationCounterNumericProcessor(computations)
    counter_processor.run_computations()
    counter_processor.show_statistics()
