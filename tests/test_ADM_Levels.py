import pytest
from ADM import ADM_Levels


class Test_TestMilIndexRequirements:
    def test_get_required_maintenance(self):
        assert False


class Test_Basic:

    @pytest.mark.xfail(reason="Don't know what to do")
    def test_calc_industrial_adm(self):
        a_system = ADM_Levels.SystemSovLevel()
        a_system.is_capital = True
        a_system.name = "UTY"
        a_system.calc_industrial_ADM_from_statistics(100, 3, 6)
        print(a_system.actualADM)
        assert False

    @pytest.mark.xfail(reason="Don't know what to do")
    def test_get_system_output(self):
        a_system = ADM_Levels.SystemSovLevel()
        a_system.is_capital = True
        a_system.name = "UTY"
        a_system.calc_industrial_ADM_from_statistics(100, 3, 5.5)
        print(a_system.get_industrial_mining_output_of_system())
        assert False
#
#
# class Test_TestSystemSovLevel():
#
#     ht.given(ActualADM = st.floats(min_value=1.0, max_value=6.0), DaysHeld = st.integers(min_value=0, max_value=101), RatsKilled = st.integers(min_value=0, max_value=8002), MinedAmount = st.integers(min_value= 0, max_value= max([i.value for i in ADM_Levels.IndIndexRequirements])+1))
#     def test_calc_industrial_adm_from_statistics(self,ActualADM, DaysHeld, RatsKilled, MinedAmount):
#         a_system = ADM_Levels.SystemSovLevel()
#
#         a_system.calc_industrial_ADM_from_statistics(RatsKilled,DaysHeld, ActualADM)
#         ht.assume(a_system.actualADM >= a_system.ADM)
#
#
#
#         assert False
#
#     ht.given(attainedval = st.integers(min_value=0, max_value=6))
#     def test_get_index(self):
#         assert False
#
#     def test_get_is_capital_index(self):
#         """
#         Tests that the is capital index is 2.0
#         :return:
#         """
#         assert ADM_Levels.CapitalIndex == 2.0
