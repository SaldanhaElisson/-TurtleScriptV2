from src.semantic_analyzer.syntatic_tree import Program, Command, VariableDeclaration, Assignment, Literal, VariableReference, RepeatLoop, BinaryExpression
from src.semantic_analyzer.analyzer import analyze_program

# Exemplo da input 1
Program(
    declarations=[],
    commands=[
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
Program(
    declarations=[VariableDeclaration("inteiro", ["tamanho_lado"])],
    commands=[
        Assignment("tamanho_lado", Literal(200, "inteiro")),
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
Program(
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
                Command("definir_cor", Literal("cyan", "texto")),
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
        )
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


