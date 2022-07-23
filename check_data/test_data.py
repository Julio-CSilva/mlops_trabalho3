import pandas as pd
import scipy.stats


# Non Deterministic Test
def test_kolmogorov_smirnov(data, ks_alpha):

    sample1, sample2 = data

    numerical_columns = [
        "accommodates",
        "bedrooms",
        "beds",
        "price",
        "minimum_nights_avg_ntm",
        "maximum_nights_avg_ntm",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_location",
        "review_scores_value",
        "reviews_per_month",
        "minimum_minimum_nights",
        "maximum_minimum_nights",
        "minimum_maximum_nights",
        "maximum_maximum_nights",
        "availability_30",
        "availability_60",
        "availability_90",
        "availability_365",
        "minimum_nights",
        "maximum_nights",
    ]
    
    # Bonferroni correction for multiple hypothesis testing
    alpha_prime = 1 - (1 - ks_alpha)**(1 / len(numerical_columns))

    for col in numerical_columns:

        # two-sided: The null hypothesis is that the two distributions are identical
        # the alternative is that they are not identical.
        ts, p_value = scipy.stats.ks_2samp(
            sample1[col],
            sample2[col],
            alternative='two-sided'
        )

        # NOTE: as always, the p-value should be interpreted as the probability of
        # obtaining a test statistic (TS) equal or more extreme that the one we got
        # by chance, when the null hypothesis is true. If this probability is not
        # large enough, this dataset should be looked at carefully, hence we fail
        assert p_value > alpha_prime
        
# Determinstic Test
def test_column_presence_and_type(data):
    
    # Disregard the reference dataset
    _, df = data

    required_columns = {
        "room_type": pd.api.types.is_object_dtype,
        "accommodates": pd.api.types.is_int64_dtype,
        "bedrooms": pd.api.types.is_float_dtype,
        "beds": pd.api.types.is_float_dtype,
        "has_availability": pd.api.types.is_object_dtype,
        "instant_bookable": pd.api.types.is_object_dtype,
        "price": pd.api.types.is_float_dtype,
        "minimum_nights_avg_ntm": pd.api.types.is_float_dtype,
        "maximum_nights_avg_ntm": pd.api.types.is_float_dtype,
        "review_scores_rating": pd.api.types.is_float_dtype,
        "review_scores_accuracy": pd.api.types.is_float_dtype,
        "review_scores_cleanliness": pd.api.types.is_float_dtype,
        "review_scores_checkin": pd.api.types.is_float_dtype,
        "review_scores_communication": pd.api.types.is_float_dtype,
        "review_scores_location": pd.api.types.is_float_dtype,
        "review_scores_value": pd.api.types.is_float_dtype,
        "reviews_per_month": pd.api.types.is_float_dtype,
        "minimum_minimum_nights": pd.api.types.is_int64_dtype,
        "maximum_minimum_nights": pd.api.types.is_int64_dtype,
        "minimum_maximum_nights": pd.api.types.is_int64_dtype,
        "maximum_maximum_nights": pd.api.types.is_int64_dtype,
        "availability_30": pd.api.types.is_int64_dtype,
        "availability_60": pd.api.types.is_int64_dtype,
        "availability_90": pd.api.types.is_int64_dtype,
        "availability_365": pd.api.types.is_int64_dtype,
        "number_of_reviews": pd.api.types.is_int64_dtype,
        "number_of_reviews_ltm": pd.api.types.is_int64_dtype,
        "number_of_reviews_l30d": pd.api.types.is_int64_dtype,
        "minimum_nights": pd.api.types.is_int64_dtype,
        "maximum_nights": pd.api.types.is_int64_dtype,
    }

    # Check column presence
    assert set(df.columns.values).issuperset(set(required_columns.keys()))

    for col_name, format_verification_funct in required_columns.items():

        assert format_verification_funct(df[col_name]), f"Column {col_name} failed test {format_verification_funct}"


# Deterministic Test
def test_column_ranges(data):
    
    # Disregard the reference dataset
    _, df = data

    ranges = {
        "accommodates": (1, 20),
        "bedrooms": (1, 30),
        "beds": (1, 60),
        "review_scores_cleanliness": (0, 5),
    }

    for col_name, (minimum, maximum) in ranges.items():

        assert df[col_name].dropna().between(minimum, maximum).all(), (
            f"Column {col_name} failed the test. Should be between {minimum} and {maximum}, "
            f"instead min={df[col_name].min()} and max={df[col_name].max()}"
        )