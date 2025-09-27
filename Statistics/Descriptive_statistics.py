
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

df = pd.read_excel("sales.xlsx")


#Descriptve Statsistics

df["Total"].head(5)
df["Total"].describe()
df["Total"].info()

df["Total"].mean()
df["Total"].median()
df["Total"].mode()
df["Total"].std()
df["Total"].min()
df["Total"].max()
df["Total"].var()
np.percentile(df["Total"], 25)
np.percentile(df["Total"], 50)
np.percentile(df["Total"], 75)


#Probability Z-score
df['z_scores'] = stats.zscore(df["Total"])

z_score = df['z_scores'][0]
probability = stats.norm.cdf(z_score)

# sampling 
sample_a = df['Total'].sample(n=40, replace=True, random_state=700)
# n= sample size , replacement = can i select same member more than 1 time
# random_state = location to start from

#Centeral Limit Theorem
estimate_list = []
for i in range (1000):
    estimate_list.append(df["Total"].sample(30, replace=True).mean())

estimate_df = pd.DataFrame(data={"esti": estimate_list})

populaion_mean = df["Total"].mean()
estimate_mean = np.mean(estimate_df)
std = np.std(df["Total"])

plt.hist(estimate_df, bins=50)

plt.axvline(populaion_mean, color="green")
plt.axvline(estimate_mean, color="red")

plt.show()




# Confidance Intervals
sample = df.sample(n=40, replace=True, random_state=700)

sample_mean =sample['Total'].mean()
sample_std = sample["Total"].std()
sample_count = sample.shape[0]

sample_st_error = sample_std/np.sqrt(sample_count)

confidence_intervals = stats.norm.interval(0.95, sample_mean, sample_st_error)





sample_a = df['Total'].sample(n=40, replace=True, random_state=700)
sample_b = df['Total'].sample(n=40, replace=True, random_state=1000)

testresult = stats.ttest_ind(sample_a, sample_b, equal_var= False)

conclusion = "Null Rejected" if (testresult.pvalue*100) < 5  else "Faield To Reject Null"
print(conclusion)