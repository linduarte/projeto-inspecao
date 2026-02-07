import os

def check_dataset_integrity(base_path):
    """
    Varre o dataset procurando por imagens (.bmp) sem máscara (.png).
    Gera um log detalhado em 'integrity_log.txt'.
    """
    # 1. Inicializamos a lista de erros de verdade
    lista_de_erros = [] 
    relatorio_texto = []

    relatorio_texto.append("RELATÓRIO DE INTEGRIDADE - DATASET INDUSTRIAL")
    relatorio_texto.append(f"Caminho: {base_path}\n" + "="*40 + "\n")

    if not os.path.exists(base_path):
        msg = f"[ERRO CRÍTICO] Caminho base não encontrado: {base_path}"
        print(msg)
        lista_de_erros.append(msg)
    else:
        # Pega as pastas de produtos (ex: product_A)
        products = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        
        for product in products:
            target_dir = os.path.join(base_path, product, "train", "bad")
            if not os.path.exists(target_dir):
                continue

            files = os.listdir(target_dir)
            originals = [f for f in files if f.endswith('.bmp')]
            masks = [f for f in files if f.endswith('.png')]
            
            for org in originals:
                base_name = os.path.splitext(org)[0]
                if f"{base_name}.png" not in masks:
                    msg_erro = f"Produto: {product} | Faltando máscara para: {org}"
                    lista_de_erros.append(msg_erro)
                    relatorio_texto.append(msg_erro)

    # 2. Escrita do Arquivo de Log
    try:
        with open("integrity_log.txt", "w", encoding="utf-8") as f:
            for linha in relatorio_texto:
                f.write(linha + "\n")
            
            if not lista_de_erros:
                f.write("\n✅ Nenhum erro de integridade encontrado.")
            else:
                f.write(f"\n❌ Total de erros: {len(lista_de_erros)}")
        
        print(f"✅ Auditoria finalizada. Erros encontrados: {len(lista_de_erros)}")
        print("📝 Detalhes salvos em: integrity_log.txt")
        
    except Exception as e:
        print(f"⚠️ Erro ao salvar o log: {e}")

    return len(lista_de_erros) == 0 # Retorna True se estiver tudo OK

if __name__ == "__main__":
    # Teste rápido apontando para o seu diretório real
    CAMINHO = r"D:\reposground\work\projeto-inspecao\data"
    check_dataset_integrity(CAMINHO)