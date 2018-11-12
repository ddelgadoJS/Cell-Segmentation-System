import unittest
import run
import cellPostProcess


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
        self.assertListEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        print("---- end test ----")

    def test_listaVacia(self):
        print("test_listaVacia")
        self.assertRaises(ValueError, run.listaT, 0)
        print("---- end test ----")

    def test_crearCSV(self):
        print("test_crearCSV")
        self.assertRaises(ValueError, run.escribirCSV, "", "", "", [], [])
        print("---- end test ----")
        
    def test_load_test_data(self):
        print("test_load_test_data")
        self.assertRaises(ValueError, run.load_test_data, [])
        print("---- end test ----")
    
    def test_predict(self):
        print("test_predict")
        self.assertRaises(ValueError, run.predict, [])
        print("---- end test ----")
        
    def test_predictWeight(self):
        print("test_predictWeight")
        self.assertRaises(ValueError, run.predict, [])
        print("---- end test ----")
        
    def test_preprocess(self):
        print("test_preprocess")
        self.assertRaises(ValueError, run.preprocess, [])
        print("---- end test ----")
        
    # ----------------------- #
        
    def test_getCentroide(self):
        print("test_getCentroide")
        self.assertRaises(ValueError, cellPostProcess.getCellCenter, [], 0, 0)
        print("---- end test ----")
        
    def test_countCells(self):
        print("test_countCells")
        self.assertRaises(ValueError, cellPostProcess.countCells, [], 0, 0)
        print("---- end test ----")
    
    def test_paintLabel(self):
        print("test_paintLabel")
        self.assertRaises(ValueError, cellPostProcess.paintLabel, [], None, 0)
        print("---- end test ----")
    
    def test_getAproxExecTime(self):
        print("test_getAproxExecTime")
        self.assertRaises(ValueError, cellPostProcess.getApproxExecTime, [])
        print("---- end test ----")
    
    def test_getAproxExecTimeImage(self):
        print("test_getAproxExecTimeImage")
        self.assertRaises(ValueError, cellPostProcess.getApproxExecTime, "failPath.png")
        print("---- end test ----")
        
    def test_cellPostProcessImage(self):
        print("test_cellPostProcessImage")
        self.assertRaises(ValueError, cellPostProcess.cellPostProcess, "failPath.png", "failName.png", False)
        print("---- end test ----")
        
    def test_escribirCSVDatos(self):
        print("test_escribirCSVDatos")
        self.assertRaises(ValueError, run.escribirCSV, "failPath.png", 1, [], [], "failPath.png")
        print("---- end test ----")
    
    def test_paintLabelIndex(self):
        print("test_paintLabelIndex")
        self.assertRaises(IndexError, cellPostProcess.paintLabel, [0,0,0], [100], 100)
        print("---- end test ----")
        
    def test_escribirCSVDatosCapturados(self):
        print("test_escribirCSVDatosCapturados")
        self.assertRaises(ValueError, run.escribirCSV, None, None, [], [], "failPath.png")
        print("---- end test ----")
    
    def test_cellPostProcess(self):
        print("test_cellPostProcessImage")
        result, result2 = cellPostProcess.cellPostProcess("C:/Users/Kevin MM/eclipse-workspace/SegmentacionCelulas/preds/1_pred.png", "1_pred.png")
        self.assertEqual(result2, [(0, 0), (9.989672977624785, 56.07401032702241), 
                         (25.17663043478261, 139.02989130434779), (36.36567164179104, 35.5), 
                         (54.22727272727273, 1.3181818181818183), (68.45454545454545, 241.43734643734643), 
                         (95.24411134903642, 174.19914346895084), (90.3141592920354, 136.24557522123897), 
                         (107.66666666666666, 254.33333333333331), (135.1878453038674, 127.83057090239413), 
                         (131.00704225352115, 251.5140845070423), (151.60869565217394, 175.0517598343685), 
                         (154.2447325769854, 73.20907617504052), (159.4927536231884, 208.39420289855082), 
                         (182.0939947780679, 184.45430809399474), (189.18971061093248, 211.62700964630227), 
                         (192.0176470588235, 249.61764705882356), (200.09546925566343, 127.80097087378648), 
                         (203.63448275862066, 171.08965517241379), (225.69747899159665, 204.97058823529403), 
                         (236.5296912114014, 39.011084718923215), (238.8961218836565, 127.13850415512469), 
                         (251.2214285714286, 195.45000000000002), (255.0, 30.0)])
        print("---- end test ----")
    
    
    

if __name__ == '__main__':
    #unittest.main()
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='reports'))