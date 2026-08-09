from PIL import Image


def remover_fundo_preto_exato(input_path, output_path):
    # 1. Abre a imagem e converte para RGBA (necessário para transparência)
    img = Image.open(input_path).convert("RGBA")

    # 2. Converte para uma lista de pixels para processar
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Define o que é "fundo": pixels muito escuros (próximos de 0,0,0)
        # Se os três canais forem próximos de zero, torna o pixel transparente
        if item[0] < 30 and item[1] < 30 and item[2] < 30:
            new_data.append((0, 0, 0, 0))  # Transparente
        else:
            new_data.append(item)  # Mantém a cor original

    # 3. Aplica os novos dados na imagem
    img.putdata(new_data)

    # 4. Salva como PNG
    img.save(output_path, "PNG")
    print(f"Sucesso! Imagem sem fundo salva em: {output_path}")


# Execução
remover_fundo_preto_exato("assets/icon.png", "assets/icon.png")