import numpy as np
import matplotlib.pyplot as plt


def calculate_cumulative_probability(num_nonces, total_nonces):
    probability_no_collision = 1
    for i in range(1, num_nonces):
        probability_no_collision *= (total_nonces - i) / total_nonces
    probability_collision = 1 - probability_no_collision
    return probability_collision

def plot_cumulative_nonce_probability():
    max_nonces = 2 ** 50
    num_points = 10
    nonces = np.linspace(0, max_nonces, num_points)
    probabilities = [calculate_cumulative_probability(int(nonce), max_nonces) for nonce in nonces]

    plt.plot(nonces, probabilities, marker='o', linestyle='-')
    plt.title('Probabilidad acumulada de repetición')
    plt.xlabel('Número de Nonces Sacados')
    plt.ylabel('Probabilidad Acumulada de Repetición de Nonce')
    plt.show()

plot_cumulative_nonce_probability()

