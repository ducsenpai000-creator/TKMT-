import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

tips = sns.load_dataset("tips")

sns.scatterplot(x="total_bill", y="tip", hue="smoker", data=tips)
plt.title("Mối quan hệ giữa tổng hóa đơn và tiền boa")
plt.show()

sns.boxplot(x="day", y="total_bill", data=tips)
plt.title("Phân bố tổng hóa đơn theo ngày")
plt.show()

sns.histplot(data=tips, x="total_bill", hue="sex", multiple="stack")
plt.title("Phân phối tổng hóa đơn theo giới tính")
plt.show()

sns.pairplot(tips, hue="smoker")
plt.show()