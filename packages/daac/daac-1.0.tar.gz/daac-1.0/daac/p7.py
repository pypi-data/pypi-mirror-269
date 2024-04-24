
from sklearn import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
df = pd.read_csv("startup_funding2021.csv")
# Bar Plot
top_5_sectors = df['Sector'].value_counts().nlargest(5)
plt.figure(figsize=(10, 6))
top_5_sectors.plot(kind='bar')
plt.title('Count of Startups by Sector (Top 5)')
plt.xlabel('Sector')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


#  Pie Chart of the stages of startups
plt.figure(figsize=(8, 8))
df['Stage'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Startup Stages')
plt.ylabel('')
plt.show()

# Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Stage', y='Founded', data=df)
plt.title('Boxplot of Year Founded by Stage')
plt.xlabel('Stage')
plt.ylabel('Year Founded')
plt.xticks(rotation=45)
plt.show()
# Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Founded'], bins=20, kde=True)
plt.title('Histogram of Year Founded')
plt.xlabel('Year Founded')
plt.ylabel('Frequency')
plt.show()

#Scatter Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='HeadQuarter', y='Sector', data=df.head(10))
plt.title('Scatter Plot of HeadQuarter vs Sector')
plt.xlabel('HeadQuarters Location')
plt.ylabel('Sector')
plt.show()

# Heatmap

top_sectors = df['Sector'].value_counts().nlargest(10).index
top_hq = df['HeadQuarter'].value_counts().nlargest(10).index

# Filter the data
df_filtered = df[df['Sector'].isin(top_sectors) & df['HeadQuarter'].isin(top_hq)]

plt.figure(figsize=(12, 8))
sns.heatmap(pd.crosstab(df_filtered['HeadQuarter'], df_filtered['Sector']), annot=True, fmt=".0f", cmap="Blues")
plt.title('Heatmap of HeadQuarter vs Sector')
plt.xlabel('HeadQuarters Location')
plt.ylabel('Sector')
plt.show()



# Line chart
plt.figure(figsize=(10, 6))
df['Founded'].value_counts().sort_index().plot()
plt.title('Number of Startups Founded Over Years')
plt.xlabel('Year')
plt.ylabel('Count')
plt.show()

# CDF
# Extract 'Founded' data
founded_data = df['Founded'].dropna()  # Drop NaN values if any

sorted_data = np.sort(founded_data)

cumulative_prob = np.arange(len(sorted_data)) / len(sorted_data)

# Plot the CDF
plt.figure(figsize=(8, 6))
sns.lineplot(x=sorted_data, y=cumulative_prob)
plt.title('Cumulative Density Function (CDF) of Year Founded')
plt.xlabel('Year Founded')
plt.ylabel('Cumulative Probability')
plt.grid(True)
plt.show()

