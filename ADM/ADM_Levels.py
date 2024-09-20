from enum import Enum


# References for numbers are located here https://zeronin.de/sovereignty/

class SovIndexLeveltoADM(Enum):
    Zero = 0.0
    One = 0.4
    Two = 0.6
    Three = 0.8
    Four = 0.9
    Five = 1.0


class IndMilIndexLeveltoADM(Enum):
    Zero = 0.0
    One = 0.6
    Two = 1.2
    Three = 1.7
    Four = 2.1
    Five = 2.5


class IntToStr(Enum):
    Zero = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5


BaseIndex = 1.0
CapitalIndex = 2.0


class MilIndexRequirements(Enum):
    Zero = 0
    One = 500
    Two = 1000
    Three = 2000
    Four = 4000
    Five = 8000

    @staticmethod
    def get_required_maintenance(level: Enum):
        """
        Converts whatever level into
        :param level:
        :return:
        """
        return level.value / 2


class IndIndexRequirements(Enum):
    Zero = 0
    One = 1500000 * 2 ** 0
    Two = 1500000 * 2 ** 1
    Three = 1500000 * 2 ** 2
    Four = 1500000 * 2 ** 3
    Five = 1500000 * 2 ** 4

    @staticmethod
    def get_required_maintenance(level: Enum):
        """
        Converts whatever level into
        :param level:
        :return:
        """
        return level.value / 2


class SovIndexRequirements(Enum):
    Zero = 0
    One = 7
    Two = 21
    Three = 35
    Four = 65
    Five = 100


def get_index_score(SovIndexLeveltoADM: Enum, name):
    return getattr(SovIndexLeveltoADM,name).value


class SystemSovLevel:
    def __init__(self):
        self.is_capital = False
        self.SovIndexADM: float = 0.0
        self.MilIndexADM: float = 0.0
        self.IndIndex: float = 0.0
        self.actualADM = 1.0
        self.ADM: float = 1.0
        self.IsSovIndexSaturated = False

    def calc_industrial_ADM_from_statistics(self, rat_kills_system: int, days_held: int, actualADM: float) -> None:
        """

        :param rat_kills_system: Returned from another function, gives the estimated rat kills in system
        :param days_held: Gives the days held by alliance
        :param actualADM: the actual ADM
        :return:
        """
        self.MilIndexADM = self.get_index(self.calculate_mil_index(rat_kills_system), MilIndexRequirements, IndMilIndexLeveltoADM)
        self.SovIndexADM = self.get_index(self.calculate_sov_index(days_held), SovIndexRequirements, SovIndexLeveltoADM)
        self.ADM = BaseIndex + self.get_is_capital_index() + self.MilIndexADM + self.SovIndexADM
        self.actualADM = actualADM

        diff = self.actualADM - self.ADM # it will always be positive or zero

        # If the diff is not 0, set IndIdex to 0.0
        if diff == 0:
            self.IndIndex = 0.0
            return None
        # If the diff is bigger than the max Index ADM possible, return error
        if diff > 2.5:
            raise ValueError(f'Diff {diff} value is too high!  ADM Calculation Not possible!')
        # If the ADM is so high that the difference between the calculated ADM components and the max ADM possible is less than the max industry index ADM:
        if self.actualADM == 6 and self.ADM + 2.5 > 6 :
            self.IsSovIndexSaturated = True

        self.IndIndex = diff
        return None

    def get_industrial_mining_output_of_system(self):
        for i in IndMilIndexLeveltoADM:
            if self.IndIndex < i.value:
                return getattr(IndIndexRequirements,i.name)


    @staticmethod
    def get_index(attained_value : int,
                  IndexScoreLookup : Enum,
                  IndexRequirements : Enum) -> float:
        """
        Retrieves the estimated Sov Index Level based on the time the current holding alliance has held it for
        :param days_held:
        :return: Score of the index
        """
        score = 0
        for i in IndexRequirements:
            if attained_value < i.value:
                return score
            score = get_index_score(IndexScoreLookup, i.name)


    def get_is_capital_index(self) -> float:
        """
        Returns the capital index score
        :return: float
        """
        return float(self.is_capital * CapitalIndex)

    def calculate_mil_index(self, rat_kills_system):
        score = 0
        for i in MilIndexRequirements:
            if rat_kills_system < i.value:
                return score
            score = get_index_score(IndMilIndexLeveltoADM,i.name)

    def calculate_sov_index(self, days_held):
        score = 0
        for i in SovIndexRequirements:
            if days_held < i.value:
                return score
            score = get_index_score(SovIndexLeveltoADM, i.name)


