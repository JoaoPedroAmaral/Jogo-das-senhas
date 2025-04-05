import tkinter as tk
import random
import pygame

pygame.mixer.init()
success_sound = pygame.mixer.Sound("correct.mp3")
failure_sound = pygame.mixer.Sound("wrong.mp3")

RULES = [
    "A senha deve conter pelo menos um número par",
    "A soma dos dígitos deve ser maior que 15",
    "A senha deve terminar em um número ímpar",
    "A senha não pode conter números repetidos",
    "O primeiro dígito deve ser maior que o último",
    "A senha deve ter pelo menos um número primo",
    "A senha deve conter pelo menos dois números ímpares",
    "A diferença entre o maior e o menor número deve ser pelo menos 4",
    "O segundo dígito deve ser menor que o quarto",
    "A senha deve conter pelo menos um múltiplo de 3",
    "A senha deve conter um número maior que 7",
    "A soma dos dígitos deve ser um número par",
    "Nenhum dígito pode ser 0",
    "A multiplicação dos dígitos deve ser maior que 50",
    "A soma dos dois últimos dígitos deve ser um número primo",
]

def GerarDicas():
    return random.sample(RULES, 3)

def validarSenha(password, hints):
    if len(password) != 3 or not password.isdigit():
        return False
    
    digits = list(map(int, password))
    valid = True
    
    if "A senha deve conter pelo menos um número par" in hints and not any(d % 2 == 0 for d in digits):
        valid = False
    if "A soma dos dígitos deve ser maior que 15" in hints and sum(digits) <= 15:
        valid = False
    if "A senha deve terminar em um número ímpar" in hints and digits[-1] % 2 == 0:
        valid = False
    if "A senha não pode conter números repetidos" in hints and len(set(digits)) < 5:
        valid = False
    if "O primeiro dígito deve ser maior que o último" in hints and digits[0] <= digits[-1]:
        valid = False
    if "A senha deve ter pelo menos um número primo" in hints and not any(d in {2, 3, 5, 7} for d in digits):
        valid = False
    if "A senha deve conter pelo menos dois números ímpares" in hints and sum(1 for d in digits if d % 2 != 0) < 2:
        valid = False
    if "A diferença entre o maior e o menor número deve ser pelo menos 4" in hints and (max(digits) - min(digits)) < 4:
        valid = False
    if "O segundo dígito deve ser menor que o ultimo" in hints and digits[1] >= digits[2]:
        valid = False
    if "A senha deve conter pelo menos um múltiplo de 3" in hints and not any(d % 3 == 0 for d in digits):
        valid = False
    if "A senha deve conter um número maior que 7" in hints and not any(d > 7 for d in digits):
        valid = False
    if "A soma dos dígitos deve ser um número par" in hints and sum(digits[:3]) % 2 != 0:
        valid = False
    if "Nenhum dígito pode ser 0" in hints and 0 in digits:
        valid = False
    if "A multiplicação dos dígitos deve ser maior que 50" in hints and (digits[0] * digits[1] * digits[2]) <= 50:
        valid = False
    if "A soma dos dois últimos dígitos deve ser um número primo" in hints:
        last_two_sum = digits[-2] + digits[-1]
        if last_two_sum not in {2, 3, 5, 7, 11, 13, 17, 19, 23}:
            valid = False
    
    return valid

class AutomatonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Autômatos")
        self.root.geometry("500x400")
        self.root.configure(bg="#222")

        self.text = tk.Label(root, text=f"Digite uma senha de 3 digitos!",bg="#222", fg="white", font=("Arial", 12,"bold"))
        self.text.pack(pady=10)

        self.hints = GerarDicas()
        self.lives = 3
        self.correct_attempts = 0

        self.hint_label = tk.Label(root, text="\n".join(self.hints), bg="#222", fg="#4EED63", font=("Arial", 12))
        self.hint_label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=5)

        self.submit_btn = tk.Button(root, text="Verificar", command=self.checarSenha, font=("Arial", 14), bg="#4EED63", fg="black")
        self.submit_btn.pack(pady=10)

        self.result_label = tk.Label(root, text="", bg="#222", fg="white", font=("Arial", 12))
        self.result_label.pack()

        self.lives_label = tk.Label(root, text=f"Vidas restantes: {self.lives}", bg="#222", fg="#FF4444", font=("Arial", 14))
        self.lives_label.pack(pady=10)
    
    def checarSenha(self):
        password = self.entry.get()
        if validarSenha(password, self.hints):
            self.correct_attempts += 1
            self.result_label.config(text="Senha válida!", fg="#4EED63")
            success_sound.play()
            self.hints = GerarDicas()
            self.hint_label.config(text="\n".join(self.hints))
            self.entry.delete(0, tk.END)
        else:
            self.lives -= 1
            self.result_label.config(text="Senha inválida!", fg="#FF4444")
            failure_sound.play()

        self.lives_label.config(text=f"Vidas restantes: {self.lives}")

        if self.correct_attempts >= 5:
            self.result_label.config(text="Parabéns! Você venceu!", fg="#FFD700")
            self.submit_btn.config(state=tk.DISABLED)
        elif self.lives == 0:
            self.result_label.config(text="Fim de jogo! Você perdeu!", fg="#FF4444")
            self.submit_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = AutomatonGame(root)
    root.mainloop()
