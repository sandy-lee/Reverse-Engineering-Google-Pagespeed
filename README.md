# Reverse engineering Google's Pagespeed Insight Tool

Acccording to a 2015 user experience study by [Erricson Consumer Labs](https://www.ericsson.com/en/press-releases/2016/2/streaming-delays-mentally-taxing-for-smartphone-users-ericsson-mobility-report) waiting for a slow webpage to load on a mobile device can induce as much anxiety as watching a horror film. Google as been promoting the idea of 'making the web faster' through a variety of initiative since 2009. A very good timeline of some of the things they have been doing can be found at [Unbounce.com](https://unbounce.com/landing-pages/2019-is-the-year-of-page-speed/). 

One of the most prolific initiatives for SEO professionals is for Google to make pagespeed one of the many factors in their ranking algorithm. To support this Google has given us the [Pagespeed Insights Tool](https://developers.google.com/speed/pagespeed/insights/) which is something that is used a lot by SEOs and webmasters to optimise a website for page speed. This tool gives great insights, however it can be a little but opaque in a how it works and anyone who has every tried to optimise a website for page speed will know it can be an expensive and labour intensive task. It would be good to be able to understand what recommendations to prioritise based on impact. That is the purpose of this project, to use machine learning to develop a model that can emulate performance metrics from the Google PageSpeed Insights tool and to give an idea of what actually contributes the most to 'good' performance and by how much. 

## The Process

In order to do this, we first need data:

1. Download a CSV of the top 1,000 most searches keywords on Google US from [mondovo.com](https://www.mondovo.com/keywords/most-searched-words-on-google)

2. Get the top 100 positions on Google US for all of those keywords using the amazing tool at [serpapi.com](http://serpapi.com/)

3. Get data from [Google's PageSppeed API](https://developers.google.com/speed/docs/insights/v5/get-started) for all those websites, selecting the features that are the most interesting:

* **Address** - URL of the page that the page speed data is about - unit: n/a
* **First Contentful Paint** - First contentful paint marks the time at which the first text or image is painted. [Learn more](https://web.dev/first-contentful-paint). - unit: **ms**
* **Time to Interactive** - First contentful paint marks the time at which the first text or image is painted. [Learn more](https://web.dev/first-contentful-paint). - unit: **ms**
* **Time to First Byte** - Time to first byte identifies the time at which your server sends a response. [Learn more](https://web.dev/time-to-first-byte). - unit: **ms**
* **DOM Size** - Browser engineers recommend pages contain fewer than ~1,500 DOM elements. The sweet spot is a tree depth \u003c 32 elements and fewer than 60 children/parent element. A large DOM can increase memory usage, cause longer [style calculations](https://developers.google.com/web/fundamentals/performance/rendering/reduce-the-scope-and-complexity-of-style-calculations) and produce costly [layout reflows](https://developers.google.com/speed/articles/reflow). [Learn more](https://web.dev/dom-size). - unit: **no. of elements**
* **Boot Up Time** - Consider reducing the time spent parsing, compiling and executing JS. You may find delivering smaller JS payloads helps with this. [Learn more](https://web.dev/bootup-time). - units **ms**
* **First Meaningful Paint** - First meaningful paint measures when the primary content of a page is visible. [Learn more](https://web.dev/first-meaningful-paint). - units **ms**
* **Speed Index** - Speed Index shows how quickly the contents of a page are visibly populated. [Learn more](https://web.dev/speed-index). - units **ms**
* **Total Blocking Time** - sum of all time periods between FCP and Time to Interactive, when task length exceeded 50ms, expressed in milliseconds. - units **ms**
* **Network Requests** - Lists the network requests that were made during page load. - units **no. of requests**
* **Total Byte Weight** - Large network payloads cost users real money and are highly correlated with long load times. [Learn more](https://web.dev/total-byte-weight). - units **bytes**

All in this gives us around 700,000 data points (yes, I know it should be a million but I couldh't get data back for all websites). My target variable will be **Speed Index** and I will be using all other features of predictors. This is a 'nice' dataset to work with as multicolinearity isn't an issue (nothing is correlation above 0.3 for Pearson Correlation) and as this is a dataset I am building myself I can control the quality.

## Model Training

This is a regression problem which means the tools I can bring to bear on this are well defined. From here the process I follow is:

1. Create datasets for training, testing and final validation (not used in training and only used once after training is complete). Also create a scaled version of the predictors for models that need it. 

2. Run a **Linear Regression** model as a baseline - the R^2 for this baseline is **0.76**, which is very good and highlights how 'nice' this dataset is.

3. Run a **Decision Tree Regressor** to see if it performs better than the baseline. It doesn't with an R^2 score of **0.6** on the test data set and an a score of 1 on the training dataset showing that it is horribly overfitting (as decision trees are prone to do). While I would avoid any kind of optimisation at this stage I attempt basic regularisation by running another model and setting **min_samples_leaf = 10**. This results in less overfitting and an R^2 score of **0.72** on the test dataset. Although better it still doesn't beat the baseline. 

4. Run a **Random Forest Regressor** and this one performed very well with an R^2 score of **0.78** on the test dataset showing that it generalises well and has performed better than the baseline.

5. Run a **Support Vector Machine Regressor** for both linear and polynomial kernals. These performance of these on the test dataset was **0.75** and **0.24** respectively. The linear kernal did well, but didn't beat the random forest regressor. The polynomial kernal didn't do so well, even with basic regularisation. Looking at pairplots for the dataset this is obviously a linear problem, but I thought I would try it out to see. Due to the poor performance of the polynomial SVM kernal, I decided to not look at other polynomial regression models.

## Model Optimisation

I decided to use a random forest regressor as this is the one that performed well versus the baseline. At this point I needed to optimise the model to improve performance and for this I used a standard GridSearch Cross Validation strategy. After running around 400 different model fits, the hyperparameters that gave the best performance are:

**max_depth = 23**
**min_samples_leaf = 3**

I trained a decision tree regressor using these hyperparamters and validated it against the final validation dataset with an R^2 of **0.8** which is very good.

## So what?

One of the great properties of Linear models, including Random Forest is that they are very transparent in showing which features contributed toward the predictions of the model. As we now have a model that we know is 80% accurate, we can very accurately determine which features matter the most to the Google PageSpeed Insights tool. Breaking this down we see the following:

* time_to_interactive	     **56.63%**
* time_to_first_byte	     **20.31%**
* first_meaningful_paint   **6.97%**
* first_contentful_paint   **3.94%**
* total_byte_weight	       **3.39%**
* boot_up_time	           **2.78%**
* network_requests	       **2.07%**
* dom_size	               **1.99%**
* total_blocking_time	     **1.94%**

The story here is interesting because while we can say it is obvious that **time_to_interactive** is the most important feature, the takeaways here are:

1) The extent to which it is much larger in terms of importance compared to any other page speed metrics shows how important compared to everything else and how much this should be a design KPI for when building new web page templates and ideally no tradeoffs as it is so important.

2) One thing that stood out when analysing this data is that these features are not particularly strongly correlated with each other (i.e. having a good first_meaningful_paint does not necessarily mean you will have a good time_to_interactive) meaning that time_to_interactive should be its on design principle, not just for SEO but for all disciplines in web design

Another interesting feature that stood out is how important time_to_first_byte is when building fast websites as this is not something that can always be controlled by site builders as it can be an infrastructure issue. It can also be one of the things that can go wrong if not properly implemented, especially in a mobile, high latency environment. 

## Next Steps

This was a fun project to do and I learned a lot. However I feel there is still a lot that can be done to improve it including:

* Use Big Query data from the [CRuX Report](https://developers.google.com/web/updates/2017/12/crux) to train a new model and get more insight, as there is still a lot of data for pagespeed that could be looked at.

* Use a clustering algorithm to see if it is possible to segment websites to try and pull out more characteristics/features to model and analyse. 

* Use Principle Component Analysis to try and train a better model to see if I can improve accuracy. This will effect how I can interogate the model for insights, however it might be the good basis for developing a predictive tool.

* There is a lot of data here and it might be interesting to use different target variables to see if more insights can be drawn.



