import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Vetor:
    def __init__(self, coordenadas):
        self.coordenadas = np.array(coordenadas)

    def produto_interno(self, outro):
        return np.dot(self.coordenadas, outro.coordenadas)

    def norma(self):
        return np.linalg.norm(self.coordenadas)

    def projecao(self, outro):
        norma_outro = outro.produto_interno(outro)
        if norma_outro == 0:
            return np.zeros_like(self.coordenadas)
        return (self.produto_interno(outro) / norma_outro) * outro.coordenadas

    def normalizar(self):
        return self.coordenadas / self.norma()

    def __repr__(self):
        return f"Vetor({self.coordenadas})"


class GramSchmidt:
    def __init__(self, lista_vetores):
        self.lista_vetores = [Vetor(v) for v in lista_vetores]
        self.lista_vetores_ortogonais = self.ortogonalizar()
        self.lista_vetores_ortonormais = self.ortonormalizar()

    def ortogonalizar(self):
        lista_vetores_ortogonais = []
        for u in self.lista_vetores:
            v = u.coordenadas
            for v_ortogonal in lista_vetores_ortogonais:
                proj = Vetor(v).projecao(Vetor(v_ortogonal))
                v = v - proj
            lista_vetores_ortogonais.append(v)
        return lista_vetores_ortogonais

    def ortonormalizar(self):
        return [Vetor(v).normalizar() for v in self.lista_vetores_ortogonais]


class Visualizacao:
    def __init__(self, vetor_original, vetor_ortogonal, vetor_ortonormal):
        self.vetor_original = vetor_original
        self.vetor_ortogonal = vetor_ortogonal
        self.vetor_ortonormal = vetor_ortonormal

    def plot_vectors_2d(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        for i, vector in enumerate(self.vetor_original):
            ax.quiver(0, 0, vector[0], vector[1], angles='xy', scale_units='xy', scale=1, color=colors[i % len(colors)],
                      label=f'v{i + 1}')
        for i, vector in enumerate(self.vetor_ortogonal):
            if not (vector == [0., 0.]).all():
                ax.quiver(0, 0, vector[0], vector[1], angles='xy', scale_units='xy', scale=1, color='orange',
                          label=f'u{i + 1} ortogonal')
            else:
                print(f"O vetor {i + 1} na base ortogonal é um vetor nulo e não será plotado.")
        for i, vector in enumerate(self.vetor_ortonormal):
            ax.quiver(0, 0, vector[0], vector[1], angles='xy', scale_units='xy', scale=1, color='purple',
                      label=f'e{i + 1} ortonormal')
        ax.legend()
        plt.show()

    def animate_gram_schmidt(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        lines = []
        projections = []
        for i, vec in enumerate(self.vetor_original):
            line, = ax.plot([], [], color=colors[i % len(colors)], label=f'v{i + 1}')
            lines.append(line)

        projection, = ax.plot([], [], '--o', color='orange', label='projeção')
        projections.append(projection)

        lista_vetores_ortogonais = []

        def update(frame):
            if frame >= len(self.vetor_original):
                return lines + projections

            u = self.vetor_original[frame]
            v = u
            for v_ortogonal in lista_vetores_ortogonais:
                norma_v_ortogonal = np.dot(v_ortogonal, v_ortogonal)
                if norma_v_ortogonal != 0:
                    v = v - np.dot(u, v_ortogonal) / norma_v_ortogonal * v_ortogonal

            if frame > 0 and len(lista_vetores_ortogonais) > 0:
                projections[0].set_data([0, lista_vetores_ortogonais[-1][0]], [0, lista_vetores_ortogonais[-1][1]])

            lines[frame].set_data([0, v[0]], [0, v[1]])
            lista_vetores_ortogonais.append(v)
            ax.legend()
            return lines + projections

        anim = FuncAnimation(fig, update, frames=len(self.vetor_original) + 1, blit=True, interval=1000)
        plt.show()


class Main:
    def __init__(self):
        self.num_vectors = 0
        self.vectors = []

    def run(self):
        self.num_vectors = int(input("Insira a quantidade de vetores que deseja analisar: "))
        for i in range(self.num_vectors):
            vec_str = input(f"Insira as coordenadas do vetor {i + 1} separadas por vírgula: ")
            vec = np.array(list(map(float, vec_str.split(','))))
            self.vectors.append(vec)

        gs = GramSchmidt(self.vectors)

        print("\nBase ortogonal:")
        for i, v in enumerate(gs.lista_vetores_ortogonais):
            print(f"u{i + 1} = {v}")

        print("\nBase ortonormal:")
        for i, v in enumerate(gs.lista_vetores_ortonormais):
            print(f"e{i + 1} = {v}")

        if self.num_vectors == 2:
            viz = Visualizacao(self.vectors, gs.lista_vetores_ortogonais, gs.lista_vetores_ortonormais)
            viz.plot_vectors_2d()
            viz.animate_gram_schmidt()
        else:
            print("\nA visualização 2D só é feita para 2 vetores.")


# Exemplo de uso
if __name__ == "__main__":
    main = Main()
    main.run()
