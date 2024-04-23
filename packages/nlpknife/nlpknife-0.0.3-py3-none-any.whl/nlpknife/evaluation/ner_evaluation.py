import pandas as pd
from pprint import pprint

from sklearn.metrics import classification_report as token_report
from seqeval.metrics import classification_report as entity_report
from nlpknife.evaluation.ner_eval_core.ner_eval import collect_named_entities
from nlpknife.evaluation.ner_eval_core.ner_eval import Evaluator
from nlpknife.evaluation.ner_eval_core.ner_eval import compute_metrics, collect_named_entities


"""
    scikit-learn=0.21.3测试通过
    REF:
        http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/
"""

class NEREvaluation:
    
    def __init__(self, y_true: list, y_pred: list, tags: list, inputs=None):
        self.y_true = y_true
        self.y_pred = y_pred
        self.token_tags = tags
        self.token_tags_map = {tag:i for i, tag in enumerate(tags)}
        self.entity_tags = self.get_entity_tags(tags)
        self.evaluator = Evaluator(y_true, y_pred, self.entity_tags)
        self.inputs = inputs

    def get_entity_tags(self, tags):
        return [tag.split("-")[1] for tag in tags if tag != "O"]

    def get_entity(self, y_pred: list)-> list:
        """
            实体聚合
        """
        results = []
        for y in y_pred:
            tmp = {
                    "input": y,
                    "entities":[]
                }
            for entity in collect_named_entities(y):
                tmp["entities"].append({"type":entity.e_type, "begin_char": entity.start_offset, "end_char": entity.end_offset})
            results.append(tmp)
        return results
    
    def core_metric(self, level):
        if level == "entity_super":
            return self.evaluator.evaluate()
        elif level == "entity_normal":
            return entity_report(self.y_true, self.y_pred)
        else:
            y_true = [self.token_tags_map[y] for item in self.y_true for y in item]
            y_pred = [self.token_tags_map[y] for item in self.y_pred for y in item]
            return token_report(y_true, y_pred, target_names = self.token_tags)
    
    def get_report(self, level = "entity_normal"):
        """
            level: token | entity_normal | entity_super
                token: token级的P/R/F1-score
                entity_normal:  entity级的P/R/F1-score
                entity_super:   entity级的具体统计和case分析，以及P/R/F1-score
        """
        if level == "entity_super":
            all_type_res, each_type_res, all_type_samples, each_type_samples = self.core_metric(level)
            metric_list = [
                    {
                        "name":"all",
                        "metric":pd.DataFrame(all_type_res)
                        }
                    ]
            for key, value in each_type_res.items():
                metric_list.append(
                        {
                            "name":key, "metric": pd.DataFrame(value)
                            }
                        )
            # 非badcase报告 
            for i, metric in enumerate(metric_list):
                pprint(metric)
            
            pprint("-"*30)
            
            # badcase报告
            if self.inputs:
                for sent, true_ents, pred_ents in zip(self.inputs, self.y_true, self.y_pred):
                    true_ents = collect_named_entities(true_ents)
                    pred_ents = collect_named_entities(pred_ents)
                    _, _, all_type_samples, each_type_samples = compute_metrics(true_ents, pred_ents, self.entity_tags)
                    pprint("".join(sent))
                    for type_key in all_type_samples:
                        del all_type_samples[type_key]["correct"]
                    pprint(all_type_samples)
                    for type_key in each_type_samples:
                        for key in each_type_samples[type_key]:
                            del each_type_samples[type_key][key]["correct"]
                    pprint(each_type_samples)
                    pprint("-"*30)
        else:
            # token报告
            all_type_res = self.core_metric(level)
            print(all_type_res)

    @staticmethod
    def data_format(inputs, y_true, y_pred):
        """
            转换基于词典标注的结果
        """
        def anno_sent(anno_list):
            true_list = ["O"] * len(input_)
            for item in anno_list:
                start = item["begin_char"]
                end = item["end_char"]
                for i in range(start, end+1):
                    if i == start:
                        true_list[i] = "B-"+item["type"]
                    else:
                        true_list[i] = "I-"+item["type"]
            return true_list
        new_inputs = []
        new_true = []
        new_pred = []
        for input_, true, pred in zip(inputs, y_true, y_pred):
            new_inputs.append(list(input_))
            new_true.append(anno_sent(true))
            new_pred.append(anno_sent(pred))
        return new_inputs, new_true, new_pred
