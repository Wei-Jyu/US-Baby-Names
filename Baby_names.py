import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import glob
%matplotlib inline

filenames = glob.glob('dir/namesbystate/*.csv')
column_names = ['State', 'Sex', 'Year', 'Name', 'Num']
Data = pd.DataFrame(columns = column_names)
i = 0
N = np.zeros((51,2))
M = np.zeros((51,2))
for f in filenames:
    data = pd.read_csv(f)
    data.columns = ['State', 'Sex', 'Year', 'Name', 'Num']
    data_select_F_1 = data.loc[(data['Name'] == 'Jessie') & (data['Sex'] == 'F')]
    N[i][0] = data_select_F_1['Num'].sum()
    data_select_F_2 = data.loc[(data['Name'] == 'Riley') & (data['Sex'] == 'F')]
    M[i][0] = data_select_F_2['Num'].sum()
    data_select_M_1 = data.loc[(data['Name'] == 'Jessie') & (data['Sex'] == 'M')]
    N[i][1] = data_select_M_1['Num'].sum()
    data_select_M_2 = data.loc[(data['Name'] == 'Riley') & (data['Sex'] == 'M')]
    M[i][1] = data_select_M_2['Num'].sum()
    i = i + 1
    Data = Data.append(data)

State = ['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','IL','IA','ID','AK','IN','KS','KY','LA','MA','MD','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']
Sample_Jessie = np.zeros(51)
Sample_Riley = np.zeros(51)
dash = '-' * 26
for i in range(51):
    if i == 0:
        print(dash)
        print('{:<10s}{:>4s}{:>10s}'.format('State','Jessie','Riley'))
        print(dash)
    else:
        Sample_Jessie[i-1] =  N[i-1][0]/(N[i-1][0] + N[i-1][1])
        Sample_Riley[i-1] =  M[i-1][0]/(M[i-1][0] + M[i-1][1])
        print('{:<10s}{:>6.2f}{:>10.2f}'.format(State[i-1], Sample_Jessie[i-1], Sample_Riley[i-1]))
t_stat, p_val = stats.ttest_ind(Sample_Jessie, Sample_Riley, equal_var=False)

Data_new = Data[Data.Year <= 2000] # Only need to consider Year <=2000
Data_new_F = Data_new[Data_new.Sex == 'F'] # split the original dataset by genders
Data_new_M = Data_new[Data_new.Sex == 'M']

Data_F = Data_new_F.drop(['State','Sex'], axis = 1) #Remove 'State' and 'Sex' Columns
Data_M = Data_new_M.drop(['State','Sex'], axis = 1)
aggregation_functions = {'Num': 'sum'}
Data_F_name = Data_F.groupby(Data_F['Name']).aggregate(aggregation_functions)
Data_M_name = Data_M.groupby(Data_M['Name']).aggregate(aggregation_functions)

#Sort by number of names to find the 5 most common names
Data_F_5 = Data_F_name.sort_values(by = 'Num', ascending=False)
Data_M_5 = Data_M_name.sort_values(by = 'Num', ascending=False)
print(Data_F_5.head(5))
print(Data_M_5.head(5))

# Select the rows associated with names from original dataset
Data_F_Mary = Data_F.loc[(Data_F['Name']=='Mary')]
Data_F_Patricia = Data_F.loc[(Data_F['Name']=='Patricia')]
Data_F_Linda = Data_F.loc[(Data_F['Name']=='Linda')]
Data_F_Barbara = Data_F.loc[(Data_F['Name']=='Barbara')]
Data_F_Jennifer = Data_F.loc[(Data_F['Name']=='Jennifer')]

# Group by year
aggregation_functions = {'Num': 'sum'}
Data_Mary = Data_F_Mary.groupby(Data_F_Mary['Year']).aggregate(aggregation_functions)
Data_Patricia = Data_F_Patricia.groupby(Data_F_Patricia['Year']).aggregate(aggregation_functions)
Data_Linda = Data_F_Linda.groupby(Data_F_Linda['Year']).aggregate(aggregation_functions)
Data_Barbara = Data_F_Barbara.groupby(Data_F_Barbara['Year']).aggregate(aggregation_functions)
Data_Jennifer = Data_F_Jennifer.groupby(Data_F_Jennifer['Year']).aggregate(aggregation_functions)

# Same thing for boys
Data_M_James = Data_M.loc[(Data_M['Name']=='James')]
Data_M_John = Data_M.loc[(Data_M['Name']=='John')]
Data_M_Robert = Data_M.loc[(Data_M['Name']=='Robert')]
Data_M_Michael = Data_M.loc[(Data_M['Name']=='Michael')]
Data_M_William = Data_M.loc[(Data_M['Name']=='William')]

Data_James = Data_M_James.groupby(Data_M_James['Year']).aggregate(aggregation_functions)
Data_John = Data_M_John.groupby(Data_M_John['Year']).aggregate(aggregation_functions)
Data_Robert = Data_M_Robert.groupby(Data_M_Robert['Year']).aggregate(aggregation_functions)
Data_Michael = Data_M_Michael.groupby(Data_M_Michael['Year']).aggregate(aggregation_functions)
Data_William = Data_M_William.groupby(Data_M_William['Year']).aggregate(aggregation_functions)

plt.plot(Data_Mary.Num/10**3)
plt.plot(Data_Patricia.Num/10**3)
plt.plot(Data_Linda.Num/10**3)
plt.plot(Data_Barbara.Num/10**3)
plt.plot(Data_Jennifer.Num/10**3)
plt.legend(['Mary','Patricia','Linda','Barbara','Jennifer'])
plt.xlabel('year')
plt.ylabel('Number of occurrences of names (thousand)')
plt.title('Plot of number of occurrences of names (for baby girls)')
plt.show()

plt.plot(Data_James.Num/10**3)
plt.plot(Data_John.Num/10**3)
plt.plot(Data_Robert.Num/10**3)
plt.plot(Data_Michael.Num/10**3)
plt.plot(Data_William.Num/10**3)
plt.legend(['James','John','Robert','Michael','William'])
plt.xlabel('year')
plt.ylabel('Number of occurrences of names (thousand)')
plt.title('Plot of number of occurrences of names (for baby boys)')
plt.show()

Data_century = Data[Data.Year > 2000]
Data_century_F = Data_century[Data_century.Sex == 'F']
Data_century_M = Data_century[Data_century.Sex == 'M']
Data_F_century = Data_century_F.drop(['State','Sex'], axis = 1) #Remove 'State' and 'Sex' Columns
Data_M_century = Data_century_M.drop(['State','Sex'], axis = 1)
aggregation_functions = {'Num': 'sum'}
Data_F_names = Data_F_century.groupby(Data_F_century['Name']).aggregate(aggregation_functions)
Data_M_names = Data_M_century.groupby(Data_M_century['Name']).aggregate(aggregation_functions)

#Sort by number of names to find the 10 most common names
Data_F_10 = Data_F_names.sort_values(by = 'Num', ascending=False)
Data_M_10 = Data_M_names.sort_values(by = 'Num', ascending=False)
Data_F10 = Data_F_10.head(10)
Data_M10 = Data_M_10.head(10)
Data_F10.plot.pie(y = 'Num', figsize = (5,5))
Data_M10.plot.pie(y = 'Num', figsize = (5,5))

# Select the rows associated with names from original dataset
Data_State = Data_new_F.drop(['Year','Sex'], axis = 1)
Data_State_Mary = Data_State.loc[(Data_State['Name']=='Mary')]
Data_State_Patricia = Data_State.loc[(Data_State['Name']=='Patricia')]
Data_State_Linda = Data_State.loc[(Data_State['Name']=='Linda')]
Data_State_Barbara = Data_State.loc[(Data_State['Name']=='Barbara')]
Data_State_Jennifer = Data_State.loc[(Data_State['Name']=='Jennifer')]

#group by 'State'
aggregation_functions = {'Num': 'sum'}
Data_Mary_State = Data_State_Mary.groupby(Data_State_Mary['State']).aggregate(aggregation_functions)
Data_Patricia_State = Data_State_Patricia.groupby(Data_State_Patricia['State']).aggregate(aggregation_functions)
Data_Linda_State = Data_State_Linda.groupby(Data_State_Linda['State']).aggregate(aggregation_functions)
Data_Barbara_State = Data_State_Barbara.groupby(Data_State_Barbara['State']).aggregate(aggregation_functions)
Data_Jennifer_State = Data_State_Jennifer.groupby(Data_State_Jennifer['State']).aggregate(aggregation_functions)

Data_Mary_State.plot.bar (y = 'Num', figsize = (8.5,6))
plt.legend('')
plt.xlabel('State')
plt.ylabel('Number of occurrences of name Mary')

Data_Patricia_State.plot.bar (y = 'Num', figsize = (8.5,6))
plt.legend('')
plt.xlabel('State')
plt.ylabel('Number of occurrences of name Patricia')

Data_Linda_State.plot.bar (y = 'Num', figsize = (8.5,6))
plt.legend('')
plt.xlabel('State')
plt.ylabel('Number of occurrences of name Linda')

Data_Barbara_State.plot.bar (y = 'Num', figsize = (8.5,6))
plt.legend('')
plt.xlabel('State')
plt.ylabel('Number of occurrences of name Barbara')

Data_Jennifer_State.plot.bar (y = 'Num', figsize = (8.5,6))
plt.legend('')
plt.xlabel('State')
plt.ylabel('Number of occurrences of name Jennifer')


