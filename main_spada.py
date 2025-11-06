import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

"""---------------------------------------------------------------------"""

patients = pd.read_csv("data/patients.csv")

patients["tranche_age"] = pd.cut(
patients.age, bins=[0,20,60,patients.age.max()], labels=['young','adult','elderly'])

patients["duree"] = (pd.to_datetime(patients.departure_date) - pd.to_datetime(patients.arrival_date)).dt.days


patients["tranche_duree"] = pd.cut(patients.duree, bins=[0,7,patients.duree.max()], labels=['- d\'une semaine',' + d\'une semaine'])
"""'patient_id', 'name', 'age', 'arrival_date', 'departure_date','service', 'satisfaction', 'tranche_age'"""

"""---------------------------------------------------------------------"""

services_weekly = pd.read_csv("data/services_weekly.csv")

services_weekly["taux_acces"] = services_weekly['patients_admitted'] / services_weekly['patients_request']

"""'week', 'month', 'service', 'available_beds', 'patients_request',
   'patients_admitted', 'patients_refused', 'patient_satisfaction',
   'staff_morale', 'event', 'taux_acces'"""

services_weekly.loc[services_weekly.week >= 49, 'month'] = 13


"""---------------------------------------------------------------------"""

staff_schedule = pd.read_csv("data/staff_schedule.csv")
"""'week', 'staff_id', 'staff_name', 'role', 'service', 'present'"""

"""---------------------------------------------------------------------"""

"""satisfaction en fonction de l'âge / service / durée"""

patients.groupby(by='age')['satisfaction'].mean().plot(
style='o', ylabel='satisfaction', title='satisfaction en fonction de l\'âge')
plt.show()

patients.groupby(by='tranche_age')['satisfaction'].mean().plot(
style='o', ylabel='satisfaction', title='satisfaction en fonction de la tranche d\'âge')

plt.show()

patients.groupby(by='service')['satisfaction'].mean().plot(
style='o', ylabel='satisfaction', title='satisfaction en fonction du service')

plt.show()

patients.groupby(by='duree')['satisfaction'].mean().plot(
style='o', ylabel='satisfaction', title='satisfaction en fonction de la durée de séjour')

plt.show()

patients.groupby(by='tranche_duree')['satisfaction'].mean().plot(
style='o', ylabel='satisfaction', title='satisfaction en fonction de la tranche de durée de séjour')

plt.show()

"""---------------------------------------------------------------------"""

"""descirption du personnel par secteur (nbf infirmiers, docteurs)"""

staff_schedule.groupby(by=['service','role'])['staff_id'].nunique().unstack(1).plot.bar(
ylabel='nombre de personnel',title='description du personnel par secteur')

plt.show()

"""---------------------------------------------------------------------"""

"""sur l'année : nbr d'entrée par tranche d'âge"""

patients.groupby(by='tranche_age')['patient_id'].count().plot(style='o',ylabel='nombre d\'entrée', title='nombre d\'entrée par tranche d\'âge')
plt.show()

"""---------------------------------------------------------------------"""

"""moral moyen staff en fct du service + moral du staff par évènement"""

services_weekly.groupby(by='service')['staff_morale'].mean().plot(style='o', ylabel='moral moyen du staff', title='moral moyen du staff par service')
plt.show()

services_weekly.groupby(by='event')['staff_morale'].mean().plot(
style='o', ylabel='moral moyen du staff', title='moral moyen du staff par évènement')
plt.show()

services_weekly.boxplot(column='staff_morale', by='service', ylabel='moral du staff')
plt.suptitle('répartition du moral du staff par service')

plt.title('')
plt.show()

"""---------------------------------------------------------------------"""

"""taux de présence de chaque membre du personnel"""

staff_schedule.groupby(by='role')['present'].mean().plot(style='o', ylabel='taux de présence', title='taux de présence par rôle')
plt.show()

"""---------------------------------------------------------------------"""

"""admission, refus au cours du temps par secteur ou taux de refus en fct du temps par secteur"""

services_weekly.groupby(by=['month','service'])['taux_acces'].mean().unstack(1).plot(
ylabel='taux d\'admission', title='taux d\'admission par secteur au cours du temps')

plt.show()

"""---------------------------------------------------------------------"""

"""nbr de requêtes par secteur au cours du temps"""

services_weekly.groupby(by=['month','event']).size().unstack(1).plot()
plt.show()

services_weekly.groupby(by=['month','service'])['patients_request'].sum().unstack(1).plot(
ylabel='nombre de requêtes', title='nombre de requêtes par secteur au cours du temps')

services_weekly.loc[services_weekly.service =='emergency'].groupby(by=['month','event']).size().unstack(1).plot(style ='o-', title="Evenements aux urgences au cours du temps")
services_weekly.loc[services_weekly.service =='general_medicine'].groupby(by=['month','event']).size().unstack(1).plot(style ='o-', title="Evenements en médecine générale au cours du temps")
plt.show()

"""---------------------------------------------------------------------"""

"""durée moyenne passée par patient par secteur + durée moyenne passée en fonction de l'âge du patient"""

patients.groupby(by=['service'])['duree'].mean().plot(
style='o', ylabel='durée moyenne (jours)', title='durée moyenne passée par patient par secteur')

plt.show()

patients.groupby(by=['tranche_age'])['duree'].mean().plot(style='o', ylabel='durée moyenne (jours)', title='durée moyenne passée par patient en fonction de l\'âge')
plt.show()

"""---------------------------------------------------------------------"""

"""nbr de lits disponibles par secteur et au cours du temps"""

services_weekly.groupby(by=['month','service'])['available_beds'].mean().unstack(1).plot(
ylabel='nombre de lits disponibles', title='nombre de lits disponibles par secteur au cours du temps')
plt.show()

"""--------------------------------------------------------------------"""