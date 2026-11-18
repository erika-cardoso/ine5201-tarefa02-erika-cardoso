import unittest

import calculadora_gui


class TesteCalculadora(unittest.TestCase):
    def test_operacao_simples(self):
        self.assertEqual(calculadora_gui.avaliar_expressao("5+2"), 7)

    def test_precedencia(self):
        self.assertEqual(calculadora_gui.avaliar_expressao("3*2+1"), 7)

    def test_operadores_consecutivos(self):
        with self.assertRaises(ValueError):
            calculadora_gui.avaliar_expressao("5++2")

    def test_divisao_por_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculadora_gui.avaliar_expressao("8/0")

    def test_formatacao_inteira(self):
        self.assertEqual(calculadora_gui.formatar_resultado(7.0), "7")


if __name__ == "__main__":
    unittest.main()
