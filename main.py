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

def carregar_itens_exemplo():
    """Adiciona itens de exemplo para demonstrar o sistema"""
    itens_exemplo = [
        {"nome_item": "Espada Longa", "raridade": "Comum"},
        {"nome_item": "Escudo de Ferro", "raridade": "Comum"},
        {"nome_item": "Adaga Afiada", "raridade": "Incomum"},
        {"nome_item": "Armadura de Couro", "raridade": "Incomum"},
        {"nome_item": "Elmo Mágico", "raridade": "Raro"},
        {"nome_item": "Botas Élfica", "raridade": "Raro"},
        {"nome_item": "Cajado Arcano", "raridade": "Épico"},
        {"nome_item": "Colar de Proteção", "raridade": "Épico"},
        {"nome_item": "Espada Flamejante", "raridade": "Lendário"},
        {"nome_item": "Anel do Poder", "raridade": "Lendário"}
    ]
    
    if messagebox.askyesno("Carregar Itens de Exemplo", 
                          "Deseja carregar 10 itens de exemplo para testar o sistema?\n\n"
                          "Isso adicionará espadas, escudos, armaduras e outros itens de várias raridades."):
        for item in itens_exemplo:
            # Verifica se o item já existe antes de adicionar
            existe = any(i['nome_item'].lower() == item['nome_item'].lower() for i in LISTA_DE_LOOT_GLOBAL)
            if not existe:
                LISTA_DE_LOOT_GLOBAL.append(item)
        
        salvar_loot_geral()
        atualizar_treeview_loot(filtro=var_filtro_itens.get())
        messagebox.showinfo("Sucesso", f"Itens de exemplo carregados com sucesso!\nAgora você pode testar o gerador de recompensas.")

def carregar_parametros(nome_arquivo):
    try:
        with open(obter_caminho(nome_arquivo), 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Se o arquivo tem a nova estrutura completa
        if "pesos_raridade" in dados:
            pesos_raridade = dados["pesos_raridade"]
            pesos_qualidade = dados.get("pesos_qualidade", {
                "Condição impecável (+2)": 5,
                "Levemente marcado (+1)": 15,
                "Normal (+0)": 50,
                "Bem usado (-1)": 20,
                "Desgastado (-2)": 10
            })
            atributos_dinamicos = dados.get("atributos_dinamicos", {
                "adicionar_cor": True,
                "chance_encantamento": True,
                "porcentagem_encantamento": 30,
                "adicionar_qualidade": True,
                "gerar_moedas": True
            })
            return pesos_raridade, pesos_qualidade, atributos_dinamicos
        else:
            # Compatibilidade com versão antiga
            return dados, {
                "Condição impecável (+2)": 5,
                "Levemente marcado (+1)": 15,
                "Normal (+0)": 50,
                "Bem usado (-1)": 20,
                "Desgastado (-2)": 10
            }, {
                "adicionar_cor": True,
                "chance_encantamento": True,
                "porcentagem_encantamento": 30,
                "adicionar_qualidade": True,
                "gerar_moedas": True
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Comum": 65, "Incomum": 20, "Raro": 10, "Épico": 4, "Lendário": 1}, {
            "Condição impecável (+2)": 5,
            "Levemente marcado (+1)": 15,
            "Normal (+0)": 50,
            "Bem usado (-1)": 20,
            "Desgastado (-2)": 10
        }, {
            "adicionar_cor": True,
            "chance_encantamento": True,
            "porcentagem_encantamento": 30,
            "adicionar_qualidade": True,
            "gerar_moedas": True
        }

def salvar_parametros():
    novos_pesos = {
        "Comum": var_peso_comum.get(), "Incomum": var_peso_incomum.get(),
        "Raro": var_peso_raro.get(), "Épico": var_peso_epico.get(),
        "Lendário": var_peso_lendario.get()
    }
    pesos_qualidades = {
        "Condição impecável (+2)": var_peso_impecavel.get(),
        "Levemente marcado (+1)": var_peso_levemente_marcado.get(),
        "Normal (+0)": var_peso_normal.get(),
        "Bem usado (-1)": var_peso_bem_usado.get(),
        "Desgastado (-2)": var_peso_desgastado.get()
    }
    atributos_dinamicos = {
        "adicionar_cor": var_adicionar_cor.get(),
        "chance_encantamento": var_chance_encantamento.get(),
        "porcentagem_encantamento": var_porcentagem_encantamento.get(),
        "adicionar_qualidade": var_adicionar_qualidade.get(),
        "gerar_moedas": var_gerar_moedas.get()
    }
    parametros_completos = {
        "pesos_raridade": novos_pesos,
        "pesos_qualidade": pesos_qualidades,
        "atributos_dinamicos": atributos_dinamicos
    }
    
    try:
        with open(obter_caminho('parametros.json'), 'w', encoding='utf-8') as f:
            json.dump(parametros_completos, f, indent=2, ensure_ascii=False)
        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert("1.0", "✅ Todas as configurações foram salvas com sucesso!")
        resultado_texto.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar os parâmetros:\n{e}")

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

def limpar_historico():
    """Limpa todo o histórico de recompensas e rolagens"""
    resposta = messagebox.askyesno("Limpar Histórico", 
                                  "Deseja limpar todo o histórico?\n\n"
                                  "Isso apagará:\n"
                                  "• Todas as recompensas geradas\n"
                                  "• Todos os logs de rolagem de dados\n\n"
                                  "Esta ação não pode ser desfeita.")
    if resposta:
        # Limpar textos na interface
        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert("1.0", "🎮 Bem-vindo ao Morikawa Loot Generator!\n\n"
                                      "🎯 Suas recompensas aparecerão aqui.\n\n"
                                      "✨ Configure as opções acima\n"
                                      "🚀 Clique em 'Gerar Recompensa Completa'\n\n"
                                      "💡 Use 'Manter Itens' para adicionar exemplos")
        resultado_texto.config(state=tk.DISABLED)
        
        resultado_dados_texto.config(state=tk.NORMAL)
        resultado_dados_texto.delete("1.0", tk.END)
        resultado_dados_texto.insert("1.0", "🎲 Resultados das rolagens aparecerão aqui")
        resultado_dados_texto.config(state=tk.DISABLED)
        
        # Remover arquivo de histórico
        try:
            arquivo_historico = obter_caminho('historico.json')
            if os.path.exists(arquivo_historico):
                os.remove(arquivo_historico)
        except Exception as e:
            print(f"Erro ao remover arquivo de histórico: {e}")
        
        messagebox.showinfo("Histórico Limpo", "Todo o histórico foi limpo com sucesso!")

def carregar_historico():
    try:
        if not os.path.exists(obter_caminho('historico.json')):
            return # Não faz nada se o arquivo de histórico não existe, mantendo a mensagem de boas-vindas

        with open(obter_caminho('historico.json'), 'r', encoding='utf-8') as f:
            dados_historico = json.load(f)
            
            conteudo_recompensas = dados_historico.get("recompensas", "")
            # Só substitui a mensagem de boas-vindas se há conteúdo válido de histórico
            if conteudo_recompensas and conteudo_recompensas.strip() and "aparecerá aqui" not in conteudo_recompensas:
                resultado_texto.config(state=tk.NORMAL)
                resultado_texto.delete("1.0", tk.END)
                resultado_texto.insert("1.0", conteudo_recompensas)
                resultado_texto.config(state=tk.DISABLED)
            
            conteudo_rolagens = dados_historico.get("rolagens", "")
            if conteudo_rolagens and conteudo_rolagens.strip() and "aparecerá aqui" not in conteudo_rolagens:
                resultado_dados_texto.config(state=tk.NORMAL)
                resultado_dados_texto.delete("1.0", tk.END)
                resultado_dados_texto.insert("1.0", conteudo_rolagens)
                resultado_dados_texto.config(state=tk.DISABLED)

    except (FileNotFoundError, json.JSONDecodeError):
        pass # Silenciosamente ignora se o arquivo estiver corrompido ou não for encontrado

# --- Lógica de Geração ---
def gerar_recompensa_completa():
    # Otimização: pre-filtrar raridades ativas uma vez só
    raridades_ativas = {}
    for nome, config in [
        ("Comum", {"check": var_comum.get(), "peso": var_peso_comum.get()}),
        ("Incomum", {"check": var_incomum.get(), "peso": var_peso_incomum.get()}),
        ("Raro", {"check": var_raro.get(), "peso": var_peso_raro.get()}),
        ("Épico", {"check": var_epico.get(), "peso": var_peso_epico.get()}),
        ("Lendário", {"check": var_lendario.get(), "peso": var_peso_lendario.get()})
    ]:
        if config["check"] and config["peso"] > 0:
            raridades_ativas[nome] = config["peso"]
    
    if not LISTA_DE_LOOT_GLOBAL:
        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert("1.0", "❌ ERRO: Nenhum item cadastrado!\n\n"
                                      "💡 Para usar o gerador:\n"
                                      "1. Vá para a aba 'Manter Itens'\n"
                                      "2. Clique em 'Carregar Itens de Exemplo'\n"
                                      "   OU adicione seus próprios itens\n"
                                      "3. Volte aqui e clique em 'Gerar Recompensa'")
        resultado_texto.config(state=tk.DISABLED)
        return
    
    # Otimização: filtrar uma vez e separar lista de pesos
    piscina_de_itens_filtrada = []
    pesos_dos_itens_filtrados = []
    for item in LISTA_DE_LOOT_GLOBAL:
        raridade = item.get('raridade')
        if raridade in raridades_ativas:
            piscina_de_itens_filtrada.append(item)
            pesos_dos_itens_filtrados.append(raridades_ativas[raridade])
    
    if not piscina_de_itens_filtrada:
        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert("1.0", "⚠️ Nenhum item disponível para sorteio!\n\n"
                                      "🔍 Verifique se:\n"
                                      "• Pelo menos uma raridade está marcada\n"
                                      "• Os pesos das raridades são maiores que 0\n"
                                      "• Existem itens cadastrados para as raridades selecionadas\n\n"
                                      "💡 Dica: Vá na aba 'Manter Itens' para ver os itens cadastrados")
        resultado_texto.config(state=tk.DISABLED)
        return
    
    quantidade_itens = var_quantidade_itens.get()
    itens_sorteados_final = []
    if quantidade_itens > 0:
        itens_sorteados_final = random.choices(piscina_de_itens_filtrada, weights=pesos_dos_itens_filtrados, k=quantidade_itens)
    
    # Listas pré-definidas para atributos dinâmicos (reutilizar)
    lista_de_cores = ["Vermelho", "Azul", "Verde", "Amarelo", "Preto", "Branco", "Roxo", "Laranja", "Cinza", "Marrom"]
    lista_de_encantamentos = ["Elétrico", "Fogo", "Gelo", "Arcano", "Luz", "Maldição", "Natural", "Sangramento", "Veneno"]
    
    # Qualidades com pesos configuráveis pelo usuário
    qualidades = {
        "Condição impecável (+2)": var_peso_impecavel.get(),
        "Levemente marcado (+1)": var_peso_levemente_marcado.get(),
        "Normal (+0)": var_peso_normal.get(),
        "Bem usado (-1)": var_peso_bem_usado.get(),
        "Desgastado (-2)": var_peso_desgastado.get()
    }
    
    resultado_texto.config(state=tk.NORMAL)
    resultado_texto.delete("1.0", tk.END)
    if itens_sorteados_final:
        resultado_texto.insert(tk.END, "🎁 Itens Sorteados:\n")
        for item in itens_sorteados_final:
            nome_item = item['nome_item']
            raridade = item['raridade']
            
            # Construir o nome completo do item com atributos
            nome_completo = nome_item
            
            # Adicionar cor se selecionado
            if var_adicionar_cor.get():
                cor = random.choice(lista_de_cores)
                nome_completo += f" {cor}"
            
            # Adicionar qualidade se selecionado
            qualidade_texto = ""
            if var_adicionar_qualidade.get():
                # Filtra qualidades com peso maior que zero
                qualidades_validas = {k: v for k, v in qualidades.items() if v > 0}
                if qualidades_validas:
                    qualidade_lista = list(qualidades_validas.keys())
                    pesos_qualidade = list(qualidades_validas.values())
                    qualidade_escolhida = random.choices(qualidade_lista, weights=pesos_qualidade, k=1)[0]
                    qualidade_texto = f" • {qualidade_escolhida}"
            
            # Adicionar encantamento se selecionado e passou na chance
            encantamento_texto = ""
            if var_chance_encantamento.get():
                chance = random.randint(1, 100)
                if chance <= var_porcentagem_encantamento.get():
                    encantamento = random.choice(lista_de_encantamentos)
                    encantamento_texto = f" • <{encantamento}>"
            
            # Montar a linha final com formatação melhorada
            linha = f"⚔️ {nome_completo}{qualidade_texto}{encantamento_texto} • ({raridade})\n"
            resultado_texto.insert(tk.END, linha, raridade)
    
    min_val, max_val = var_min_moedas.get(), var_max_moedas.get()
    if min_val > max_val: min_val, max_val = max_val, min_val
    quantidade_gerada = 0
    if var_gerar_moedas.get():
        quantidade_gerada = random.randint(min_val, max_val)
    if quantidade_gerada > 0:
        if itens_sorteados_final:
            resultado_texto.insert(tk.END, "\n") 
        resultado_texto.insert(tk.END, f"💰 Moedas (LMD): {quantidade_gerada}")
    if not itens_sorteados_final and quantidade_gerada == 0:
        resultado_texto.insert(tk.END, "🤔 Nada foi gerado!\n\n"
                                       "💡 Verifique:\n"
                                       "• Quantidade de itens > 0\n"
                                       "• Gerar moedas ativado\n"
                                       "• Pelo menos uma raridade selecionada")
    resultado_texto.config(state=tk.DISABLED)
    janela.focus_set()

# --- Funções CRUD ---
def atualizar_treeview_loot(filtro=""):
    # Otimização: limpar apenas se necessário
    children = tree_loot.get_children()
    if children:
        tree_loot.delete(*children)  # Método mais rápido
    
    # Filtrar e ordenar em uma só operação
    if filtro:
        filtro_lower = filtro.lower()
        lista_para_exibir = [item for item in LISTA_DE_LOOT_GLOBAL 
                           if filtro_lower in item['nome_item'].lower()]
    else:
        lista_para_exibir = LISTA_DE_LOOT_GLOBAL
    
    # Ordenar apenas se necessário
    if len(lista_para_exibir) > 1:
        lista_para_exibir.sort(key=lambda item: item['nome_item'])
    
    # Inserção otimizada
    for i, item in enumerate(lista_para_exibir):
        tree_loot.insert("", "end", iid=str(i), 
                        values=(item['nome_item'], item['raridade']), 
                        tags=(item['raridade'],))

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
PESOS_INICIAIS, PESOS_QUALIDADES_INICIAIS, ATRIBUTOS_INICIAIS = carregar_parametros('parametros.json')

janela = tk.Tk()
janela.title("Morikawa Loot")

# NOVA OTIMIZAÇÃO: Ocultar janela durante carregamento para evitar flickering
janela.withdraw()  # Esconde a janela

try:
    caminho_icone = obter_caminho('icone.ico')
    janela.iconbitmap(caminho_icone)
except tk.TclError:
    print("Aviso: Arquivo 'icone.ico' não encontrado. Usando ícone padrão.")
except Exception as e:
    print(f"Erro ao carregar ícone: {e}")

janela.geometry("750x600")  # Tamanho inicial adequado
janela.minsize(650, 500)  # Mínimo funcional
# Configurar expansão completa da janela
janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

sv_ttk.set_theme("dark")
def alternar_tema():
    if sv_ttk.get_theme() == "light":
        sv_ttk.set_theme("dark")
    else:
        sv_ttk.set_theme("light")

notebook = ttk.Notebook(janela)
notebook.grid(row=0, column=0, sticky="nsew")  # Remover padding para usar toda a tela

# Otimização para reduzir "flickering" das abas - MUITO melhorada
def on_tab_changed(event):
    # Não fazer nada! Deixar o canvas se ajustar naturalmente
    pass

notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

frame_botoes_tema = ttk.Frame(janela)
frame_botoes_tema.grid(row=1, column=0, sticky="e", padx=5, pady=(0, 5))
botao_tema = ttk.Button(frame_botoes_tema, text="Alternar Tema", command=alternar_tema)
botao_tema.pack()

# --- Aba 1: Gerador de Recompensa ---
tab_sorteio = ttk.Frame(notebook)
notebook.add(tab_sorteio, text='Gerador de Recompensa')

# Configurar expansão total da aba
tab_sorteio.columnconfigure(0, weight=1)
tab_sorteio.rowconfigure(0, weight=1)

# Criar Canvas com Scrollbar para toda a aba - Otimizado
canvas_sorteio = tk.Canvas(tab_sorteio, highlightthickness=0)
scrollbar_sorteio = ttk.Scrollbar(tab_sorteio, orient="vertical", command=canvas_sorteio.yview)
frame_scrollable = ttk.Frame(canvas_sorteio)

# Flag para controlar reconfigurações
canvas_configurado = False

# Configuração responsiva do canvas - MUITO otimizada
def configurar_canvas(event=None):
    global canvas_configurado
    
    # Evitar reconfigurações desnecessárias
    if not frame_scrollable.winfo_exists():
        return
    
    try:
        # Só reconfigurar se realmente necessário
        bbox = canvas_sorteio.bbox("all")
        if bbox:
            canvas_sorteio.configure(scrollregion=bbox)
        
        # Ajustar largura para usar toda a tela - CORRIGIDO
        canvas_width = canvas_sorteio.winfo_width()
        if canvas_width > 1:
            canvas_sorteio.itemconfig(canvas_window, width=canvas_width)
            canvas_configurado = True
            
    except tk.TclError:
        pass

# Configurar responsividade completa do frame scrollable
frame_scrollable.columnconfigure(0, weight=1)
frame_scrollable.rowconfigure(0, weight=0)  # Configs
frame_scrollable.rowconfigure(1, weight=0)  # Quantidades  
frame_scrollable.rowconfigure(2, weight=0)  # Botões
frame_scrollable.rowconfigure(3, weight=0)  # Qualidades
frame_scrollable.rowconfigure(4, weight=1)  # Resultados - usa toda altura restante

# Bind otimizado - só quando realmente necessário
def on_frame_configure(event):
    # Reconfigurar sempre para manter responsividade
    if event.widget == frame_scrollable:
        janela.after_idle(configurar_canvas)

# Bind para redimensionamento da janela - garantir responsividade completa
def on_canvas_configure(event):
    # Quando o canvas muda de tamanho, ajustar o frame interno
    canvas_width = event.width
    canvas_sorteio.itemconfig(canvas_window, width=canvas_width)

frame_scrollable.bind("<Configure>", on_frame_configure)
canvas_sorteio.bind("<Configure>", on_canvas_configure)

canvas_window = canvas_sorteio.create_window((0, 0), window=frame_scrollable, anchor="nw")
canvas_sorteio.configure(yscrollcommand=scrollbar_sorteio.set)

canvas_sorteio.pack(side="left", fill="both", expand=True)
scrollbar_sorteio.pack(side="right", fill="y")

# Configuração inicial única - após tudo estar pronto
def configuracao_inicial():
    try:
        # Forçar configuração inicial completa
        canvas_sorteio.update_idletasks()
        configurar_canvas()
        # Garantir que o canvas use toda a largura
        canvas_width = canvas_sorteio.winfo_width()
        if canvas_width > 1:
            canvas_sorteio.itemconfig(canvas_window, width=canvas_width)
        # Marcar como configurado
        global canvas_configurado
        canvas_configurado = True
    except:
        pass

janela.after(200, configuracao_inicial)  # Delay maior para garantir que tudo está carregado

# Bind mouse wheel com limites mais rigorosos e otimizado
def _on_mousewheel(event):
    try:
        # Verificar se estamos na aba correta
        current_tab = notebook.index(notebook.select())
        if current_tab != 0:  # Só funciona na primeira aba (Gerador de Recompensa)
            return
            
        # Obter informações do canvas
        bbox = canvas_sorteio.bbox("all")
        if not bbox:
            return
        
        canvas_height = canvas_sorteio.winfo_height()
        content_height = bbox[3] - bbox[1]
        
        # Se o conteúdo cabe na tela, não rolar
        if content_height <= canvas_height:
            return
        
        # Obter posição atual do scroll
        current_top = canvas_sorteio.canvasy(0)
        
        # Calcular novo scroll - movimento mais suave
        scroll_amount = int(-1*(event.delta/120))
        new_top = current_top + (scroll_amount * 15)  # Reduzido de 20 para 15 pixels
        
        # Limitar o scroll
        if new_top < 0:
            new_top = 0
        elif new_top > (content_height - canvas_height):
            new_top = content_height - canvas_height
        
        # Aplicar o scroll apenas se mudou significativamente
        if abs(new_top - current_top) > 2:  # Só rolar se diferença for > 2px
            canvas_sorteio.yview_moveto(new_top / content_height)
    except (tk.TclError, ZeroDivisionError):
        pass  # Ignorar erros

canvas_sorteio.bind_all("<MouseWheel>", _on_mousewheel)
var_comum = tk.BooleanVar(value=True); var_incomum = tk.BooleanVar(value=True); var_raro = tk.BooleanVar(value=True); var_epico = tk.BooleanVar(value=True); var_lendario = tk.BooleanVar(value=True)
var_peso_comum = tk.IntVar(value=PESOS_INICIAIS.get("Comum", 65)); var_peso_incomum = tk.IntVar(value=PESOS_INICIAIS.get("Incomum", 20)); var_peso_raro = tk.IntVar(value=PESOS_INICIAIS.get("Raro", 10)); var_peso_epico = tk.IntVar(value=PESOS_INICIAIS.get("Épico", 4)); var_peso_lendario = tk.IntVar(value=PESOS_INICIAIS.get("Lendário", 1))
var_quantidade_itens = tk.IntVar(value=3)  # 3 itens por padrão para demo mais interessante
var_min_moedas = tk.IntVar(value=1)
var_max_moedas = tk.IntVar(value=100)
var_gerar_moedas = tk.BooleanVar(value=ATRIBUTOS_INICIAIS.get("gerar_moedas", True))

# Novas variáveis para atributos dinâmicos
var_adicionar_cor = tk.BooleanVar(value=ATRIBUTOS_INICIAIS.get("adicionar_cor", True))
var_chance_encantamento = tk.BooleanVar(value=ATRIBUTOS_INICIAIS.get("chance_encantamento", True))
var_porcentagem_encantamento = tk.IntVar(value=ATRIBUTOS_INICIAIS.get("porcentagem_encantamento", 30))
var_adicionar_qualidade = tk.BooleanVar(value=ATRIBUTOS_INICIAIS.get("adicionar_qualidade", True))

# Variáveis para os pesos das qualidades
var_peso_impecavel = tk.IntVar(value=PESOS_QUALIDADES_INICIAIS.get("Condição impecável (+2)", 5))
var_peso_levemente_marcado = tk.IntVar(value=PESOS_QUALIDADES_INICIAIS.get("Levemente marcado (+1)", 15))
var_peso_normal = tk.IntVar(value=PESOS_QUALIDADES_INICIAIS.get("Normal (+0)", 50))
var_peso_bem_usado = tk.IntVar(value=PESOS_QUALIDADES_INICIAIS.get("Bem usado (-1)", 20))
var_peso_desgastado = tk.IntVar(value=PESOS_QUALIDADES_INICIAIS.get("Desgastado (-2)", 10))
frame_configs = ttk.LabelFrame(frame_scrollable, text="1. Configure as Probabilidades e Atributos", padding="8")
frame_configs.pack(fill=tk.X, pady=(0, 10), padx=5, side=tk.TOP)

# Criar um frame interno com duas colunas
frame_interno = ttk.Frame(frame_configs)
frame_interno.pack(fill=tk.BOTH, expand=True)
frame_interno.columnconfigure(0, weight=1)
frame_interno.columnconfigure(2, weight=1)

# Coluna esquerda - Raridades
frame_raridades = ttk.Frame(frame_interno)
frame_raridades.pack(side=tk.LEFT, fill="both", expand=True, padx=(0,10))

ttk.Label(frame_raridades, text="Incluir?", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5, pady=3)
ttk.Label(frame_raridades, text="Raridade", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=5, pady=3)
ttk.Label(frame_raridades, text="Peso", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=5, pady=3)

ttk.Label(frame_raridades, text="Incluir?", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5, pady=3)
ttk.Label(frame_raridades, text="Raridade", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=5, pady=3)
ttk.Label(frame_raridades, text="Peso", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=5, pady=3)

ttk.Checkbutton(frame_raridades, variable=var_comum).grid(row=1, column=0, padx=5, pady=2)
ttk.Label(frame_raridades, text="Comum").grid(row=1, column=1, padx=5, pady=2, sticky="w")
ttk.Spinbox(frame_raridades, from_=0, to=1000, textvariable=var_peso_comum, width=8).grid(row=1, column=2, padx=5, pady=2)

ttk.Checkbutton(frame_raridades, variable=var_incomum).grid(row=2, column=0, padx=5, pady=2)
ttk.Label(frame_raridades, text="Incomum").grid(row=2, column=1, padx=5, pady=2, sticky="w")
ttk.Spinbox(frame_raridades, from_=0, to=1000, textvariable=var_peso_incomum, width=8).grid(row=2, column=2, padx=5, pady=2)

ttk.Checkbutton(frame_raridades, variable=var_raro).grid(row=3, column=0, padx=5, pady=2)
ttk.Label(frame_raridades, text="Raro").grid(row=3, column=1, padx=5, pady=2, sticky="w")
ttk.Spinbox(frame_raridades, from_=0, to=1000, textvariable=var_peso_raro, width=8).grid(row=3, column=2, padx=5, pady=2)

ttk.Checkbutton(frame_raridades, variable=var_epico).grid(row=4, column=0, padx=5, pady=2)
ttk.Label(frame_raridades, text="Épico").grid(row=4, column=1, padx=5, pady=2, sticky="w")
ttk.Spinbox(frame_raridades, from_=0, to=1000, textvariable=var_peso_epico, width=8).grid(row=4, column=2, padx=5, pady=2)

ttk.Checkbutton(frame_raridades, variable=var_lendario).grid(row=5, column=0, padx=5, pady=2)
ttk.Label(frame_raridades, text="Lendário").grid(row=5, column=1, padx=5, pady=2, sticky="w")
ttk.Spinbox(frame_raridades, from_=0, to=1000, textvariable=var_peso_lendario, width=8).grid(row=5, column=2, padx=5, pady=2)

# Separador vertical
ttk.Separator(frame_interno, orient='vertical').pack(side=tk.LEFT, fill='y', padx=5)

# Coluna direita - Atributos dinâmicos
frame_atributos = ttk.Frame(frame_interno)
frame_atributos.pack(side=tk.LEFT, fill="both", expand=True, padx=(5,0))

ttk.Label(frame_atributos, text="Atributos Dinâmicos", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,10))

ttk.Checkbutton(frame_atributos, text="Adicionar Cor Aleatória?", variable=var_adicionar_cor).grid(row=1, column=0, columnspan=3, padx=5, pady=3, sticky="w")

check_encantamento = ttk.Checkbutton(frame_atributos, text="Chance de Encantamento?", variable=var_chance_encantamento)
check_encantamento.grid(row=2, column=0, columnspan=2, padx=5, pady=3, sticky="w")

spinbox_encantamento = ttk.Spinbox(frame_atributos, from_=0, to=100, textvariable=var_porcentagem_encantamento, width=8)
label_porcentagem = ttk.Label(frame_atributos, text="%")

def toggle_controle_encantamento():
    if var_chance_encantamento.get():
        spinbox_encantamento.grid(row=3, column=0, padx=5, pady=3)
        label_porcentagem.grid(row=3, column=1, padx=5, pady=3)
    else:
        spinbox_encantamento.grid_remove()
        label_porcentagem.grid_remove()

var_chance_encantamento.trace_add("write", lambda *args: toggle_controle_encantamento())
toggle_controle_encantamento()

check_qualidade = ttk.Checkbutton(frame_atributos, text="Adicionar Qualidade do Item?", variable=var_adicionar_qualidade)
check_qualidade.grid(row=4, column=0, columnspan=3, padx=5, pady=3, sticky="w")

# Frame para quantidades
frame_quantidades = ttk.LabelFrame(frame_scrollable, text="2. Quantidades", padding="8")
frame_quantidades.pack(fill=tk.X, pady=(0, 10), padx=5, side=tk.TOP)

frame_quant_interno = ttk.Frame(frame_quantidades)
frame_quant_interno.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame_quant_interno, text="Qtd. Itens:").grid(row=0, column=0, padx=5, pady=3, sticky="e")
ttk.Spinbox(frame_quant_interno, from_=0, to=20, textvariable=var_quantidade_itens, width=10).grid(row=0, column=1, padx=5, pady=3, sticky="w")

check_moedas = ttk.Checkbutton(frame_quant_interno, text="Gerar Moedas?", variable=var_gerar_moedas)
check_moedas.grid(row=1, column=0, columnspan=2, padx=5, pady=3, sticky="w")

label_min_moedas = ttk.Label(frame_quant_interno, text="Min:")
spinbox_min_moedas = ttk.Spinbox(frame_quant_interno, from_=0, to=10000, textvariable=var_min_moedas, width=10)
label_max_moedas = ttk.Label(frame_quant_interno, text="Max:")
spinbox_max_moedas = ttk.Spinbox(frame_quant_interno, from_=0, to=10000, textvariable=var_max_moedas, width=10)

def toggle_controles_moedas():
    if var_gerar_moedas.get():
        label_min_moedas.grid(row=2, column=0, padx=5, pady=2, sticky="e")
        spinbox_min_moedas.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        label_max_moedas.grid(row=3, column=0, padx=5, pady=2, sticky="e")
        spinbox_max_moedas.grid(row=3, column=1, padx=5, pady=2, sticky="w")
    else:
        label_min_moedas.grid_remove()
        spinbox_min_moedas.grid_remove()
        label_max_moedas.grid_remove()
        spinbox_max_moedas.grid_remove()

var_gerar_moedas.trace_add("write", lambda *args: toggle_controles_moedas())
toggle_controles_moedas()

# Frame para botões - sempre visível
frame_botoes = ttk.Frame(frame_scrollable)
frame_botoes.pack(pady=(10, 15), side=tk.TOP, fill=tk.X)

botao_sortear_tudo = ttk.Button(frame_botoes, text="🎲 Gerar Recompensa!", command=gerar_recompensa_completa)
botao_sortear_tudo.pack(side=tk.LEFT, padx=5, expand=True, fill="x")

botao_salvar = ttk.Button(frame_botoes, text="💾 Salvar", command=salvar_parametros)
botao_salvar.pack(side=tk.LEFT, padx=5, expand=True, fill="x")

botao_limpar_historico = ttk.Button(frame_botoes, text="🗑️ Limpar Histórico", command=limpar_historico)
botao_limpar_historico.pack(side=tk.LEFT, padx=5, expand=True, fill="x")
# Sub-frame para pesos das qualidades
frame_qualidades = ttk.LabelFrame(frame_scrollable, text="Pesos das Qualidades", padding="8")

def toggle_frame_qualidades():
    if var_adicionar_qualidade.get():
        frame_qualidades.pack(fill=tk.X, pady=(0, 10), padx=5, after=frame_configs)
        # Organização em grid compacto
        ttk.Label(frame_qualidades, text="Qualidade").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Label(frame_qualidades, text="Peso").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        
        # Controles de peso para cada qualidade em grid 2x3 para economizar espaço
        ttk.Label(frame_qualidades, text="Impecável (+2)").grid(row=1, column=0, padx=5, pady=1, sticky="w")
        ttk.Spinbox(frame_qualidades, from_=0, to=100, textvariable=var_peso_impecavel, width=6).grid(row=1, column=1, padx=5, pady=1)
        
        ttk.Label(frame_qualidades, text="Leve marcado (+1)").grid(row=1, column=2, padx=5, pady=1, sticky="w")
        ttk.Spinbox(frame_qualidades, from_=0, to=100, textvariable=var_peso_levemente_marcado, width=6).grid(row=1, column=3, padx=5, pady=1)
        
        ttk.Label(frame_qualidades, text="Normal (+0)").grid(row=2, column=0, padx=5, pady=1, sticky="w")
        ttk.Spinbox(frame_qualidades, from_=0, to=100, textvariable=var_peso_normal, width=6).grid(row=2, column=1, padx=5, pady=1)
        
        ttk.Label(frame_qualidades, text="Bem usado (-1)").grid(row=2, column=2, padx=5, pady=1, sticky="w")
        ttk.Spinbox(frame_qualidades, from_=0, to=100, textvariable=var_peso_bem_usado, width=6).grid(row=2, column=3, padx=5, pady=1)
        
        ttk.Label(frame_qualidades, text="Desgastado (-2)").grid(row=3, column=0, padx=5, pady=1, sticky="w")
        ttk.Spinbox(frame_qualidades, from_=0, to=100, textvariable=var_peso_desgastado, width=6).grid(row=3, column=1, padx=5, pady=1)
    else:
        frame_qualidades.pack_forget()
        # Limpa todos os widgets do frame
        for widget in frame_qualidades.winfo_children():
            widget.destroy()

# Vincula a função ao checkbox
var_adicionar_qualidade.trace_add("write", lambda *args: toggle_frame_qualidades())

# Chama a função inicialmente para definir o estado correto
toggle_frame_qualidades()

# Frame para resultados - compacto mas funcional e totalmente responsivo
frame_resultados = ttk.LabelFrame(frame_scrollable, text="📋 Recompensas Geradas", padding="8")
frame_resultados.pack(fill="both", expand=True, pady=(0, 10), padx=5)

# Configurar responsividade completa do frame de resultados
frame_resultados.columnconfigure(0, weight=1)
frame_resultados.rowconfigure(0, weight=1)

# Container para Text widget e scrollbar
container_resultado = ttk.Frame(frame_resultados)
container_resultado.grid(row=0, column=0, sticky="nsew")
container_resultado.columnconfigure(0, weight=1)
container_resultado.rowconfigure(0, weight=1)

# Área de resultados responsiva - altura adaptável, usa toda a tela
resultado_texto = tk.Text(container_resultado, height=12, wrap="word", relief="flat", borderwidth=0, font=("Segoe UI", 9))
resultado_texto.grid(row=0, column=0, sticky="nsew")

# Scrollbar vertical para a área de resultados
scrollbar_resultado = ttk.Scrollbar(container_resultado, orient="vertical", command=resultado_texto.yview)
scrollbar_resultado.grid(row=0, column=1, sticky="ns")
resultado_texto.config(yscrollcommand=scrollbar_resultado.set)

# Função para ajustar responsividade - SUPER otimizada
def ajustar_responsividade(event=None):
    # Desabilitar completamente para evitar flickering
    pass

# Função para resetar scroll ao topo quando necessário
def resetar_scroll():
    canvas_sorteio.yview_moveto(0)

# Desabilitar bind de responsividade que causa flickering
# janela.bind('<Configure>', ajustar_responsividade)  # DESABILITADO
for raridade, cor in CORES_RARIDADE.items():
    resultado_texto.tag_configure(raridade, foreground=cor)

# Mensagem inicial compacta
resultado_texto.config(state=tk.NORMAL)
resultado_texto.insert("1.0", "🎲 Morikawa Loot Generator\n\n"
                              "✨ Configure as opções acima\n"
                              "🚀 Clique em 'Gerar Recompensa Completa'\n\n"
                              "💡 Use 'Manter Itens' para adicionar exemplos")
resultado_texto.config(state=tk.DISABLED)

# --- Aba 2: Manter Itens ---
tab_manter_loot = ttk.Frame(notebook)
notebook.add(tab_manter_loot, text='Manter Itens')

# Configurar expansão completa da aba - igual ao Gerador de Recompensas
tab_manter_loot.columnconfigure(0, weight=1)
tab_manter_loot.rowconfigure(0, weight=0)  # Filtro fixo
tab_manter_loot.rowconfigure(1, weight=1)  # Tabela - usa toda a tela disponível
tab_manter_loot.rowconfigure(2, weight=0)  # Formulário fixo
tab_manter_loot.rowconfigure(3, weight=0)  # Botões fixo
tab_manter_loot.rowconfigure(4, weight=0)  # Exemplo fixo
var_filtro_itens = tk.StringVar()
frame_filtro = ttk.LabelFrame(tab_manter_loot, text="Busca", padding=8)
frame_filtro.grid(row=0, column=0, pady=(5, 3), padx=10, sticky="ew")
ttk.Label(frame_filtro, text="Filtrar por nome:").pack(side=tk.LEFT, padx=(0,5))
entry_filtro = ttk.Entry(frame_filtro, textvariable=var_filtro_itens)
entry_filtro.pack(fill="x", expand=True)
def aplicar_filtro(*args):
    atualizar_treeview_loot(filtro=var_filtro_itens.get())
var_filtro_itens.trace_add("write", aplicar_filtro)
frame_lista = ttk.LabelFrame(tab_manter_loot, text="Lista de Itens", padding=8)
frame_lista.grid(row=1, column=0, pady=(3, 3), padx=10, sticky="nsew")
frame_lista.rowconfigure(0, weight=1)
frame_lista.columnconfigure(0, weight=1)
cols = ('nome_item', 'raridade')
tree_loot = ttk.Treeview(frame_lista, columns=cols, show='headings', height=20)  # Aumentar ainda mais para 20
tree_loot.grid(row=0, column=0, sticky="nsew")
tree_loot.column('nome_item', width=400, minwidth=250)  # Aumentar ainda mais a largura
tree_loot.column('raridade', width=130, minwidth=110, anchor=tk.CENTER)  # Aumentar largura
scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree_loot.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
tree_loot.configure(yscrollcommand=scrollbar.set)
tree_loot.heading('nome_item', text='Nome Item', command=lambda: ordenar_coluna(tree_loot, 'nome_item', False))
tree_loot.heading('raridade', text='Raridade', command=lambda: ordenar_coluna(tree_loot, 'raridade', False))
for raridade, cor in CORES_RARIDADE.items():
    tree_loot.tag_configure(raridade, foreground=cor)
frame_formulario = ttk.LabelFrame(tab_manter_loot, text="Adicionar / Editar Item", padding=8)
frame_formulario.grid(row=2, column=0, pady=(3, 3), padx=10, sticky="ew")
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
frame_botoes_crud.grid(row=3, column=0, padx=10, pady=(3, 3), sticky="ew")
# ### MUDANÇA ### - O botão de limpar campos agora limpa a raridade também
ttk.Button(frame_botoes_crud, text="Adicionar Novo", command=adicionar_item).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
ttk.Button(frame_botoes_crud, text="Salvar Edição", command=salvar_edicao_item).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
ttk.Button(frame_botoes_crud, text="Excluir Selecionado", command=excluir_item).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
ttk.Button(frame_botoes_crud, text="Limpar Campos", command=limpar_campos_crud).pack(side=tk.LEFT, expand=True, fill='x', padx=5)

# Botão para carregar itens de exemplo
frame_exemplo = ttk.Frame(tab_manter_loot, padding=5)
frame_exemplo.grid(row=4, column=0, padx=5, sticky="ew")
ttk.Button(frame_exemplo, text="🎲 Carregar Itens de Exemplo", command=carregar_itens_exemplo).pack(expand=True, fill='x')

# --- Aba 3: Rolar Dados ---
tab_dados = ttk.Frame(notebook)
notebook.add(tab_dados, text='Rolar Dados')

# Configurar expansão completa da aba - igual ao Gerador de Recompensas
tab_dados.columnconfigure(0, weight=1)
tab_dados.rowconfigure(0, weight=0)  # Quantidade de dados fixo
tab_dados.rowconfigure(1, weight=0)  # Dados padrão fixo
tab_dados.rowconfigure(2, weight=0)  # Dado custom fixo
tab_dados.rowconfigure(3, weight=1)  # Resultados - usa toda a tela disponível

var_quantidade_dados = tk.IntVar(value=1)
var_lados_custom = tk.IntVar(value=6)
frame_quantidade_dados = ttk.LabelFrame(tab_dados, text="1. Quantidade de Dados", padding=10)
frame_quantidade_dados.grid(row=0, column=0, pady=(10, 10), padx=10, sticky="ew")
ttk.Label(frame_quantidade_dados, text="Rodar:").pack(side=tk.LEFT, padx=(0, 8))
ttk.Spinbox(frame_quantidade_dados, from_=1, to=100, textvariable=var_quantidade_dados, width=5).pack(side=tk.LEFT)
ttk.Label(frame_quantidade_dados, text="dado(s)").pack(side=tk.LEFT, padx=(8, 0))

frame_dados_padrao = ttk.LabelFrame(tab_dados, text="2. Dados Padrão", padding=10)
frame_dados_padrao.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="ew")
botoes_dados_info = [4, 6, 8, 10, 12, 20, 100]
coluna_atual = 0
for lados in botoes_dados_info:
    botao = ttk.Button(frame_dados_padrao, text=f"d{lados}", command=lambda l=lados: chamar_rolagem(l))
    botao.grid(row=0, column=coluna_atual, padx=8, pady=8, sticky="ew")
    frame_dados_padrao.columnconfigure(coluna_atual, weight=1)
    coluna_atual += 1
frame_dado_custom = ttk.LabelFrame(tab_dados, text="3. Dado Personalizado (d?)", padding=10)
frame_dado_custom.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")
ttk.Label(frame_dado_custom, text="Lados:").pack(side=tk.LEFT, padx=(0, 8))
ttk.Spinbox(frame_dado_custom, from_=2, to=1000, textvariable=var_lados_custom, width=8).pack(side=tk.LEFT, expand=True, fill="x")
ttk.Button(frame_dado_custom, text="Rolar!", command=lambda: chamar_rolagem(var_lados_custom.get())).pack(side=tk.LEFT, padx=(15, 0))

frame_resultado_dados = ttk.LabelFrame(tab_dados, text="Resultados", padding=10)
frame_resultado_dados.grid(row=3, column=0, pady=(0, 10), padx=10, sticky="nsew")

# Configurar responsividade completa do frame de resultados - igual ao Gerador de Recompensas
frame_resultado_dados.columnconfigure(0, weight=1)
frame_resultado_dados.rowconfigure(1, weight=1)  # Text widget usa toda altura disponível
frame_log_botoes = ttk.Frame(frame_resultado_dados)
frame_log_botoes.grid(row=0, column=0, sticky="ew", pady=(0, 5))
ttk.Button(frame_log_botoes, text="Limpar Log de Rolagens", command=limpar_log_rolagens).pack(side='right')

resultado_dados_texto = tk.Text(frame_resultado_dados, height=10, wrap="word", relief="flat", borderwidth=0, font=("Segoe UI", 11))
resultado_dados_texto.grid(row=1, column=0, sticky="nsew")
resultado_dados_texto.config(state=tk.DISABLED)

# --- Finalização ---
tree_loot.bind("<<TreeviewSelect>>", on_item_selecionado)
tree_loot.bind("<Delete>", on_delete_key)
# ### MUDANÇA ### - Adiciona o atalho da tecla Enter para o campo de nome do item
entry_nome_crud.bind("<Return>", on_enter_no_campo_nome)
atualizar_treeview_loot()
carregar_historico()

# Salva os parâmetros no formato correto se necessário
def verificar_e_atualizar_parametros():
    try:
        with open(obter_caminho('parametros.json'), 'r', encoding='utf-8') as f:
            dados = json.load(f)
        # Se não tem a estrutura nova, atualiza
        if "pesos_raridade" not in dados:
            salvar_parametros()
    except:
        # Se há erro ao ler, cria novo arquivo
        salvar_parametros()

verificar_e_atualizar_parametros()

def ao_fechar():
    salvar_historico()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", ao_fechar)

# FUNÇÃO FINAL: Mostrar janela apenas quando tudo estiver pronto
def mostrar_janela():
    try:
        # Configurar tudo uma última vez
        configurar_canvas()
        # Centralizar janela na tela
        janela.update_idletasks()
        x = (janela.winfo_screenwidth() // 2) - (750 // 2)
        y = (janela.winfo_screenheight() // 2) - (600 // 2)
        janela.geometry(f"750x600+{x}+{y}")
        # Mostrar janela
        janela.deiconify()  # Mostra a janela
    except:
        janela.deiconify()  # Fallback - mostrar mesmo se há erro

# Aguardar 300ms para tudo carregar, então mostrar
janela.after(300, mostrar_janela)

janela.mainloop()