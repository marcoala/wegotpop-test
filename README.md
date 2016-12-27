# The task


Implement a simple search service, with suitable test coverage, using any Python web framework (micro frameworks are welcomed).
The service should accept http GET requests which may include any of the following search criteria:
```
age range (minimum and maximum)
location (latitude, longitude and radius)
maximum rate
gender
```

**Optional**: each parameter supplied should also have a rank/weight.

The response from the search service must be a JSON-encoded list of artists from the attached dataset which match the criteria.

Ordering of the search results is very important.  The most relevant artists should come up first in the list.  It is up to you decide how to interpret "most relevant".  If you've included the optional 'weight' parameters then the relevance could include how to give consideration to the rank/weight of each search criterion.

Feel free to choose your own strategy and in effect make your own user stories, but here is an example:

_I want to find artists of as close to a particular age and gender close to the filming locations so that they can get there quickly._

There's no need for any front-end code or other presentation of the data.

**Notes on the dataset**:
- All of the artist are in locations around London (latitude: 51.5126064, longitude: -0.1802461).
- The youngest artists are 16 years old and the oldest are 74.
- Rates range from 10.00 to 39.97
- There are 999 artists in the file.
- There are 499 male artists and 500 female artists.
- All UUIDs are unique.

# Solution

## Technology

Since micro frameworks were suggested Flask was an obvious choice: I've some experience with it and it's simple and fast to setup. For the same reasons I've choose to deploy the application to Heroku.

For the search engine, a Relational Database was not an option, PostgreSQL can deal with geo data, but score the matches and apply different weight to each field is impossible.

This narrow the circle to Solr and ElasticSearch, for the purpose of the task they are equivalent. The only difference is that on Heroku the Solr plugin has no free plan, while ES does.

## Ordering

The definition of the "most relevant artist" is highly opinable, and since the data available are so limited, I've decided to analyse the problem starting from the datas (usually I do the other way around, I start from the best possible solutions and then I exclude the technically impossible).


**gender**: in the data available this is binary state and can't be scored. So I've just assumed that there are only three user stories: the user just want a male artist, the user just want a female artist, the user accept both.


**maximum rate**: this is numerical, so we can just assume that the user want the cheapest first, so he can save money. Maybe an improvement can be to allow a minimum rate: in case of too many results the user may want to exclude amateurs.


**age range**: since we're talking about actors I assume that when someone ask for people between 15 and 25 they mean that they want someone that _looks_ between 15 and 25. So it's safe to assume that we can extend the research of a few years (let's say 5), but the artist that are in this extended range should have a score much lower than who match the range exactly.


**location**: score the results by the distance from the origin point is the most obvious solution. At the same time what the user want is people who can reach the shooting location quickly, for this purpose someone who is at 5km form the shooting location and someone who is at 7km should be considered roughly equal since both can reach that location in minutes with a car.

Find a way to calculate the travelling time seems an overkill for this problem, my proposal is to have three ranges of distance, and give the same score to everyone that is in the same range.

Like in the age range I assume that we can extend the search a bit further the defined range, but we've to classify to give to this results a much lower score.


Said that the most important parameter is definitely age, since is the closest that we've to the look of the artist. Followed by price and location at the same level.
