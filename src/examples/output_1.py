import turtle

screen = turtle.Screen()
t = turtle.Turtle()
screen.title("Resultado - Exemplo 1")


x = 0
y = 0
velocidade = 0.0
condicao_ativa = False
mensagem = ""
x = 10
y = (25 + x)
velocidade = 5.5
condicao_ativa = True
mensagem = "Olá, mundo!"
if condicao_ativa:
    x = (x * 2)
    velocidade = (velocidade / 2)
else:
    y = (y - 5)
while (x < 100):
    x = (x + 1)

turtle.done()