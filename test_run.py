import unittest
import run

class TestRun(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        print('setUpClass')
    
    @classmethod
    def tearDownClass(self):
        print('tearDownClass')
    
    def setUp(self):
        print('setUp')
    
    def tearDown(self):
        print('tearDown\n')
    
    def test_listaT(self):
        print("test_listaT")
        result = run.listaT(6)
        self.assertIsNotNone(result, "None")
        print("---- end test ----")
        
    def test_generacionLista(self):
        print("test_generacionLista")
        result = run.listaT(10)
        self.assertListEqual(result, [1,2,3,4,5,6,7,8,9])
        print("---- end test ----")
    
    def test_listaVacia(self):
        print("test_listaVacia")
        self.assertRaises(ValueError, run.listaT, 0)
        print("---- end test ----")
        
    def test_crearCSV(self):
        print("test_crearCSV")
        self.assertRaises(ValueError, run.escribirCSV, "", "", "")
        print("---- end test ----")

if __name__ == '__main__':
    unittest.main()