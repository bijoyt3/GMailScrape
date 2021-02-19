# GRE_QuestionRepository
Created a repository of GRE questions scraped from daily Kaplan Test Prep emails

Halfway through studying for the GRE, I ran into an issue many people have faced before: I ran out of free, offical ETS test prep materials. Not one to try third party test materials, I scoured the internet for more official math and verbal questions. At my wits' end, I realized that "wait, I have a treasure trove of questions sitting in my email inbox". Thus began the process of extracting the valuable question data from the emails and storing them in an Excel file as a respository of vetted, high-quality test questions. 

## The Process:

### Step 1: Export Emails

I used the Google Takeout service (https://takeout.google.com/settings/takeout) to export my own Google data to my local drive. Before using Takeout, I categorized all GRE Daily Question emails into a group identified by a label. I was then able to export only the emails that had that label as an .mbox file. 

### Step 2: Extract Question, Answer, and Image data 

I used the 'email' library to decode the emails into readable text then used 'beautifulsoup' to extract only the text data that I needed including the question, the five answer choices, and any images that may have been in the email. I had to iterate through each email object (509 objects) to extract the text data I needed. 

### Step 3: Store them in Excel

I stored all the extracted data into distinct lists, combined them into a DataFrame, removed duplicates, and converted it into an Excel file. I was left with 322 new, official GRE questions for practice.
