from src.models.user import db, User
from src.models.module import Module, Lesson
from src.models.quiz import Quiz, Question
from datetime import datetime, date
import json

def create_initial_data():
    """Cria dados iniciais para o sistema de treinamento da Amar Assist"""
    
    # Verificar se já existem dados
    if Module.query.first():
        return  # Dados já existem
    
    try:
        # Criar usuário administrador padrão
        admin_user = User(
            username='admin',
            email='admin@amarassist.com.br',
            full_name='Administrador do Sistema',
            department='TI',
            position='Administrador',
            hire_date=date.today(),
            is_admin=True,
            is_active=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # Criar usuário de teste para vendas
        sales_user = User(
            username='vendedor_teste',
            email='vendedor@amarassist.com.br',
            full_name='Vendedor de Teste',
            department='Vendas',
            position='Consultor de Vendas',
            hire_date=date.today(),
            is_admin=False,
            is_active=True
        )
        sales_user.set_password('vendedor123')
        db.session.add(sales_user)
        
        # Módulo 1: Fundamentos do Mercado
        module1 = Module(
            title='Fundamentos do Mercado Funerário',
            description='Compreenda o mercado brasileiro de planos funerários, regulamentações e oportunidades de negócio.',
            order_index=1,
            is_active=True
        )
        db.session.add(module1)
        
        # Módulo 2: Conhecimento da Empresa
        module2 = Module(
            title='Conhecimento da Amar Assist',
            description='História, cultura, posicionamento e estrutura da maior insurtech brasileira de pós-saúde.',
            order_index=2,
            is_active=True
        )
        db.session.add(module2)
        
        # Módulo 3: Portfólio de Produtos e Serviços (FOCO PRINCIPAL)
        module3 = Module(
            title='Portfólio de Produtos e Serviços',
            description='Conheça em detalhes todos os produtos da Amar Assist: planos funerários, jazigos, assistências 24h e seguros.',
            order_index=3,
            is_active=True
        )
        db.session.add(module3)
        
        db.session.commit()  # Commit para obter IDs dos módulos
        
        # IMPLEMENTAÇÃO DETALHADA DO MÓDULO 3.1 - TÉCNICAS DE VENDAS
        
        # Lição 3.1: Planos Funerários Familiares
        lesson_31 = Lesson(
            module_id=module3.id,
            title='Planos Funerários Familiares - Características e Benefícios',
            content='''
# Planos Funerários Familiares Amar Assist

## Visão Geral
Os Planos Funerários Familiares da Amar Assist representam a principal linha de produtos da empresa, oferecendo proteção completa para toda a família em momentos de maior necessidade.

## Características Principais

### Cobertura Nacional
- Rede de mais de 3.000 funerárias parceiras
- Atendimento 24 horas por dia, 7 dias por semana
- Cobertura em todo território nacional

### Tipos de Planos Disponíveis
1. **Plano Básico**: Cobertura essencial com serviços fundamentais
2. **Plano Intermediário**: Cobertura ampliada com benefícios adicionais
3. **Plano Premium**: Cobertura completa com todos os benefícios

### Benefícios Inclusos
- Assistência funeral completa
- Traslado nacional e internacional
- Assistência psicológica para a família
- Seguro de vida gratuito incluso
- Carência reduzida para acidentes

## Diferenciais Competitivos

### 1. Maior Rede do Brasil
Com mais de 3.000 funerárias parceiras, garantimos atendimento em qualquer localidade do país.

### 2. Avaliação 4.7/5 no Reclame Aqui
Reconhecimento pela qualidade do atendimento e resolução de problemas.

### 3. Tecnologia e Inovação
- Aplicativo móvel para solicitações
- Plataforma digital completa
- Atendimento via WhatsApp

### 4. Experiência no Mercado
Mais de 125 mil clientes protegidos e anos de experiência no setor.

## Público-Alvo

### Perfil Demográfico
- Famílias de classe média e média alta
- Idade entre 35 e 65 anos
- Renda familiar acima de R$ 3.000

### Motivações de Compra
- Proteção da família
- Planejamento financeiro
- Tranquilidade em momentos difíceis
- Evitar custos elevados de última hora

## Processo de Vendas

### 1. Identificação de Necessidades
- Compreender a estrutura familiar
- Avaliar preocupações específicas
- Identificar experiências anteriores

### 2. Apresentação de Soluções
- Demonstrar benefícios específicos
- Comparar com concorrentes
- Mostrar casos de sucesso

### 3. Tratamento de Objeções
- Questões sobre preço
- Dúvidas sobre cobertura
- Preocupações com carência

### 4. Fechamento
- Urgência baseada em proteção
- Facilidades de pagamento
- Garantias oferecidas

## Materiais de Apoio
[PLACEHOLDER PARA VÍDEO: Apresentação dos Planos Funerários]
[PLACEHOLDER PARA PDF: Tabela Completa de Planos e Preços]
[PLACEHOLDER PARA ÁUDIO: Depoimentos de Clientes Satisfeitos]
            ''',
            order_index=1,
            lesson_type='text',
            duration_minutes=45,
            is_active=True
        )
        db.session.add(lesson_31)
        
        # Lição 3.2: Planos Jazigo Garantido
        lesson_32 = Lesson(
            module_id=module3.id,
            title='Planos Jazigo Garantido - Investimento e Proteção',
            content='''
# Planos Jazigo Garantido

## Conceito e Importância
O Plano Jazigo Garantido representa uma das soluções mais completas da Amar Assist, combinando proteção funerária com investimento em patrimônio familiar.

## Características do Produto

### Tipos de Jazigos
1. **Jazigo Simples**: Para 2 pessoas
2. **Jazigo Familiar**: Para 4 pessoas  
3. **Jazigo Premium**: Para 6 pessoas

### Localização
- Cemitérios de primeira linha
- Localizações privilegiadas
- Fácil acesso para visitação

## Vantagens Competitivas

### Investimento Patrimonial
- Valorização ao longo do tempo
- Patrimônio transferível para herdeiros
- Proteção contra inflação

### Garantia de Disponibilidade
- Reserva garantida em cemitérios parceiros
- Sem preocupação com disponibilidade futura
- Localização privilegiada assegurada

## Argumentos de Venda

### Para Famílias Tradicionais
- Manutenção da unidade familiar
- Tradição e valores familiares
- Investimento para gerações futuras

### Para Investidores
- Ativo real com valorização
- Proteção contra inflação
- Diversificação de portfólio

[PLACEHOLDER PARA VÍDEO: Tour Virtual pelos Cemitérios Parceiros]
[PLACEHOLDER PARA IMAGEM: Galeria de Jazigos Disponíveis]
            ''',
            order_index=2,
            lesson_type='text',
            duration_minutes=30,
            is_active=True
        )
        db.session.add(lesson_32)
        
        # Lição 3.3: Seguros Complementares
        lesson_33 = Lesson(
            module_id=module3.id,
            title='Seguros de Vida e Internação - Proteção Completa',
            content='''
# Seguros Complementares Amar Assist

## Seguro de Vida Gratuito

### Características
- Incluso automaticamente nos planos funerários
- Cobertura por morte natural ou acidental
- Valor da indenização varia conforme o plano

### Benefícios
- Proteção adicional sem custo extra
- Auxílio financeiro para a família
- Processo de indenização simplificado

## Seguro Internação

### Cobertura
- Diária por internação hospitalar
- Cobertura nacional
- Sem carência para acidentes

### Público-Alvo
- Autônomos e profissionais liberais
- Complemento ao plano de saúde
- Proteção de renda familiar

## Estratégias de Cross-Selling

### Identificação de Oportunidades
- Cliente já interessado em proteção
- Necessidades complementares
- Momento ideal para oferta

### Apresentação Integrada
- Mostrar como os produtos se complementam
- Benefícios do pacote completo
- Economia na contratação conjunta

[PLACEHOLDER PARA PDF: Resumo Completo do Seguro Internação]
[PLACEHOLDER PARA ÁUDIO: Explicação dos Benefícios do Seguro de Vida]
            ''',
            order_index=3,
            lesson_type='text',
            duration_minutes=25,
            is_active=True
        )
        db.session.add(lesson_33)
        
        db.session.commit()  # Commit para obter IDs das lições
        
        # CRIAR QUIZZES PARA CADA LIÇÃO
        
        # Quiz da Lição 3.1
        quiz_31 = Quiz(
            lesson_id=lesson_31.id,
            title='Avaliação: Planos Funerários Familiares',
            description='Teste seus conhecimentos sobre os planos funerários da Amar Assist',
            passing_score=80,
            max_attempts=3,
            time_limit_minutes=15,
            is_active=True
        )
        db.session.add(quiz_31)
        db.session.commit()
        
        # Questões do Quiz 3.1
        questions_31 = [
            {
                'question_text': 'Quantas funerárias parceiras a Amar Assist possui em sua rede?',
                'question_type': 'multiple_choice',
                'options': ['Mais de 1.000', 'Mais de 2.000', 'Mais de 3.000', 'Mais de 5.000'],
                'correct_answer': 'Mais de 3.000',
                'explanation': 'A Amar Assist possui a maior rede do Brasil com mais de 3.000 funerárias parceiras.',
                'points': 2,
                'order_index': 1
            },
            {
                'question_text': 'Qual é a avaliação da Amar Assist no Reclame Aqui?',
                'question_type': 'multiple_choice',
                'options': ['4.5/5', '4.7/5', '4.8/5', '4.9/5'],
                'correct_answer': '4.7/5',
                'explanation': 'A Amar Assist mantém uma excelente avaliação de 4.7/5 no Reclame Aqui.',
                'points': 1,
                'order_index': 2
            },
            {
                'question_text': 'O seguro de vida é incluso gratuitamente nos planos funerários?',
                'question_type': 'true_false',
                'options': ['Verdadeiro', 'Falso'],
                'correct_answer': 'Verdadeiro',
                'explanation': 'Sim, todos os planos funerários incluem seguro de vida gratuito.',
                'points': 2,
                'order_index': 3
            },
            {
                'question_text': 'Quantos clientes a Amar Assist possui atualmente protegidos?',
                'question_type': 'multiple_choice',
                'options': ['Mais de 100 mil', 'Mais de 125 mil', 'Mais de 150 mil', 'Mais de 200 mil'],
                'correct_answer': 'Mais de 125 mil',
                'explanation': 'A Amar Assist protege mais de 125 mil clientes em todo o Brasil.',
                'points': 1,
                'order_index': 4
            },
            {
                'question_text': 'Qual é o principal diferencial competitivo da Amar Assist?',
                'question_type': 'multiple_choice',
                'options': ['Preço mais baixo', 'Maior rede de funerárias', 'Atendimento local apenas', 'Produtos limitados'],
                'correct_answer': 'Maior rede de funerárias',
                'explanation': 'O principal diferencial é possuir a maior rede de funerárias parceiras do Brasil.',
                'points': 2,
                'order_index': 5
            }
        ]
        
        for q_data in questions_31:
            question = Question(
                quiz_id=quiz_31.id,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                points=q_data['points'],
                order_index=q_data['order_index']
            )
            question.set_options(q_data['options'])
            db.session.add(question)
        
        # Quiz da Lição 3.2
        quiz_32 = Quiz(
            lesson_id=lesson_32.id,
            title='Avaliação: Planos Jazigo Garantido',
            description='Avalie seu conhecimento sobre os planos de jazigo',
            passing_score=75,
            max_attempts=3,
            time_limit_minutes=10,
            is_active=True
        )
        db.session.add(quiz_32)
        db.session.commit()
        
        # Questões do Quiz 3.2
        questions_32 = [
            {
                'question_text': 'Qual é a principal vantagem do Plano Jazigo Garantido como investimento?',
                'question_type': 'multiple_choice',
                'options': ['Liquidez imediata', 'Valorização ao longo do tempo', 'Rendimento mensal', 'Isenção de impostos'],
                'correct_answer': 'Valorização ao longo do tempo',
                'explanation': 'O jazigo é um ativo real que se valoriza ao longo do tempo, protegendo contra inflação.',
                'points': 2,
                'order_index': 1
            },
            {
                'question_text': 'O jazigo pode ser transferido para herdeiros?',
                'question_type': 'true_false',
                'options': ['Verdadeiro', 'Falso'],
                'correct_answer': 'Verdadeiro',
                'explanation': 'Sim, o jazigo é um patrimônio familiar transferível para herdeiros.',
                'points': 1,
                'order_index': 2
            },
            {
                'question_text': 'Quantas pessoas o Jazigo Premium comporta?',
                'question_type': 'multiple_choice',
                'options': ['2 pessoas', '4 pessoas', '6 pessoas', '8 pessoas'],
                'correct_answer': '6 pessoas',
                'explanation': 'O Jazigo Premium é projetado para comportar até 6 pessoas.',
                'points': 1,
                'order_index': 3
            }
        ]
        
        for q_data in questions_32:
            question = Question(
                quiz_id=quiz_32.id,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                points=q_data['points'],
                order_index=q_data['order_index']
            )
            question.set_options(q_data['options'])
            db.session.add(question)
        
        # Quiz da Lição 3.3
        quiz_33 = Quiz(
            lesson_id=lesson_33.id,
            title='Avaliação: Seguros Complementares',
            description='Teste seus conhecimentos sobre os seguros oferecidos',
            passing_score=70,
            max_attempts=3,
            time_limit_minutes=10,
            is_active=True
        )
        db.session.add(quiz_33)
        db.session.commit()
        
        # Questões do Quiz 3.3
        questions_33 = [
            {
                'question_text': 'O Seguro de Vida é cobrado separadamente do plano funerário?',
                'question_type': 'true_false',
                'options': ['Verdadeiro', 'Falso'],
                'correct_answer': 'Falso',
                'explanation': 'O Seguro de Vida é incluso gratuitamente em todos os planos funerários.',
                'points': 2,
                'order_index': 1
            },
            {
                'question_text': 'Qual é o público-alvo principal do Seguro Internação?',
                'question_type': 'multiple_choice',
                'options': ['Funcionários CLT', 'Autônomos e profissionais liberais', 'Aposentados apenas', 'Estudantes'],
                'correct_answer': 'Autônomos e profissionais liberais',
                'explanation': 'O Seguro Internação é ideal para autônomos e profissionais liberais como complemento ao plano de saúde.',
                'points': 2,
                'order_index': 2
            },
            {
                'question_text': 'O que é cross-selling no contexto dos produtos Amar Assist?',
                'question_type': 'multiple_choice',
                'options': ['Vender apenas um produto', 'Oferecer produtos complementares', 'Cancelar produtos existentes', 'Reduzir preços'],
                'correct_answer': 'Oferecer produtos complementares',
                'explanation': 'Cross-selling é a estratégia de oferecer produtos complementares que atendam necessidades adicionais do cliente.',
                'points': 1,
                'order_index': 3
            }
        ]
        
        for q_data in questions_33:
            question = Question(
                quiz_id=quiz_33.id,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                points=q_data['points'],
                order_index=q_data['order_index']
            )
            question.set_options(q_data['options'])
            db.session.add(question)
        
        db.session.commit()
        print("Dados iniciais criados com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar dados iniciais: {str(e)}")
        raise e

