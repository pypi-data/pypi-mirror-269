"""
This file contains ModelExplainer and RuleBuilder classes that explain a tree ensemble
model by extracting rules to explain the positive class. This file contains the
implementation of TE2Rules Algorithm described in the paper:
"TE2Rules: Explaining Tree Ensembles using Rules"
(https://arxiv.org/abs/2206.14359/).
"""

from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd
import sklearn
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from tqdm import tqdm
from xgboost import XGBClassifier

from te2rules.adapter import (
    ScikitGradientBoostingClassifierAdapter,
    ScikitRandomForestClassifierAdapter,
    XgboostXGBClassifierAdapter,
)
from te2rules.rule import Rule
from te2rules.tree import RandomForest

log = logging.getLogger()


class ModelExplainer:
    """
    The :mod:`te2rules.explainer.ModelExplainer` module explains
    Tree Ensemble models (TE) like XGBoost, Random Forest, trained
    on a binary classification task, using a rule list. The algorithm
    used by TE2Rules is based on Apriori Rule Mining.
    For more details on the algorithm, please check out our paper
    `TE2Rules: Explaining Tree Ensembles using Rules
    <https://arxiv.org/abs/2206.14359/>`_.
    """

    def __init__(
        self,
        model: sklearn.ensemble | XGBClassifier,
        feature_names: List[str],
        verbose: bool = False,
    ):
        """
        Initialize the explainer with the trained tree ensemble model
        and feature names used by the model.

        Returns a ModelExplainer object

        Parameters
        ----------
        model: sklearn.ensemble.GradientBoostingClassifier or \
            sklearn.ensemble.RandomForestClassifier or \
            xgboost.XGBClassifier
            The trained Tree Ensemble model to be explained.
            The model is expected to be a binary classifier.
        feature_name: List[str]
            List of feature names used by the `model`. Only alphanumeric characters and
            underscores are allowed in feature names.
        verbose: bool, optional
            Optional boolean value to give more insights on the running of the
            explanation algorithm.
            Default = False

        Returns
        -------
        self: te2rules.explainer.ModelExplainer
            A ModelExplainer object initialized with the model to be explained.

        Raises
        ------
        ValueError:
            when `model` is not a supported Tree Ensemble Model.
            Currently, only scikit-learn's GradientBoostingClassifier,
            RandomForestClassifier and xgboost's XGBClassifier are supported.

        ValueError:
            when `feature_name` list contains a name that has any character other
            than alphanumeric characters or underscore.

        """
        self.feature_names = feature_names
        for f in feature_names:
            if re.search("[^a-zA-Z0-9_]", f):
                raise ValueError(
                    "Only alphanumeric characters and underscores are allowed "
                    + "in feature names. But found feature name: "
                    + str(f)
                )

        if verbose is True:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
        else:
            logging.basicConfig(format="%(message)s")

        if isinstance(model, GradientBoostingClassifier):
            self.random_forest = ScikitGradientBoostingClassifierAdapter(
                model, feature_names
            ).random_forest
        elif isinstance(model, RandomForestClassifier):
            self.random_forest = ScikitRandomForestClassifierAdapter(
                model, feature_names
            ).random_forest
        elif isinstance(model, XGBClassifier):
            self.random_forest = XgboostXGBClassifierAdapter(
                model, feature_names
            ).random_forest
        else:
            raise ValueError(
                "Only GradientBoostingClassifier, RandomForestClassifier "
                + "and XGBClassifier "
                + "are supported. But received "
                + str(type(model))
            )

    def explain(
        self,
        X: List[List[float]],
        y: List[int],
        num_stages: Optional[int] = None,
        min_precision: float = 0.95,
        jaccard_threshold: float = 0.20,
    ) -> List[str]:
        """
        A method to extract rule list from the tree ensemble model.
        This method takes in input features used by the model and predicted class
        output by the model.

        Returns a List of rule strings.

        Parameters
        ----------
        X: 2d numpy.array
            2 dimensional input data used by the `model`
        y: 1d numpy.array
            1 dimensional model class predictions (0 or 1) from the `model`
        num_stages: int, optional
            The algorithm runs in stages starting from stage 1, stage 2 to all the way
            till stage n where n is the number of trees in the ensemble.
            Stopping the algorithm at an early stage  results in a few short rules
            (with quicker run time, but less coverage in data). By default,
            the algorithm explores all stages before terminating.
        min_precision: float, optional
            This parameter controls the minimum precision of extracted rules.
            Setting it to a smaller threshold, allows extracting shorter
            (more interpretable, but less faithful) rules.
            By default, the algorithm uses a minimum precision threshold of 0.95.
        jaccard_threshold: float, optional
            This parameter (between 0 and 1) controls how rules from different node
            combinations are combined. Setting it to a smaller threshold, ensures that
            only rules that are very different from one another are combined, speeding
            up the algorithm at the cost of missing some rules that can potentially
            explain the model. Combining similar rules that cover very similar set of
            instances do not provide any new information for the explainer algorithm.
            By default, the algorithm uses a jaccard threshold of 0.20.


        Returns
        -------
        rules: List[str]
            A List of human readable rules.

        Raises
        ------
        ValueError:
            when `X` and `y` are of different length.

        ValueError:
            when entries in `y` are other than 0 and 1. Only binary
            classification is supported.

        Notes
        -----
        The data is used for extracting rules with relevant
        combination of input features. Without data, explainer would need
        to extract rules for all possible combinations of input features,
        including those combinations which are extremely rare in the data.

        Examples
        --------
        >>> from te2rules.explainer import ModelExplainer
        >>> model_explainer = ModelExplainer(model=model, feature_names=feature_names)
        >>> rules = model_explainer.explain(X=x_train, y=y_train_pred)
        """

        if len(X) != len(y):
            raise ValueError("X and y should have the same length")
        for i in range(len(y)):
            if y[i] not in [0, 1]:
                raise ValueError("entries y should only be 0 or 1.")

        self.rule_builder = RuleBuilder(
            random_forest=self.random_forest,
            num_stages=num_stages,
            min_precision=min_precision,
            jaccard_threshold=jaccard_threshold,
        )

        self.rules = [str(r) for r in self.rule_builder.explain(X, y)]
        self.longer_rules = [str(r) for r in self.rule_builder.longer_rules]

        return self.rules

    def _prune_rules_by_dropping_terms(
        self,
        rules: List[Rule],
        X: List[List[float]],
        y: List[int],
        min_precision: float,
    ) -> List[str]:
        """
        A method to prune rules by dropping terms one by one and checking if the
        precision of pruned rules on X, y has precision greater than or equal to
        min_precision. The pruned rule with least number of terms with precision
        above the min_precision threshold is returned.

        Returns a List of rule strings.

        Parameters
        ----------
        rule: List[Rule]
            List of rules to be pruned
        X: 2d numpy.array
            2 dimensional input data used to evaluate the rules
        y: 1d numpy.array
            1 dimensional model class predictions (0 or 1) from the `model`
        min_precision: float, optional
            minimum precision required for pruned rules.

        Returns
        -------
        pruned_rules: List[str]
            A List of pruned rule strings.
        """

        def get_precision(
            query_rule: str, data: List[List[float]], label: List[int]
        ) -> float:
            precision = 0.0
            df = pd.DataFrame(data, columns=self.feature_names)
            support = df.query(query_rule).index.tolist()
            y_rule: List[int] = [0] * len(df)
            for i in support:
                y_rule[i] = 1
                if label[i] == 1:
                    precision = precision + 1
            precision = precision / len(support)
            return precision

        def drop_clause(
            clauses: List[str],
            data: List[List[float]],
            label: List[int],
            min_precision: float,
        ) -> List[List[str]]:
            dropped = []
            for c in clauses:
                pruned_clauses = clauses[:]
                pruned_clauses.remove(c)
                pruned_query_rule = " & ".join(pruned_clauses)
                if pruned_query_rule != "":
                    precision = get_precision(pruned_query_rule, data, label)
                    if precision >= min_precision:
                        dropped.append(pruned_clauses)
            return dropped

        pruned_rules_str = []
        for i in range(len(rules)):
            shorter_rules = [rules[i].decision_rule]
            shorter_rules_str = [str(rules[i])]

            while len(shorter_rules) > 0:
                shorter_rules_backup = shorter_rules
                shorter_rules_str_backup = shorter_rules_str
                shorter_rules = []
                shorter_rules_str = []
                for c in shorter_rules_backup:
                    for r in drop_clause(c, X, y, min_precision):
                        if " & ".join(r) not in shorter_rules_str:
                            shorter_rules.append(r)
                            shorter_rules_str.append(" & ".join(r))

            shorter_rules = shorter_rules_backup
            shorter_rules_str = shorter_rules_str_backup
            shorter_rules_len = [len(r) for r in shorter_rules]
            shorter_rules_precision = [
                get_precision(r, X, y) for r in shorter_rules_str
            ]

            index = 0
            for j in range(len(shorter_rules)):
                if shorter_rules_len[j] < shorter_rules_len[index]:
                    index = j
                if shorter_rules_len[j] == shorter_rules_len[index]:
                    if shorter_rules_precision[j] > shorter_rules_precision[index]:
                        index = j

            pruned_rules_str.append(shorter_rules_str[index])

        return pruned_rules_str

    def predict(self, X: List[List[float]]) -> List[int]:
        """
        A method to apply rules found by the explain() method
        on a given input data. Any data that satisfies at least
        one rule from the rule list found by the explain() is labelled
        as belonging to the positive class. All other data is labelled
        as belonging to the negative class.

        This method can only be called after calling the explain()
        method. Otherwise, it throws AttributeError.

        Returns a List of class predictions coressponding to the data.

        Parameters
        ----------
        X: 2d numpy.array
            2 dimensional input data to apply the rules extracted by the explainer.

        Returns
        -------
        class_predictions: List[int]
            A List of class predictions coressponding to the data.

        Raises
        ------
        AttributeError:
            when called before calling explain()
        """
        try:
            df = pd.DataFrame(X, columns=self.feature_names)
            y_rules = self.rule_builder.apply(df)
        except AttributeError:
            raise AttributeError(
                "rules to explain the tree ensemble are not set. "
                + "Call explain() before calling apply()"
            )
        return y_rules

    def get_fidelity(
        self, X: Optional[List[List[float]]] = None, y: Optional[List[int]] = None
    ) -> Tuple[float, float, float]:
        """
        A method to evaluate the rule list extracted by the `explain` method

        Returns a fidelity on positives, negative, overall

        Parameters
        ----------
        X: 2d numpy.array, optional
            2 dimensional data with feature values used for calculating fidelity.
            Defaults to data used by the model for rule extraction.
        y: 1d numpy.array, optional
            1 dimensional model class predictions (0 or 1) from the `model` on X.
            Defaults to model class predictions on the data used
            by the model for rule extraction.

        Returns
        -------
        fidelity: [float, float, float]
            Fidelity is the fraction of data for which the rule list agrees
            with the tree ensemble. Returns the fidelity on overall data,
            positive predictions and negative predictions by the model.

        Examples
        --------
        >>> (fidelity, fidelity_pos, fidelity_neg) = model_explainer.get_fidelity()
        """
        if (X is not None) and (y is not None):
            df = pd.DataFrame(X, columns=self.feature_names)
            y_rules = self.rule_builder.apply(df)
            fidelity_positives = 0.0
            fidelity_negatives = 0.0
            positives = 0.0 + 1e-6
            negatives = 0.0 + 1e-6
            for i in range(len(y)):
                if y[i] == 1:
                    positives = positives + 1
                    if y[i] == y_rules[i]:
                        fidelity_positives = fidelity_positives + 1
                if y[i] == 0:
                    negatives = negatives + 1
                    if y[i] == y_rules[i]:
                        fidelity_negatives = fidelity_negatives + 1

            fidelity = (fidelity_positives + fidelity_negatives) / (
                positives + negatives
            )
            fidelity_positives = fidelity_positives / positives
            fidelity_negatives = fidelity_negatives / negatives
            return (fidelity, fidelity_positives, fidelity_negatives)

        return self.rule_builder.get_fidelity()

    def explain_instance_with_rules(
        self, X: List[List[float]], explore_all_rules: bool = True
    ) -> List[List[str]]:
        """
        A method to explain the model output for a list of inputs using rules.
        For each instance in the list, if the model output is positive, this method
        returns a corresponding list of rules that explain that instance.
        For any instance in the list, for which the model output is negative,
        this method returns an empty list corresponding to that instance.

        Returns a list of explanations corresponding to each input.
        Each explanation is a list of possible rules that can explain
        the corresponding instance.

        Parameters
        ----------
        X: 2d numpy.array
            2 dimensional data with feature values that can be sent
            to the model for predicting outcome.
        explore_all_rules: boolean, optional
            optional boolean variable guiding the algorithm's behavior.
            When set to True, the algorithm considers all possible rules (longer_rules)
            extracted by the explain() function before employing set cover to select
            a condensed subset of rules. When set to False, the algorithm considers
            only the condensed subset of rules returned by explain().

            By default, the function utilizes all possible rules (longer_rules) obtained
            through explain().

        Returns
        -------
        list of explaining rules for each instance, with each explanation presented
        as a list of rules each of which can independently explain the instance.
        """
        dataframe = pd.DataFrame(X, columns=self.feature_names)
        if explore_all_rules is True:
            rules = self.longer_rules
        else:
            rules = self.rules

        rule_support = []
        for r in rules:
            support = dataframe.query(str(r)).index.tolist()
            rule_support.append(support)

        selected_rules: List[List[str]] = []
        for i in range(len(dataframe)):
            selected_rules.append([])
        for i in range(len(rule_support)):
            for j in rule_support[i]:
                selected_rules[j].append(rules[i])

        return selected_rules


class RuleBuilder:
    """
    A class to get rules from individual trees in a tree ensemble
    and combine them together in multiple stages to explain cross-tree
    interactions within the tree ensemble. RuleBuilder consists of:
    1) The tree ensemble model, from which to extract rules
        to explain the positive class.
    2) number of stages: The rules are combined in stages starting
        from stage 1, stage 2 to all the way till stage n where n
        is the number of trees in the ensemble. The rules extracted
        in stage i, capture rules from i-tree interactions in the
        tree ensemble.
    3) minimum precision: minimum precision of extracted rules
    4) jaccard threshold: minimum similarity score (between 0 and 1)
        of rules to be combined in each stage.

    RuleBuilder implements the TE2Rules algorithm. Calling explain()
    explains the tree ensemble using rules for the postive class
    prediction.
    """

    def __init__(
        self,
        random_forest: RandomForest,
        num_stages: Optional[int] = None,
        min_precision: float = 0.95,
        jaccard_threshold: float = 0.20,
    ):
        self.random_forest = random_forest
        # if num_stages not set by user, will set it to the number of trees
        # note that we neednum_stages <= num_trees
        if num_stages is not None:
            self.num_stages = min(num_stages, self.random_forest.get_num_trees())
        else:
            self.num_stages = self.random_forest.get_num_trees()
        self.min_precision = min_precision
        self.jaccard_threshold = jaccard_threshold

    def explain(self, X: List[List[float]], y: List[int]) -> List[Rule]:
        """
        A method to extract rule list for explaining the positive
        class prediction from the tree ensemble model using input data
        and class labels predicted by the model.

        TE2Rules Algorithm is implemented here.
        For more details on the algorithm, please check out our paper
        "TE2Rules: Explaining Tree Ensembles using Rules"
        (https://arxiv.org/abs/2206.14359/).

        A rough sketch of the steps:
        Run in stages 1 to n = num trees in the ensemble
        or till there is unexplained positive class labels
        beyond the class labels already explained by
        the explanations (solutions):
        1) generate candidate rules from the tree ensemble:
            a) In stage 1: candidates = rules from individual trees in the ensemble.
                deduplicate rules generated from multiple source trees and combine
                the sources into the rule's identity.
            b) In stage > 1: For generating candidate rules for cross tree interactions
                beyond rules from a single tree, generate candidates for the next stage
                by combining rules from k tree combinations to get rules for
                k + 1 tree combinations.
        2) generate explanations (solutions) from the candidates:
            a) Filter candidates to check if it explains any positive class
                prediction. If a rule does not explain any positive class
                prediction, it can be discarded.
            b) Filter the candidates to check if the rules qualifies to be an
                explanation. Does it have sufficient precision? If it does,
                it can be promoted to a list of explanations (solutions).

        Post Processing, after all stages:
        3) Simplify explanations (solutions), by deduplicating them,
            dropping redundant terms to make the rules shorter. Select rules with
            high coverage using a greedy set cover on the set of positive class labels
            explained by each rule. Return the explanations (solutions).
        """
        self.data = X
        self.labels = y

        self.positives = []
        for i in range(len(self.labels)):
            if self.labels[i] == 1:
                self.positives.append(i)
        log.info("")
        log.info("Positives: " + str(len(self.positives)))

        log.info("")
        log.info("Rules from trees")
        self.candidate_rules = self.random_forest.get_rules(data=self.data)
        self.candidate_rules = [
            r for r in self.candidate_rules if len(r.decision_rule) > 0
        ]
        self.solution_rules: List[Rule] = []
        log.info(str(len(self.candidate_rules)) + " candidate rules")

        log.info("Deduping")
        self.candidate_rules = self._deduplicate(self.candidate_rules)
        self.solution_rules = self._deduplicate(self.solution_rules)
        log.info(str(len(self.candidate_rules)) + " candidate rules")

        self._generate_solutions()

        log.info("Simplifying Solutions")
        self.solution_rules = self._shorten(self.solution_rules)
        self.solution_rules = self._deduplicate(self.solution_rules)
        log.info(str(len(self.solution_rules)) + " solutions")

        self.longer_rules = [r for r in self.solution_rules]

        # log.info("")
        # log.info("Removing subset rules")
        # self._remove_subset_rules()
        # log.info(str(len(self.solution_rules)) + " solutions")

        log.info("")
        log.info("Set Cover")
        total_support: List[int] = []
        for r in self.solution_rules:
            total_support = list(set(total_support).union(set(r.decision_support)))
        self._rules_to_cover_positives(
            list(set(total_support).intersection(set(self.positives)))
        )
        log.info(str(len(self.solution_rules)) + " rules found")

        return self.solution_rules

    def _rules_to_cover_positives(self, positives: List[int]) -> None:
        """
        A method to select rules with high coverage using a
        greedy set cover on the set of positive class labels
        explained by each rule.
        """
        original_rules = {}
        positive_coverage = {}
        for r in self.solution_rules:
            positive_coverage[str(r)] = list(
                set(positives).intersection(set(r.decision_support))
            )
            original_rules[str(r)] = r

        selected_rules: List[Rule] = []
        covered_positives: List[int] = []

        while (len(covered_positives) < len(positives)) and (
            len(selected_rules) < len(self.solution_rules)
        ):
            max_coverage_rule = list(positive_coverage.keys())[0]
            for rule in list(positive_coverage.keys()):
                if len(positive_coverage[rule]) > len(
                    positive_coverage[max_coverage_rule]
                ):
                    max_coverage_rule = rule
                else:
                    if len(positive_coverage[rule]) == len(
                        positive_coverage[max_coverage_rule]
                    ):
                        if len(original_rules[rule].decision_rule) < len(
                            original_rules[max_coverage_rule].decision_rule
                        ):
                            max_coverage_rule = rule
            """
            scores = self._score_rule_using_data(
                original_rules[max_coverage_rule], self.labels
                )
            avg_score = 0.0
            if len(scores) > 0:
                avg_score = sum(scores) / len(scores)

            print(
                int(len(set(self.positives).intersection(set(original_rules[max_coverage_rule].decision_support)))/len(set(self.positives))*100*10)/10,
                int(avg_score*100*10)/10,
                max_coverage_rule
                )
            """
            selected_rules.append(original_rules[max_coverage_rule])
            new_covered_positives = positive_coverage[max_coverage_rule]
            covered_positives = list(
                set(covered_positives).union(set(new_covered_positives))
            )

            for rule in list(positive_coverage.keys()):
                positive_coverage[rule] = list(
                    set(positive_coverage[rule]).difference(set(new_covered_positives))
                )
                if len(positive_coverage[rule]) == 0:
                    positive_coverage.pop(rule)

        self.solution_rules = selected_rules

    def _generate_solutions(self) -> None:
        """
        A method to generate explanations (solutions) in
        stages 1 to n = num trees in the tree ensemble:

        1) In stage 1, candidates = rules from tree in tree ensemble (stage 0)
            When stage > 1, for generating candidates rules for cross tree
            interactions beyond rules from a single tree, generate candidates
            for the next stage by combining rules from k tree combinations
            to get rules for k + 1 tree combinations.
        2) Filter candidates to check if it explains any positive class prediction. If
            a rule does not explain any positive class prediction, it can be discarded.
        3) Filter the candidates to check if the rules qualifies to be an explanation.
            Does it have sufficient precision? If it does, it can be promoted to
            a list of explanations (solutions).
        4) Prune candidates to keep only those which have unexplained positives
            in their support
        5) Deduplicate candidate and solution rules generated from multiple
            source trees and combine the sources into the rule's identity.
        """
        log.info("")
        log.info("Running Apriori")
        log.info("")

        self.positives_to_explain = self.positives
        for stage in range(self.num_stages):
            if len(self.positives_to_explain) == 0:
                continue

            log.info("")

            log.info("Rules from " + str(stage + 1) + " trees")

            new_candidates = []
            new_solutions = []
            if stage == 0:
                for i in tqdm(range(len(self.candidate_rules))):
                    r = self.candidate_rules[i]
                    is_solution, keep_candidate = self._filter_candidates(
                        r, self.labels
                    )
                    if is_solution is True:
                        new_solutions.append(r)
                    if keep_candidate is True:
                        new_candidates.append(r)
            else:
                join_indices = self._get_join_indices(self.candidate_rules)
                for i, j in tqdm(join_indices):
                    joined_rule = self.candidate_rules[i].join(self.candidate_rules[j])
                    if joined_rule is not None:
                        is_solution, keep_candidate = self._filter_candidates(
                            joined_rule, self.labels
                        )
                        if is_solution is True:
                            new_solutions.append(joined_rule)
                        if keep_candidate is True:
                            new_candidates.append(joined_rule)

            self.candidate_rules = new_candidates
            self.solution_rules = self.solution_rules + new_solutions
            log.info(str(len(self.candidate_rules)) + " candidates")
            log.info(str(len(self.solution_rules)) + " solutions")

            # log.info("Removing subset rules")
            # self._remove_subset_rules()
            # log.info(str(len(self.solution_rules)) + " solutions")

            for rule in new_solutions:
                self.positives_to_explain = list(
                    set(self.positives_to_explain).difference(
                        set(rule.decision_support)
                    )
                )

            log.info("Unexplained Positives")
            log.info(len(self.positives_to_explain))

            log.info("Pruning Candidates")
            self.candidate_rules = self._prune(
                self.candidate_rules, self.positives_to_explain
            )
            log.info(str(len(self.candidate_rules)) + " candidates")

            log.info("Deduping")
            self.candidate_rules = self._deduplicate(self.candidate_rules)
            self.solution_rules = self._deduplicate(self.solution_rules)
            log.info(str(len(self.candidate_rules)) + " candidates")
            log.info(str(len(self.solution_rules)) + " solutions")

            fidelity, fidelity_positives, fidelity_negatives = self.get_fidelity()

            log.info("Fidelity")
            log.info(
                "Total: "
                + f"{fidelity:.6f}"
                + ", Positive: "
                + f"{fidelity_positives:.6f}"
                + ", Negative: "
                + f"{fidelity_negatives:.6f}"
            )
            log.info("")

    def _remove_subset_rules(
        self,
    ) -> None:
        """
        A method to remove rules whose support is fully contained
        in the support of another rule.
        """
        for runs in range(2):
            invalid = [True] * len(self.solution_rules)
            for i in range(len(self.solution_rules)):
                rule_i = self.solution_rules[i]
                for j in range(i + 1, len(self.solution_rules)):
                    rule_j = self.solution_rules[j]
                    if set(rule_j.decision_support).issubset(
                        set(rule_i.decision_support)
                    ):
                        invalid[j] = False

            valid_rules = []
            for i in range(len(self.solution_rules)):
                if invalid[i] is True:
                    valid_rules.append(self.solution_rules[i])

            valid_rules.reverse()
            self.solution_rules = valid_rules
        return

    def _score_rule_using_data(self, rule: Rule, labels: List[int]) -> List[int]:
        """
        A method to score all rules using the data in their
        support and their corresponding labels predicted by
        the tree ensemble model. This method returns list of
        class labels of the data satisfied by the rule.
        """
        decision_value = []
        for data_index in rule.decision_support:
            decision_value.append(labels[data_index])
        return decision_value

    """
    def score_rule_using_model(self, rule: Rule) -> Tuple[float, float]:
        min_score, max_score = self.random_forest.get_rule_score(rule.decision_rule)
        return min_score, max_score
    """

    def _filter_candidates(self, rule: Rule, labels: List[int]) -> Tuple[bool, bool]:
        """
        A method to filter candidates to check if they are explanations
        (solutions) with rule precision > min_precision.
        a) Filter candidates to check if it explains any positive class
            prediction. If a rule does not explain any positive class
            prediction, it can be discarded.
        b) Filter the candidates to check if the rules qualifies to be an
            explanation. Does it have sufficient precision? If it does,
            it can be promoted to a list of explanations (solutions).
        """
        scores = self._score_rule_using_data(rule, labels)
        max_score = 0.0
        avg_score = 0.0
        if len(scores) > 0:
            max_score = max(scores)
            avg_score = sum(scores) / len(scores)

        min_precision = avg_score

        if min_precision >= self.min_precision:
            # solution
            # throw candidate: it is already a solution
            is_solution = True
            keep_candidate = False
            return is_solution, keep_candidate
        else:
            # not solution
            is_solution = False
            if max_score == 0:
                # throw candidate: it cannot become a solution
                keep_candidate = False
                return is_solution, keep_candidate
            else:
                # keep candidate: it can become a solution
                keep_candidate = True
                return is_solution, keep_candidate

    def get_fidelity(self, use_top: Optional[int] = None) -> Tuple[float, float, float]:
        """
        A method to compute fidelity of the rule list.
        Fidelity is defined as the fraction of data on which the
        explanation (rule list) agrees with the tree ensemble.
        This method returns the fidelity on the overall data,
        data with positive class predictions and negative class
        predictions, respectively by the tree ensemble model.
        """
        if use_top is None:
            use_top = len(self.solution_rules)

        support: Set[int] = set()
        for i in range(use_top):
            r = self.solution_rules[i]
            support = support.union(set(r.decision_support))

        y_pred_rules = [0] * len(self.labels)
        for s in support:
            y_pred_rules[s] = 1

        fidelity_positives = 0.0
        fidelity_negatives = 0.0
        positives = 0.0 + 1e-6
        negatives = 0.0 + 1e-6
        for i in range(len(self.labels)):
            if self.labels[i] == 1:
                positives = positives + 1
                if y_pred_rules[i] == self.labels[i]:
                    fidelity_positives = fidelity_positives + 1
            if self.labels[i] == 0:
                negatives = negatives + 1
                if y_pred_rules[i] == self.labels[i]:
                    fidelity_negatives = fidelity_negatives + 1

        return (
            (fidelity_positives + fidelity_negatives) / (positives + negatives),
            fidelity_positives / positives,
            fidelity_negatives / negatives,
        )

    def _deduplicate(self, rules: List[Rule]) -> List[Rule]:
        """
        A method to deduplicate rules generated from multiple
        source trees and combine the sources into the rule's identity.
        """
        rules_map = {}
        for i in range(len(rules)):
            key = str(rules[i])
            if key not in rules_map:
                rules_map[key] = rules[i]
            else:
                rules_map[key].identity = list(
                    set(rules_map[key].identity).union(set(rules[i].identity))
                )

        dedup_rules = [rules_map[r] for r in rules_map]
        return dedup_rules

    def _shorten(self, rules: List[Rule]) -> List[Rule]:
        """
        A method to shorten the rules by dropping redundant
        terms to make the rules shorter.
        Example:
        "f1 < 10 and f1 < 5" is shortened to "f1 < 5"
        """
        for i in range(len(rules)):
            pred_dict = {}
            for pred in rules[i].decision_rule:
                f, op, val = pred.split()
                # determine direction of op
                op_type = "equal"
                if op in ("<", "<="):
                    op_type = "less than"
                elif op in (">", ">="):
                    op_type = "greater than"
                # store value if haven't seen (f, op_type)
                if (f, op_type) not in pred_dict:
                    pred_dict[(f, op_type)] = (op, val)
                # otherwise, combine rules
                else:
                    old_op, old_val = pred_dict[(f, op_type)]
                    if (old_op == "<=" and op == "<" and val == old_val) or (
                        old_op == ">=" and op == ">" and val == old_val
                    ):
                        pred_dict[(f, op_type)] = (op, val)
                    elif (op_type == "less than" and val < old_val) or (
                        op_type == "greater than" and val > old_val
                    ):
                        pred_dict[(f, op_type)] = (op, val)
            # make shorter rule from predicate list
            final_rule = []
            for f, _ in pred_dict:
                op, val = pred_dict[(f, _)]
                final_rule.append((" ").join([f, op, val]))
            rules[i].decision_rule = final_rule
        return rules

    def apply(self, df: pd.DataFrame) -> List[int]:
        """
        A method to apply rules found by the explain() method
        on a given pandas dataframe. Any data that satisfies at least
        one rule from the rule list found by the explain() is labelled
        as belonging to the positive class. All other data is labelled
        as belonging to the negative class.

        This method can only be called after calling the explain()
        method. Otherwise, it throws AttributeError.
        """
        if not hasattr(self, "solution_rules"):
            raise AttributeError(
                "rules to explain the tree ensemble are not set. "
                + "Call explain() before calling apply()"
            )
        coverage: Set[int] = set()
        for r in self.solution_rules:
            support = df.query(str(r)).index.tolist()
            coverage = coverage.union(set(support))

        y_rules: List[int] = [0] * len(df)
        for i in coverage:
            y_rules[i] = 1

        return y_rules

    def _get_join_indices(self, rules: List[Rule]) -> List[Tuple[int, int]]:
        """
        A method to generate index pairs from a given list of rules such that
        the rules from coressponding indices can be joined to become candidates
        for the next stage.

        In each stage, the candidate rules are formed by performing a conjunction
        of all possible k-tree combinations. The source trees from which the rules
        are formed is stored in the rule's identity.

        This method finds indices i, j such that conjunction of k-tree rules
        rule[i] and rule[j] gives a rule from a (k+1)-tree combination

        Example: rules from 3-tree combinations:
        identity of rule[i]: ["0_1,1_1,2_0", "0_1,1_3,2_1"]
        identity of rule[j]: ["1_1,2_0,3_0", "1_3,2_1,3_1"]
        identity of conjunction of rule[i] and rule[j]:
        ["0_1,1_1,2_0,3_0", 0_1,1_3,2_1,3_1"]

        Note that for a conjunction of k-tree rules to result in a (k+1)-tree
        rule, suffix of some identity of rule[i] must be same as prefix of
        some identity of rule[j].
        """
        for i in range(len(rules)):
            rules[i].create_identity_map()

        left_map: Dict[str, List[int]] = {}
        right_map: Dict[str, List[int]] = {}
        for i in range(len(rules)):
            left_keys = list(rules[i].left_identity_map.keys())
            for j in range(len(left_keys)):
                if left_keys[j] not in left_map:
                    left_map[left_keys[j]] = []
                left_map[left_keys[j]].append(i)

            right_keys = list(rules[i].right_identity_map.keys())
            for j in range(len(right_keys)):
                if right_keys[j] not in right_map:
                    right_map[right_keys[j]] = []
                right_map[right_keys[j]].append(i)

        join_keys = list(set(left_map.keys()).intersection(set(right_map.keys())))

        pairs = set()
        count_all = 0
        count_valid = 0
        for i in range(len(join_keys)):
            for j in left_map[join_keys[i]]:
                for k in right_map[join_keys[i]]:
                    join_status = True

                    # Joins in stage 2
                    if join_keys[i] == "":
                        identity_left = [
                            int(x.split("_")[0])
                            for x in self.candidate_rules[j].identity
                        ]
                        identity_right = [
                            int(x.split("_")[0])
                            for x in self.candidate_rules[k].identity
                        ]
                        if min(identity_left) < max(identity_right):
                            join_status = True
                        else:
                            join_status = False

                    if (j != k) and ((j, k) not in pairs) and (join_status is True):
                        count_all = count_all + 1

                        support_j = set(self.candidate_rules[j].decision_support)
                        support_k = set(self.candidate_rules[k].decision_support)
                        support_intersection_jk = support_j.intersection(support_k)
                        pos_support_intersection_jk = (
                            support_intersection_jk.intersection(
                                set(self.positives_to_explain)
                            )
                        )
                        support_union_jk = support_j.union(support_k)
                        jaccard_similarity_score = len(support_intersection_jk) / len(
                            support_union_jk
                        )
                        if len(pos_support_intersection_jk) > 0:
                            if (jaccard_similarity_score > 0) and (
                                jaccard_similarity_score <= self.jaccard_threshold
                            ):
                                pairs.add((j, k))
                                count_valid = count_valid + 1

        log.info("Using only " + str(int(count_valid / count_all * 100)) + "% pairs")
        log.info("Using only " + str(int(len(pairs) / count_all * 100)) + "% pairs")

        pairs_list = list(pairs)
        # pairs_list.sort()  # can be removed
        return pairs_list

    def _prune(self, rules: List[Rule], positives: List[int]) -> List[Rule]:
        """
        A method to choose rules which have unexplained positives in their support.
        """
        pruned_rules = []
        for i in range(len(rules)):
            decision_support_positive = list(
                set(rules[i].decision_support).intersection(set(positives))
            )

            if len(decision_support_positive) > 0:
                pruned_rules.append(rules[i])

        return pruned_rules
