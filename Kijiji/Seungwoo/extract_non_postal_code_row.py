import pandas

df = pandas.read_csv('kijiji_full_result_with_postal_code.csv',delimiter=',')
df = df.loc[df['Postal Code'].isnull()]
df.to_csv('kijiji_full_result_non_postal_code.csv')
