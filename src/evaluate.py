import os
import pandas as pd
from help_desk import HelpDesk
from dotenv import load_dotenv, find_dotenv
from langchain.evaluation import load_evaluator
from langchain.evaluation import EmbeddingDistance
from config import EVALUATION_DATASET


def predict(model, question):
    result, sources = model.retrieval_qa_inference(question, verbose=False)
    return result


def open_evaluation_dataset(filepath):
    df = pd.read_csv(filepath, delimiter='\t')
    return df


def get_levenshtein_distance(model, reference_text, prediction_text):
    evaluator = load_evaluator("string_distance")
    return evaluator.evaluate_strings(
        prediction=prediction_text,
        reference=reference_text
    )

def get_cosine_distance(model, reference_text, prediction_text):
    evaluator = load_evaluator("embedding_distance", distance_metric=EmbeddingDistance.COSINE)
    return evaluator.evaluate_strings(
        prediction=prediction_text,
        reference=reference_text
    )

def evaluate_dataset(model, dataset, verbose=True):
    predictions = []
    levenshtein_distances = []
    cosine_distances = []
    for i, row in dataset.iterrows():
        prediction_text = predict(model, row['Questions'])

        # Distances
        levenshtein_distance = get_levenshtein_distance(model, row['Réponses'].strip(), prediction_text.strip())
        cosine_distance = get_cosine_distance(model, row['Réponses'].strip(), prediction_text.strip())

        if verbose:
            print("\n QUESTIONS \n", row['Questions'])
            print("\n REPONSES \n", row['Réponses'])
            print("\n PREDICTION \n", prediction_text)
            print("\n LEV DISTANCE \n", levenshtein_distance['score'])
            print("\n COS DISTANCE \n", cosine_distance['score'])

        predictions.append(prediction_text)
        levenshtein_distances.append(levenshtein_distance['score'])
        cosine_distances.append(cosine_distance['score'])

    dataset['Prédiction'] = predictions
    dataset['Levenshtein_Distance'] = levenshtein_distances
    dataset['Cosine_Distance'] = cosine_distances
    dataset.to_csv(EVALUATION_DATASET, index=False, sep= '\t')
    return dataset


def run():
    dataset = open_evaluation_dataset(EVALUATION_DATASET)
    results = evaluate_dataset(model, dataset)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    model = HelpDesk(new_db=True)
    dataset = open_evaluation_dataset(EVALUATION_DATASET)
    evaluate_dataset(model, dataset)

    print('Mean Levenshtein distance: ', dataset['Levenshtein_Distance'].mean())
    print('Mean Cosine distance: ', dataset['Cosine_Distance'].mean())