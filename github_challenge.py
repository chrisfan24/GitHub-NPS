import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#SETUP

survey_data = pd.read_csv("/Users/chrisfan/Downloads/nps-exercise.csv", thousands = ',')
ratings = survey_data['answer-10']
acct_ages = survey_data['github_age_in_days']
pd.to_numeric(acct_ages)
total_ratings = ratings.count()
num_surveys = len(ratings)

#count() function excludes the surveys that didn't include a recommendation. 

promoters = ratings[ratings >= 9]
num_promoters = promoters.count()

detractors = ratings[ratings <= 6]
num_detractors = detractors.count()

no_ratings = ratings[ratings.isnull()]

def calc_NPS(p, d, t):
    return (float(p - d) / t) * 100

NPS = calc_NPS(num_promoters, num_detractors, total_ratings)
NPS_withNull = calc_NPS(num_promoters, num_detractors, num_surveys)

#NPS is 60.01% excluding the surveys which didn't have an answer for
#likely the user was to recommend GitHub. Including those users, NPS
#is 59.75.

plt.xticks(range(0, 2500, 365))
plt.hist(acct_ages, bins = range(0, 2500, 365))
plt.title("Age of Survey")
plt.xlabel("Age (days)")
plt.ylabel("Count")


age0 = survey_data[(survey_data['github_age_in_days'] > 0) & (survey_data['github_age_in_days'] <= 365)]
age1 = survey_data[(survey_data['github_age_in_days'] > 365) & (survey_data['github_age_in_days'] <= 365*2)]
age2 = survey_data[(survey_data['github_age_in_days'] > 365*2) & (survey_data['github_age_in_days'] <= 365*3)]
age3 = survey_data[(survey_data['github_age_in_days'] > 365*3) & (survey_data['github_age_in_days'] <= 365*4)]
age4 = survey_data[(survey_data['github_age_in_days'] > 365*4) & (survey_data['github_age_in_days'] <= 365*5)]
age5 = survey_data[(survey_data['github_age_in_days'] > 365*5) & (survey_data['github_age_in_days'] <= 365*6)]
age6 = survey_data[(survey_data['github_age_in_days'] > 365*6)]

#Checking that together, the bins have the same count as the whole dataset

(age0.shape[0] + age1.shape[0] + age2.shape[0] + age3.shape[0] 
+ age4.shape[0] + age5.shape[0] + age6.shape[0] == acct_ages.count())

#NPS Function

def get_NPS(survey): 
    promoters = survey[survey['answer-10'] >= 9]['answer-10'].count()
    detractors = survey[survey['answer-10'] <= 6]['answer-10'].count()
    total = survey['answer-10'].count()
    
    return float(promoters - detractors) / total * 100
    

#NPS by age analysis

NPS_by_age = []
NPS_by_age.append(get_NPS(age0))
NPS_by_age.append(get_NPS(age1))
NPS_by_age.append(get_NPS(age2))
NPS_by_age.append(get_NPS(age3))
NPS_by_age.append(get_NPS(age4))
NPS_by_age.append(get_NPS(age5))
NPS_by_age.append(get_NPS(age6))
    

plt.bar(range(0, 7), NPS_by_age)
plt.title("NPS by Age")
plt.ylabel('NPS')
plt.xlabel('Age')

#NPS is lowest for accounts that are less than two years old - accounts of 
#age 1 have an NPS of 46, while accounts of age 2 have an NPS of 56.6. For the rest
#of GitHub accounts, NPS stays above 60, peaking at 72 for accounts that are between 5
#and 6 years old. However, almost half (734/1600) of GitHub accounts who took this 
#survey are age 0 or 1, so customer sentiment for newer users is worth analyzing. 

#NPS by role analysis

PM = survey_data[(survey_data['answer-3'] == 'Project/product manager')]
ExP = survey_data[(survey_data['answer-3'] == 'Experienced programmer')]
Designer = survey_data[(survey_data['answer-3'] == 'Designer')]
NewP = survey_data[(survey_data['answer-3'] == 'New programmer')]
Writer = survey_data[(survey_data['answer-3'] == 'Writer')]
Other = survey_data[(survey_data['answer-3'] == 'Other (please specify)')]

count_by_role = []
count_by_role.append(PM['id'].count())
count_by_role.append(ExP['id'].count())
count_by_role.append(Designer['id'].count())
count_by_role.append(NewP['id'].count())
count_by_role.append(Writer['id'].count())
count_by_role.append(Other['id'].count())

plt.xticks(range(0, 6), ['PM', 'Ex Programmer', 'Designer', 'New Programmer', 'Writer', 'Other'])
plt.bar(range(0, 6), count_by_role)
plt.title('Survey Counts by Role')
plt.xlabel('Role')
plt.ylabel('Survey count')

NPS_by_role = []
NPS_by_role.append(get_NPS(PM))
NPS_by_role.append(get_NPS(ExP))
NPS_by_role.append(get_NPS(Designer))
NPS_by_role.append(get_NPS(NewP))
NPS_by_role.append(get_NPS(Writer))
NPS_by_role.append(get_NPS(Other))

plt.xticks(range(0, 6), ['PM', 'Experienced', 'Designer', 'New Programmer', 'Writer', 'Other'])
plt.bar(range(0, 6), NPS_by_role)
plt.title('NPS by Role')
plt.xlabel('Role')
plt.ylabel('NPS')



