import dearpygui.dearpygui as dpg
try:
    import utils  # Tenta importar se estiverem na mesma pasta
except ImportError:
    from src import utils  # Tenta se estiver executando da raiz
import numpy as np
from PIL import Image
import os

# --- CONFIGURAÇÃO DE CAMINHOS ---
DATA_DIR = r"D:\reposground\work\projeto-inspecao\data\product_A\train\bad"

def iniciar_verificacao():
    caminho_base = r"D:\reposground\work\projeto-inspecao\data"
    # Chamamos a função do utils.py
    utils.check_dataset_integrity(caminho_base)

def get_image_pairs(directory):
    if not os.path.exists(directory):
        print(f"Erro: Diretório {directory} não encontrado.")
        return []
    files = os.listdir(directory)
    originals = [f for f in files if f.endswith('.bmp')]
    pairs = []
    for org in originals:
        base = os.path.splitext(org)[0]
        mask = base + ".png"
        if mask in files:
            pairs.append({
                "org": os.path.join(directory, org),
                "msk": os.path.join(directory, mask),
                "name": base
            })
    return pairs

samples = get_image_pairs(DATA_DIR)
current_idx = 0

def load_processed_data(idx, alpha):
    """Carrega original e cria uma máscara colorida com alpha"""
    sample = samples[idx]
    
    # Abrir e garantir mesmo tamanho
    img_org_raw = Image.open(sample["org"]).convert("RGBA")
    img_msk_raw = Image.open(sample["msk"]).convert("RGBA").resize(img_org_raw.size)
    
    # Converter para Numpy (0.0 a 1.0)
    arr_org = np.array(img_org_raw, dtype=np.float32) / 255.0
    arr_msk = np.array(img_msk_raw, dtype=np.float32) / 255.0
    
    # Criar a sobreposição: Pintar a máscara de Vermelho (R=1, G=0, B=0)
    # Usamos o brilho da máscara original para definir onde o vermelho aparece
    overlay = np.zeros_like(arr_org)
    overlay[:, :, 0] = 1.0  # Canal Vermelho
    overlay[:, :, 3] = arr_msk[:, :, 0] * alpha  # Transparência baseada no slider
    
    return img_org_raw.width, img_org_raw.height, arr_org.flatten(), overlay.flatten()

# --- CALLBACKS ---
def update_ui():
    alpha = dpg.get_value("slider_alpha")
    w, h, data_org, data_ovl = load_processed_data(current_idx, alpha)
    
    dpg.set_value("tex_org", data_org)
    dpg.set_value("tex_ovl", data_ovl)
    dpg.set_value("txt_status", f"Amostra: {samples[current_idx]['name']} ({current_idx+1}/{len(samples)})")

def on_next(sender, app_data):
    global current_idx
    current_idx = (current_idx + 1) % len(samples)
    update_ui()

def on_prev(sender, app_data):
    global current_idx
    current_idx = (current_idx - 1) % len(samples)
    update_ui()

# --- INTERFACE DEAR PYGUI ---
dpg.create_context()

# Carregar dados iniciais para configurar texturas
w_init, h_init, d_org_init, d_ovl_init = load_processed_data(0, 0.5)

with dpg.texture_registry():
    dpg.add_dynamic_texture(width=w_init, height=h_init, default_value=d_org_init, tag="tex_org")
    dpg.add_dynamic_texture(width=w_init, height=h_init, default_value=d_ovl_init, tag="tex_ovl")

with dpg.window(label="Inspetor Industrial v2.0", width=900, height=900):
    dpg.add_text("Análise de Defeitos com Sobreposição Alpha", color=[0, 255, 0])
    dpg.add_text("", tag="txt_status")
    
    with dpg.group(horizontal=True):
        dpg.add_button(label="<< ANTERIOR", callback=on_prev, width=100)
        dpg.add_button(label="PRÓXIMO >>", callback=on_next, width=100)
    
    dpg.add_spacer(height=10)
    dpg.add_slider_float(label="Intensidade da Máscara", tag="slider_alpha", 
                         default_value=0.5, max_value=1.0, callback=update_ui)
    
    dpg.add_separator()
    
    # Aqui a mágica: Desenhamos uma imagem sobre a outra
    with dpg.drawlist(width=800, height=800):
        dpg.draw_image("tex_org", [0, 0], [800, 800])
        dpg.draw_image("tex_ovl", [0, 0], [800, 800])

dpg.create_viewport(title='DPG Rookie Lab - Alpha Blending', width=950, height=950)
dpg.setup_dearpygui()
dpg.show_viewport()
update_ui() # Força primeira atualização
dpg.start_dearpygui()
dpg.destroy_context()

# No final do arquivo, antes de iniciar o dpg.start_dearpygui()
if __name__ == "__main__":
    iniciar_verificacao()
    # dpg.start_dearpygui()...