# Lead Scoring for Hyros

## Business case
Hyros is a software that allows advertisers and digital marketers to accuratley attribute the return on their advertising (ROAS) accross platforms. The company has been delivering amazing results for their customers who mostly come in by word of mouth. However they are looking towards outbound outreach to scale higher and are looking to hire more salespeople. Hyros wants to grow and it can only scale so high with word of mouth so it's ramping up outbound strategies. The goal here is to see if we can make the sales process more efficient, this way the sales team can retain or increase it's closing rate and Hyros won't need to make as many hires; 1) save time, 2) save money, 3) more closing = more money. 

## The problem
Finding the right prospects is time consuming. This is a common problem in sales and marketing, however this especially is an issue for Hyros because they are selective about the customers they choose to onboard. How much would it suck to expand a sales team only to have them bring in customers that are unualified or unlikley to benefit from the service? a lot! Getting the wrong customers on sales calls will decrease closing rates, especially SQL-to-MQL, at best and create negative customer experiences that reflect badly on the company at worst. Additionally, Hyros has an unfixed pricing model because they are a highly customizable product, this adds a degree of complexity to the lead prospecting process.

## Requirements
* Be able to quantify the quality of a given lead.
* Able to score roughly the amount of leads Hyros gets a day at one time, I estimate that they get about 70 leads per day. Because of their rapid growth goals I will aim to make sure the models can score 200 leads at one time in a reasonable time frame.
* Speed is a good selling point but scoring n leads at a time is a higher priority
* Most of our users will be on laptops so the application will be designed with that setup in mind.

## Solution
I am going to build a binary classification model that scores leads on a scale of 0 to 1, additionally I will build a regression model of sorts to predict the monthly value of a lead as Hyros has an unfixed pricing model. This way the team can see what leads are likley to convert and which ones could bring Hyros more revenue should they convert. These values will be aggregated together somehow and will be scaled from 1 to 10. The application will also concatenate the predictions with the Sales Team's spreadsheet. 

## Feasability
This project must have buy in from Hyros to be able tobe  compleated. That being said, I can pull data from known Hyros customers. I can find customers of Anytrack.io, a rival product, as well as generate slightly different datapoints to simulate leads that didn't close. I can seek buy in from Hyros to get access to their internal data to make the project 100%. This is risky business because I don't know what I'll be left with if they don't like or want it. I am going to continue with the project as of now but I will have to be flexible moving forward. 

# Questions for Sales reps at Software companies
1. If I were to make a lead scoring app for sales teams to use how would it need to work to be practical? About how many leads should it be able to score at one time? Does it need to be fast or it it okay is it runs a bit slower? Do you think the users would be more likley to use desktops or laptops?
3. As a [title] at [company] What do you think are the main factors that go into selling a high ticket software product? What attributes do you look at in a prospect?
