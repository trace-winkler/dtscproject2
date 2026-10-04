# Project Two Summary
Project Two is centered around the utilization of machine learning models. I decided to focus on the topic of the NFL, and what position teams are expected to draft using their first round draft pick based on preseason positional rankings.

## Variables
### Team Needs
This variable covers depth chart strength, starter quality, backup quality, injuries, age of starters, contract length, and free agency losses.
### Team Draft Tendencies
Team Draft Tendencies will cover gm drafting tendencies, coaching scheme, and team philosophy, which I describe as the willingness for teams to draft big hitters over depth players. 
### Draft Context
This includes draft pick number, draft pick trading history, and the expected availability of top prospects at the teams draft position. 
### Team Performance
Team Performance goes over team record, their offensive and defensive performance, cap space, age of roster, and their defensive scheme type. 

## Project Two Introduction
My research question for this project is "Can machine learning models accurately predict which position an NFL team will select in the first round of the NFL draft based on preseason positional group rankings?" While I would have liked to use end of season statistics, I wanted this project to be up-to-date, and as such, I decided that I would use preseason rankings. 

For this project, I had to select two machine learning models, and due to the categorical nature of my topic and research question, I decided to use a logistic regression model, and a decision tree model. 

A multinomial logistic regression model is applicable to my vision for this project because it's a statistical method that is commonly used to predict the probability of a categorical outcome that has more than two categories. 

The decision to use a decision tree was clear when I realized that it could also process categorical data. Decision trees can handle categorical data, and they are also able to produce categorical outputs. On top of that, they also capture nonlinear relationships very well, and they're easy to visualize and interpret. 

## Learning Model One, Logistic Regression
This model was made to estimate the probability that a team's first-round pick would be used on a certain position group (QB, WR, RB, OL, DL, DB). It's supposed to do this by weighing the ESPN positional rankings, the teams pick number, their win percentage, and the team's recent draft history. I decided tha the best setting would be strong regularization with balanced class weights. Even at it's best, the model only got 22.5% accuracy, which is just barely better than the 18.8% baseline. Of the two, this model is the more interpretable one. 

<img width="400" height="400" alt="confusion_logistic" src="https://github.com/user-attachments/assets/cd638410-bb56-4a6a-bf5d-bd4861d2db3b" />

This multinomial logistic regression model honestly performs pretty well for the offensive line and defensive line classes, with 21 correct predictions for OL, and 16 correct predictions for the DL. Besides this, it gets confused, and gets very confused when it has to identify quarterbacks and wide receivers. When compared to the decision tree, it's my conclusion that it's predictions are distributed much more evenly, however it still has a strong habit when it comes to predicting OL and DL>

## Learning Model Two, Decision Tree
This model was made to split the data of the features until it was able to reach a predicted position. The problem I ran in to was that the tree's roots were very shallow, which was due to the data I provided. This tells me that the data only supports a few reliable patterns, which isn't the result I wanted. At it's best, it had 27.7% accuracy, which mainly came from the tree correctly predicting Offensive Line draft statistics. The decision tree model never once correctly predicted Wide Receiver draft statistics.

<img width="400" height="400" alt="confusion_tree" src="https://github.com/user-attachments/assets/9711e2d7-31a3-4e7e-ae2b-2e361a34b232" />

The confusion matrix above shows that the decision tree performs best when identifying the OL class, with 36 correct predictions. However, there is still a lot of confusion between DL and OL, as well as WR and OL. Overall, the model tends to predict OL much more frequently than the other classes, which leads to some misclassification of DL, DL, QB, and WR.

## Model Comparison
Between the two models, the decision tree appears to perform better overall, in my eyes. I came to this conclusion because it was able to generate more correct predictions, and had better overall recognition of several of the minority classes. Despite this small victory for the decision tree model, it's obvious to me that both models struggle, especially when it comes to distinguishing classes that can be confused with OL.

## Project Two Final Statement
It's hardly an understatement for me to say that I got too ambitious with this project. I tried to categorize human behavior and decisions, which I now realize is a mistake. the beauty of humans is their unpredictability, unless you're a new data scientist trying to make an demanding project. Ever since I first got into football, I understood that NFL teams often "draft for need." Since I started working on this project, I took "draft for need" as a way to measure how teams would draft when their positional groups were put to the test. 

The conclusion I have come to is that both models beat the baseline, but only barely, and most picks were still misclassified. The decision tree's accuracy ranged greatly from 18.8% to 41.9% across the years, so I must declare that the results from both models are unstable. The result is a negative one.

To answer the research question, no. The preseason positional rankings could not predict first-round positions and picks accurately from the data I collected. After working on this project, I truly realized how hard data science is when it comes to human habits and decision-making. NFL teams often draft the best pick available instead of their specific position of need. During the season, trades change teams plans and their drafting needs. On top of this, the data I collected did not include prospect data, which is important when it comes to determining the skill level of the player. 

While I am disappointed, I do feel like I learned a lot about data science from this project. Although the models run, and the code works, the results are weak. Despite the lack of result strength, the models successfully answer my research question. Using preseason positional rankings, a decision tree, and a multinomial logistic regression model, I was unable to predict first round draft choices accurately. 

Overall, I am not upset that this project didn't turn out the way I wanted it to. While my grade on the assignment might showcase how well it went, I am proud that I was able to learn from this experience. I plan on using this experience to think critically about the data I use from this point on.

## Sources
Berri, D. J., & Simmons, R. (2011). Catching a draft: On the process of selecting quarterbacks in the National Football League amateur draft. Journal of Productivity Analysis, 35(1), 37–49. [https://doi.org/10.1007/s11123-009-0154-6](https://doi.org/10.1007/s11123-009-0154-6)

Hendricks, W., DeBrock, L., & Koenker, R. (2003). Uncertainty, hiring, and subsequent performance: The NFL draft. Journal of Labor Economics, 21, 857–886. [https://doi.org/10.1086/377025](https://doi.org/10.1086/377025)

Massey, C., & Thaler, R. H. (2013). The loser's curse: Decision making and market efficiency in the National Football League draft. Management Science, 59(7), 1479–1495. [https://doi.org/10.1287/mnsc.1120.1657](https://doi.org/10.1287/mnsc.1120.1657)

Pitts, J. D., & Evans, B. (2019). Drafting for success: How good are NFL teams at identifying future productivity at offensive-skill positions in the draft? The American Economist, 64(1), 102–122. [https://doi.org/10.1177/0569434518812678](https://doi.org/10.1177/0569434518812678)

[NFLVerse Python Packages](https://nflverse.nflverse.com/)

[NFL 2026 Preseason Positional Rankings](https://www.espn.com/nfl/story/_/id/49638556/2026-nfl-season-positional-group-best-worst-quarterbacks-cornerbacks-receivers)

[NFL 2025 Preseason Positional Rankings](https://www.espn.com/nfl/story/_/id/45908900/2025-nfl-season-positional-group-best-worst-quarterbacks-cornerbacks-receivers)

[NFL 2024 Preseason Positional Rankings](https://www.espn.com/nfl/insider/story/_/id/40847171/2024-nfl-positional-ranking-team-units-best-worst)

[NFL 2023 Preseason Positional Rankings](https://www.espn.com/nfl/insider/story/_/id/38129445/ranking-2023-nfl-position-groups-best-worst-team-units-quarterback-receiver)

### Return to the [Project Directory](https://trace-winkler.github.io/project-directory/)
### Return to the [Homepage](https://trace-winkler.github.io/data-science-portfolio/)
### Check out my [Blog](https://trace-winkler.github.io/blog/)
