import os
import matplotlib.pyplot as plt

class ChartHelper:

    def __init__(self):
        pass

    @staticmethod
    def draw_chart(data, file_name="Test.png"):
        result_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "Result")
        file_name = os.path.join(result_path, file_name)
        plt.figure()
        data.plot()
        plt.savefig(file_name)