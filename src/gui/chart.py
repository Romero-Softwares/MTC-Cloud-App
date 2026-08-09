import flet as ft
from database.client import buscar_historico, supabase
def abrir_grafico(page, pena_id, cliente_id, traduzir=None):
    def t(chave):
        if traduzir:
            return traduzir(chave)
        fallback = {
            "reading_time": "Horário da leitura",
            "history": "Histórico",
            "close": "Fechar",
        }
        return fallback.get(chave, chave)

    dados = buscar_historico(pena_id, cliente_id)
    if not dados:
        return

    axis_text_color = ft.Colors.WHITE70
    chart_border_color = ft.Colors.BLUE_GREY_600
    grid_color = ft.Colors.BLUE_GREY_700

    # Extrair valores convertendo para float
    valores = [float(d['valor']) for d in dados]
    val_min = min(valores)
    val_max = max(valores)

    # Margem para o gráfico ter respiro
    # Se a diferença for muito pequena, definimos uma margem fixa
    diff = val_max - val_min
    margem = 30 if diff > 7 else 7
    min_y = max(0, val_min - margem)
    max_y = val_max + margem
    grid_interval = max((max_y - min_y) / 4, 1)

    pontos = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(
                    i,
                    v,
                    tooltip=f"{v:.1f}",
                    tooltip_style=ft.TextStyle(
                        color=ft.Colors.ORANGE,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                    ),
                )
                for i, v in enumerate(valores)
            ],
            stroke_width=3,
            color="orange",
            curved=True,
            stroke_cap_round=True,
        )
    ]

    # Eixo X: Horários simplificados
    step = max(1, len(dados) // 5)
    labels_x = [
        ft.ChartAxisLabel(
            value=i,
            label=ft.Text(
                d['timestamp_local'].split(" ")[1][:5],
                size=9,
                color=axis_text_color,
            )
        ) for i, d in enumerate(dados) if i % step == 0
    ]
    labels_y = [
        ft.ChartAxisLabel(
            value=min_y + (grid_interval * i),
            label=ft.Text(
                f"{min_y + (grid_interval * i):.0f}",
                size=11,
                color=axis_text_color,
            ),
        )
        for i in range(5)
    ]

    chart = ft.LineChart(
        data_series=pontos,
        min_y=min_y,
        max_y=max_y,
        tooltip_bgcolor=ft.Colors.BLUE_GREY_700,
        tooltip_rounded_radius=4,
        # Eixo X: Com rotação e margem superior
        bottom_axis=ft.ChartAxis(
            labels=labels_x,
            labels_size=20,  # Espaço dedicado para os horários não colidirem
            labels_interval=1,
            title=ft.Text(t("reading_time"), size=12, color="white")  # Rótulo para organizar
        ),
        # Eixo Y: Mais espaço à esquerda
        left_axis=ft.ChartAxis(
            labels=labels_y,
            labels_size=50,  # Espaço maior para números de temperatura (evita quebrar)
            labels_interval=grid_interval,  # O Flet vai auto-ajustar, mas isto ajuda
            show_labels=True,

        ),

        # Garante que as bordas não cortam o texto
        border=ft.border.all(1, chart_border_color),
        horizontal_grid_lines=ft.ChartGridLines(interval=grid_interval, color=grid_color, width=1),
        expand=True,
    )

    dlg = ft.AlertDialog(
        content_padding=0,
        title_padding=0,
        actions_padding=0,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.bottom_center,
                end=ft.alignment.top_center,
                colors=[ft.Colors.GREY_900, ft.Colors.BLUE_GREY_800]
            ),
            border_radius=15,
            padding=20,
            content=ft.Column([
                ft.Text(f"{t('history')}: {pena_id}", size=20, weight="bold", color="white"),
                ft.Container(height=10),
                ft.Container(content=chart, height=260, width=550),
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.TextButton(
                            t("close"),
                            icon=ft.Icons.CLOSE,
                            on_click=lambda e: page.close(dlg),
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE_GREY_700,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ], tight=True)
        )
    )

    page.open(dlg)
    page.update()
