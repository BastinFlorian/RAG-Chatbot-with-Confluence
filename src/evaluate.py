import os
import sys
import pandas as pd
from help_desk import HelpDesk
from dotenv import load_dotenv, find_dotenv
from langchain.evaluation import load_evaluator

sys.path.append('../')
from config import EVALUATION_DATASET

load_dotenv(find_dotenv())

def get_predicted_output(model, input_text):
    result, sources = model.retrieval_qa_inference(input_text, verbose=False)
    return result


def open_evaluation_dataset(filepath):
    df = pd.read_csv(filepath, delimiter='\t')
    return df


def evaluate(model, input_text, reference_text):
    predicted_output = get_predicted_output(model, input_text)
    evaluator = load_evaluator("string_distance")
    return evaluator.evaluate_strings(
        prediction=predicted_output,
        reference=reference_text
    )

def evaluate_dataset(model, dataset):
    predictions = []
    distances = []
    for i, row in dataset.iterrows():
        prediction = get_predicted_output(model, row['Réponses'])
        distance = evaluate(model, row['Réponses'], prediction)

        predictions.append(prediction)
        distances.append(distance['score'])

    dataset['Prédiction'] = predictions
    dataset['Distance'] = distances
    dataset.to_csv(EVALUATION_DATASET, index=False, sep= '\t')
    return dataset


def run():
    dataset = open_evaluation_dataset(EVALUATION_DATASET)
    results = evaluate_dataset(model, dataset)


if __name__ == '__main__':
    model = HelpDesk(new_db=True)
    dataset = open_evaluation_dataset(EVALUATION_DATASET)
    evaluate_dataset(model, dataset)
    print('Mean Levenshtein distance: ', dataset['Distance'].mean())
