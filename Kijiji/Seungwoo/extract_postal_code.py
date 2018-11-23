import pandas

df = pandas.read_csv('kijiji_full_result.csv',delimiter=',')
df['Postal Code'] = df['Address'].str.extract(r'([a-zA-Z][0-9][a-zA-Z]\s*[0-9][a-zA-Z][0-9])')
df.to_csv('kijiji_full_result_with_postal_code.csv', index=False)

df = pandas.read_csv('kijiji_full_result_with_postal_code.csv',delimiter=',')
df = df.loc[df['Postal Code'].isnull()]
df.to_csv('kijiji_full_result_non_postal_code.csv', index=False)
