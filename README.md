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
