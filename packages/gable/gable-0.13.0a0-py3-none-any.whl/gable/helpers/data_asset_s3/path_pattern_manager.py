import re
from datetime import datetime
from typing import Dict, Iterable, Optional

DATE_PLACEHOLDER_TO_REGEX = {
    "{YYYY}/{MM}/{DD}/{HH}": r"(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-9]|2[0-3])",
    "{YYYY}/{MM}/{DD}": r"(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])",
    "{YYYYMMDD_HH}": r"(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])_([01][0-9]|2[0-3])",
    "{YYYYMMDDHH}": r"(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])([01][0-9]|2[0-3])",
    "{YYYYMMDD}": r"(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])",
    "{YYYY-MM-DD}": r"(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])",
    "{epoch}": r"(?<!\d)\d{10}(?!\d)",
}


class PathPatternManager:
    """
    Manages the transformation and storage of file paths based on specified patterns.
    This class provides functionalities to add file paths after transforming them
    to a standardized format and to retrieve these paths based on matching patterns.

    Attributes:
        pattern_to_paths Dict[str, re.Pattern]: A dictionary that maps transformed
        path patterns to list of regex used to search for s3 files.
        pattern_to_actual_paths Dict[str, set[str]]: A dictionary that maps
        path patterns to the actual file paths that match the pattern.
    """

    def __init__(self):
        self.pattern_to_regex_paths: Dict[str, re.Pattern] = {}
        self.pattern_to_actual_paths: Dict[str, set[str]] = {}

    def substitute_if_unix_timestamp(self, path: str) -> str:
        """
        Checks if the path segment contains a UNIX timestamp and
        replaces it with a placeholder.
        """
        match = re.search(DATE_PLACEHOLDER_TO_REGEX["{epoch}"], path)
        if match:
            timestamp = int(match.group(0))
            try:
                date_time = datetime.fromtimestamp(timestamp)
                if datetime(2000, 1, 1) <= date_time <= datetime(2030, 12, 31):
                    path = path.replace(match.group(0), "{epoch}")
            except ValueError:
                pass
        return path

    def substitute_date_placeholders(self, path) -> str:
        """
        Applies regex patterns to replace date placeholders in paths with their regex equivalents.

        Args:
            path (str): The file path that may contain date patterns.

        Returns:
            str: The file path with dates standardized to placeholders.
        """
        for placeholder, regex in DATE_PLACEHOLDER_TO_REGEX.items():
            path = re.sub(regex, placeholder, path)
        path = self.substitute_if_unix_timestamp(path)
        return path

    def template_to_regex(self, template) -> re.Pattern:
        """Converts a string template with placeholders into a regex pattern."""
        regex_pattern = template
        for placeholder, regex in DATE_PLACEHOLDER_TO_REGEX.items():
            regex_pattern = regex_pattern.replace(placeholder, regex)
        return re.compile(regex_pattern)

    def get_all_patterns(self) -> Iterable[str]:
        """
        Returns a list of all patterns that have been added to the manager.
        """
        return self.pattern_to_regex_paths.keys()

    def get_pattern_to_actual_paths(self) -> Dict[str, set[str]]:
        """
        Returns a dictionary of all patterns and their corresponding file paths.
        """
        return self.pattern_to_actual_paths

    def get_regex_from_pattern(self, pattern: str) -> Optional[re.Pattern]:
        """
        Returns the matching regex for pattern that has been added to the manager.
        """
        return self.pattern_to_regex_paths.get(pattern, None)

    def add_filepaths(self, filepath: list[str]) -> None:
        """
        Transforms a file path based on predefined patterns and stores the transformed
        path along with the original file path in the manager.

        Args:
            filepath (str): The file path to be added, which will be transformed and stored.
        """
        unique_filepaths = set(filepath)
        for path in unique_filepaths:
            transformed_path = self.substitute_date_placeholders(path)
            if transformed_path not in self.pattern_to_regex_paths:
                regex_pattern = self.template_to_regex(transformed_path)
                self.pattern_to_regex_paths[transformed_path] = regex_pattern
                self.pattern_to_actual_paths[transformed_path] = set([path])
            else:
                self.pattern_to_actual_paths[transformed_path].add(path)
