import tkinter as tk
import numpy as np
from tkinter import simpledialog


class JogoVetores:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo Vetores Ortonormais")

        # Configuração do canvas
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Vetores ortonormais iniciais
        self.e1 = np.array([1, 0], dtype=float)
        self.e2 = np.array([0, 1], dtype=float)

        # Ponto inicial
        self.ponto = np.array([200, 200], dtype=float)
        self.ponto_id = self.canvas.create_oval(self.ponto[0] - 5, self.ponto[1] - 5, self.ponto[0] + 5,
                                                self.ponto[1] + 5, fill="blue")

        # Conectar teclas ao movimento
        self.root.bind('<Up>', self.mover)
        self.root.bind('<Down>', self.mover)
        self.root.bind('<Left>', self.mover)
        self.root.bind('<Right>', self.mover)

        # Adicionar botões para inserir, ortogonalizar vetores e inverter direção
        self.btn_inserir_vetor = tk.Button(self.root, text="Inserir Vetor", command=self.inserir_vetor)
        self.btn_inserir_vetor.pack()

        self.btn_ortogonalizar = tk.Button(self.root, text="Ortogonalizar", command=self.ortogonalizar_vetores)
        self.btn_ortogonalizar.pack()

        self.btn_inverter = tk.Button(self.root, text="Inverter Direção", command=self.inverter_direcao)
        self.btn_inverter.pack()

        self.vetores = []

    def mover(self, event):
        if event.keysym == 'Up':
            self.ponto -= self.e2 * 10  # Mover na direção do vetor e2
        elif event.keysym == 'Down':
            self.ponto += self.e2 * 10  # Mover na direção oposta do vetor e2
        elif event.keysym == 'Left':
            self.ponto -= self.e1 * 10  # Mover na direção oposta do vetor e1
        elif event.keysym == 'Right':
            self.ponto += self.e1 * 10  # Mover na direção do vetor e1

        # Limitar o ponto à área de 400x400 pixels
        self.ponto = np.clip(self.ponto, 0, 400)

        # Atualizar a posição do ponto no canvas
        self.canvas.coords(self.ponto_id, self.ponto[0] - 5, self.ponto[1] - 5, self.ponto[0] + 5, self.ponto[1] + 5)

    def inserir_vetor(self):
        coords = simpledialog.askstring("Inserir Vetor", "Insira as coordenadas do vetor separadas por vírgula:")
        if coords:
            vetor = np.array(list(map(float, coords.split(','))), dtype=float)
            self.vetores.append(vetor)
            self.desenhar_vetores()

    def ortogonalizar_vetores(self):
        vetores_ortogonais = self.gram_schmidt(self.vetores)
        self.vetores = vetores_ortogonais
        if len(vetores_ortogonais) >= 2:
            self.e1 = vetores_ortogonais[0]
            self.e2 = vetores_ortogonais[1]
        self.desenhar_vetores()

    def inverter_direcao(self):
        # Inverter as direções dos vetores ortonormais
        self.e1 = -self.e1
        self.e2 = -self.e2
        self.desenhar_vetores()

    def gram_schmidt(self, vetores):
        vetores_ortogonais = []
        for v in vetores:
            w = v - sum(np.dot(v, u) / np.dot(u, u) * u for u in vetores_ortogonais)
            if np.linalg.norm(w) > 1e-10:  # Ignorar vetores ortogonais nulos
                vetores_ortogonais.append(w)
        return vetores_ortogonais

    def desenhar_vetores(self):
        self.canvas.delete("vetor")
        for vetor in self.vetores:
            self.canvas.create_line(200, 200, 200 + vetor[0] * 50, 200 - vetor[1] * 50, arrow=tk.LAST, fill="red",
                                    tags="vetor")


# Classe Main para iniciar o jogo
class Main:
    def run(self):
        root = tk.Tk()
        jogo = JogoVetores(root)
        root.mainloop()


if __name__ == "__main__":
    main = Main()
    main.run()
