import numpy as np
import pandas as pd


def div_to_prob(numerator, denominator):
    return np.where(denominator == 0, 1, numerator / denominator)


def div_check_zero(numerator, denominator):
    return np.where(denominator == 0, np.inf, numerator / denominator)


class InterestMeasures:
    _function_registry = []

    def _init__(self, A, B, AB, N):
        """
        Initializes an Interest Measures.

        :param A: A list representing the probabilities for events in A. List or numpy array.
        :param B: A list representing the probabilities for events in B. List or numpy array.
        :param AB: A list representing the probabilities for events in AB. List or numpy array.
        :param N: An integer representing the number of transactions. Default is 10.
        :param measures: Optional. A list of measures. Default is None.
        """

        super().__init__()

        self.AB = np.array(AB).reshape(-1, 1)
        self.A = np.array(A).reshape(-1, 1)
        self.B = np.array(B).reshape(-1, 1)
        self.N = N

        self.notB = 1 - self.B  # P(~B)
        self.notA = 1 - self.A  # P(~self.A)
        self.AnotB = self.A - self.AB  # P(self.A~B)
        self.notAB = self.B - self.AB  # P(~self.AB)
        self.notAnotB = 1 - self.B - self.A + self.AB  # P(~self.A~B)
        self.B_A = div_to_prob(self.AB, self.A)  # P(B|self.A)
        self.A_B = div_to_prob(self.AB, self.B)  # P(self.A|B)
        self.B_notA = div_to_prob(self.notAB, self.notA)  # P(B|~self.A)
        self.A_notB = div_to_prob(self.AnotB, self.notB)  # P(self.A|~B)
        self.notB_notA = 1 - self.B_notA  # P(~B|~self.A)
        self.notA_notB = 1 - self.A_notB  # P(~self.A|~B)
        self.notB_A = 1 - self.B_A  # P(~B|self.A)
        self.notA_B = 1 - self.A_B  # P(~self.A|B)

    def _register_functions(self):
        for name, func in self.__class__.__dict__.items():
            if hasattr(func, '__call__') and not name.startswith('_'):
                self._function_registry.append(name)

    def wrapper(self, func):
        setattr(self, func.__name__, func)
        self._register_functions()
        return func

    def _len__(self):
        return len(self.A)

    @wrapper
    def one_way_support(self):
        return self.B_A * np.log2(self.B_A / self.B)

    def two_way_support(self):
        return self.AB * np.log2(self.AB / (self.A * self.B))

    def accuracy(self):
        return self.AB + self.notAnotB

    def added_value(self):
        return self.B_A - self.B

    def chi_square(self):
        return div_check_zero(((self.AB - (self.A * self.B)) ** 2) * self.N, self.A * self.notA * self.B * self.notB)

    def collective_strength(self):
        return (((self.AB + self.notAnotB) / ((self.A * self.B) + (self.notA * self.notB))) *
                (div_check_zero(1 - (self.A * self.B) - (self.notA * self.notB),
                                np.around((1 - self.AB - self.notAnotB), 10))))

    def complement_class_support(self):
        """
        Complement Class Support

        Negative interest measure.
        """
        return -1 * div_check_zero(self.AnotB, self.notB)

    def conditional_entropy(self):
        return (-1 * self.B_A * np.log2(self.B_A) +
                np.where(self.notB_A == 0, 0, -1 * self.notB_A * np.log2(self.notB_A)))

    def confidence(self):
        return self.B_A

    def confidence_causal(self):
        return (self.B_A + self.notA_notB) / 2

    def confirm_causal(self):
        return self.AB + self.notAnotB - (2 * self.AnotB)

    def confirm_descriptive(self):
        return self.AB - self.AnotB

    def confirmed_confidence_causal(self):
        return ((self.B_A + self.notA_notB) / 2) - self.notB_A

    def conviction(self):
        return div_check_zero(self.A * self.notB, self.AnotB)

    def correlation_coefficient(self):
        return div_check_zero(self.AB - (self.A * self.B), np.sqrt(self.A * self.B * self.notA * self.notB))

    def cosine(self):
        return self.AB / np.sqrt(self.A * self.B)

    def coverage(self):
        return self.A

    def dir(self):
        result = np.zeros(self.B.shape)

        result = np.where(np.logical_and((self.B <= 0.5), (self.B_A <= 0.5)), 0, result)

        result = np.where(
            np.logical_and(
                np.logical_and((self.B <= 0.5), (self.B_A > 0.5)), (self.B_A != 1)
            ),
            1 + (self.B_A * np.log2(self.B_A)) + (self.notB_A * np.log2(self.notB_A)),
            result,
        )

        result = np.where(
            np.logical_and(
                np.logical_and((self.B <= 0.5), (self.B_A > 0.5)), (self.B_A == 1)
            ),
            1,
            result,
        )

        result = np.where(
            np.logical_and((self.B > 0.5), (self.B_A <= 0.5)),
            1 + (1 / (self.B * np.log2(self.B) + self.notB * np.log2(self.notB))),
            result,
        )

        result = np.where(
            np.logical_and(
                np.logical_and((self.B > 0.5), (self.B_A > 0.5)), (self.B_A != 1)
            ),
            1 - ((self.B_A * np.log2(self.B_A) + self.notB_A * np.log2(self.notB_A)) / (
                    self.B * np.log2(self.B) + self.notB * np.log2(self.notB))),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((self.B > 0.5), (self.B_A > 0.5)), (self.B_A == 1)),
            1 - ((self.B_A * np.log2(self.B_A)) / (self.B * np.log2(self.B) + self.notB * np.log2(self.notB))),
            result,
        )

        result = np.where(self.B == 1, -np.inf, result)

        return result

    def _dir_for_tic(self, A, B, AB):
        B_A = np.around(AB / A, 11)
        notB = 1 - B
        notB_A = np.around(1 - B_A, 11)

        result = np.zeros(B.shape)

        result = np.where(np.logical_and((B <= 0.5), (B_A <= 0.5)), 0, result)

        result = np.where(
            np.logical_and(np.logical_and((B <= 0.5), (B_A > 0.5)), (B_A != 1)),
            1 + B_A * np.log2(B_A) + notB_A * np.log2(notB_A),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((B <= 0.5), (B_A > 0.5)), (B_A == 1)),
            1 + B_A * np.log2(B_A),
            result,
        )

        result = np.where(
            np.logical_and((B > 0.5), (B_A <= 0.5)),
            1 + (1 / (B * np.log2(B) + notB * np.log2(notB))),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((B > 0.5), (B_A > 0.5)), (B_A != 1)),
            1
            - (B_A * np.log2(B_A) + notB_A * np.log2(notB_A))
            / (B * np.log2(B) + notB * np.log2(notB)),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((B > 0.5), (B_A > 0.5)), (B_A == 1)),
            1 - (B_A * np.log2(B_A)) / (B * np.log2(B) + notB * np.log2(notB)),
            result,
        )

        result = np.where(B == 1, -np.inf, result)

        return result

    def exemple_and_counterexemple_rate(self):
        return 1 - (self.AnotB / self.AB)

    def f_measure(self):
        return (2 * self.A_B * self.B_A) / (self.A_B + self.B_A)

    def ganascia(self):
        return (2 * self.B_A) - 1

    def gini_index(self):
        return ((self.A * ((self.B_A ** 2) + (self.notB_A ** 2))) +
                (self.notA * ((self.B_notA ** 2) + (self.notB_notA ** 2))) -
                (self.B ** 2) -
                (self.notB ** 2))

    def goodman_kruskal(self):
        part1 = (
                np.max([self.AB, self.AnotB], axis=0)
                + np.max([self.notAB, self.notAnotB], axis=0)
                + np.max([self.AB, self.notAB], axis=0)
                + np.max([self.AnotB, self.notAnotB], axis=0)
                - np.max([self.A, self.notA], axis=0)
                - np.max([self.B, self.notB], axis=0)
        )

        part2 = (
                2
                - np.max([self.A, self.notA], axis=0)
                - np.max([self.B, self.notB], axis=0)
        )

        return div_check_zero(part1, part2)

    def implication_index(self):
        """
        Implication Index

        Negative interest measure.
        """
        return -1 * div_check_zero((self.AnotB - (self.A * self.notB)), np.sqrt(self.A * self.notB))

    def information_gain(self):
        return np.log2((self.AB / (self.A * self.B)))

    def jaccard(self):
        return self.AB / (self.A + self.B - self.AB)

    def j_measure(self):
        return (self.AB * np.log2(self.B_A / self.B) +
                (np.where((self.notB * self.notB_A) == 0, 0, self.AnotB * np.log2(self.notB_A / self.notB), )))

    def kappa(self):
        return div_check_zero(
            ((self.B_A * self.A) + (self.notB_notA * self.notA) - (self.A * self.B) - (self.notA * self.notB)),
            1 - (self.A * self.B) - (self.notA * self.notB))

    def klosgen(self):
        return np.sqrt(self.A) * (self.B_A - self.B)

    def k_measure(self):
        return (self.B_A * np.log2(self.B_A / self.B) +
                self.B_A * np.log2(self.B_A / self.notB) -
                np.where(self.notB_notA == 0, 0, (self.notB_notA * np.log2(self.notB_notA / self.notB))) -
                np.where(self.notB_notA == 0, 0, (self.notB_notA * np.log2(self.notB_notA / self.B))))

    def kulczynski_1(self):
        return div_check_zero(self.AB, self.AnotB + self.notAB)

    def kulczynski_2(self):
        return ((self.AB / self.A) + (self.AB / self.B)) / 2

    def laplace_correction(self):
        return (self.N * self.AB + 1) / (self.N * self.A + 2)

    def least_contradiction(self):
        return (self.AB - self.AnotB) / self.B

    def leverage(self):
        return self.B_A - (self.A * self.B)

    def lift(self):
        return self.AB / (self.A * self.B)

    def loevinger(self):
        return np.where(self.notB == 0, 0, 1 - (self.AnotB / (self.A * self.notB)))

    def logical_necessity(self):
        """
        Logical Necessity

        Negative interest measure.
        """
        return -1 * div_check_zero(self.notA_B, self.notA_notB)

    def mutual_information(self):
        return (self.AB * np.log2(self.AB / (self.A * self.B)) +
                np.where(self.AnotB == 0, 0, self.AnotB * np.log2(self.AnotB / (self.A * self.notB))) +
                np.where(self.notAB == 0, 0, self.notAB * np.log2(self.notAB / (self.notA * self.B))) +
                np.where(self.notAnotB == 0, 0, self.notAnotB * np.log2(self.notAnotB / (self.notA * self.notB))))

    def normalized_mutual_information(self):
        return div_check_zero(np.around(self._mutual_information(), 10),
                              np.where(
                                  self.A == 1,
                                  (-self.A * np.log2(self.A)),
                                  (-self.A * np.log2(self.A)) - (self.notA * np.log2(self.notA)),
                              ))

    def odd_multiplier(self):
        return div_check_zero(self.AB * self.notB, self.B * self.AnotB)

    def odds_ratio(self):
        return div_check_zero(self.AB * self.notAnotB, self.AnotB * self.notAB)

    def piatetsky_shapiro(self):
        return self.AB - (self.A * self.B)

    def prevalence(self):
        return self.B

    def putative_causal_dependency(self):
        return (((self.B_A - self.B) / 2) +
                (self.notA_notB - self.notA) -
                (self.notB_A - self.notB) -
                (self.A_notB - self.A))

    def recall(self):
        return self.A_B

    def relative_risk(self):
        return div_check_zero(self.B_A, self.B_notA)

    def sebag_schoenaure(self):
        return div_check_zero(self.AB, self.AnotB)

    def specificity(self):
        return self.notB_notA

    def support(self):
        return self.AB

    def theil_uncertainty_coefficient(self):
        return div_check_zero(np.around(self._mutual_information(), 10),
                              np.where(self.B == 1,
                                       (-self.B * np.log2(self.B)),
                                       (-self.B * np.log2(self.B)) - (self.notB * np.log2(self.notB)),
                                       ))

    def tic(self):
        part2 = np.around(self.__dir_for_tic(A=self.notB, B=self.notA, AB=self.notAnotB), 10)
        return np.where(self.B == 1, -np.inf, np.sqrt(np.around(self._dir(), 10) * part2))

    def yuleQ(self):
        return div_check_zero((self.AB * self.notAnotB) - (self.AnotB * self.notAB),
                              (self.AB * self.notAnotB) + (self.AnotB * self.notAB))

    def yuleY(self):
        return div_check_zero(np.sqrt(self.AB * self.notAnotB) - np.sqrt(self.AnotB * self.notAB),
                              np.sqrt(self.AB * self.notAnotB) + np.sqrt(self.AnotB * self.notAB))

    def zhang(self):
        part1 = self.AB - (self.A * self.B)
        part2 = np.max([self.AB * (1 - self.B), self.B * (self.A - self.AB)], axis=0)

        return div_check_zero(part1, part2)

    def modified_lift(self):
        return self.notAnotB / self.AnotB

    def dm2(self):
        return self.notAnotB / (self.AnotB * np.sqrt(self.B))

    def dm3(self):
        return (self.notAnotB * self.A) / (self.AnotB * np.sqrt(self.B))

    def dm4(self):
        self.notAnotB / (self.AnotB * np.sqrt(self.A))

