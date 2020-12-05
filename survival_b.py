#Import required libraries:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

#Read the dataset:
data = pd.read_csv("lung.csv")
data.head()

#Organize our data:
#If status = 1 , then dead = 0
#If status = 2 , then dead = 1
data.loc[data.status == 1, 'dead'] = 0
data.loc[data.status == 2, 'dead'] = 1
data.head()

#Create two objects for groups:
#km_m for male data:
#km_f for female data:
km_m = KaplanMeierFitter() 
km_f = KaplanMeierFitter() 

#Dividing data into groups:
Male = data.query("sex == 1")
Female = data.query("sex == 2")

#View data of Male group:
Male.head()

#View data of Female group:
Female.head()

#Fit data into objects:
km_m.fit(durations =  Male["time"],event_observed = Male["dead"] ,label="Male")
km_f.fit(durations =  Female["time"],event_observed = Female["dead"], label="Female")

#Event table for male group:
km_m.event_table

#Event table for female group:
km_f.event_table

#Predict value based on time:
km_m.predict(11)

#Predict value based on time:
km_f.predict(11)

#Get complete data of survival function for male group:
km_m.survival_function_

#Get complete data of survival function for female group:
km_f.survival_function_

#Plot the survival_function data:
km_m.plot()
km_f.plot()
plt.xlabel("Days Passed")
plt.ylabel("Survival Probability")
plt.title("km")

#Cumulative density for male group:
km_m.cumulative_density_

#Cumulative density for female group:
km_f.cumulative_density_

#PLot the graph for cumulative density for both groups:
km_m.plot_cumulative_density()
km_f.plot_cumulative_density()
plt.title("Cumulative Density")
plt.xlabel("Number of days")
plt.ylabel("Probability")

#Hazard Function:
from lifelines import NelsonAalenFitter

#Fitting the data into objects:
naf_m = NelsonAalenFitter()
naf_f = NelsonAalenFitter()
naf_m.fit(Male["time"],event_observed = Male["dead"])
naf_f.fit(Female["time"],event_observed = Female["dead"])

#Cumulative hazard for male group:
naf_m.cumulative_hazard_

#Cumulative hazard for female group:
naf_f.cumulative_hazard_

#Plot the graph for cumulative hazard:
naf_m.plot_cumulative_hazard(label="Male")
naf_f.plot_cumulative_hazard(label="Female")
plt.title("Cumulative Hazard Plot")
plt.xlabel("Number of Days")
plt.ylabel("Cumulative Hazard")

#Conditional median time to event of interest:
km_m.conditional_time_to_event_

#Conditional median time left for event for male group:
median_time_to_event = km_m.conditional_time_to_event_
plt.plot(median_time_to_event,label="Median Time left")
plt.title("Medain time to event")
plt.xlabel("Total days")
plt.ylabel("Conditional median time to event")
plt.legend()

#Conditional median time to event of interest for female group:
km_f.conditional_time_to_event_

#Conditional median time left for event for female group:
median_time_to_event = km_f.conditional_time_to_event_
plt.plot(median_time_to_event,label="Median Time left")
plt.title("Medain time to event")
plt.xlabel("Total days")
plt.ylabel("Conditional median time to event")
plt.legend()

#Survival probability with confidence interval for male group:
km_m.confidence_interval_survival_function_

#Plot survival function with confidence interval for male group:
confidence_surv_func = km_m.confidence_interval_survival_function_
plt.plot(confidence_surv_func["Male_lower_0.95"],label="Lower")
plt.plot(confidence_surv_func["Male_upper_0.95"],label="Upper")
plt.title("Survival Function With Confidence Interval")
plt.xlabel("Number of days")
plt.ylabel("Survival Probability")
plt.legend()

#Survival probability with confidence interval for female group:
km_f.confidence_interval_survival_function_

#Plot survival function with confidence interval for female group:
confidence_surv_func = km_f.confidence_interval_survival_function_
plt.plot(confidence_surv_func["Female_lower_0.95"],label="Lower")
plt.plot(confidence_surv_func["Female_upper_0.95"],label="Upper")
plt.title("Survival Function With Confidence Interval")
plt.xlabel("Number of days")
plt.ylabel("Survival Probability")
plt.legend()

#Plot the cumulative_hazard and cumulative density:
km_m.plot_cumulative_density(label="Male Density")
naf_m.plot_cumulative_hazard(label="Male Hazard")
plt.xlabel("Number of Days")

#Plot the cumulative_hazard and cumulative density:
km_f.plot_cumulative_density(label="Female Density")
naf_f.plot_cumulative_hazard(label="Female Hazard")
plt.xlabel("Number of Days")

#Define variables for log-rank test:
Time_A = Male['time']
Event_A = Male['dead']

Time_B = Female['time']
Event_B = Female['dead']

#Performing the Log-Rank test:
from lifelines.statistics import logrank_test

results = logrank_test(Time_A, Time_B, event_observed_A=Event_A, event_observed_B=Event_B)
results.print_summary()

#Print the P-value:
print("P-value :",results.p_value)