from src.semantic_analyzer.syntatic_tree import Comment, Program, Command, VariableDeclaration, Assignment, Literal, VariableReference, RepeatLoop, BinaryExpression, WhileLoop, IfStatement

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
            count=Literal(50, "inteiro"),
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
    ]
)

AST_Input_4 = Program(
    declarations=[
        VariableDeclaration("inteiro", ["lado"]),
        VariableDeclaration("texto", ["cor"]),
    ],
    commands=[
        WhileLoop(
            condition=BinaryExpression(
                left=VariableReference("lado"),
                operator="<",
                right=Literal(100, "inteiro")
            ),
            body=[
                IfStatement(
                    condition=BinaryExpression(
                        left=VariableReference("lado"),
                        operator="<",
                        right=Literal(100, "inteiro")
                    ),
                    true_branch=[
                        Command("definir_cor", Literal("cyan", "texto")),
                        Command("avancar", VariableReference("lado")),
                        Command("girar_direita", Literal(90, "inteiro")),
                    ],
                    false_branch=[
                        Command("definir_cor", Literal("red", "texto")),
                        Command("avancar", Literal(50, "inteiro")),
                        Command("girar_direita", Literal(45, "inteiro")),
                    ]
                ),
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
        ),
        Assignment("lado", Literal(5, "inteiro")),
        Command("cor_de_fundo", Literal("black", "texto")),
        Command("definir_espessura", Literal(2, "inteiro")),
        Command("definir_cor", Literal("white", "texto")),
        Command("escrever", Literal("Compiladores 2025.1", "texto")),
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



