"""
Script para integrar documentos fornecidos ao sistema de treinamento
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.user import db
from src.models.module import Module, Lesson, MediaFile
from src.models.quiz import Quiz, Question
from datetime import datetime

def integrate_documents():
    """Integra os documentos fornecidos ao sistema de treinamento"""
    
    # Caminho para os documentos
    docs_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'documents')
    
    try:
        # Buscar módulo 3 (Portfólio de Produtos)
        module3 = Module.query.filter_by(title='Portfólio de Produtos e Serviços').first()
        if not module3:
            print("Módulo 3 não encontrado")
            return
        
        # Integrar conteúdo específico baseado nos documentos
        integrate_tabela_planos(module3, docs_path)
        integrate_contratos(module3, docs_path)
        integrate_objecoes_vendas(module3, docs_path)
        integrate_perguntas_frequentes(module3, docs_path)
        integrate_script_vendas(module3, docs_path)
        integrate_seguro_internacao(module3, docs_path)
        integrate_legislacao(module3, docs_path)
        
        print("Documentos integrados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao integrar documentos: {str(e)}")

def integrate_tabela_planos(module, docs_path):
    """Integra a tabela de planos ao sistema"""
    
    # Atualizar lição 3.1 com informações da tabela de planos
    lesson_31 = Lesson.query.filter_by(module_id=module.id, order_index=1).first()
    if lesson_31:
        # Adicionar referência ao documento
        tabela_path = os.path.join(docs_path, 'TabeladePlanoseJazigos.pdf')
        if os.path.exists(tabela_path):
            # Criar registro de mídia para o PDF
            media_file = MediaFile(
                filename='tabela_planos_jazigos.pdf',
                original_filename='Tabela de Planos e Jazigos.pdf',
                file_path=tabela_path,
                file_type='pdf',
                file_size=os.path.getsize(tabela_path),
                mime_type='application/pdf',
                lesson_id=lesson_31.id
            )
            db.session.add(media_file)
            
            # Atualizar conteúdo da lição
            lesson_31.content += """

## Tabela de Planos e Preços

Para informações detalhadas sobre todos os planos disponíveis, valores e condições, consulte a **Tabela de Planos e Jazigos** em anexo.

### Informações Importantes:
- Valores atualizados para 2024/2025
- Condições especiais por região
- Descontos para pagamento à vista
- Planos familiares com cobertura ampliada

[DOCUMENTO ANEXO: Tabela de Planos e Jazigos.pdf]
            """

def integrate_contratos(module, docs_path):
    """Integra os contratos ao sistema"""
    
    lesson_31 = Lesson.query.filter_by(module_id=module.id, order_index=1).first()
    if lesson_31:
        # Contrato 2020
        contrato_2020_path = os.path.join(docs_path, 'Contrato_Amar_Assist_Modelo_PFF_2020-05-29-1139-NOVO2020.pdf')
        if os.path.exists(contrato_2020_path):
            media_file = MediaFile(
                filename='contrato_pff_2020.pdf',
                original_filename='Contrato Amar Assist Modelo PFF 2020.pdf',
                file_path=contrato_2020_path,
                file_type='pdf',
                file_size=os.path.getsize(contrato_2020_path),
                mime_type='application/pdf',
                lesson_id=lesson_31.id
            )
            db.session.add(media_file)
        
        # Contrato 2025
        contrato_2025_path = os.path.join(docs_path, 'Contrato_Amar_Assist_Modelo_PFF_2025.pdf')
        if os.path.exists(contrato_2025_path):
            media_file = MediaFile(
                filename='contrato_pff_2025.pdf',
                original_filename='Contrato Amar Assist Modelo PFF 2025.pdf',
                file_path=contrato_2025_path,
                file_type='pdf',
                file_size=os.path.getsize(contrato_2025_path),
                mime_type='application/pdf',
                lesson_id=lesson_31.id
            )
            db.session.add(media_file)

def integrate_objecoes_vendas(module, docs_path):
    """Integra o material de objeções de vendas"""
    
    # Criar nova lição específica para objeções
    objecoes_lesson = Lesson(
        module_id=module.id,
        title='Tratamento de Objeções - Técnicas Avançadas',
        content="""
# Tratamento de Objeções em Vendas de Planos Funerários

## Importância do Tratamento de Objeções

O tratamento adequado de objeções é fundamental no processo de vendas de planos funerários, pois:

- Demonstra profissionalismo e conhecimento
- Constrói confiança com o cliente
- Transforma resistência em oportunidade
- Aumenta significativamente a taxa de conversão

## Principais Objeções e Respostas

### 1. Objeções de Preço
**Objeção**: "Está muito caro"
**Resposta**: Demonstrar valor vs. custo, comparar com custos de funeral sem plano

### 2. Objeções de Necessidade
**Objeção**: "Não preciso agora, sou jovem"
**Resposta**: Explicar que acidentes não escolhem idade, carência reduzida

### 3. Objeções de Confiança
**Objeção**: "Não confio em planos"
**Resposta**: Mostrar avaliação 4.7/5 no Reclame Aqui, cases de sucesso

## Material Complementar

Consulte o documento anexo "Objeções de Vendas" para técnicas detalhadas e scripts específicos.

[DOCUMENTO ANEXO: ObjecoesVendas.pdf]
        """,
        order_index=4,
        lesson_type='text',
        duration_minutes=40,
        is_active=True
    )
    db.session.add(objecoes_lesson)
    db.session.commit()
    
    # Adicionar arquivo de objeções
    objecoes_path = os.path.join(docs_path, 'ObjecoesVendas.pdf')
    if os.path.exists(objecoes_path):
        media_file = MediaFile(
            filename='objecoes_vendas.pdf',
            original_filename='Objeções de Vendas.pdf',
            file_path=objecoes_path,
            file_type='pdf',
            file_size=os.path.getsize(objecoes_path),
            mime_type='application/pdf',
            lesson_id=objecoes_lesson.id
        )
        db.session.add(media_file)

def integrate_perguntas_frequentes(module, docs_path):
    """Integra as perguntas frequentes"""
    
    # Criar lição de FAQ
    faq_lesson = Lesson(
        module_id=module.id,
        title='Perguntas Frequentes - Produtos Amar Assist',
        content="""
# Perguntas Frequentes sobre os Produtos da Amar Assist

## Importância do Conhecimento de FAQ

Dominar as perguntas frequentes é essencial para:

- Antecipar dúvidas dos clientes
- Fornecer respostas precisas e confiáveis
- Demonstrar expertise no produto
- Acelerar o processo de vendas

## Principais Categorias de Perguntas

### Planos Funerários
- Cobertura e benefícios
- Carência e restrições
- Processo de acionamento
- Documentação necessária

### Jazigos
- Localização e disponibilidade
- Transferência e herança
- Manutenção e conservação
- Valorização patrimonial

### Seguros Complementares
- Cobertura do seguro de vida
- Condições do seguro internação
- Processo de indenização
- Documentos necessários

## Material de Referência

Consulte o documento completo "Perguntas Frequentes sobre os Produtos da Amar Assist" para todas as perguntas e respostas detalhadas.

[DOCUMENTO ANEXO: PerguntasFrequentessobreosProdutosdaAmarAssist2.pdf]
        """,
        order_index=5,
        lesson_type='text',
        duration_minutes=35,
        is_active=True
    )
    db.session.add(faq_lesson)
    db.session.commit()
    
    # Adicionar arquivo de FAQ
    faq_path = os.path.join(docs_path, 'PerguntasFrequentessobreosProdutosdaAmarAssist2.pdf')
    if os.path.exists(faq_path):
        media_file = MediaFile(
            filename='faq_produtos.pdf',
            original_filename='Perguntas Frequentes sobre os Produtos da Amar Assist.pdf',
            file_path=faq_path,
            file_type='pdf',
            file_size=os.path.getsize(faq_path),
            mime_type='application/pdf',
            lesson_id=faq_lesson.id
        )
        db.session.add(media_file)

def integrate_script_vendas(module, docs_path):
    """Integra o script oficial de vendas"""
    
    # Criar lição de script de vendas
    script_lesson = Lesson(
        module_id=module.id,
        title='Script Oficial de Vendas - Modelo 2020',
        content="""
# Script Oficial de Vendas Amar Assist

## Importância do Script Estruturado

Um script bem estruturado:

- Garante consistência na abordagem
- Cobre todos os pontos importantes
- Reduz ansiedade do vendedor
- Melhora taxa de conversão

## Estrutura do Script

### 1. Abertura e Rapport
- Apresentação pessoal e da empresa
- Criação de conexão com o cliente
- Identificação de necessidades

### 2. Apresentação do Produto
- Benefícios principais
- Diferenciais competitivos
- Cases de sucesso

### 3. Tratamento de Objeções
- Escuta ativa
- Respostas estruturadas
- Reforço de benefícios

### 4. Fechamento
- Criação de urgência
- Facilitação do pagamento
- Confirmação da decisão

## Material de Referência

Consulte o "Script Oficial 2020" para o texto completo e variações por situação.

[DOCUMENTO ANEXO: Script-Oficial-2020.docx]

## Personalização do Script

Lembre-se de:
- Adaptar à sua personalidade
- Considerar o perfil do cliente
- Praticar até ficar natural
- Atualizar conforme feedback
        """,
        order_index=6,
        lesson_type='text',
        duration_minutes=45,
        is_active=True
    )
    db.session.add(script_lesson)
    db.session.commit()
    
    # Adicionar arquivo de script
    script_path = os.path.join(docs_path, 'Script-Oficial-2020.docx')
    if os.path.exists(script_path):
        media_file = MediaFile(
            filename='script_oficial_2020.docx',
            original_filename='Script Oficial 2020.docx',
            file_path=script_path,
            file_type='document',
            file_size=os.path.getsize(script_path),
            mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            lesson_id=script_lesson.id
        )
        db.session.add(media_file)

def integrate_seguro_internacao(module, docs_path):
    """Integra informações do seguro internação"""
    
    # Atualizar lição 3.3 com informações do seguro internação
    lesson_33 = Lesson.query.filter_by(module_id=module.id, order_index=3).first()
    if lesson_33:
        # Adicionar arquivo do resumo
        seguro_path = os.path.join(docs_path, 'resumo-Seguro-Internacao.docx')
        if os.path.exists(seguro_path):
            media_file = MediaFile(
                filename='resumo_seguro_internacao.docx',
                original_filename='Resumo Seguro Internação.docx',
                file_path=seguro_path,
                file_type='document',
                file_size=os.path.getsize(seguro_path),
                mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                lesson_id=lesson_33.id
            )
            db.session.add(media_file)
            
            # Atualizar conteúdo
            lesson_33.content += """

## Documentação Oficial

Para informações técnicas completas sobre o Seguro Internação, incluindo condições gerais, coberturas específicas e processo de contratação, consulte o documento oficial em anexo.

[DOCUMENTO ANEXO: resumo-Seguro-Internacao.docx]
            """

def integrate_legislacao(module, docs_path):
    """Integra estudo sobre legislação"""
    
    # Criar lição sobre legislação
    legislacao_lesson = Lesson(
        module_id=module.id,
        title='Legislação dos Planos Funerários - Lei 13.261/2016',
        content="""
# Legislação dos Planos Funerários no Brasil

## Lei 13.261/2016 - Marco Regulatório

A Lei nº 13.261, de 22 de março de 2016, estabeleceu a regulamentação federal para planos de assistência funerária no Brasil.

## Principais Pontos da Legislação

### Empresas Autorizadas
- Apenas empresas criadas especificamente para administrar planos funerários
- Necessidade de autorização do poder público municipal
- Cumprimento de exigências financeiras específicas

### Obrigações Contratuais
- Contrato detalhado obrigatório
- Descrição completa dos serviços
- Condições de cancelamento claras
- Regras de reajuste transparentes

### Garantias Financeiras
- Patrimônio líquido mínimo (12% da receita líquida anual)
- Reserva de solvência (10% do faturamento)
- Capital mínimo (5% da receita de contratos novos)
- Auditoria contábil independente

### Fiscalização
- Sistema Nacional de Defesa do Consumidor
- Penalidades por descumprimento
- Possibilidade de interdição em casos graves

## Importância para o Vendedor

Conhecer a legislação permite:
- Transmitir segurança ao cliente
- Explicar garantias legais
- Diferenciar empresas regulares das irregulares
- Responder questionamentos técnicos

## Estudo Completo

Para análise detalhada da legislação, incluindo atualizações para 2025 e interpretações práticas, consulte o estudo completo em anexo.

[DOCUMENTO ANEXO: EstudoCompletosobreaLeidosPlanosFunerarios.md]
        """,
        order_index=7,
        lesson_type='text',
        duration_minutes=30,
        is_active=True
    )
    db.session.add(legislacao_lesson)
    db.session.commit()
    
    # Adicionar arquivo de legislação
    legislacao_path = os.path.join(docs_path, 'EstudoCompletosobreaLeidosPlanosFunerarios.md')
    if os.path.exists(legislacao_path):
        media_file = MediaFile(
            filename='estudo_legislacao.md',
            original_filename='Estudo Completo sobre a Lei dos Planos Funerários.md',
            file_path=legislacao_path,
            file_type='document',
            file_size=os.path.getsize(legislacao_path),
            mime_type='text/markdown',
            lesson_id=legislacao_lesson.id
        )
        db.session.add(media_file)

if __name__ == '__main__':
    # Este script deve ser executado no contexto da aplicação Flask
    print("Execute este script através da aplicação Flask principal")

