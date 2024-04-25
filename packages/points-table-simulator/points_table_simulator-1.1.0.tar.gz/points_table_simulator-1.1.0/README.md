# points-table-simulator🔢

During the later part of the league stages in many multi-team tournaments 🏆 such as 🏏 Indian Premier League(IPL), Australian Big Bash League (BBL), ets., the fans will look for possible match outcomes for the remaining league matches, which could lead their favourite team to get qualified for further stage in the tournament (Playoffs). Here, the fans calculate their points table📊 to see their favourite team being placed in the position needed to qualify for Playoffs🏃🏻.

This tool🛠️ come as handy for those Sports enthusiasts which would help them to forsee the necessary remaining match outcomes to see their favourite team qualifying for playoffs✅ with the necessary match outcomes along with the respective points table📊.

<hr>

This python package📦 will simulate the points table📊 based on different possible results in a sports tournament.

The PointsTableSimulator package provides a powerful tool for simulating and analyzing points tables for sports tournaments. Whether you're organizing or following a tournament, this package offers the flexibility to input tournament schedules, define points systems, and explore various match outcome scenarios to understand team standings and qualification possibilities.

## Installation

Install this package with pip

```
pip install points-table-simulator
```
    
## Usage/Examples

Please find the example usage from the below python code

```python
from points_table_simulator import PointsTableSimulator
import pandas as pd

# Load the tournament schedule DataFrame
tournament_schedule = pd.read_csv("tournament_schedule.csv")

# Note: 
# The tournament schedule DataFrame should have the following columns:
#   - "match_number" column containing the match number
#   - "home" column containing the home team names
#   - "away" column containing the away team names
#   - "winner" column containing the match result (winning_team_name, draw, or no result)

# If the tournament schedule DataFrame contains different names than this, you can use arguments in PointsTableSimulator class to
# specify the column names. 

# Instantiate the PointsTableSimulator object
simulator = PointsTableSimulator(
    tournament_schedule=tournament_schedule,
    points_for_a_win=3,
    points_for_a_no_result=1,
    points_for_a_draw=1
)

# Get the current points table
current_table = simulator.current_points_table      # current_points_table is an attribute of PointsTableSimulator class

# Simulate qualification scenarios for a specific team
points_tables, qualification_match_results = simulator.simulate_the_qualification_scenarios(
    team_name="Team A",
    top_x_position_in_the_table=4,
    desired_number_of_scenarios=5
)

# points_tables - will return the list of points_tables (pd.Dataframe) for different qualification scenarios
# qualification_match_results - will return the list of table containing remaining match outcomes which could favour their team to get qualified for the given position
```

>This package can also be used in Football tournaments such as English Premier League (EPL), Laliga, etc., when you want to generate the scenarios in which your favourite team can be placed in your expected position in the pointstable.

## License

[MIT](https://choosealicense.com/licenses/mit/)
