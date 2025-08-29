import tkinter as tk
from tkinter import ttk, messagebox
import random
import csv
import json
import sys
import os
import sv_ttk
from datetime import datetime

# Dicionário de cores para as raridades
CORES_RARIDADE = {
    "Comum": "gray",
    "Incomum": "#4CAF50",
    "Raro": "#2196F3",
    "Épico": "#9C27B0",
    "Lendário": "#FF9800"
}

# --- FUNÇÃO PARA ENCONTRAR ARQUIVOS ---
def obter_caminho(nome_arquivo):
    # Esta função garante que os arquivos sejam encontrados, tanto no modo de desenvolvimento quanto no executável
    if hasattr(sys, '_MEIPASS'):
        caminho_base = sys._MEIPASS
    else:
        caminho_base = os.path.abspath(".")
    return os.path.join(caminho_base, nome_arquivo)

# --- Funções de Carregamento e Salvamento ---
def carregar_loot_geral(nome_arquivo):
    lista_completa = []
    try:
        with open(obter_caminho(nome_arquivo), 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for linha in leitor:
                if any(field.strip() for field in linha.values()):
                    lista_completa.append(linha)
            return lista_completa
    except FileNotFoundError:
        with open(obter_caminho(nome_arquivo), 'w', newline='', encoding='utf-8') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(['nome_item', 'raridade'])
        return []
    except Exception as e:
        messagebox.showerror("Erro Crítico", f"Não foi possível ler o arquivo '{nome_arquivo}':\n{e}")
        return []

def salvar_loot_geral():
    try:
        with open(obter_caminho('loot_geral.csv'), 'w', newline='', encoding='utf-8') as arquivo_csv:
            if not LISTA_DE_LOOT_GLOBAL:
                escritor = csv.writer(arquivo_csv)
                escritor.writerow(['nome_item', 'raridade'])
                return
            fieldnames = ['nome_item', 'raridade']
            escritor = csv.DictWriter(arquivo_csv, fieldnames=fieldnames)
            escritor.writeheader()
            escritor.writerows(LISTA_DE_LOOT_GLOBAL)
    except Exception as e:
        messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar as alterações no 'loot_geral.csv':\n{e}")

def carregar_parametros(nome_arquivo):
    try:
        with open(obter_caminho(nome_arquivo), 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Comum": 65, "Incomum": 20, "Raro": 10, "Épico": 4, "Lendário": 1}

def salvar_parametros():
    novos_pesos = {
        "Comum": var_peso_comum.get(), "Incomum": var_peso_incomum.get(),
        "Raro": var_peso_raro.get(), "Épico": var_peso_epico.get(),
        "Lendário": var_peso_lendario.get()
    }
    with open(obter_caminho('parametros.json'), 'w', encoding='utf-8') as f:
        json.dump(novos_pesos, f, indent=2)
    resultado_texto.config(state=tk.NORMAL)
    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert("1.0", "Pesos salvos com sucesso!")
    resultado_texto.config(state=tk.DISABLED)

def salvar_historico():
    # Esta função precisa de uma lógica para não salvar o texto padrão
    recompensas_content = resultado_texto.get("1.0", tk.END).strip()
    rolagens_content = resultado_dados_texto.get("1.0", tk.END).strip()

    dados_historico = {
        "recompensas": recompensas_content if "aparecerá aqui" not in recompensas_content else "",
        "rolagens": rolagens_content if "aparecerá aqui" not in rolagens_content else ""
    }
    with open(obter_caminho('historico.json'), 'w', encoding='utf-8') as f:
        json.dump(dados_historico, f, indent=2)

def carregar_historico():
    try:
        if not os.path.exists(obter_caminho('historico.json')):
            return # Não faz nada se o arquivo de histórico não existe

        with open(obter_caminho('historico.json'), 'r', encoding='utf-8') as f:
            dados_historico = json.load(f)
            conteudo_recompensas = dados_historico.get("recompensas", "")
            resultado_texto.config(state=tk.NORMAL)
            resultado_texto.delete("1.0", tk.END)
            resultado_texto.insert("1.0", conteudo_recompensas or "O resultado da recompensa aparecerá aqui.")
            resultado_texto.config(state=tk.DISABLED)
            
            conteudo_rolagens = dados_historico.get("rolagens", "")
            resultado_dados_texto.config(state=tk.NORMAL)
            resultado_dados_texto.delete("1.0", tk.END)
            resultado_dados_texto.insert("1.0", conteudo_rolagens or "O resultado das rolagens aparecerá aqui...")
            resultado_dados_texto.config(state=tk.DISABLED)

    except (FileNotFoundError, json.JSONDecodeError):
        pass # Silenciosamente ignora se o arquivo estiver corrompido ou não for encontrado

# --- Lógica de Geração ---
def gerar_recompensa_completa():
    raridades_config = {
        "Comum": {"check": var_comum.get(), "peso": var_peso_comum.get()},
        "Incomum": {"check": var_incomum.get(), "peso": var_peso_incomum.get()},
        "Raro": {"check": var_raro.get(), "peso": var_peso_raro.get()},
        "Épico": {"check": var_epico.get(), "peso": var_peso_epico.get()},
        "Lendário": {"check": var_lendario.get(), "peso": var_peso_lendario.get()}
    }
    if not LISTA_DE_LOOT_GLOBAL:
        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert("1.0", "ERRO: 'loot_geral.csv' está vazio.\nAdicione itens na aba 'Manter Itens'.")
        resultado_texto.config(state=tk.DISABLED)
        return
    
    piscina_de_itens_filtrada = []
    pesos_dos_itens_filtrados = []
    for item in LISTA_DE_LOOT_GLOBAL:
        raridade = item.get('raridade')
        if raridade and raridades_config.get(raridade, {}).get("check") and raridades_config.get(raridade, {}).get("peso", 0) > 0:
            piscina_de_itens_filtrada.append(item)
            pesos_dos_itens_filtrados.append(raridades_config[raridade]["peso"])
    if not piscina_de_itens_filtrada:
        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert("1.0", "Nenhum item disponível para sorteio.\nVerifique as raridades selecionadas, seus pesos e se existem itens cadastrados para elas.")
        resultado_texto.config(state=tk.DISABLED)
        return
    
    quantidade_itens = var_quantidade_itens.get()
    itens_sorteados_final = []
    if quantidade_itens > 0:
        itens_sorteados_final = random.choices(piscina_de_itens_filtrada, weights=pesos_dos_itens_filtrados, k=quantidade_itens)
    
    resultado_texto.config(state=tk.NORMAL)
    resultado_texto.delete("1.0", tk.END)
    if itens_sorteados_final:
        resultado_texto.insert(tk.END, "Itens Sorteados:\n")
        for item in itens_sorteados_final:
            raridade = item['raridade']
            linha = f"- {item['nome_item']} ({raridade})\n"
            resultado_texto.insert(tk.END, linha, raridade)
    min_val, max_val = var_min_moedas.get(), var_max_moedas.get()
    if min_val > max_val: min_val, max_val = max_val, min_val
    quantidade_gerada = random.randint(min_val, max_val)
    if quantidade_gerada > 0:
        if itens_sorteados_final:
            resultado_texto.insert(tk.END, "\n") 
        resultado_texto.insert(tk.END, f"Moedas (LMD): {quantidade_gerada}")
    if not itens_sorteados_final and quantidade_gerada == 0:
        resultado_texto.insert(tk.END, "Nada foi gerado. Verifique a quantidade de itens ou o range de moedas.")
    resultado_texto.config(state=tk.DISABLED)
    janela.focus_set()

# --- Funções CRUD ---
def atualizar_treeview_loot(filtro=""):
    for i in tree_loot.get_children():
        tree_loot.delete(i)
    lista_para_exibir = sorted(LISTA_DE_LOOT_GLOBAL, key=lambda item: item['nome_item'])
    if filtro:
        filtro = filtro.lower()
        lista_filtrada = [item for item in lista_para_exibir if filtro in item['nome_item'].lower()]
        lista_para_exibir = lista_filtrada
    iids_usados = set()
    for item in lista_para_exibir:
        raridade = item['raridade']
        nome_base = item['nome_item']
        iid_final = nome_base
        sufixo_contador = 2
        while iid_final in iids_usados:
            iid_final = f"{nome_base}_{sufixo_contador}"
            sufixo_contador += 1
        iids_usados.add(iid_final)
        tree_loot.insert("", "end", iid=iid_final, values=(item['nome_item'], raridade), tags=(raridade,))

def on_item_selecionado(event):
    if not tree_loot.selection(): return
    selecionado_id = tree_loot.selection()[0]
    item_dict = tree_loot.item(selecionado_id)
    if not item_dict['values']: return
    nome, raridade = item_dict['values']
    var_nome_item_crud.set(nome)
    var_raridade_item_crud.set(raridade)

# ### MUDANÇA ### - Função de limpar campos agora tem a opção de manter a raridade
def limpar_campos_crud(manter_raridade=False):
    var_nome_item_crud.set("")
    if not manter_raridade:
        var_raridade_item_crud.set("")
    if tree_loot.selection():
        tree_loot.selection_remove(tree_loot.selection()[0])
    entry_nome_crud.focus_set() # Põe o foco no campo de nome

def adicionar_item():
    nome = var_nome_item_crud.get().strip()
    raridade = var_raridade_item_crud.get()
    if not nome or not raridade:
        messagebox.showerror("Campos Vazios", "O nome e a raridade do item não podem estar vazios.")
        return
    # ### MUDANÇA ### - Validação para impedir nomes que começam com número
    if nome[0].isdigit():
        messagebox.showerror("Nome Inválido", "O nome do item não pode começar com um número.")
        return
    for item in LISTA_DE_LOOT_GLOBAL:
        if item['nome_item'].lower() == nome.lower():
            messagebox.showwarning("Item Duplicado", f"O item '{nome}' já existe na lista.")
            return
    LISTA_DE_LOOT_GLOBAL.append({"nome_item": nome, "raridade": raridade})
    salvar_loot_geral()
    atualizar_treeview_loot(filtro=var_filtro_itens.get())
    # ### MUDANÇA ### - Chama a limpeza mantendo a raridade
    limpar_campos_crud(manter_raridade=True)

def salvar_edicao_item():
    if not tree_loot.selection():
        messagebox.showwarning("Nenhum Item", "Selecione um item na lista para editar.")
        return
    selecionado_id = tree_loot.selection()[0]
    item_original = tree_loot.item(selecionado_id)['values'][0]
    novo_nome = var_nome_item_crud.get().strip()
    nova_raridade = var_raridade_item_crud.get()
    if not novo_nome or not nova_raridade:
        messagebox.showerror("Campos Vazios", "O nome e a raridade não podem estar vazios.")
        return
    # ### MUDANÇA ### - Validação para impedir nomes que começam com número
    if novo_nome[0].isdigit():
        messagebox.showerror("Nome Inválido", "O nome do item não pode começar com um número.")
        return
    for item in LISTA_DE_LOOT_GLOBAL:
        if item['nome_item'] == item_original:
            item['nome_item'] = novo_nome
            item['raridade'] = nova_raridade
            break
    salvar_loot_geral()
    atualizar_treeview_loot(filtro=var_filtro_itens.get())
    limpar_campos_crud(manter_raridade=True)
    
def excluir_item():
    if not tree_loot.selection():
        messagebox.showwarning("Nenhum Item", "Selecione um item na lista para excluir.")
        return
    selecionado_id = tree_loot.selection()[0]
    nome_para_excluir = tree_loot.item(selecionado_id)['values'][0]
    if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o item '{nome_para_excluir}'?"):
        item_para_remover = None
        for item in LISTA_DE_LOOT_GLOBAL:
            if item['nome_item'] == nome_para_excluir:
                item_para_remover = item
                break
        if item_para_remover:
            LISTA_DE_LOOT_GLOBAL.remove(item_para_remover)
            salvar_loot_geral()
            atualizar_treeview_loot(filtro=var_filtro_itens.get())
            limpar_campos_crud()
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar o item para excluir.")

def ordenar_coluna(tree, col, reverse):
    lista_para_ordenar = [(tree.set(k, col), k) for k in tree.get_children('')]
    lista_para_ordenar.sort(reverse=reverse)
    for index, (val, k) in enumerate(lista_para_ordenar):
        tree.move(k, '', index)
    arrow = '▼' if reverse else '▲'
    for c in tree['columns']:
        original_text = c.replace('_', ' ').title()
        if c != col:
             tree.heading(c, text=original_text, command=lambda c=c: ordenar_coluna(tree, c, False))
        else:
            tree.heading(col, text=f"{original_text} {arrow}", command=lambda: ordenar_coluna(tree, col, not reverse))

def logar_rolagem_em_arquivo(texto_log):
    with open(obter_caminho('rolagens_log.txt'), 'a', encoding='utf-8') as f:
        f.write(texto_log + "\n")

def chamar_rolagem(lados):
    try:
        quantidade = var_quantidade_dados.get()
        if quantidade <= 0 or lados <= 0:
            messagebox.showwarning("Valor Inválido", "A quantidade e os lados do dado devem ser maiores que zero.")
            return
        rolagens = [random.randint(1, lados) for _ in range(quantidade)]
        soma = sum(rolagens)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        resultado_str = f"[{timestamp}] Rolando {quantidade}d{lados}: {rolagens} -> Total: {soma}"
        logar_rolagem_em_arquivo(resultado_str)
        resultado_dados_texto.config(state=tk.NORMAL)
        conteudo_atual = resultado_dados_texto.get("1.0", tk.END)
        resultado_dados_texto.delete("1.0", tk.END)
        resultado_dados_texto.insert("1.0", resultado_str + "\n" + conteudo_atual.lstrip('\n'))
        resultado_dados_texto.config(state=tk.DISABLED)
        janela.focus_set()
    except tk.TclError:
        messagebox.showerror("Erro de Entrada", "Por favor, insira um número válido.")

def limpar_log_rolagens():
    if messagebox.askyesno("Confirmar Limpeza", "Tem certeza que deseja apagar todo o log de rolagens da tela e do arquivo 'rolagens_log.txt'?"):
        resultado_dados_texto.config(state=tk.NORMAL)
        resultado_dados_texto.delete("1.0", tk.END)
        resultado_dados_texto.insert("1.0", "Log limpo. O resultado das rolagens aparecerá aqui...")
        resultado_dados_texto.config(state=tk.DISABLED)
        try:
            with open(obter_caminho('rolagens_log.txt'), 'w', encoding='utf-8') as f:
                f.write(f"Log limpo em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível limpar o arquivo de log:\n{e}")
        salvar_historico()

def on_enter_no_campo_nome(event):
    """Verifica se um item está selecionado para decidir entre salvar a edição ou adicionar um novo item."""
    if tree_loot.selection():
        salvar_edicao_item()
    else:
        adicionar_item()

def on_delete_key(event):
    excluir_item()

# --- Início do Programa e Interface Gráfica ---
LISTA_DE_LOOT_GLOBAL = carregar_loot_geral('loot_geral.csv')
PESOS_INICIAIS = carregar_parametros('parametros.json')

janela = tk.Tk()
janela.title("Morikawa Loot")
try:
    caminho_icone = obter_caminho('icone.ico')
    janela.iconbitmap(caminho_icone)
except tk.TclError:
    print("Aviso: Arquivo 'icone.ico' não encontrado. Usando ícone padrão.")
except Exception as e:
    print(f"Erro ao carregar ícone: {e}")


janela.geometry("600x800")
janela.minsize(550, 700)
janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

sv_ttk.set_theme("dark")
def alternar_tema():
    if sv_ttk.get_theme() == "light":
        sv_ttk.set_theme("dark")
    else:
        sv_ttk.set_theme("light")

notebook = ttk.Notebook(janela)
notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

frame_botoes_tema = ttk.Frame(janela)
frame_botoes_tema.grid(row=1, column=0, sticky="e", padx=10, pady=(0, 10))
botao_tema = ttk.Button(frame_botoes_tema, text="Alternar Tema", command=alternar_tema)
botao_tema.pack()

# --- Aba 1: Gerador de Recompensa ---
tab_sorteio = ttk.Frame(notebook)
notebook.add(tab_sorteio, text='Gerador de Recompensa')
var_comum = tk.BooleanVar(value=True); var_incomum = tk.BooleanVar(value=True); var_raro = tk.BooleanVar(value=True); var_epico = tk.BooleanVar(value=False); var_lendario = tk.BooleanVar(value=False)
var_peso_comum = tk.IntVar(value=PESOS_INICIAIS.get("Comum", 65)); var_peso_incomum = tk.IntVar(value=PESOS_INICIAIS.get("Incomum", 20)); var_peso_raro = tk.IntVar(value=PESOS_INICIAIS.get("Raro", 10)); var_peso_epico = tk.IntVar(value=PESOS_INICIAIS.get("Épico", 4)); var_peso_lendario = tk.IntVar(value=PESOS_INICIAIS.get("Lendário", 1))
var_quantidade_itens = tk.IntVar(value=1)
var_min_moedas = tk.IntVar(value=1)
var_max_moedas = tk.IntVar(value=100)
frame_configs = ttk.LabelFrame(tab_sorteio, text="1. Configure as Probabilidades (Pesos)", padding="10")
frame_configs.pack(fill=tk.X, pady=5, padx=5, side=tk.TOP)
ttk.Label(frame_configs, text="Incluir?").grid(row=0, column=0); ttk.Label(frame_configs, text="Raridade").grid(row=0, column=1); ttk.Label(frame_configs, text="Peso").grid(row=0, column=2)
ttk.Checkbutton(frame_configs, variable=var_comum).grid(row=1, column=0); ttk.Label(frame_configs, text="Comum").grid(row=1, column=1); ttk.Spinbox(frame_configs, from_=0, to=1000, textvariable=var_peso_comum, width=5).grid(row=1, column=2)
ttk.Checkbutton(frame_configs, variable=var_incomum).grid(row=2, column=0); ttk.Label(frame_configs, text="Incomum").grid(row=2, column=1); ttk.Spinbox(frame_configs, from_=0, to=1000, textvariable=var_peso_incomum, width=5).grid(row=2, column=2)
ttk.Checkbutton(frame_configs, variable=var_raro).grid(row=3, column=0); ttk.Label(frame_configs, text="Raro").grid(row=3, column=1); ttk.Spinbox(frame_configs, from_=0, to=1000, textvariable=var_peso_raro, width=5).grid(row=3, column=2)
ttk.Checkbutton(frame_configs, variable=var_epico).grid(row=4, column=0); ttk.Label(frame_configs, text="Épico").grid(row=4, column=1); ttk.Spinbox(frame_configs, from_=0, to=1000, textvariable=var_peso_epico, width=5).grid(row=4, column=2)
ttk.Checkbutton(frame_configs, variable=var_lendario).grid(row=5, column=0); ttk.Label(frame_configs, text="Lendário").grid(row=5, column=1); ttk.Spinbox(frame_configs, from_=0, to=1000, textvariable=var_peso_lendario, width=5).grid(row=5, column=2)
ttk.Button(frame_configs, text="Salvar Pesos como Padrão", command=salvar_parametros).grid(row=6, column=1, columnspan=2, pady=10)
frame_quantidades = ttk.LabelFrame(tab_sorteio, text="2. Escolha as Quantidades", padding="10")
frame_quantidades.pack(fill=tk.X, pady=10, padx=5, side=tk.TOP)
ttk.Label(frame_quantidades, text="Qtd. Itens:").grid(row=0, column=0, padx=5, pady=5)
ttk.Spinbox(frame_quantidades, from_=0, to=20, textvariable=var_quantidade_itens, width=5).grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_quantidades, text="Min Moedas:").grid(row=1, column=0, padx=5, pady=5)
ttk.Spinbox(frame_quantidades, from_=0, to=10000, textvariable=var_min_moedas, width=8).grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_quantidades, text="Max Moedas:").grid(row=1, column=2, padx=5, pady=5)
ttk.Spinbox(frame_quantidades, from_=0, to=10000, textvariable=var_max_moedas, width=8).grid(row=1, column=3, padx=5, pady=5)
frame_botoes_sorteio = ttk.Frame(tab_sorteio)
frame_botoes_sorteio.pack(pady=10, side=tk.TOP)
botao_sortear_tudo = ttk.Button(frame_botoes_sorteio, text="Gerar Recompensa Completa!", command=gerar_recompensa_completa)
botao_sortear_tudo.pack(side=tk.LEFT, padx=5)
resultado_texto = tk.Text(tab_sorteio, height=10, wrap="word", relief="flat", borderwidth=0, font=("Segoe UI", 11))
resultado_texto.pack(pady=10, padx=5, fill="both", expand=True, side=tk.TOP)
for raridade, cor in CORES_RARIDADE.items():
    resultado_texto.tag_configure(raridade, foreground=cor)
resultado_texto.config(state=tk.DISABLED)

# --- Aba 2: Manter Itens ---
tab_manter_loot = ttk.Frame(notebook)
notebook.add(tab_manter_loot, text='Manter Itens')
tab_manter_loot.columnconfigure(0, weight=1)
tab_manter_loot.rowconfigure(1, weight=1)
var_filtro_itens = tk.StringVar()
frame_filtro = ttk.LabelFrame(tab_manter_loot, text="Busca", padding=10)
frame_filtro.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
ttk.Label(frame_filtro, text="Filtrar por nome:").pack(side=tk.LEFT, padx=(0,5))
entry_filtro = ttk.Entry(frame_filtro, textvariable=var_filtro_itens)
entry_filtro.pack(fill="x", expand=True)
def aplicar_filtro(*args):
    atualizar_treeview_loot(filtro=var_filtro_itens.get())
var_filtro_itens.trace_add("write", aplicar_filtro)
frame_lista = ttk.LabelFrame(tab_manter_loot, text="Lista de Itens", padding=10)
frame_lista.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
frame_lista.rowconfigure(0, weight=1)
frame_lista.columnconfigure(0, weight=1)
cols = ('nome_item', 'raridade')
tree_loot = ttk.Treeview(frame_lista, columns=cols, show='headings', height=10)
tree_loot.grid(row=0, column=0, sticky="nsew")
tree_loot.column('nome_item', width=300)
tree_loot.column('raridade', width=100, anchor=tk.CENTER)
scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree_loot.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
tree_loot.configure(yscrollcommand=scrollbar.set)
tree_loot.heading('nome_item', text='Nome Item', command=lambda: ordenar_coluna(tree_loot, 'nome_item', False))
tree_loot.heading('raridade', text='Raridade', command=lambda: ordenar_coluna(tree_loot, 'raridade', False))
for raridade, cor in CORES_RARIDADE.items():
    tree_loot.tag_configure(raridade, foreground=cor)
frame_formulario = ttk.LabelFrame(tab_manter_loot, text="Adicionar / Editar Item", padding=10)
frame_formulario.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
var_nome_item_crud = tk.StringVar()
var_raridade_item_crud = tk.StringVar()
ttk.Label(frame_formulario, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nome_crud = ttk.Entry(frame_formulario, textvariable=var_nome_item_crud, width=40)
entry_nome_crud.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Label(frame_formulario, text="Raridade:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
combo_raridade_crud = ttk.Combobox(frame_formulario, textvariable=var_raridade_item_crud, 
                                     values=['Comum', 'Incomum', 'Raro', 'Épico', 'Lendário'], state="readonly")
combo_raridade_crud.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
frame_formulario.columnconfigure(1, weight=1)
frame_botoes_crud = ttk.Frame(tab_manter_loot, padding=5)
frame_botoes_crud.grid(row=3, column=0, padx=5, sticky="ew")
# ### MUDANÇA ### - O botão de limpar campos agora limpa a raridade também
ttk.Button(frame_botoes_crud, text="Adicionar Novo", command=adicionar_item).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
ttk.Button(frame_botoes_crud, text="Salvar Edição", command=salvar_edicao_item).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
ttk.Button(frame_botoes_crud, text="Excluir Selecionado", command=excluir_item).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
ttk.Button(frame_botoes_crud, text="Limpar Campos", command=limpar_campos_crud).pack(side=tk.LEFT, expand=True, fill='x', padx=5)

# --- Aba 3: Rolar Dados ---
tab_dados = ttk.Frame(notebook)
notebook.add(tab_dados, text='Rolar Dados')
var_quantidade_dados = tk.IntVar(value=1)
var_lados_custom = tk.IntVar(value=6)
frame_quantidade_dados = ttk.LabelFrame(tab_dados, text="1. Quantidade de Dados", padding=10)
frame_quantidade_dados.pack(pady=10, padx=10, fill="x")
ttk.Label(frame_quantidade_dados, text="Rodar:").pack(side=tk.LEFT, padx=(0,5))
ttk.Spinbox(frame_quantidade_dados, from_=1, to=100, textvariable=var_quantidade_dados, width=5).pack(side=tk.LEFT)
ttk.Label(frame_quantidade_dados, text="dado(s)").pack(side=tk.LEFT, padx=(5,0))
frame_dados_padrao = ttk.LabelFrame(tab_dados, text="2. Dados Padrão", padding=10)
frame_dados_padrao.pack(pady=5, padx=10, fill="x")
botoes_dados_info = [4, 6, 8, 10, 12, 20, 100]
coluna_atual = 0
for lados in botoes_dados_info:
    botao = ttk.Button(frame_dados_padrao, text=f"d{lados}", command=lambda l=lados: chamar_rolagem(l))
    botao.grid(row=0, column=coluna_atual, padx=5, pady=5, sticky="ew")
    frame_dados_padrao.columnconfigure(coluna_atual, weight=1)
    coluna_atual += 1
frame_dado_custom = ttk.LabelFrame(tab_dados, text="3. Dado Personalizado (d?)", padding=10)
frame_dado_custom.pack(pady=5, padx=10, fill="x")
ttk.Label(frame_dado_custom, text="Lados:").pack(side=tk.LEFT, padx=(0,5))
ttk.Spinbox(frame_dado_custom, from_=2, to=1000, textvariable=var_lados_custom, width=8).pack(side=tk.LEFT, expand=True, fill="x")
ttk.Button(frame_dado_custom, text="Rolar!", command=lambda: chamar_rolagem(var_lados_custom.get())).pack(side=tk.LEFT, padx=(10,0))
frame_resultado_dados = ttk.LabelFrame(tab_dados, text="Resultados", padding=10)
frame_resultado_dados.pack(pady=10, padx=10, fill="both", expand=True)
frame_log_botoes = ttk.Frame(frame_resultado_dados)
frame_log_botoes.pack(fill='x', pady=(0, 5))
ttk.Button(frame_log_botoes, text="Limpar Log de Rolagens", command=limpar_log_rolagens).pack(side='right')
resultado_dados_texto = tk.Text(frame_resultado_dados, height=10, wrap="word", relief="flat", borderwidth=0, font=("Segoe UI", 11))
resultado_dados_texto.pack(fill="both", expand=True)
resultado_dados_texto.config(state=tk.DISABLED)

# --- Finalização ---
tree_loot.bind("<<TreeviewSelect>>", on_item_selecionado)
tree_loot.bind("<Delete>", on_delete_key)
# ### MUDANÇA ### - Adiciona o atalho da tecla Enter para o campo de nome do item
entry_nome_crud.bind("<Return>", on_enter_no_campo_nome)
atualizar_treeview_loot()
carregar_historico()
def ao_fechar():
    salvar_historico()
    janela.destroy()
janela.protocol("WM_DELETE_WINDOW", ao_fechar)
janela.mainloop()