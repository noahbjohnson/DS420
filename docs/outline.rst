****************
Project Proposal
****************

**Food Desert Analysis**

*Completed by Noah B Johnson and Tristan Shaffer for DS420 (Machine Learning) at Luther College*

We will use the United States Department of Agriculture's Economic
Research Service `Food Environment
Atlas <https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads/>`__
to classify areas as 'food deserts.'

We will use the USDA definition to categorize the county-level data.
Once initially classified, we will use the variables not included in the
USDA formula to build a classification model with our computed
categories as the response.

The Issue
#########

According to the `American Nutrition
Association <http://americannutritionassociation.org/>`__, a food desert
is an area, especially one with low-income residents, that has limited
access to affordable and nutritious food. `Their site
says <http://americannutritionassociation.org/newsletter/usda-defines-food-deserts>`__:
> This has become a big problem because while food deserts are often
short on whole food providers, especially fresh fruits and vegetables,
instead, they are heavy on local quickie marts that provide a wealth of
processed, sugar, and fat laden foods that are known contributors to our
nation’s obesity epidemic.

In addition to obesity, many other health issues are associated with
poor access to affordable healthy foods.

The Data
#########

Atlas Data
************

    `From the Atlas
    Site <https://www.ers.usda.gov/data-products/food-environment-atlas/about-the-atlas/>`__

Food environment factors—such as store/restaurant proximity, food
prices, food and nutrition assistance programs, and community
characteristics—interact to influence food choices and diet quality.
Research has been documenting the complexity of these interactions, but
more research is needed to identify causal relationships and effective
policy interventions.

The objectives of the Atlas are:

-  to assemble statistics on food environment indicators to stimulate
   research on the determinants of food choices and diet quality, and

-  to provide a spatial overview of a community's ability to access
   healthy food and its success in doing so.

Other Data
************

If the data included from the USDA's dataset is not sufficient to build
our model, we can use datasets from the `US Census
Bureau <https://census.gov>`__ or other US agencies and reporting
organizations to provide more features.

`FIPS (geographic identifiers)
dataset <https://www.census.gov/geographies/reference-files/2017/demo/popest/2017-fips.html>`__ located at ``/src/midterm/data/us_zip_fips_county.csv``

The Classification
####################

The USDA defines what's considered a food desert and which areas will be
helped by this initiative: To qualify as a “low-access community,” at
least 500 people and/or at least 33 percent of the census tract's
population must reside more than one mile from a supermarket or large
grocery store.(\ `from the ANA <http://americannutritionassociation.org/newsletter/usda-defines-food-deserts>`__)

Our goal is to see if we can build a model to predict this
classification on a county level.

Milestones
#############

Midterm
********

    [x]︎ Write a module to parse the food atlas data

    [x]︎ Spot check data integrity

    [x]︎ Classify data using USDA criteria

    [] Visualize the USDA classification


Final
**********

    [] Analyze the USDA classification

    [] Model with the USDA classification as the response (basic logistic regression)

    [] Assess model(s) fit and residuals

    [] Analyze logistic model factors

    [] Complex modeling:

      [] Logistic regression with interactions

      [] SVM (Linear SVC, SVC, nuSVC)
      
      [] Nearest neighbors
      
      [] SGD

    [] Find a better classification (exploratory clustering)
      
      [] Mean shift
      
      [] K-Means
      
      [] GMM/Spectral clustering
      
    [] Synthesize final report from findings
