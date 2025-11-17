import unittest
from src.core.prototype import Prototype
from src.logics.prototype_report import PrototypeReport
from src.singletons.start_service import StartService
from src.singletons.repository import Repository
from src.core.exceptions import OperationException
class TestPrototype(unittest.TestCase):
    def test_any_test_prototype_filter(self):



        start=StartService()
        start.start()
        start_prototype = PrototypeReport(start.__repository.transactions_key)
        nomenclatures=Repository.data[Repository.nomencluture_key]
        if len(nomenclatures)==0:
            raise OperationException("List is Empty")
        first_nomenclature = nomenclatures(0)
        next_prototype=start_prototype.filter_by_nomenclature

        assert len(next_prototype.data)>0
        assert len(start_prototype.data)>0
        assert len(start_prototype.data)>=len(next_prototype.data)
    def test_my_prototype_filter(self):
        start=StartService()
        start.start()
        start_prototype = PrototypeReport(start.__repository.nomenclatures_key)
        nomenclatures=start.pro
        if len(nomenclatures)==0:
            raise OperationException("List is Empty")
        first_nomenclature = nomenclatures(0)
        


        
        next_prototype=start_prototype.filter()

        assert len(next_prototype.data)>0
        assert len(start_prototype.data)>0
        assert len(start_prototype.data)>=len(next_prototype.data)


if __name__ == "__main__":
    unittest.main()
