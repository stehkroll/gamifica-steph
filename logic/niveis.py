# logic/niveis.py

def calcular_nivel(xp_total):
    nivel = 1
    xp_necessario = 100
    while xp_total >= xp_necessario and nivel < 99:
        xp_total -= xp_necessario
        nivel += 1
        xp_necessario += 10
    progresso = xp_total / xp_necessario
    return nivel, progresso, xp_necessario
