def calcular_nivel(pontos):
    xp_total = pontos
    nivel = 1
    xp_necessario = 100

    while xp_total >= xp_necessario and nivel < 99:
        xp_total -= xp_necessario
        nivel += 1
        xp_necessario = int(xp_necessario * 1.1)

    xp_atual = xp_total
    progresso = int((xp_atual / xp_necessario) * 100)

    return nivel, xp_atual, xp_necessario, progresso
