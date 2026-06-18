"""
Advanced Efficiency Management (AEM)
Global constants used throughout the module.

Supports:
- United States
- Canada
- Metric (International)

Do NOT place business logic here.
Only reusable constants.
"""

# ==========================================================
# API VERSION
# ==========================================================

API_VERSION = "v1"


# ==========================================================
# SUPPORTED COUNTRIES
# ==========================================================

COUNTRY_US = "US"
COUNTRY_CA = "CA"
COUNTRY_METRIC = "METRIC"

SUPPORTED_COUNTRIES = [
    COUNTRY_US,
    COUNTRY_CA,
    COUNTRY_METRIC,
]


# ==========================================================
# UNIT SYSTEMS
# ==========================================================

UNIT_US = "imperial"
UNIT_METRIC = "metric"


# ==========================================================
# DISTANCE CONVERSIONS
# ==========================================================

KM_TO_MILES = 0.621371
MILES_TO_KM = 1.609344


# ==========================================================
# FUEL CONVERSIONS
# ==========================================================

LITER_TO_US_GALLON = 0.264172
US_GALLON_TO_LITER = 3.78541


# ==========================================================
# FUEL ECONOMY CONVERSIONS
# ==========================================================

# 1 km/L = 2.35214583 MPG (US)
KMPL_TO_MPG = 2.35214583

# 1 MPG (US) = 0.425144 km/L
MPG_TO_KMPL = 0.425144


# ==========================================================
# SPEED CONVERSIONS
# ==========================================================

KMH_TO_MPH = 0.621371
MPH_TO_KMH = 1.609344


# ==========================================================
# DEFAULT INPUT VALUES
# ==========================================================

DEFAULT_NET_FACTOR = 1.0

DEFAULT_PASSENGERS = 1

DEFAULT_TIRE_PRESSURE = 100

DEFAULT_ODOMETER = 0

DEFAULT_AC_LEVEL = 0

DEFAULT_LOAD = 0


# ==========================================================
# LIMITS
# ==========================================================

MIN_SPEED = 10

MAX_SPEED = 200

MIN_NET_FACTOR = 0.01

MAX_NET_FACTOR = 1.00

MIN_DISTANCE = 0.1

MAX_DISTANCE = 10000

MIN_FUEL = 0.1

MAX_FUEL = 500


# ==========================================================
# RESPONSE STATUS
# ==========================================================

STATUS_SUCCESS = "success"

STATUS_ERROR = "error"


# ==========================================================
# ERROR CODES
# ==========================================================

ERROR_VALIDATION = "VALIDATION_ERROR"

ERROR_CALCULATION = "CALCULATION_ERROR"

ERROR_DATABASE = "DATABASE_ERROR"

ERROR_UNKNOWN = "UNKNOWN_ERROR"


# ==========================================================
# FACTOR TABLES
# ==========================================================

VALID_LOAD_VALUES = [
    0,
    25,
    50,
    75,
    100,
]

VALID_AC_LEVELS = [
    0,
    1,
    2,
    3,
    4,
    5,
]

VALID_PASSENGERS = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    
]


# ==========================================================
# VEHICLE RATING
# ==========================================================

EFFICIENCY_EXCELLENT = "Excellent"

EFFICIENCY_GOOD = "Good"

EFFICIENCY_AVERAGE = "Average"

EFFICIENCY_POOR = "Poor"


# ==========================================================
# DEFAULT CURRENCY
# ==========================================================

CURRENCY_USD = "USD"

CURRENCY_CAD = "CAD"

DEFAULT_CURRENCY = CURRENCY_USD


# ==========================================================
# RESPONSE KEYS
# ==========================================================

KEY_STATUS = "status"

KEY_MESSAGE = "message"

KEY_DATA = "data"

KEY_ERRORS = "errors"

KEY_TIMESTAMP = "timestamp"


# ==========================================================
# MODULE NAME
# ==========================================================

MODULE_NAME = "Advanced Efficiency Management"

MODULE_SHORT_NAME = "AEM"