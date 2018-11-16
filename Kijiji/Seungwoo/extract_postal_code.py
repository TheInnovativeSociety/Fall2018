import pandas

df = pandas.read_csv('kijiji_full_result.csv',delimiter=',')
df['Postal Code'] = df['Address'].str.extract(r'([A-Z][0-9][A-Z]\s[0-9][A-Z][0-9])')

