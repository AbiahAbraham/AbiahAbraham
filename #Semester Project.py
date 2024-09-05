#Semester Project
#Team members: Abiah, Ogo, Rakesh, Hrithik

import tkinter as tk
import math

class RationalNum(object):
    def __init__(self, numerator, denominator):
        if denominator < 0:
            raise ValueError("Denominator can NOT be a negative integer!")
        self._num = numerator
        self._denom = denominator
        self.normalize()
        self._operation_stack = []


    def getNumerator(self):
        return self._num

    def setNumerator(self, n):
        self._num = n

    def getDenominator(self):
        return self._denom

    def setDenominator(self, d):
        if d <= 0:
            raise ValueError("Denominator can NOT be a negative integer!")
        self._denom = d

    def normalize(self):
        gcd = math.gcd(self._num, self._denom)
        if gcd not in (0, 1):
            self._num //= gcd
            self._denom //= gcd
        if self._num==0:
          self._denom = 1

    def isPositive(self):
        return self._num * self._denom > 0

    def isZero(self):
        return self._num == 0

    def __eq__(self, other):
        if not isinstance(other, RationalNum):
          return False
        return self._num == other._num and self._denom == other._denom

    def __str__(self):
        return f"{self._num}/{self._denom}"

    def __add__(self, other):
        common_denominator = self._denom * other._denom
        new_numerator = self._num * other._denom + self._denom * other._num
        result = RationalNum(new_numerator, common_denominator)
        self.push_operation(('+', other, result))
        return result

    def __sub__(self, other):
        common_denominator = self._denom * other._denom
        new_numerator = self._num * other._denom - self._denom * other._num
        result = RationalNum(new_numerator, common_denominator)
        self.push_operation(('-', other, result))
        return result

    def __mul__(self, other):
        new_numerator = self._num * other._num
        new_denominator = self._denom * other._denom
        result = RationalNum(new_numerator, new_denominator)
        self.push_operation(('*', other, result))
        return result

    def __truediv__(self, other):
        if other.isZero():
            raise ValueError("Division by zero is not allowed")
        new_numerator = self._num * other._denom
        new_denominator = self._denom * other._num
        result = RationalNum(new_numerator, new_denominator)
        self.push_operation(('/', other, result))
        return result

    def push_operation(self, operation):
        self._operation_stack.append(operation)

    def pop_operation(self):
        if self._operation_stack:
            return self._operation_stack.pop()
        else:
            return None

    def clear_operations(self):
        self._operation_stack = []

    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a
    
a= RationalNum(2,4)
b=RationalNum(3,12)
print(a+b, a-b, a*b, a/b)

class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Rational Calculator")

        # Entry widget to display the input and results
        self.entry = tk.Entry(master, width=20, font=('Arial', 14))
        self.entry.grid(row=0, column=0, columnspan=4)

        # Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'sqrt', '+',
            '(', ')', 'undo', 'C', '=',
        ]

        row_val = 1
        col_val = 0

        # Create and place buttons in the grid
        for button in buttons:
            tk.Button(master, text=button, width=5, height=2, command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Stack to store the input expression
        self.stack = []

    def on_button_click(self, button):
        if button == '=':
            try:
                result = self.evaluate_expression()
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.stack = [str(result)]
            except:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
                self.stack = []
        elif button == 'sqrt':
            self.stack.append('math.sqrt(')
            self.entry.insert(tk.END, 'sqrt(')
        elif button == 'C':
            self.entry.delete(0, tk.END)
            self.stack = []
        elif button == 'undo':
            current_text = self.entry.get()
            if current_text:
                self.entry.delete(0, tk.END)
                self.stack.pop()
                new_text = current_text[:-1]
                self.entry.insert(tk.END, new_text)
        else:
            self.stack.append(button)
            self.entry.insert(tk.END, button)


    def evaluate_expression(self):
        expression = ''.join(self.stack)
        # Replace '/' with '/'
        expression = expression.replace('//', '/')
        # Use Fraction to handle rational numbers
        result = eval(expression)
        # If the result is a Fraction, convert it to a float
        if isinstance(result, RationalNum):
            result = result.__str__()
        return result


class RationalCalculator(RationalNum, Calculator):
    def __init__(self, master):
        RationalNum.__init__(self, 0, 1)
        Calculator.__init__(self, master)

    def calculate(self):
        if self.head is None:
            return None

        current = self.head
        result = current.data

        while current.next_node is not None and current.next_node.next_node is not None:
            operator = current.next_node.data
            operand = current.next_node.next_node.data
            current = current.next_node

            result = self.perform_operation(result, operator, operand)

        return result

    # Override other methods as needed

if __name__ == "__main__":
    root = tk.Tk()
    calculator = RationalCalculator(root)
    root.mainloop()
