from django.core.exceptions import ValidationError
from datetime import datetime, date

def validate_today_date(value):
  """
  Validates if the provided date is not in the future.

  Args:
      value: The date string to validate.

  Raises:
      ValidationError: If the date is in the future or the format is invalid.
  """
  try:
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(value, '%B %d, %Y').date()

    # Check if the parsed date is in the future
    if date_obj > date.today():
      raise ValidationError('The date cannot be in the future.')
  except ValueError:
    raise ValidationError('Invalid date format. Please use the format "Month Day, Year".')