import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
import os
import json

# Read the config.json file
with open('config.json') as f:
    config = json.load(f)

# Extract the password from the config
emailuser = config['email']
password = config['password']

# read the three datasets
df1 = pd.read_csv('products_wong.csv', delimiter=';')
df2 = pd.read_csv('products_hk.csv', delimiter=';')
df3 = pd.read_csv('products_tailoy.csv', delimiter=';')

# merge the three datasets
col_f = list(df1.columns)
df2.columns = col_f
df3.columns = col_f

merged_df = pd.concat([df1, df2, df3], ignore_index=True)
merged_df.to_csv("dataset3.csv", sep=',', index=None)
#merged_df = pd.merge(merged_df, df3, on='id')

# print the merged dataset
#print(merged_df)


# Email credentials
sender_email = emailuser
app_password = password

# Connect to SMTP server
smtp_server = 'smtp.mail.yahoo.com'
smtp_port = 587
smtp_connection = smtplib.SMTP(smtp_server, smtp_port)

# Start TLS encryption
smtp_connection.starttls()

# Authenticate with app password
smtp_connection.login(sender_email, app_password)

# Compose email message
subject = 'Table of Data'
body = 'Please see the attached table of data.'
message = MIMEMultipart()
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Define attachment file path
#file_path = './dataset3.csv'

# Read data from the CSV file
#with open(file_path, 'r') as file:
#    csv_data = file.read()

# Add table data as attachment

#table_attachment = MIMEApplication(csv_data, _subtype='csv')
#table_attachment.add_header('Content-Disposition', 'attachment', filename='table.csv')
#message.attach(table_attachment)

# attach the files to the email
file_names = ['products_tottus.csv', 'dataset3.csv']
for file_name in file_names:
    with open(file_name, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype=os.path.splitext(file_name)[1][1:])
        attach.add_header('Content-Disposition', 'attachment', filename=file_name)
        message.attach(attach)

# Send email
recipient_email = 'jesustaco0@gmail.com'
smtp_connection.sendmail(sender_email, recipient_email, message.as_string())

# Close the SMTP connection
smtp_connection.quit()
