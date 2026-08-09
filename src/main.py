import flet as ft
import asyncio
import base64
import io
import re
from datetime import datetime, timedelta, UTC
import time
txt_id = None
txt_nome = None
TOLERANCIA_ATRASO_SEGUNDOS = 60
IDIOMAS = {
    "pt": {
        "language": "Idioma",
        "starting": "Iniciando MTC Cloud...",
        "alert": "Aviso",
        "close": "Fechar",
        "updating_view": "Atualizando visualização...",
        "live": "AO VIVO",
        "all": "Todos",
        "none": "Nenhum",
        "select_station": "Selecione uma estação",
        "theme_tooltip": "Alternar tema",
        "release_to_refresh": "Solte para atualizar",
        "pull_to_refresh": "Puxe para atualizar",
        "updating": "Atualizando...",
        "average": "MÉDIA",
        "min": "MÍN",
        "max": "MÁX",
        "selector": "Seletor:",
        "remote_guide": "Guia de monitoramento remoto:",
        "sync_tip": "Sincronização: Os dados são atualizados automaticamente a cada 5 segundos.",
        "interactivity_tip": "Interatividade: Clique nos cards para abrir o histórico detalhado daquela pena.",
        "offline_tip": "Status Offline: Se o card ficar vermelho, verifique a conexão do hardware com a internet.",
        "temperature_tips": "Dicas de temperatura:",
        "green_tip": "Verde: Abaixo de 176°C",
        "yellow_tip": "Amarelo: 176-189°C",
        "orange_tip": "Laranja: 190-192°C",
        "red_tip": "Vermelho: Acima de 192°C",
        "app_usage": " USO DO APP CLOUD",
        "understood": "ENTENDIDO",
        "updating_data": "Atualizando dados...",
        "terminal_offline": "Terminal Offline",
        "no_signal": "Sem sinal ou ID inválido",
        "no_signal_status": "SEM SINAL",
        "server_signal_lost": "Ops! Perdemos o sinal com o servidor Cloud.",
        "welcome_dashboard": "Bem-vindo ao Dashboard",
        "no_station_linked": "Nenhuma estação vinculada.",
        "instructions": "Instruções:",
        "instruction_1": "1. Abra o menu lateral (botão superior esquerdo)",
        "instruction_2": "2. Clique em 'Vincular Nova Estação'",
        "instruction_3": "3. Introduza o ID da sua estação para ver os dados",
        "my_stations": "Minhas Estações",
        "no_station": "Nenhuma estação",
        "link_station_start": "Vincule uma estação para começar",
        "link_new_station": "Vincular Nova Estação",
        "add_station_start": "Adicione uma estação para começar",
        "station_id": "ID da Estação",
        "station_name": "Nome da Estação",
        "decoding_qr": "A decodificar QR Code...",
        "qr_not_decoded": "QR Code não decodificado!",
        "no_image_selected": "Nenhuma imagem selecionada",
        "fill_data": "Preencha corretamente os dados.",
        "link": "Vincular",
        "read_qr": "Ler QR Code",
        "cancel": "Cancelar",
        "save": "Salvar",
        "view_chart": "Visualizar Gráfico",
        "view_history": "Ver Histórico",
        "last_sync": "Última Sincronização",
        "station_interval": "Intervalo definido na Estação",
        "updated": "Atualizado",
        "no_recent_data": "Sem dados recentes",
        "equipment": "Equipamento",
        "equipments": "Equipamentos",
        "seconds": "segundos",
        "reading_time": "Horário da leitura",
        "history": "Histórico",
    },
    "en": {
        "language": "Language",
        "starting": "Starting MTC Cloud...",
        "alert": "Notice",
        "close": "Close",
        "updating_view": "Updating view...",
        "live": "LIVE",
        "all": "All",
        "none": "None",
        "select_station": "Select a station",
        "theme_tooltip": "Toggle theme",
        "release_to_refresh": "Release to refresh",
        "pull_to_refresh": "Pull to refresh",
        "updating": "Updating...",
        "average": "AVG",
        "min": "MIN",
        "max": "MAX",
        "selector": "Selector:",
        "remote_guide": "Remote monitoring guide:",
        "sync_tip": "Sync: Data is updated automatically every 5 seconds.",
        "interactivity_tip": "Interactivity: Tap cards to open the detailed history for that probe.",
        "offline_tip": "Offline status: If the card turns red, check the hardware internet connection.",
        "temperature_tips": "Temperature tips:",
        "green_tip": "Green: Below 176°C",
        "yellow_tip": "Yellow: 176-189°C",
        "orange_tip": "Orange: 190-192°C",
        "red_tip": "Red: Above 192°C",
        "app_usage": " CLOUD APP USAGE",
        "understood": "OK",
        "updating_data": "Updating data...",
        "terminal_offline": "Terminal Offline",
        "no_signal": "No signal or invalid ID",
        "no_signal_status": "NO SIGNAL",
        "server_signal_lost": "We lost the Cloud server signal.",
        "welcome_dashboard": "Welcome to the Dashboard",
        "no_station_linked": "No station linked.",
        "instructions": "Instructions:",
        "instruction_1": "1. Open the side menu (top-left button)",
        "instruction_2": "2. Tap 'Link New Station'",
        "instruction_3": "3. Enter your station ID to view data",
        "my_stations": "My Stations",
        "no_station": "No station",
        "link_station_start": "Link a station to get started",
        "link_new_station": "Link New Station",
        "add_station_start": "Add a station to get started",
        "station_id": "Station ID",
        "station_name": "Station Name",
        "decoding_qr": "Decoding QR Code...",
        "qr_not_decoded": "QR Code not decoded!",
        "no_image_selected": "No image selected",
        "fill_data": "Fill in the data correctly.",
        "link": "Link",
        "read_qr": "Read QR Code",
        "cancel": "Cancel",
        "save": "Save",
        "view_chart": "View Chart",
        "view_history": "View History",
        "last_sync": "Last Sync",
        "station_interval": "Interval set on Station",
        "updated": "Updated",
        "no_recent_data": "No recent data",
        "equipment": "Device",
        "equipments": "Devices",
        "seconds": "seconds",
        "reading_time": "Reading time",
        "history": "History",
    },
}

def get_cor_temperatura(valor):
    if valor <= 176:
        return ft.Colors.GREEN_400
    elif valor <= 189:
        return ft.Colors.YELLOW_400
    elif valor <= 192:
        return ft.Colors.ORANGE_400
    else:
        return ft.Colors.RED_800

def intervalo_para_segundos(intervalo):
    if intervalo is None:
        return 10
    if isinstance(intervalo, (int, float)):
        return max(1, int(intervalo))

    texto = str(intervalo).strip().lower()
    if not texto:
        return 10

    partes_hora = texto.split(":")
    if len(partes_hora) == 3 and all(p.isdigit() for p in partes_hora):
        horas, minutos, segundos = [int(p) for p in partes_hora]
        return max(1, horas * 3600 + minutos * 60 + segundos)

    match = re.search(r"(\d+(?:[,.]\d+)?)", texto)
    if not match:
        return 10

    valor = float(match.group(1).replace(",", "."))
    if "hora" in texto or "hour" in texto:
        valor *= 3600
    elif "min" in texto:
        valor *= 60
    return max(1, int(valor))

def parse_created_at(valor):
    if not valor:
        return None
    texto = str(valor).strip()
    try:
        if texto.endswith("Z"):
            texto = texto[:-1] + "+00:00"
        data = datetime.fromisoformat(texto)
        if data.tzinfo is None:
            data = data.replace(tzinfo=UTC)
        return data.astimezone(UTC)
    except ValueError:
        return None

def leitura_esta_recente(dados, agora):
    intervalo = intervalo_para_segundos(dados.get("intervalo"))
    limite_segundos = intervalo + TOLERANCIA_ATRASO_SEGUNDOS
    criado_em = parse_created_at(dados.get("created_at"))
    if not criado_em:
        return False
    idade_segundos = (agora - criado_em).total_seconds()
    return idade_segundos <= limite_segundos

def main(page: ft.Page):
    idioma_inicial = page.client_storage.get("idioma") or "pt"
    if idioma_inicial not in IDIOMAS:
        idioma_inicial = "pt"

    if page.platform == ft.PagePlatform.ANDROID:
        page.window.full_screen = True

    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    splash_screen = ft.Container(
        content=ft.Column([
            ft.Image(src="splash.png", width=180, height=180, fit=ft.ImageFit.CONTAIN),
            ft.Container(height=30),
            ft.ProgressRing(color="blue", stroke_width=3, width=30, height=30),
            ft.Container(height=10),
            ft.Text(IDIOMAS[idioma_inicial]["starting"], color=ft.Colors.BLUE_GREY_400, size=14)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        alignment=ft.alignment.center
    )
    
    page.add(splash_screen)
    page.update()
    
    # Imports pesados carregados de forma assíncrona/tardia (Lazy Loading)
    from PIL import Image
    from gui.chart import abrir_grafico, supabase
    import requests
    
    time.sleep(0.5)

    id_salvo = page.client_storage.get("id_ativo")
    nome_salvo_storage = page.client_storage.get("nome_ativo")
    tema_escuro = page.client_storage.get("tema_escuro")
    if tema_escuro is None:
        tema_escuro = True
        page.client_storage.set("tema_escuro", True)
    idioma = page.client_storage.get("idioma") or "pt"
    if idioma not in IDIOMAS:
        idioma = "pt"
        page.client_storage.set("idioma", idioma)

    def t(chave):
        return IDIOMAS.get(idioma, IDIOMAS["pt"]).get(chave, IDIOMAS["pt"].get(chave, chave))

    def nome_sem_status(nome):
        return re.sub(r"\s*\((SEM SINAL|NO SIGNAL)\)$", "", nome or "", flags=re.IGNORECASE)

    def nome_com_status_sem_sinal(nome):
        return f"{nome_sem_status(nome)} ({t('no_signal_status')})"

    nome_salvo = nome_salvo_storage or t("select_station")

    page.theme_mode = ft.ThemeMode.DARK if tema_escuro else ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_900 if tema_escuro else ft.Colors.BLUE_GREY_50

    estado_id = {"valor": id_salvo}
    estacoes = page.client_storage.get("estacoes") or []
    filtro_selecionado = {"valor": "Todos"}
    cards_fornos = {}
    
    print(f"Ultimo ID conectado: {estado_id['valor']}")
    alert_info = ft.AlertDialog(title=ft.Text(t("alert")), actions=[ft.ElevatedButton(t("close"), on_click=lambda _: page.close(alert_info))])

    loading_grid = ft.Container(
        content=ft.Column([
            ft.ProgressRing(color="blue", stroke_width=3),
            ft.Text(t("updating_view"), color=ft.Colors.BLUE_GREY_400, size=14)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
        visible=False,
        alignment=ft.alignment.center,
        height=200
    )

    scroll_grid = {"no_topo": True}

    def acompanhar_scroll_grid(e):
        scroll_grid["no_topo"] = (e.pixels or 0) <= 5

    grid = ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.HIDDEN,
        expand=True,
        on_scroll=acompanhar_scroll_grid,
        on_scroll_interval=100,
    )
    grid_bottom_spacer = ft.Container(height=24)

    def garantir_respiro_inferior_grid():
        if grid_bottom_spacer in grid.controls:
            grid.controls.remove(grid_bottom_spacer)
        grid.controls.append(grid_bottom_spacer)
    
    titulo_estacao = ft.Text(f"{nome_salvo.upper()}", size=20, weight="bold", color=ft.Colors.WHITE)
    
    live_indicator = ft.Container(
        content=ft.Row([
            ft.Container(width=8, height=8, border_radius=4, bgcolor=ft.Colors.GREEN_400),
            ft.Text(t("live"), size=10, color=ft.Colors.GREEN_400, weight=ft.FontWeight.W_500)
        ], spacing=5),
        visible=False
    )

    last_update_text = ft.Text("", size=11, color=ft.Colors.BLUE_GREY_400)
    
    dropdown_penas = ft.Dropdown(
        options=[ft.dropdown.Option("Todos", t("all"))],
        value="Todos",
        width=150,
        on_change=lambda e: aplicar_filtro(e)
    )

    count_penas = ft.Text(t("none"), size=12, color=ft.Colors.BLUE_GREY_400)

    tema_btn = ft.ElevatedButton(
        "Dark" if tema_escuro else "Light",
        icon=ft.Icons.DARK_MODE if tema_escuro else ft.Icons.LIGHT_MODE,
        on_click=lambda e: alternar_tema(e),
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_GREY_800 if tema_escuro else ft.Colors.BLUE_600,
            elevation=6,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
        ),
        tooltip=t("theme_tooltip")
    )

    idioma_btn = ft.ElevatedButton(
        "PT" if idioma == "pt" else "EN",
        icon=ft.Icons.LANGUAGE,
        on_click=lambda e: alternar_idioma(e),
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_GREY_800 if tema_escuro else ft.Colors.BLUE_600,
            elevation=6,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
        ),
        tooltip=t("language"),
    )

    def alternar_tema(e):
        nonlocal tema_escuro
        tema_escuro = not tema_escuro
        page.client_storage.set("tema_escuro", tema_escuro)
        page.theme_mode = ft.ThemeMode.DARK if tema_escuro else ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.GREY_900 if tema_escuro else ft.Colors.BLUE_GREY_50
        tema_btn.text = "Dark" if tema_escuro else "Light"
        tema_btn.icon = ft.Icons.DARK_MODE if tema_escuro else ft.Icons.LIGHT_MODE
        tema_btn.style.bgcolor = ft.Colors.BLUE_GREY_800 if tema_escuro else ft.Colors.BLUE_600
        idioma_btn.style.bgcolor = ft.Colors.BLUE_GREY_800 if tema_escuro else ft.Colors.BLUE_600
        atualizar_cores_tema()
        atualizar_grid_tema()
        atualizar_drawer()
        if not estado_id.get("valor"):
            mostrar_tela_vazia()
        page.update()

    def alternar_idioma(e):
        nonlocal idioma
        idioma = "en" if idioma == "pt" else "pt"
        page.client_storage.set("idioma", idioma)
        idioma_btn.text = "PT" if idioma == "pt" else "EN"
        idioma_btn.tooltip = t("language")
        tema_btn.tooltip = t("theme_tooltip")
        alert_info.title.value = t("alert")
        alert_info.actions[0].text = t("close")
        loading_grid.content.controls[1].value = t("updating_view")
        live_indicator.content.controls[1].value = t("live")
        pull_refresh_indicator.content.controls[1].value = t("release_to_refresh")
        card_media.content.content.controls[0].value = t("average")
        card_min.content.content.controls[0].value = t("min")
        card_max.content.content.controls[0].value = t("max")
        dropdown_penas.options = [ft.dropdown.Option("Todos", t("all"))] + [
            ft.dropdown.Option(pid) for pid in cards_fornos.keys()
        ]
        if not cards_fornos:
            count_penas.value = t("none")
        else:
            visiveis = sum(1 for c in cards_fornos.values() if c.visible)
            count_penas.value = f"{visiveis} {t('equipment') if visiveis == 1 else t('equipments')}"
        if "(" in titulo_estacao.value:
            titulo_estacao.value = nome_com_status_sem_sinal(titulo_estacao.value)
        card.content.content.controls[0].controls[1].value = t("terminal_offline")
        card.content.content.controls[3].value = t("no_signal")
        for card_forno in cards_fornos.values():
            col = card_forno.content.content
            col.controls[0].controls[3].content.value = t("view_chart")
            col.controls[0].controls[4].tooltip = t("view_history")
            if ": " in col.controls[3].value:
                col.controls[3].value = f"{t('last_sync')}: {col.controls[3].value.split(': ', 1)[1]}"
            intervalo_text = col.controls[4].controls[1]
            if ": " in intervalo_text.value:
                intervalo_text.value = f"{t('station_interval')}: {intervalo_text.value.split(': ', 1)[1]}"
            intervalo_text.value = re.sub(r"\bsegundos\b|\bseconds\b", t("seconds"), intervalo_text.value, flags=re.IGNORECASE)
        atualizar_drawer()
        if estado_id.get("valor"):
            mostrar_grid()
        else:
            mostrar_tela_vazia()
        page.update()

    def atualizar_cores_tema():
        cor_texto = ft.Colors.WHITE if tema_escuro else ft.Colors.GREY_900
        cor_secundaria = ft.Colors.BLUE_GREY_400 if tema_escuro else ft.Colors.GREY_600
        titulo_estacao.color = cor_texto
        appbar.bgcolor = ft.Colors.BLACK87 if tema_escuro else ft.Colors.WHITE
        appbar.leading.icon_color = ft.Colors.WHITE if tema_escuro else ft.Colors.GREY_900
        appbar.title.controls[1].color = ft.Colors.WHITE if tema_escuro else ft.Colors.GREY_900
        for action in appbar.actions:
            action.icon_color = ft.Colors.BLUE_GREY_200 if tema_escuro else ft.Colors.GREY_700
        conteudo_central.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.Colors.GREY_900, ft.Colors.BLUE_GREY_900] if tema_escuro else [ft.Colors.BLUE_GREY_50, ft.Colors.WHITE]
        )
        conteudo_central.image = ft.DecorationImage(
            src="industrial_dark.svg" if tema_escuro else "industrial_light.svg",
            repeat=ft.ImageRepeat.REPEAT,
            fit=ft.ImageFit.NONE,
            opacity=0.28 if tema_escuro else 0.42
        )
        dropdown_penas.border_color = ft.Colors.BLUE_400 if tema_escuro else ft.Colors.GREY_400
        last_update_text.color = ft.Colors.BLUE_GREY_400 if tema_escuro else ft.Colors.GREY_600
        live_indicator.content.controls[1].color = ft.Colors.GREEN_400 if tema_escuro else ft.Colors.GREEN_600
        live_indicator.content.controls[0].bgcolor = ft.Colors.GREEN_400 if tema_escuro else ft.Colors.GREEN_600
        for c in [card_media, card_min, card_max]:
            c.content.content.controls[0].color = cor_secundaria

    def atualizar_grid_tema():
        bg_card = ft.Colors.GREY_800 if tema_escuro else ft.Colors.WHITE
        cor_texto = ft.Colors.WHITE if tema_escuro else ft.Colors.GREY_900
        cor_sub = ft.Colors.BLUE_GREY_400 if tema_escuro else ft.Colors.GREY_600
        for card in cards_fornos.values():
            card.content.bgcolor = bg_card
            col = card.content.content
            col.controls[0].controls[1].color = cor_texto
            col.controls[3].color = cor_sub

    def aplicar_filtro(e=None):
        filtro_selecionado["valor"] = e.control.value if e else "Todos"
        termo = filtro_selecionado["valor"]
        
        for card in cards_fornos.values():
            card.visible = False
            
        loading_grid.visible = True
        if loading_grid not in grid.controls:
            grid.controls.append(loading_grid)
        page.update()
        
        time.sleep(0.4)
        
        nao_cards = [c for c in grid.controls if not isinstance(c, ft.Card)]
        grid.controls.clear()
        grid.controls.extend(nao_cards)
        
        visiveis = 0
        for pid, card in cards_fornos.items():
            if termo == "Todos" or termo == pid:
                card.visible = True
                grid.controls.append(card)
                visiveis += 1
            else:
                card.visible = False
                
        count_penas.value = f"{visiveis} {t('equipment') if visiveis == 1 else t('equipments')}"
        
        loading_grid.visible = False
        if loading_grid in grid.controls:
            grid.controls.remove(loading_grid)
        garantir_respiro_inferior_grid()
        page.update()

    def chamar_grafico(e, p_id, id_atual):
        loading_grafico.visible = True
        page.update()
        abrir_grafico(page, p_id, id_atual, t)
        loading_grafico.visible = False
        page.update()

    loading_grafico = ft.Container(
        content=ft.ProgressBar(color="blue"),
        visible=False,
        alignment=ft.alignment.center,
padding=10
    )

    carregando = ft.ProgressBar(visible=False, color="blue")
    pull_refresh = {"distancia": 0, "ativo": False}
    pull_refresh_indicator = ft.Container(
        visible=False,
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=8, bottom=4),
        content=ft.Row(
            [
                ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.BLUE_400),
                ft.Text(t("release_to_refresh"), size=12, color=ft.Colors.BLUE_GREY_400),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    def atualizar_pull_indicator(texto, mostrar=True):
        pull_refresh_indicator.visible = mostrar
        pull_refresh_indicator.content.controls[1].value = texto
        page.update()

    def pull_to_refresh_start(e):
        pull_refresh["distancia"] = 0
        pull_refresh["ativo"] = scroll_grid["no_topo"]

    def pull_to_refresh_update(e):
        if not pull_refresh["ativo"]:
            return

        delta = e.primary_delta if e.primary_delta is not None else e.delta_y
        pull_refresh["distancia"] = max(0, pull_refresh["distancia"] + delta)

        if pull_refresh["distancia"] > 35 and not pull_refresh_indicator.visible:
            atualizar_pull_indicator(t("pull_to_refresh"))
        elif pull_refresh["distancia"] > 40:
            atualizar_pull_indicator(t("release_to_refresh"))

    def pull_to_refresh_end(e):
        deve_atualizar = pull_refresh["ativo"] and pull_refresh["distancia"] > 40
        pull_refresh["distancia"] = 0
        pull_refresh["ativo"] = False

        if deve_atualizar:
            atualizar_pull_indicator(t("updating"))
            forcar_atualizacao(e)
        pull_refresh_indicator.visible = False
        page.update()
    
    card_media = ft.Card(
        elevation=8,
        content=ft.Container(
            content=ft.Column([ft.Text(t("average"), size=11, color=ft.Colors.BLUE_GREY_400), ft.Text("--- °C", size=18, weight="bold", color=ft.Colors.BLUE_400)]), 
            padding=10,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_GREY_800, ft.Colors.GREY_900]
            ),
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS
        )
    )
    card_min = ft.Card(
        elevation=8,
        content=ft.Container(
            content=ft.Column([ft.Text(t("min"), size=11, color=ft.Colors.BLUE_GREY_400), ft.Text("--- °C", size=18, weight="bold", color=ft.Colors.GREEN_400)]), 
            padding=10,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_GREY_800, ft.Colors.GREY_900]
            ),
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS
        )
    )
    card_max = ft.Card(
        elevation=8,
        content=ft.Container(
            content=ft.Column([ft.Text(t("max"), size=11, color=ft.Colors.BLUE_GREY_400), ft.Text("--- °C", size=18, weight="bold", color=ft.Colors.RED_400)]), 
            padding=10,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_GREY_800, ft.Colors.GREY_900]
            ),
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS
        )
    )
    
    metricas_row = ft.Row(spacing=10, alignment=ft.MainAxisAlignment.SPACE_EVENLY, controls=[card_media, card_min, card_max])

    def atualizar_metricas(dados_agrupados):
        if not dados_agrupados:
            card_media.content.content.controls[1].value = "--- °C"
            card_min.content.content.controls[1].value = "--- °C"
            card_max.content.content.controls[1].value = "--- °C"
            return
        valores = [float(d['valor']) for d in dados_agrupados.values()]
        media = sum(valores) / len(valores)
        minima = min(valores)
        maxima = max(valores)
        card_media.content.content.controls[1].value = f"{media:.1f} °C"
        card_min.content.content.controls[1].value = f"{minima:.1f} °C"
        card_max.content.content.controls[1].value = f"{maxima:.1f} °C"
        card_media.content.content.controls[1].color = get_cor_temperatura(media)
        card_min.content.content.controls[1].color = get_cor_temperatura(minima)
        card_max.content.content.controls[1].color = get_cor_temperatura(maxima)

    conteudo_central = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column([
            ft.Row([titulo_estacao, ft.Container(expand=True), live_indicator, last_update_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            metricas_row,
            ft.Row([ft.Icon(ft.Icons.DEVICE_HUB, size=20), ft.Text(t("selector"), size=14), dropdown_penas, count_penas], spacing=10),
            grid
        ])
    )

    def abrir_info_app(page: ft.Page):
        conteudo_uso = ft.Column([
            ft.Text(t("remote_guide"), weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_200),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            ft.Row([ft.Icon(ft.Icons.SYNC_ALT, color="blue", size=20), ft.Text(t("sync_tip"), size=14, expand=True)]),
            ft.Row([ft.Icon(ft.Icons.TOUCH_APP, color="orange", size=20), ft.Text(t("interactivity_tip"), size=14, expand=True)]),
            ft.Row([ft.Icon(ft.Icons.SIGNAL_CELLULAR_CONNECTED_NO_INTERNET_4_BAR, color="red", size=20), ft.Text(t("offline_tip"), size=14, expand=True)]),
            #ft.Row([ft.Icon(ft.Icons.SCREEN_ROTATION, color="green", size=20), ft.Text("Visualização: O App é responsivo. Use na horizontal para melhor leitura dos gráficos.", size=14, expand=True)]),
            ft.Divider(height=10),
            ft.Text(t("temperature_tips"), weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_200),
            ft.Row([ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.GREEN_400, size=16), ft.Text(t("green_tip"), size=12, expand=True)]),
            ft.Row([ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.YELLOW_400, size=16), ft.Text(t("yellow_tip"), size=12, expand=True)]),
            ft.Row([ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.ORANGE_400, size=16), ft.Text(t("orange_tip"), size=12, expand=True)]),
            ft.Row([ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.RED_400, size=16), ft.Text(t("red_tip"), size=12, expand=True)]),
        ], tight=True, spacing=15, width=400)

        dialogo = ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_400), ft.Text(t("app_usage"))]),
            content=conteudo_uso,
            actions=[ft.TextButton(t("understood"), on_click=lambda _: page.close(dialogo))],
        )
        page.open(dialogo)

    def forcar_atualizacao(e):
        page.open(ft.SnackBar(content=ft.Text(t("updating_data")), padding=ft.padding.all(15), margin=ft.margin.all(10)))
        page.close(page.drawer)
        cards_fornos.clear()
        grid.controls.clear()
        open_loading()
        
        estado_id["valor"] = page.client_storage.get("id_ativo")
        page.update()

    card = ft.Card(
        content=ft.Container(
            padding=20,
            bgcolor=ft.Colors.RED_900,
            border_radius=15,
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.CLOUD_OFF, color="yellow"),
                        ft.Text(t("terminal_offline"), size=20, weight="bold", color=ft.Colors.RED_300)]),
                ft.Text("0.0 °C", size=40, color=ft.Colors.ORANGE, weight="bold"),
                ft.ProgressBar(value=0, color=ft.Colors.ORANGE),
                ft.Text(t("no_signal"), size=10, color=ft.Colors.BLUE_GREY_400)
            ])
        )
    )

    def mostrar_baner_conexao():
        banner_erro = ft.Banner(bgcolor=ft.Colors.AMBER_700, leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER_900, size=40), content=ft.Text(t("server_signal_lost"), color=ft.Colors.BLACK), actions=[ft.TextButton(t("understood"), on_click=lambda _: page.close(banner_erro))])
        page.open(banner_erro)

    def mostrar_tela_vazia():
        cor_icone = ft.Colors.BLUE_GREY_500 if tema_escuro else ft.Colors.BLUE_GREY_600
        cor_titulo = ft.Colors.WHITE if tema_escuro else ft.Colors.GREY_900
        cor_subtitulo = ft.Colors.BLUE_GREY_400 if tema_escuro else ft.Colors.BLUE_GREY_700
        cor_painel = ft.Colors.GREY_800 if tema_escuro else ft.Colors.WHITE
        cor_instrucao_titulo = ft.Colors.BLUE_200 if tema_escuro else ft.Colors.BLUE_700
        cor_instrucao_texto = ft.Colors.BLUE_GREY_300 if tema_escuro else ft.Colors.BLUE_GREY_700
        cor_instrucao_icone = ft.Colors.BLUE_400 if tema_escuro else ft.Colors.BLUE_600

        conteudo_central.content = ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOUD_OFF, size=100, color=cor_icone),
                    padding=20
                ),
                ft.Text(t("welcome_dashboard"), size=26, weight="bold", color=cor_titulo),
                ft.Text(t("no_station_linked"), color=cor_subtitulo),
                ft.Container(
                    content=ft.Column([
                        ft.Text(t("instructions"), weight="bold", color=cor_instrucao_titulo),
                        ft.Row([ft.Icon(ft.Icons.ARROW_RIGHT, size=18, color=cor_instrucao_icone), ft.Text(t("instruction_1"), size=12, color=cor_instrucao_texto)], spacing=5),
                        ft.Row([ft.Icon(ft.Icons.ARROW_RIGHT, size=18, color=cor_instrucao_icone), ft.Text(t("instruction_2"), size=12, color=cor_instrucao_texto)], spacing=5),
                        ft.Row([ft.Icon(ft.Icons.ARROW_RIGHT, size=18, color=cor_instrucao_icone), ft.Text(t("instruction_3"), size=12, color=cor_instrucao_texto)], spacing=5),
                    ], spacing=5),
                    margin=ft.margin.only(top=30),
                    padding=20,
                    border_radius=10,
                    bgcolor=cor_painel
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        carregando.visible = False
        page.update()

    def mostrar_grid():
        garantir_respiro_inferior_grid()
        conteudo_central.content = ft.Column([
            ft.Row([titulo_estacao, ft.Container(expand=True), live_indicator, last_update_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            metricas_row,
            ft.Row([ft.Icon(ft.Icons.DEVICE_HUB, size=20), ft.Text(t("selector"), size=14), dropdown_penas, count_penas], spacing=10),
            grid
        ])
        page.update()

    def open_loading():
        carregando.visible = True
        page.update()

    def atualizar_drawer():
        cor_fundo = ft.Colors.GREY_800 if tema_escuro else ft.Colors.WHITE
        cor_texto = ft.Colors.WHITE if tema_escuro else ft.Colors.GREY_900
        cor_secundaria = ft.Colors.BLUE_GREY_500 if tema_escuro else ft.Colors.GREY_600
        cor_icon_ativo = ft.Colors.BLUE_400
        cor_bg_ativo = ft.Colors.BLUE_900 if tema_escuro else ft.Colors.BLUE_50
        
        header_drawer = ft.Container(
            content=ft.Column([
                ft.Row([
                    idioma_btn,
                    ft.Container(expand=True),
                    tema_btn,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=18),
                ft.Row([
                    ft.Icon(ft.Icons.WIFI_TETHERING_ROUNDED, color=ft.Colors.WHITE, size=32),
                    ft.Text(t("my_stations"), size=20, weight=ft.FontWeight.W_800, color=ft.Colors.WHITE)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=15, color=ft.Colors.WHITE24)
            ], tight=True, spacing=6),
            padding=ft.padding.only(top=50, left=20, right=20, bottom=15),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_800, ft.Colors.BLUE_GREY_900] if tema_escuro else [ft.Colors.BLUE_600, ft.Colors.BLUE_400]
            ),
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20),
            margin=ft.margin.only(bottom=10)
        )
        page.drawer.controls = [header_drawer]
        
        if not estacoes:
            page.drawer.controls.append(ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CLOUD_OFF, size=40, color=cor_secundaria),
                    ft.Text(t("no_station"), size=14, color=cor_secundaria),
                    ft.Text(t("link_station_start"), size=11, color=cor_secundaria, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=30,
                alignment=ft.alignment.center
            ))
        else:
            for i, est in enumerate(estacoes):
                is_ativo = est['id'] == estado_id.get("valor")
                page.drawer.controls.append(ft.Container(
                    content=ft.ListTile(
                        leading=ft.Container(
                            content=ft.Icon(ft.Icons.THERMOSTAT, color="red"),#deve ser vermelho sempre isso é padrão.
                            bgcolor=ft.Colors.BLUE_700 if is_ativo else (ft.Colors.BLUE_GREY_700 if tema_escuro else ft.Colors.GREY_300),
                            border_radius=20,
                            width=40,
                            height=40,
                            alignment=ft.alignment.center
                        ),
                        title=ft.Text(est['nome'], weight=ft.FontWeight.BOLD if is_ativo else ft.FontWeight.NORMAL, color=cor_icon_ativo if is_ativo else cor_texto),
                        subtitle=ft.Text(f"ID: {est['id'][:12]}...", size=10, color=ft.Colors.BLUE_GREY_500),
                        trailing=ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400, on_click=lambda e, idx=i: [estacoes.pop(idx), page.client_storage.set("estacoes", estacoes), atualizar_drawer()]),
                        on_click=lambda e, id_sel=est['id'], nome_sel=est['nome']: [
                            page.close(page.drawer),
                            page.client_storage.set("id_ativo", id_sel),
                            page.client_storage.set("nome_ativo", nome_sel),
                            estado_id.update({"valor": id_sel}),
                            cards_fornos.clear(),
                            grid.controls.clear(),
                            open_loading(),
                            setattr(titulo_estacao, "value", f"{nome_sel.upper()}"),
                            mostrar_grid(),
                            page.update()
                        ]
                    ),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.center_left,
                        end=ft.alignment.center_right,
                        colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_GREY_900] if tema_escuro else [ft.Colors.BLUE_100, ft.Colors.WHITE]
                    ) if is_ativo else None,
                    bgcolor=ft.Colors.TRANSPARENT if not is_ativo else None,
                    border_radius=12,
                    margin=ft.margin.symmetric(horizontal=10, vertical=4)
                ))
        
        btn_vincular = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ADD_LINK, color=ft.Colors.WHITE),
                ft.Text(t("link_new_station"), color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=15)
            ], alignment=ft.MainAxisAlignment.CENTER),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_600, ft.Colors.BLUE_800]
            ),
            padding=15,
            border_radius=30,
            on_click=abrir_dialogo_vinculo,
            ink=True,
        )
        
        btn_container = ft.Container(content=btn_vincular, margin=ft.margin.only(top=50), padding=ft.padding.all(15))
        
        drawer_items = page.drawer.controls[1:] if len(page.drawer.controls) > 1 else []
        
        if not estacoes:
            msg_vazio = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WIFI_OFF, size=40, color=cor_secundaria),
                    ft.Text(t("no_station_linked"), size=14, color=cor_secundaria),
                    ft.Text(t("add_station_start"), size=11, color=cor_secundaria, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=30,
                alignment=ft.alignment.center,
                expand=True
            )
            page.drawer.controls = [header_drawer, msg_vazio, btn_container]
        else:
            page.drawer.controls = [header_drawer] + drawer_items + [btn_container]
        
        page.update()

    def abrir_dialogo_vinculo(e=None):
        page.close(page.drawer)
        
        global txt_id, txt_nome
        txt_id = ft.TextField(label=t("station_id"), color="white", label_style=ft.TextStyle(color=ft.Colors.WHITE))
        txt_nome = ft.TextField(label=t("station_name"), color="white", label_style=ft.TextStyle(color=ft.Colors.WHITE))
        
        def processar_qr_via_api(caminho_imagem):
            try:   
                img = Image.open(caminho_imagem)
                img.thumbnail((800, 800), Image.LANCZOS)
                buffer = io.BytesIO()
                img.save(buffer, format='PNG', quality=90)
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                url = "https://quickchart.io/qr-read"
                response = requests.post(url, json={'image': img_base64}, timeout=30)
                
                if response.status_code == 200:
                    resultado = response.json()
                    if resultado.get('result'):
                        return resultado['result']
                return None
            except Exception as e:
                return None

        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                page.open(ft.SnackBar(content=ft.Text(t("decoding_qr"))))
                id_lido = processar_qr_via_api(e.files[0].path)
                if id_lido:
                    txt_id.value = id_lido
                    page.update()
                else:
                    page.open(ft.SnackBar(content=ft.Text(t("qr_not_decoded"))))
            else:
                page.open(ft.SnackBar(content=ft.Text(t("no_image_selected"))))

        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        file_picker.on_result = on_result

        def escanear_qr_camera(e):
            page.close(page.drawer)
            file_picker.pick_files(
                file_type=ft.FilePickerFileType.IMAGE,
                allow_multiple=False,
            )

        def salvar(e):
            if txt_id.value:
                estacoes.append({"id": txt_id.value, "nome": txt_nome.value})
                page.client_storage.set("estacoes", estacoes)
                page.client_storage.set("id_ativo", txt_id.value)
                page.client_storage.set("nome_ativo", txt_nome.value)
                estado_id.update({"valor": txt_id.value})
                titulo_estacao.value = txt_nome.value.upper()
                
                atualizar_drawer()
                mostrar_grid()
                page.close(dlg)
            else:
                alert_info.content = ft.Text(t("fill_data"))
                page.open(alert_info)

        dlg = ft.AlertDialog(
            title=ft.Text(t("link")),
            content=ft.Container(
                padding=20,
                border_radius=20,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.bottom_center,
                    end=ft.alignment.top_center,
                    colors=[ft.Colors.GREY_900, ft.Colors.BLUE_GREY_800]
                ),
                content=ft.Column(height=180, controls=[
                txt_id,
                txt_nome,
                ft.ElevatedButton(t("read_qr"), icon=ft.Icons.QR_CODE_SCANNER, on_click=escanear_qr_camera)
            ]),
            
            ), actions=[
                ft.ElevatedButton(t("cancel"), on_click=lambda _: page.close(dlg)),
                ft.ElevatedButton(t("save"), on_click=salvar)
            ])
        page.open(dlg)

    page.drawer = ft.NavigationDrawer()
    atualizar_drawer()

    appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=lambda e:page.open(page.drawer)),
        title=ft.Row([ft.Icon(ft.Icons.MONITOR_HEART, color="blue"), ft.Text("MTChart Pro Cloud", weight="bold")]),
        actions=[ft.IconButton(ft.Icons.REFRESH, on_click=forcar_atualizacao), ft.IconButton(ft.Icons.INFO_OUTLINED, on_click=lambda _:abrir_info_app(page))],
        bgcolor=ft.Colors.BLACK87,
    )
    atualizar_cores_tema()

    if estacoes:
        open_loading()
        mostrar_grid()
    else:
        mostrar_tela_vazia()

    async def sync_loop():
        while True:
            await asyncio.sleep(5)
            id_atual = estado_id.get("valor")
            if not id_atual:
                continue
                
            try:
                limite_tempo = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
                res = supabase.table("leituras_cloud").select("*").eq("cliente_id", id_atual).gte("created_at", limite_tempo).order("created_at", desc=False).execute()
                
                if not res.data:
                    grid.controls.clear()
                    grid.controls.append(card)
                    garantir_respiro_inferior_grid()
                    cards_fornos.clear()
                    carregando.visible = False
                    live_indicator.visible = False
                    titulo_estacao.value = nome_com_status_sem_sinal(titulo_estacao.value)
                    atualizar_metricas({})
                else:
                    titulo_estacao.value = nome_sem_status(titulo_estacao.value)
                    
                    nao_cards = [c for c in grid.controls if not isinstance(c, ft.Card)]
                    grid.controls.clear()
                    grid.controls.extend(nao_cards)
                    carregando.visible = False

                    agora = datetime.now(UTC)
                    ultimas_leituras = {item['pena_id']: item for item in res.data}
                    dados_agrupados = {
                        pena_id: dados
                        for pena_id, dados in ultimas_leituras.items()
                        if leitura_esta_recente(dados, agora)
                    }

                    if not dados_agrupados:
                        grid.controls.clear()
                        grid.controls.append(card)
                        garantir_respiro_inferior_grid()
                        cards_fornos.clear()
                        carregando.visible = False
                        live_indicator.visible = False
                        last_update_text.value = t("no_recent_data")
                        titulo_estacao.value = nome_com_status_sem_sinal(titulo_estacao.value)
                        atualizar_metricas({})
                        dropdown_penas.options = [ft.dropdown.Option("Todos", t("all"))]
                        count_penas.value = t("none")
                        page.update()
                        continue
                    
                    intervalo_str = f"10 {t('seconds')}"
                    primeira_leitura_recente = next(iter(dados_agrupados.values()))
                    if primeira_leitura_recente.get("intervalo"):
                        intervalo_str = primeira_leitura_recente["intervalo"]
                        intervalo_str = re.sub(r"\bsegundos\b|\bseconds\b", t("seconds"), str(intervalo_str), flags=re.IGNORECASE)
                    
                    atualizar_metricas(dados_agrupados)
                    live_indicator.visible = True
                    last_update_text.value = f"{t('updated')}: {datetime.now().strftime('%H:%M:%S')}"
                    
                    new_penas = set(dados_agrupados.keys())
                    
                    pids_to_remove = [pid for pid in cards_fornos if pid not in new_penas]
                    for pid in pids_to_remove:
                        card_old = cards_fornos.pop(pid)
                        if card_old in grid.controls:
                            grid.controls.remove(card_old)
                    
                    for pid, dados in dados_agrupados.items():
                        valor = float(dados['valor'])
                        cor_temp = get_cor_temperatura(valor)
                        termo = filtro_selecionado["valor"]
                        
                        if pid in cards_fornos:
                            col = cards_fornos[pid].content.content
                            col.controls[1].value = f"{valor:.1f} °C"
                            col.controls[1].color = cor_temp
                            col.controls[2].value = valor / 1200
                            col.controls[2].color = cor_temp
                            col.controls[3].value = f"{t('last_sync')}: {dados['timestamp_local'][0:19]}"
                            cards_fornos[pid].visible = (termo == "Todos" or termo == pid)
                            if cards_fornos[pid].visible and cards_fornos[pid] not in grid.controls:
                                grid.controls.append(cards_fornos[pid])
                            elif not cards_fornos[pid].visible and cards_fornos[pid] in grid.controls:
                                grid.controls.remove(cards_fornos[pid])
                        else:
                            novo_card = ft.Card(
                                elevation=8,
                                content=ft.Container(
                                    padding=20,
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.bottom_right,
                                        colors=[ft.Colors.BLUE_GREY_800, ft.Colors.GREY_900]
                                    ),
                                    border_radius=15,
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.Icons.THERMOSTAT, color="red" ), #deve ser vermelho sempre
                                            ft.Text(pid, size=16, weight="bold", color="white"),
                                            ft.Container(expand=True),
                                            ft.Container(content=ft.Text(t("view_chart"), size=12, color="white")),
                                            ft.IconButton(tooltip=t("view_history"), icon=ft.Icons.MONITOR_HEART_ROUNDED, icon_size=30, icon_color=ft.Colors.BLUE_400, on_click=lambda e, p=pid: chamar_grafico(e, p, id_atual))
                                        ]),
                                        ft.Text(f"{valor:.1f} °C", size=40, color=cor_temp, weight="bold"),
                                        ft.ProgressBar(value=valor/1200, color=cor_temp),
                                        ft.Text(f"{t('last_sync')}: {dados['timestamp_local'][0:19]}", size=10, color=ft.Colors.BLUE_GREY_400),
                                        ft.Row([
                                            ft.Icon(ft.Icons.TIMER, size=14, color=ft.Colors.BLUE_GREY_400),
                                            ft.Text(f"{t('station_interval')}: ({intervalo_str})s", size=10, color=ft.Colors.BLUE_GREY_400)
                                        ], spacing=4)
                                    ])
                                )
                            )
                            cards_fornos[pid] = novo_card
                            novo_card.visible = (termo == "Todos" or termo == pid)
                            if novo_card.visible:
                                grid.controls.append(novo_card)
                
                dropdown_penas.options = [ft.dropdown.Option("Todos", t("all"))] + [ft.dropdown.Option(pid) for pid in cards_fornos.keys()]
                
                visiveis = sum(1 for c in cards_fornos.values() if c.visible)
                count_penas.value = f"{visiveis} {t('equipment') if visiveis == 1 else t('equipments')}"
                
                carregando.visible = False
                garantir_respiro_inferior_grid()
                page.update()
            except Exception as e:
                grid.controls.clear()
                grid.controls.append(card)
                garantir_respiro_inferior_grid()
                cards_fornos.clear()
                carregando.visible = False
                page.update()
                print(f"Erro Sync: {e}")
            
            page.update()
    page.controls.clear()
    page.appbar = appbar
    page.add(
        ft.GestureDetector(
            content=ft.Container(
                content=ft.Column([
                    carregando,
                    loading_grafico,
                    pull_refresh_indicator,
                    conteudo_central
                ], expand=True, spacing=0),
                expand=True
            ),
            drag_interval=25,
            on_vertical_drag_start=pull_to_refresh_start,
            on_vertical_drag_update=pull_to_refresh_update,
            on_vertical_drag_end=pull_to_refresh_end,
            expand=True
        )
    )
    page.update()
    page.run_task(sync_loop)

ft.app(target=main, assets_dir="assets")
