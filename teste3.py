import tkinter as tk
import numpy as np
from tkinter import simpledialog

class Vetor:
    def __init__(self, x, y, tag):
        self._coords = np.array([x, y], dtype=float)
        self._tag = tag  # Adiciona uma tag para diferenciar os vetores

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, new_coords):
        self._coords = np.array(new_coords, dtype=float)

    @property
    def tag(self):
        return self._tag

    def girar(self, angulo):
        theta = np.radians(angulo)
        R = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        self._coords = R @ self._coords

    def ortogonal(self):
        return Vetor(-self._coords[1], self._coords[0], self._tag)

class JogoVetores:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo Vetores Ortonormais")

        # Configuração do canvas
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Vetores ortonormais iniciais
        self.e1_inicial = Vetor(0, -1, 'e1')  # Vetor inicial apontando para cima
        self.e2_inicial = Vetor(1, 0, 'e2')  # Vetor inicial ortogonal
        self.e1 = Vetor(0, -1, 'e1')  # Inicializando e1 para cima
        self.e2 = Vetor(1, 0, 'e2')  # Inicializando e2 ortogonal a e1

        # Ponto inicial
        self.ponto = Vetor(200, 200, 'mov')
        self.ponto_id = self.canvas.create_oval(
            float(self.ponto.coords[0] - 5), float(self.ponto.coords[1] - 5),
            float(self.ponto.coords[0] + 5), float(self.ponto.coords[1] + 5), fill="blue")
        self.seta_id = self.canvas.create_line(
            float(self.ponto.coords[0]), float(self.ponto.coords[1]),
            float(self.ponto.coords[0] + self.e1.coords[0] * 20),
            float(self.ponto.coords[1] + self.e1.coords[1] * 20), arrow=tk.LAST, fill="blue")

        # Conectar teclas ao movimento e rotação
        self.root.bind('<Up>', self.mover)
        self.root.bind('<Down>', self.mover)
        self.root.bind('<Left>', self.mover)
        self.root.bind('<Right>', self.mover)
        self.root.bind('<w>', self.mover)
        self.root.bind('<s>', self.mover)
        self.root.bind('<a>', self.mover)
        self.root.bind('<d>', self.mover)
        self.root.bind('<j>', self.girar_vetor)
        self.root.bind('<k>', self.girar_vetor)

        # Adicionar botões para inserir, ortogonalizar vetores, girar e resetar a base
        self.btn_inserir_vetor1 = tk.Button(self.root, text="Inserir Vetor 1",
                                            command=lambda: self.inserir_vetor('vetor1'))
        self.btn_inserir_vetor1.pack()

        self.btn_inserir_vetor2 = tk.Button(self.root, text="Inserir Vetor 2",
                                            command=lambda: self.inserir_vetor('vetor2'))
        self.btn_inserir_vetor2.pack()

        self.btn_ortogonalizar = tk.Button(self.root, text="Ortogonalizar", command=self.ortogonalizar_vetores)
        self.btn_ortogonalizar.pack()

        self.btn_girar = tk.Button(self.root, text="Girar Base", command=self.girar_base)
        self.btn_girar.pack()

        self.btn_resetar = tk.Button(self.root, text="Resetar Base", command=self.resetar_base)
        self.btn_resetar.pack()

        self.vetores = []

    def mover(self, event):
        if event.keysym == 'Up' or event.keysym == 'w':
            self.ponto.coords += self.e1.coords * 10  # Mover na direção da seta (e1)
        elif event.keysym == 'Down' or event.keysym == 's':
            self.ponto.coords -= self.e1.coords * 10  # Mover na direção oposta da seta (e1)
        elif event.keysym == 'Left' or event.keysym == 'a':
            self.ponto.coords -= self.e2.coords * 10  # Mover na direção ortogonal esquerda (e2)
        elif event.keysym == 'Right' or event.keysym == 'd':
            self.ponto.coords += self.e2.coords * 10  # Mover na direção ortogonal direita (e2)

        # Limitar o ponto à área de 400x400 pixels
        self.ponto.coords = np.clip(self.ponto.coords, 0, 400)

        # Atualizar a posição do ponto no canvas
        self.canvas.coords(self.ponto_id, float(self.ponto.coords[0] - 5), float(self.ponto.coords[1] - 5),
                           float(self.ponto.coords[0] + 5), float(self.ponto.coords[1] + 5))

        # Print para monitorar
        print(f"Movendo ponto: {self.ponto.coords}")

        self.atualizar_seta()
        self.desenhar_vetores()

    def atualizar_seta(self):
        ponta_seta = self.ponto.coords + self.e1.coords * 20
        self.canvas.coords(self.seta_id, float(self.ponto.coords[0]), float(self.ponto.coords[1]),
                           float(ponta_seta[0]), float(ponta_seta[1]))

        # Print para monitorar
        print(f"Atualizando seta: {self.e1.coords}")

    def girar_vetor(self, event):
        angulo = {'j': 5, 'k': -5}
        direcao = angulo.get(event.keysym, 0)
        self.e1.girar(direcao)
        self.e2 = self.e1.ortogonal()

        # Print para monitorar
        print(f"Girando vetor: e1={self.e1.coords}, e2={self.e2.coords}")

        self.atualizar_seta()
        self.desenhar_vetores()

    def inserir_vetor(self, tag):
        coords = simpledialog.askstring("Inserir Vetor", "Insira as coordenadas do vetor separadas por vírgula:")
        if coords:
            vetor_coords = list(map(float, coords.split(',')))
            vetor = Vetor(vetor_coords[0], vetor_coords[1], tag)
            # Verificar se já existe um vetor com a mesma tag e substituir
            self.vetores = [v for v in self.vetores if v.tag != tag]
            self.vetores.append(vetor)
            self.desenhar_vetores()

            # Print para monitorar
            print(f"Inserindo vetor: {vetor.coords}")

    def ortogonalizar_vetores(self):
        vetor1 = next((v for v in self.vetores if v.tag == 'vetor1'), None)
        vetor2 = next((v for v in self.vetores if v.tag == 'vetor2'), None)
        if vetor1 is not None and vetor2 is not None:
            u1 = vetor1.coords / np.linalg.norm(vetor1.coords)  # Normalizar vetor1
            proj_u1 = np.dot(vetor2.coords, u1) * u1  # Projeção de vetor2 em u1
            u2 = vetor2.coords - proj_u1  # Subtrair a projeção de vetor2
            u2 = u2 / np.linalg.norm(u2)  # Normalizar u2

            # Garantir que u2 esteja na direção correta usando o produto vetorial
            if np.cross(u1, u2) < 0:
                u2 = -u2

            # Atualizar vetor1 e vetor2 com os vetores ortogonais encontrados
            vetor1.coords = u1
            vetor2.coords = u2

            self.e1.coords = u1
            self.e2.coords = u2

            # Verificação se os vetores são iguais
            if np.allclose(vetor1.coords, self.e1.coords, atol=1e-8):
                print("Os vetores v1 e e1 estão iguais")
            else:
                print("Os vetores v1 e e1 estão diferentes")

            if np.allclose(vetor2.coords, self.e2.coords, atol=1e-8):
                print("Os vetores v2 e e2 estão iguais")
            else:
                print("Os vetores v2 e e2 estão diferentes")

            # Print para monitorar
            print(f"Ortogonalizando vetores: e1={self.e1.coords}, e2={self.e2.coords}")

            self.atualizar_seta()
            self.desenhar_vetores()

    def girar_base(self):
        angulo = simpledialog.askfloat("Girar Base", "Insira o ângulo de rotação em graus:")
        if angulo is not None:
            self.e1.girar(angulo)
            self.e2 = self.e1.ortogonal()

            # Print para monitorar
            print(f"Girando base: e1={self.e1.coords}, e2={self.e2.coords}")

            self.atualizar_seta()
            self.desenhar_vetores()

    def resetar_base(self):
        self.e1 = Vetor(self.e1_inicial.coords[0], self.e1_inicial.coords[1], 'e1')
        self.e2 = Vetor(self.e2_inicial.coords[0], self.e2_inicial.coords[1], 'e2')
        self.atualizar_seta()
        self.desenhar_vetores()

        # Print para monitorar
        print(f"Resetando base: e1={self.e1.coords}, e2={self.e2.coords}")

    def desenhar_vetores(self):
        self.canvas.delete("vetor")
        for vetor in self.vetores:
            self.canvas.create_line(200, 200,
                                    200 + vetor.coords[0] * 50,
                                    200 + vetor.coords[1] * 50, arrow=tk.LAST,
                                    fill="red", tags="vetor")

        # Print para monitorar
        print(f"Desenhando vetores: {[v.coords for v in self.vetores]}")


# Classe Main para iniciar o jogo
class Main:
    def run(self):
        root = tk.Tk()
        jogo = JogoVetores(root)
        root.mainloop()


if __name__ == "__main__":
    main = Main()
    main.run()