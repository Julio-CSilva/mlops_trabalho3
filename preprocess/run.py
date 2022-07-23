import argparse
import logging
import os
import pandas as pd
import wandb

# configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    datefmt='%d-%m-%Y %H:%M:%S')

# reference for a logging obj
logger = logging.getLogger()

def process_args(args):
    """
    Arguments
        args - command line arguments
        args.input_artifact: Fully qualified name for the raw data artifact
        args.artifact_name: Name for the W&B artifact that will be created
        args.artifact_type: Type of the artifact to create
        args.artifact_description: Description for the artifact
    """
    
    # create a new wandb project
    run = wandb.init(job_type="process_data")
    
    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()
    
    # columns used 
    columns = ["room_type","accommodates","bedrooms","beds",
           "price","minimum_nights","maximum_nights","minimum_minimum_nights",
           "maximum_minimum_nights","minimum_maximum_nights","maximum_maximum_nights",
           "minimum_nights_avg_ntm","maximum_nights_avg_ntm","has_availability",
           "availability_30","availability_60","availability_90",
           "availability_365","number_of_reviews",
           "number_of_reviews_ltm","number_of_reviews_l30d",
           "review_scores_rating","review_scores_accuracy",
           "review_scores_cleanliness","review_scores_checkin","review_scores_communication",
           "review_scores_location","review_scores_value",
           "instant_bookable","calculated_host_listings_count",
           "calculated_host_listings_count_entire_homes",
           "calculated_host_listings_count_private_rooms",
           "calculated_host_listings_count_shared_rooms","reviews_per_month"]
    
    # create a dataframe from the artifact path
    df = pd.read_csv(artifact_path)
    
    # Delete duplicated rows
    #logger.info("Dropping duplicates")
    #df.drop_duplicates(inplace=True)
    
    logger.info("Select Columns")
    df = df[columns]

    logger.info("Drop NaN")
    df = df.dropna()


    logger.info("Price to float64")
    df['price'] = df['price'].str.replace("$", "")
    df['price'] = df['price'].str.replace(",", "")
    df['price'] = df['price'].astype("float")
    
    # Generate a "clean data file"
    filename = "preprocessed_data.csv"
    df.to_csv(filename,index=False)
    
    # Create a new artifact and configure with the necessary arguments
    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description
    )
    artifact.add_file(filename)
    
    # Upload the artifact to Wandb
    logger.info("Logging artifact")
    run.log_artifact(artifact)

    # Remote temporary files
    os.remove(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True
    )

    # get arguments
    ARGS = parser.parse_args()

    # process the arguments
    process_args(ARGS)

