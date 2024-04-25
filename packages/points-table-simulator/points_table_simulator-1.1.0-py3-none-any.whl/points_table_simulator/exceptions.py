"""
Custom Exceptions Module

This module defines custom exception classes used in the project.

Classes:
    InvalidColumnNamesError: Exception raised when the invalid column names are found in the tournament schedule DataFrame.
    InvalidScheduleDataError: Exception raised when the input schedule dataframe is invalid.
    NoQualifyingScenariosError: Exception raised when no qualifying scenarios are found for the given team.
    TeamNotFoundError: Exception raised when the team is not found in the tournament schedule.
    TournamentCompletionBelowCutoffError: Exception raised when the percentage of tournament completion is below the specified cutoff.
"""


class InvalidColumnNamesError(ValueError):
    """
    Custom error class for invalid column names in the tournament schedule DataFrame.
    """

    def __init__(self, column_name: str, column_value: str):
        self.column_name = column_name
        self.column_value = column_value
        super().__init__(f"{column_name} '{column_value}' is not found in given tournament_schedule columns")


class InvalidScheduleDataError(ValueError):
    """Exception raised when the input schedule dataframe is invalid."""

    def __init__(self, column_name: str):
        self.column_name = column_name
        super().__init__(f"the given schedule contains rows with empty values or NaN in the {column_name} column")


class NoQualifyingScenariosError(Exception):
    """Exception raised when no qualifying scenarios are found for the given team."""

    def __init__(self, points_table_position: int, team_name: str):
        self.points_table_position = points_table_position
        self.team_name = team_name
        super().__init__(f"No qualifying scenarios found for team '{team_name}' at position {points_table_position}")


class TeamNotFoundError(Exception):
    """Exception raised when the team is not found in the tournament schedule."""

    def __init__(self, message="Team not found in tournament schedule"):
        self.message = message
        super().__init__(self.message)


class TournamentCompletionBelowCutoffError(Exception):
    """Exception raised when the percentage of tournament completion is below the specified cutoff."""

    def __init__(self, cutoff_percentage: float, tournament_completion_percentage: float):
        self.cutoff_percentage = cutoff_percentage
        self.tournament_completion_percentage = tournament_completion_percentage
        super().__init__(
            f"Tournament completion percentage is {tournament_completion_percentage}%, which is less than the specified cutoff of {self.cutoff_percentage}%"
        )
