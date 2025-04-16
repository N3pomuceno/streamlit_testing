import pandas as pd

from logger import setup_logger


def ranking_metrics(df: pd.DataFrame, metrics: list) -> pd.DataFrame:
    """
    Function to rank the models based on the provided metrics.
    """
    ranked_df = df.copy()

    for metric in metrics:
        ranked_df[f"rank_{metric}"] = df.groupby("fr_aval_id")[metric].rank(
            ascending=False, method="min"
        )

    # Sum only the rank values
    rank_columns = [f"rank_{metric}" for metric in metrics]
    ranked_df["total_rank"] = ranked_df[rank_columns].sum(axis=1)

    return ranked_df


def get_top_n_models(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Function to get the top N models based on the total rank.
    """
    df_sorted = df.sort_values(by=["fr_aval_id", "total_rank"], ascending=[True, True])
    result = df_sorted.groupby("fr_aval_id").head(n)
    return result


def get_top_n_documents(df: pd.DataFrame, n: int) -> list:
    """
    Function to get the top N Documentos based on the total rank.
    """
    df_sorted = df.sort_values(by=["total_rank", "fr_aval_id"], ascending=[True, True])
    relevant_documents = list(df_sorted["material fact"].unique())[:n]

    df_sorted = df_sorted[df_sorted["material fact"].isin(relevant_documents)]
    df_sorted["new_id"] = pd.factorize(df_sorted["fr_aval_id"])[0]
    return df_sorted


def main():
    logger = setup_logger("logs", "create_dataframe.log", "INFO")

    # Load the DataFrame
    logger.info("Loading DataFrame...")
    df = pd.read_csv(
        "data/MeLLL_AIDA_FINANCE_WITHMETRICS.csv", encoding="utf-8", sep=","
    )
    df["fr_aval_id"] = df["material fact"] + df["id"]

    # Define the metrics to rank
    metrics = [
        "BLEU_score",
        "BERTScore_Precision",
        "BERTScore_Recall",
        "BERTScore_F1",
        "rouge1",
        "rouge2",
        "rougeL",
        "rougeLsum",
        "CTC_groundness",
        "CTC_groundness_ref",
        "CTC_factual",
        "CTC_factual_ref",
    ]

    # User input top n Models and top n Documents
    logger.info("Getting user input for top N models and documents...")
    n_model = input("Enter the number of top models to retrieve: ")
    n_document = input("Enter the number of top documents to retrieve: ")

    # Rank the models based on the metrics
    logger.info("Ranking models based on metrics...")
    ranked_df = ranking_metrics(df, metrics)

    # Get the top n models for each material fact
    df_top_n_models = get_top_n_models(ranked_df, int(n_model))

    # Get the top n unique material facts
    df_top_n_documents = get_top_n_documents(df_top_n_models, int(n_document))

    print(df_top_n_documents[["id", "generator_model", "total_rank"]].head(12))

    # Save the ranked DataFrame to a CSV file
    logger.info("Saving ranked DataFrame to CSV...")
    df_top_n_documents.to_csv(
        "data/m{}_fr{}_rankedModels.csv".format(n_model, n_document), index=False
    )


if __name__ == "__main__":
    main()
