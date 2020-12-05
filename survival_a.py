#https://www.statslectures.com/r-scripts-datasets

#Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

#Read dataset
data = pd.read_csv("C:/Users/Seanlove/Desktop/Data Science/Python/lifelines/datasets/lung.csv", sep=',')

#structure of data and additional info about data
print(data.info())

#First five items of the data
print(data.head())

#print columns in data
print(data.columns)

#statistical information about the data
data.describe()

#plot histogram for sex of the patient
print(data["sex"].hist())

#Create an object of KaplanMeierFitter:
km = KaplanMeierFitter()

#Organize our data
#If status =1, then dead =0
#If status =2, then dead =1

data.loc[data.status == 1, 'dead'] = 0
data.loc[data.status == 2, 'dead'] = 1

data.head()

#Fit the parameter values in our object:
km.fit(durations = data["time"], event_observed = data["dead"])

#print the event table
km.event_table
#removed = observed + censored
#censored = person that did not die
#Observed = persons that died

#Calculating the survival probability for a given time
event_at_0 =km.event_table.iloc[0,:]
#Calculate the survival probability for t=0
surv_for_0 = (event_at_0.at_risk - event_at_0.observed)/event_at_0.at_risk
surv_for_0

#Calculating the survival probability for a given time
event_at_11 =km.event_table.iloc[2,:]
#Calculate the survival probability for t=11
surv_for_11 = (event_at_11.at_risk - event_at_11.observed)/event_at_11.at_risk
surv_for_11

#Full list of survival probailities
print(km.survival_function_)

#Plot the graph
km.plot()
plt.ylim([0, 1])
plt.title("The Kaplan-Meier Estimate")
plt.xlabel("Number of days")
plt.ylabel("Probability of survival")
plt.show()

#Median number of days
print("The median survival time:", km.median_survival_time_)

#Survival probability with confidence interval
print(km.confidence_interval_survival_function_)

#plot survival function with confidence interval
conf_surv_func = km.confidence_interval_survival_function_
plt.plot(conf_surv_func["KM_estimate_lower_0.95"], label="Lower")
plt.plot(conf_surv_func["KM_estimate_upper_0.95"], label="Upper")
plt.title("Survival Function With Confidence Interval")
plt.xlabel("Number of days")
plt.ylabel("Survival probability")
plt.legend()
#For the plot to be shown
plt.show()

#Probability of a subject dying
#p(1022) = p(0) + .... + p(1022)
km.cumulative_density_

#plot the cumulative density graph
km.plot_cumulative_density()
plt.title("Cumulative Density Plot")
plt.xlabel("Number of days")
plt.ylabel("Probability of person's death")
plt.show()

#cumulative density with confidence interval
km.confidence_interval_cumulative_density_

#plot cumulative density with confidence interval
conf_cum_density = km.confidence_interval_cumulative_density_
plt.plot(km.confidence_interval_cumulative_density_["KM_estimate_lower_0.95"], label="Lower")
plt.plot(km.confidence_interval_cumulative_density_["KM_estimate_upper_0.95"], label="Upper")
plt.title("Cumulative Density With Confidence Interval")
plt.xlabel("Number of days")
plt.ylabel("Cumulative Density")
plt.legend()
plt.show()

#cumulative density at a specific time:
print(km.cumulative_density_at_times(times=1022))

#Conditional median time to event of interest
print(km.conditional_time_to_event_)

#Hazard function:
from lifelines import NelsonAalenFitter

#Create an object of NelsonAalenFitter:
naf = NelsonAalenFitter()

#Fit our data into the object:
naf.fit(data["time"], event_observed=data["dead"])

#Print the cumulative hazard:
naf.cumulative_hazard_

#Plot the cumulative hazard grpah:
naf.plot_cumulative_hazard()
plt.title("Cumulative Probability for Event of Interest")
plt.xlabel("Number of days")
plt.ylabel("Cumulative Probability of person's death")

#We can predict the value at a certain point :
print("Time = 500 days: ",naf.predict(500))
print("Time = 1022 days: ",naf.predict(1022))

#Cumulative hazard with confidence interval:
naf.confidence_interval_

#Plot cumulative hazard with confidence interval:
confidence_interval = naf.confidence_interval_
plt.plot(confidence_interval["NA_estimate_lower_0.95"],label="Lower")
plt.plot(confidence_interval["NA_estimate_upper_0.95"],label="Upper")
plt.title("Cumulative hazard With Confidence Interval")
plt.xlabel("Number of days")
plt.ylabel("Cumulative hazard")
plt.legend()

#Plot the cumulative_hazard and cumulative density:
km.plot_cumulative_density(label="Cumulative Hazard")
naf.plot_cumulative_hazard(label="Cumulative Density")
plt.xlabel("Number of Days")






