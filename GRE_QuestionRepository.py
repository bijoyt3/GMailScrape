#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:01:21 2021

@author: bijoythomas
"""

import mailbox
import bs4
import email
import unicodedata
import pandas as pd
import datetime
import html

### Import Mbox Export from GMail
mb = mailbox.mbox('GRE Question of the Day.mbox')

### Lists to be populated with desired elements
date_sent = []
subject = []
links = []
image_links = []
question = []
ansA = []
ansB = []
ansC = []
ansD = []
ansE = []

### Created an iterable grouping of answer choice lists
choices = [ansA, ansB, ansC, ansD, ansE]

### Create list of image classes for readability
image_classes = ['content_image', 'contentImage', 'contentImage latex']

def get_html(message):
    msg = email.message_from_string(str(message))
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            #Parse base64 Emails
            if part['Content-Transfer-Encoding'] == 'base64':
                base64msg = email.message_from_string(message.as_bytes().decode(encoding='UTF-8'))
                for base64part in base64msg.walk():
                    if base64part.get_content_type() == 'text/html':
                        return base64part.get_payload()
            else:
                #Parse regular Emails
                return part.get_payload()


### Iterate through all mbox objects
for mail in mb:
    
   ### Retrieve Date
   date_obj = datetime.datetime.strptime(mail['Date'], '%a, %d %b %Y %H:%M:%S %z')
   date_sent.append(date_obj.strftime('%m/%d/%Y'))
    
   ### Retrieve Subject
   subject.append(mail['Subject'])
   
   ### Create soup object
   soup = bs4.BeautifulSoup(get_html(mail), 'html.parser')
   
   ### Get Image Links
   if soup.findAll('img', {'class': image_classes}):
       temp_list = [image['src'] for image in soup.findAll('img', {'class': image_classes})]
       image_links.append(temp_list) 
   else: 
       image_links.append("No Image")  
   
   ### Get Question
   if soup.findAll('h4', class_='subheadline'):
       subheading = soup.find('h4', class_='subheadline', string='ANSWER SELECTION')
       question.append(unicodedata.normalize("NFKD", subheading.find_previous_sibling('p').text))
    
   ### Get Answer Choices
   if soup.findAll('h4', class_='subheadline', string='ANSWER SELECTION'):
       subheading = soup.find('h4', class_='subheadline', string='ANSWER SELECTION')
       
       ### Handles questions with only 4 choices
       if len(subheading.find_all_next('p')) == 4:
           ansE.append("No Value")
           
       for i, word in zip(choices, subheading.find_all_next('p')):
          i.append(unicodedata.normalize("NFKD", html.unescape(word.text).replace('\n', '')))

### Populate DateFrame          
questions_df = pd.DataFrame(data={'Date': date_sent, 'Email Subject': subject, 'Image Links': image_links, 
                                  'Question': question, 'Choice A': ansA, 'Choice B': ansB, 'Choice C': ansC,
                                  'Choice D': ansD, 'ChoiceE': ansE})

### Remove Duplicate Questions
questions_df.drop_duplicates(subset='Question', keep="last", inplace=True)

### Export to Excel
questions_df.to_excel('GRE_QuestionsDatabase.xlsx')
