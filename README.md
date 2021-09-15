# Lead Scoring for Hyros

## Business case
Hyros is a software that allows advertisers and digital marketers to accurately attribute the return on their advertising (ROAS) across platforms. The company has been delivering amazing results for their customers who mostly come in by word of mouth. However, they are looking towards outbound outreach to scale higher and are looking to hire more salespeople. Hyros wants to grow, and it can only scale so high with word of mouth so it's ramping up outbound strategies. The goal here is to see if we can make the sales process more efficient, this way the sales team can retain or increase its closing rate and Hyros won't need to make as many hires; 1) save time, 2) save money, 3) more closing = more money.

## The problem
Finding the right prospects is time consuming. This is a common problem in sales and marketing; however, this especially is an issue for Hyros because they are selective about the customers they choose to onboard. How much would it suck to expand a sales team only to have them bring in customers that are unqualified or unlikely to benefit from the service? a lot! Getting the wrong customers on sales calls will decrease closing rates, especially SQL-to-MQL, at best and create negative customer experiences that reflect badly on the company at worst.

## Requirements
* •	Be able to quantify the quality of a given lead.
•	Able to score roughly the number of leads Hyros gets a day at one time, I estimate that they get about 70 leads per day. Because of their rapid growth goals, I will aim to make sure the models can score 200 leads at one time in a reasonable time frame.
•	Speed is a good selling point but scoring n leads at a time is a higher priority
•	Most of our users will be on laptops so the application will be designed with that setup in mind.

## Solution
I am going to build a binary classification model that scores leads on a scale of 0 to 1, additionally I will build a regression model of sorts to predict the monthly value that Hyros could bring to the lead. This way the team can see what leads are likely to convert and which ones could bring Hyros more revenue should they convert. These values will be aggregated together somehow and will be scaled from 1 to 10. The application will also concatenate the predictions with the Sales Team's spreadsheet. 

<img src="images/process2.png/">

## Feasability
With the data that I have it isn't realistic to have a very good model as I'm only able to collect 60-90 datapoints. If I can conduct a survey for businesses that have gone through the sales process at hyros create a data flywheel. If I'm able to find the leads that didn't purchase it will be leading to better performance in the model and a more accurate analysis overall. The main bottleneck of this project is getting the leads and finding the ad spend of each lead in a programmatic manner.

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

# Data needed
## individual features
1. name
2. landing page
3. customer
4. domain
5. model
6. source
7. subscriber
8. adspend
9. hardcosts
10. percent social
11. percent display
12. percent search paid
13. percent search
14. visits
15. monthly visits change
16. bounce rate 
17. dominant platform
18. polarity
19. subjectivity
20. words
21. triggers
22. links
23. revenue

## aggregated features
1. ad revenue = revenue * percent paid
5. roas = ad revenue / new customers
6. cac = adspend / new customers
7. profit = revenue - adspend - hardcosts
8. lpc = words+1 * triggers+1 * links+1
9. profit margin = profit / revenue
10. average order value
11. monthly customers

## data sources
* Similarweb: 10, 11, 12, 13, 14, 15, 16, 17
* landing page: 20, 21, 22
* Survey: 1, 2, 3, 4, 5, 6?, 7?, 8?, 9?, 10?
* Dominant social media platform (we will just twitter for now because it's easier): 18, 19
* fullcontact: 23

## data collection strategy
The initial dataset, check6.csv, is a very small dataset of 60 rows that I manually collected. The reason for this was that I was struggling with the web scraping and data pipeline and I desperately wanted a dataset that I could analyze. This way I could have data to work with so that I would be motivated to work on my statistics skills and keep my data analytics skills sharp while I worked on getting my scrapers to work. To collect more data, I will conduct a survey for those who have gone through the Hyros sales process, participants will be asked a few questions which will be stored into a database. These results will give the data pipeline the knowledge necessary to connect to all the data sources which will be used to insert the rest of the information into the database.

Moving forward I will need to pay for access to Similar web’s API in order to make this scalable, fortunately my tutoring side hustle will give me the funding necessary. I have also built a leadgen survey with flask that will ask incoming leads for their latest landing page, revenue, ad spend, business domain, and business model (ecommerce, consulting, info/coaching, other) and store the results in a MySQL database, API calls will also be made to twitter, full contact, and similar web and the data will be stored in separate tables within the database. Finally, a python script takes all the data, some features will also be combined to form the aggregated features as listed above.

**Survey Questions**
1. What is the domain name of your business? (ie. FrankKern.com)
2. Please provide the url to the landing page of your latest ad campaign 
3. Have you purchased Hyros?
4. What domain is your business in? (ie. Fitness)
5. What best describes the products/services that make up the most of your revenue? [Consulting, Information\Coaching, Tangible Products, Other]
6. How much do you spend on ads per month?
7. What are your monthly hardcosts? (these exclude employees, rent, and adspend)
8. How did you find out about Hyros? (Youtube, Facebook, Twitter, Word of Mouth, Other)

**Where to find participants?**
1. The Hyros facebook group (this is a private group and may be hard to join)
2. Join discussions in relevant groups
3. Join the Hyros affiliates facebook group

## types of features
Throughout our dataset we have 3 main types of features. These are qualification, information, and relationship. Qualification features determine if a customer is qualified to do business with us in the first place, these include ad spend, type of business, and number of paid traffic platforms. Information features are used to help estimate the results Hyros can bring to a particular customer based on the performance of the customer's digital marketing, combined with qualification features we can develop a pricing model to predict what that customer could be worth to us. The third type of feature is Relationship features, these features are near impossible to access without buy in, these inform us on the relationship between the customer and Hyros. These include things like 'source of lead' and other details surrounding the customer's behavior throughout the sales process, With these features we can better predict a lead's probability of closing although it is likely that we can still do reasonably well just with Qualification and Information features.

## EDA
I've made a dashboard in tableau that helps sales reps visualize the difference between customers and non-customers to better understand their leads/prospects. This current dashboard compares a sample of known customers of Hyros against an equally sized sample of similar businesses that are not customers of Hyros. https://public.tableau.com/app/profile/spencer.holley/viz/HyrosLeadsSample/HyrosLeadsSample

## model selection
I'm very early in this project but I've dabbled with a very simple bayseian model that I coded from scratch.

see video here: https://www.youtube.com/watch?v=CaodNoFFX18&t=158s
