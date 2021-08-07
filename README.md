# Lead Scoring for Hyros

## Business case
Hyros is a software that allows advertisers and digital marketers to accuratley attribute the return on their advertising (ROAS) accross platforms. The company has been delivering amazing results for their customers who mostly come in by word of mouth. However they are looking towards outbound outreach to scale higher and are looking to hire more salespeople. Hyros wants to grow and it can only scale so high with word of mouth so it's ramping up outbound strategies. The goal here is to see if we can make the sales process more efficient, this way the sales team can retain or increase it's closing rate and Hyros won't need to make as many hires; 1) save time, 2) save money, 3) more closing = more money. 

## The problem
Finding the right prospects is time consuming. This is a common problem in sales and marketing, however this especially is an issue for Hyros because they are selective about the customers they choose to onboard. How much would it suck to expand a sales team only to have them bring in customers that are unqualified or unlikley to benefit from the service? a lot! Getting the wrong customers on sales calls will decrease closing rates, especially SQL-to-MQL, at best and create negative customer experiences that reflect badly on the company at worst.

## Requirements
* Be able to quantify the quality of a given lead.
* Able to score roughly the amount of leads Hyros gets a day at one time, I estimate that they get about 70 leads per day. Because of their rapid growth goals I will aim to make sure the models can score 200 leads at one time in a reasonable time frame.
* Speed is a good selling point but scoring n leads at a time is a higher priority
* Most of our users will be on laptops so the application will be designed with that setup in mind.

## Solution
I am going to build a binary classification model that scores leads on a scale of 0 to 1, additionally I will build a regression model of sorts to predict the monthly value that Hyros could bring to the lead. This way the team can see what leads are likley to convert and which ones could bring Hyros more revenue should they convert. These values will be aggregated together somehow and will be scaled from 1 to 10. The application will also concatenate the predictions with the Sales Team's spreadsheet. 

## Feasability
This project must have buy in from Hyros to be able to be  compleated. That being said, I can pull data from known Hyros customers. I can find customers of Anytrack.io, a rival product, as well as generate slightly different datapoints to simulate leads that didn't close. I can seek buy in from Hyros to get access to their internal data to make the project 100%. This is risky business because I don't know what I'll be left with if they don't like or want it. I am going to continue with the project as of now but I will have to be flexible moving forward. 

## KPI's and metrics
**Business KPI's**
1. SQL closing rate; because Hyros is stepping up it's outbound outreach it is especially looking to increase closing rate from leads qualified by the sales team as opposed to the marketing team
2.  Sales cycle length
3.  closing ratio
4.  SQC revenue; I don't know if this is an offical metric but we are trying to increase revenue from sales qulaified customers
5.  Customer LTV

**Model KPI's**
1. Precision
2. Mean Absolute Error

# Questions for Sales reps at Software companies
1. If I were to make a lead scoring app for sales teams to use how would it need to work to be practical? About how many leads should it be able to score at one time? Does it need to be fast or it it okay is it runs a bit slower? Do you think the users would be more likley to use desktops or laptops?
3. As a [title] at [company] What do you think are the main factors that go into selling a high ticket software product? What attributes do you look at in a prospect?

# Data needed
## individual features

## aggregated features

## data sources
* Similarweb: 
* landing page: 
* Survey: 
* Dominant social media platform (we will just twitter for now because it's easier): 
* Zoominfo:

## data collection strategy
I'm going to store the names of the customers and put in filler values for source of lead in a database. I will iterate through the leads and make the requests and add all of it to the database. The data will be loaded in with Pandas and preporcessed for model training. We will update the database as new leads come in. Additionally, I will scrape each lead's most recent landing page to get features 16 - 18. So far I've set up a web crawler with the Scrapy library and it seems that I will be able to scrape features 2, 5, 8, 9, and 12 from Similar Web without too much trouble. I currently have 60 datapoints that I collected manually so that I have something to analyze, this way my analytics dosen't get rusty while I develop my Data Engineering skills. I also see value in conducting surveys in the facebook group for additional data, this can also be a great opportunity to promote my work!

## types of features
Throughout our dataset we have 3 main types of features. These are qualification, information, and relationship. Qualification features determine if a customer is qualified to do business with us in the first place, these include adspend, type of business, and number of paid traffic platforms. Information features are used to help estimate the results Hyros can bring to a particular customer based on the preformance of the customer's digital marketing, combined with qualification features we can develop a pricing model to predict what that customer could be worth to us. The third type of feature is Relationship features, these features are near inpossible to access without buy in, these inform us on the relationship between the customer and Hyros. These include things like 'source of lead' and other details surrounding the customer's behaivor throughout the sales process, With these features we can better predict a lead's probability of closing although it is likley that we can still do reasonably well just with Qualification and Information features.

