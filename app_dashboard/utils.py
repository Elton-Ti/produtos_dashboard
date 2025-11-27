import pandas as pd
import os
from django.conf import settings
from .models import Produto
from datetime import datetime

def importar_planilha():
    """Importa dados da planilha Excel para o banco de dados"""
    try:
        caminho_planilha = os.path.join(settings.BASE_DIR, 'produtos.xls')
        
        # Verificar se arquivo existe
        if not os.path.exists(caminho_planilha):
            return {'erro': f'Arquivo não encontrado: {caminho_planilha}'}
        
        # Ler planilha Excel - FORÇAR engine openpyxl para .xls
        try:
            df = pd.read_excel(caminho_planilha, engine='openpyxl')
        except:
            # Se não funcionar com openpyxl, tenta com xlrd
            try:
                df = pd.read_excel(caminho_planilha, engine='xlrd')
            except:
                return {'erro': 'Não foi possível ler o arquivo Excel. Instale xlrd: pip install xlrd'}
        
        # Converter dados
        produtos_importados = 0
        produtos_atualizados = 0
        
        for index, row in df.iterrows():
            # Verificar se a linha tem dados válidos
            if pd.isna(row['ID']) or pd.isna(row['Nome']):
                continue
                
            # Converter data
            try:
                data_cadastro = datetime.strptime(str(row['Data Cadastro']), '%Y-%m-%d').date()
            except:
                data_cadastro = datetime.now().date()
            
            # Converter status ativo
            ativo = True if str(row['Ativo']).lower() == 'sim' else False
            
            # Criar ou atualizar produto
            produto, created = Produto.objects.update_or_create(
                id_produto=int(row['ID']),
                defaults={
                    'nome': row['Nome'],
                    'categoria': row['Categoria'],
                    'marca': row['Marca'],
                    'preco': float(row['Preço']),
                    'estoque': int(row['Estoque']),
                    'data_cadastro': data_cadastro,
                    'ativo': ativo
                }
            )
            
            if created:
                produtos_importados += 1
            else:
                produtos_atualizados += 1
        
        return {
            'importados': produtos_importados,
            'atualizados': produtos_atualizados,
            'total': len(df)
        }
    
    except Exception as e:
        return {'erro': str(e)}