from src.semantic_analyzer.syntatic_tree import Comment, Program, Command, VariableDeclaration, Assignment, Literal, VariableReference, RepeatLoop, BinaryExpression
from src.semantic_analyzer.analyzer import analyze_program

# Exemplo da input 1
AST_Input_1 = Program(
    declarations=[],
    commands=[
        Comment("Desenha as quatro arestas do quadrado"),
        Command("avancar", Literal(150, "inteiro")),
        Command("girar_direita", Literal(90, "inteiro")),
        Command("avancar", Literal(150, "inteiro")),
        Command("girar_direita", Literal(90, "inteiro")),
        Command("avancar", Literal(150, "inteiro")),
        Command("girar_direita", Literal(90, "inteiro")),
        Command("avancar", Literal(150, "inteiro")),
        Command("girar_direita", Literal(90, "inteiro")),
    ]
)

# Exemplo da input 2
AST_Input_2 = Program(
    declarations=[VariableDeclaration("inteiro", ["tamanho_lado"])],
    commands=[
        Assignment("tamanho_lado", Literal(200, "inteiro")),
        Comment("Desenha uma estrela de 5 pontas"),
        Command("avancar", VariableReference("tamanho_lado")),
        Command("girar_direita", Literal(144, "inteiro")),
        Command("avancar", VariableReference("tamanho_lado")),
        Command("girar_direita", Literal(144, "inteiro")),
        Command("avancar", VariableReference("tamanho_lado")),
        Command("girar_direita", Literal(144, "inteiro")),
        Command("avancar", VariableReference("tamanho_lado")),
        Command("girar_direita", Literal(144, "inteiro")),
        Command("avancar", VariableReference("tamanho_lado")),
        Command("girar_direita", Literal(144, "inteiro")),
    ]
)

# Exemplo da input 3
AST_Input_3 = Program(
    declarations=[
        VariableDeclaration("inteiro", ["lado"]),
        VariableDeclaration("texto", ["cor"]),
    ],
    commands=[
        Assignment("lado", Literal(5, "inteiro")),
        Command("cor_de_fundo", Literal("black", "texto")),
        Command("definir_espessura", Literal(2, "inteiro")),
        RepeatLoop(
            count=50,
            body=[
                Comment("Muda a cor da linha a cada iteração"),
                Command("definir_cor", Literal("cyan", "texto")),
                Comment("Desenha e aumenta o lado"),
                Command("avancar", VariableReference("lado")),
                Command("girar_direita", Literal(90, "inteiro")),
                Assignment("lado",
                    BinaryExpression(
                        left=VariableReference("lado"),
                        operator="+",
                        right=Literal(5, "inteiro")
                    )
                ),
            ]
        ),
        Command("escrever", Literal("Teste", "texto")),
        Command("posicao_atual", []),
    ]
)

error = Program(
    declarations=[
        VariableDeclaration("inteiro", ["lado"]),
        VariableDeclaration("texto", ["cor"]),
    ],
    commands=[
        Assignment("lado", Literal(5, "inteiro")),
        Command("cor_de_fundo", [Literal("black", "texto")]),
        Command("definir_espessura", [Literal(2, "inteiro")]),
        RepeatLoop(
            count=Literal(50, "inteiro"),
            body=[
                Command("definir_cor", [Literal("cyan", "texto")]),
                Command("avancar", [VariableReference("lado")]),
                Command("girar_direita", [Literal(90, "inteiro")]),
                Assignment("lado", BinaryExpression(
                    left=VariableReference("lado"),
                    operator="+",
                    right=Literal(5, "inteiro")
                ))
            ]
        )
    ]
)

try:
    analyze_program(error)
    print("Análise semântica concluída com sucesso!")
except Exception as e:
    print(f"Erro semântico: {e}")


