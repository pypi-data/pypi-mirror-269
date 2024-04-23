'''
Description: aka.zhp
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-08 22:25:37
LastEditTime: 2024-01-10 22:52:45
'''

import yaml
from pprint import pprint
from datasets import Dataset
from ragas import evaluate
from ragas.llms import LangchainLLM
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.llms import AzureOpenAI
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

import os
CONFIG = yaml.safe_load(open("config/config.yaml", "r"))

for key in [
            "OPENAI_API_TYPE",
            "OPENAI_API_VERSION",
            "OPENAI_API_BASE",
            "OPENAI_API_KEY"
            ]:
    os.environ[key] = CONFIG[key]


class RAGEvaluation:
    def __init__(self):
        self.azure_model,self.azure_embeddings = self._init_azure_model()
        self.metrics = [faithfulness,
                        context_recall,
                        context_precision,
                        answer_relevancy
                        ]
        self._init_metrics()
        
    def _init_azure_model(self):
        azure_model = AzureChatOpenAI(
            deployment_name=CONFIG["AZURE_MODEL"]["CHAT"]["DEPLOYMENT_NAME"],
            model=CONFIG["AZURE_MODEL"]["CHAT"]["MODEL_NAME"]
        )
        azure_embeddings = AzureOpenAIEmbeddings(
             deployment=CONFIG["AZURE_MODEL"]["EMBEDDING"]["DEPLOYMENT_NAME"],
            model=CONFIG["AZURE_MODEL"]["EMBEDDING"]["MODEL_NAME"]
        )
        return azure_model,azure_embeddings
    
    def _init_metrics(self):
        ragas_azure_model = LangchainLLM(self.azure_model)
        for m in self.metrics:
            if m == answer_relevancy:
                m.embeddings = self.azure_embeddings
            m.__setattr__("llm", ragas_azure_model)
    
    def get_evaluation(self,questions, answers, contexts, ground_truths):
        data = {
            "question":questions,
            "answer":answers,
            "contexts":contexts,
            "ground_truths":ground_truths
        }
        input_dataset = Dataset.from_dict(data)
        result = evaluate(
            dataset = input_dataset, 
            metrics=self.metrics,
        )
        return result

if __name__ == "__main__":
    rag_eval = RAGEvaluation()

    questions = ["What did the president say about Justice Breyer?", 
                "What did the president say about Intel's CEO?",
                "What did the president say about gun violence?",
                ]
    ground_truths = [
                    ["The president said that Justice Breyer has dedicated his life to serve the country and thanked him for his service."],
                    ["The president said that Pat Gelsinger is ready to increase Intel's investment to $100 billion."],
                    ["The president asked Congress to pass proven measures to reduce gun violence."]
                    ]
    answers = []
    contexts = []
    for query in questions:
        answers.append("The president said that Justice Breyer has dedicated his life to serve the country and thanked him for his service.")
        contexts.append(
            ["The president said that Justice Breyer has dedicated his life to serve the country and thanked him for his service.",
            "The president said that Justice Breyer has dedicated his life to serve the country and thanked him for his service.",
            "The president said that Justice Breyer has dedicated his life to serve the country and thanked him for his service."
            ]
                        )
    print(rag_eval.get_evaluation(questions, answers, contexts, ground_truths))

