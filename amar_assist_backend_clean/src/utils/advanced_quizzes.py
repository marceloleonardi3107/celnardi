"""
Quizzes avançados baseados no conteúdo real dos documentos fornecidos
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.user import db
from src.models.module import Module, Lesson
from src.models.quiz import Quiz, Question

def create_advanced_quizzes():
    """Cria quizzes avançados baseados nos documentos reais"""
    
    try:
        # Buscar módulo 3
        module3 = Module.query.filter_by(title='Portfólio de Produtos e Serviços').first()
        if not module3:
            print("Módulo 3 não encontrado")
            return
        
        # Criar quizzes para as novas lições
        create_objecoes_quiz(module3)
        create_faq_quiz(module3)
        create_script_quiz(module3)
        create_legislacao_quiz(module3)
        
        db.session.commit()
        print("Quizzes avançados criados com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar quizzes avançados: {str(e)}")

def create_objecoes_quiz(module):
    """Cria quiz sobre tratamento de objeções"""
    
    # Buscar lição de objeções
    objecoes_lesson = Lesson.query.filter_by(
        module_id=module.id,
        title='Tratamento de Objeções - Técnicas Avançadas'
    ).first()
    
    if not objecoes_lesson:
        return
    
    # Criar quiz
    quiz = Quiz(
        lesson_id=objecoes_lesson.id,
        title='Avaliação: Tratamento de Objeções',
        description='Teste suas habilidades em tratamento de objeções de vendas',
        passing_score=80,
        max_attempts=3,
        time_limit_minutes=20,
        is_active=True
    )
    db.session.add(quiz)
    db.session.commit()
    
    # Questões baseadas em objeções reais
    questions = [
        {
            'question_text': 'Qual é a melhor resposta para a objeção "Está muito caro"?',
            'question_type': 'multiple_choice',
            'options': [
                'Posso fazer um desconto especial para você',
                'Vamos demonstrar o valor vs. custo de um funeral sem plano',
                'Nossos concorrentes cobram mais caro',
                'O preço é fixo, não posso alterar'
            ],
            'correct_answer': 'Vamos demonstrar o valor vs. custo de um funeral sem plano',
            'explanation': 'A melhor abordagem é demonstrar valor, mostrando que o custo do plano é muito menor que os gastos de um funeral sem proteção.',
            'points': 3,
            'order_index': 1
        },
        {
            'question_text': 'Como responder à objeção "Sou muito jovem, não preciso agora"?',
            'question_type': 'multiple_choice',
            'options': [
                'Realmente, você pode esperar mais alguns anos',
                'Acidentes não escolhem idade e temos carência reduzida para acidentes',
                'Jovens pagam mais caro se esperarem',
                'Todos os jovens falam isso'
            ],
            'correct_answer': 'Acidentes não escolhem idade e temos carência reduzida para acidentes',
            'explanation': 'É importante mostrar que a proteção é necessária em qualquer idade, especialmente considerando acidentes.',
            'points': 3,
            'order_index': 2
        },
        {
            'question_text': 'A avaliação da Amar Assist no Reclame Aqui é um argumento válido contra objeções de confiança?',
            'question_type': 'true_false',
            'options': ['Verdadeiro', 'Falso'],
            'correct_answer': 'Verdadeiro',
            'explanation': 'Sim, a avaliação 4.7/5 no Reclame Aqui é uma prova concreta da confiabilidade da empresa.',
            'points': 2,
            'order_index': 3
        },
        {
            'question_text': 'Qual é a técnica mais eficaz para tratar objeções?',
            'question_type': 'multiple_choice',
            'options': [
                'Argumentar imediatamente contra a objeção',
                'Escutar, compreender, responder e confirmar',
                'Ignorar a objeção e continuar a apresentação',
                'Oferecer desconto imediatamente'
            ],
            'correct_answer': 'Escutar, compreender, responder e confirmar',
            'explanation': 'A técnica ECRC (Escutar, Compreender, Responder, Confirmar) é a mais eficaz para tratamento de objeções.',
            'points': 2,
            'order_index': 4
        },
        {
            'question_text': 'Quantas funerárias parceiras a Amar Assist possui para usar como argumento de cobertura?',
            'question_type': 'multiple_choice',
            'options': [
                'Mais de 1.500',
                'Mais de 2.500',
                'Mais de 3.000',
                'Mais de 4.000'
            ],
            'correct_answer': 'Mais de 3.000',
            'explanation': 'A Amar Assist possui mais de 3.000 funerárias parceiras, sendo a maior rede do Brasil.',
            'points': 1,
            'order_index': 5
        }
    ]
    
    for q_data in questions:
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data['question_text'],
            question_type=q_data['question_type'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            points=q_data['points'],
            order_index=q_data['order_index']
        )
        question.set_options(q_data['options'])
        db.session.add(question)

def create_faq_quiz(module):
    """Cria quiz sobre perguntas frequentes"""
    
    faq_lesson = Lesson.query.filter_by(
        module_id=module.id,
        title='Perguntas Frequentes - Produtos Amar Assist'
    ).first()
    
    if not faq_lesson:
        return
    
    quiz = Quiz(
        lesson_id=faq_lesson.id,
        title='Avaliação: Perguntas Frequentes',
        description='Teste seu conhecimento sobre as perguntas mais comuns dos clientes',
        passing_score=75,
        max_attempts=3,
        time_limit_minutes=15,
        is_active=True
    )
    db.session.add(quiz)
    db.session.commit()
    
    questions = [
        {
            'question_text': 'Qual é o principal benefício de conhecer bem as perguntas frequentes?',
            'question_type': 'multiple_choice',
            'options': [
                'Impressionar o cliente com conhecimento',
                'Antecipar dúvidas e acelerar o processo de vendas',
                'Evitar fazer apresentações longas',
                'Mostrar superioridade sobre concorrentes'
            ],
            'correct_answer': 'Antecipar dúvidas e acelerar o processo de vendas',
            'explanation': 'Conhecer as FAQs permite antecipar dúvidas, fornecendo respostas precisas que aceleram a decisão de compra.',
            'points': 2,
            'order_index': 1
        },
        {
            'question_text': 'As perguntas sobre carência são frequentes em planos funerários?',
            'question_type': 'true_false',
            'options': ['Verdadeiro', 'Falso'],
            'correct_answer': 'Verdadeiro',
            'explanation': 'Sim, questões sobre carência estão entre as mais frequentes, especialmente sobre carência reduzida para acidentes.',
            'points': 1,
            'order_index': 2
        },
        {
            'question_text': 'Qual categoria de perguntas é mais comum sobre jazigos?',
            'question_type': 'multiple_choice',
            'options': [
                'Preços e formas de pagamento',
                'Localização e disponibilidade',
                'Processo de construção',
                'Materiais utilizados'
            ],
            'correct_answer': 'Localização e disponibilidade',
            'explanation': 'Clientes se preocupam principalmente com a localização dos cemitérios e disponibilidade de jazigos.',
            'points': 2,
            'order_index': 3
        }
    ]
    
    for q_data in questions:
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data['question_text'],
            question_type=q_data['question_type'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            points=q_data['points'],
            order_index=q_data['order_index']
        )
        question.set_options(q_data['options'])
        db.session.add(question)

def create_script_quiz(module):
    """Cria quiz sobre script de vendas"""
    
    script_lesson = Lesson.query.filter_by(
        module_id=module.id,
        title='Script Oficial de Vendas - Modelo 2020'
    ).first()
    
    if not script_lesson:
        return
    
    quiz = Quiz(
        lesson_id=script_lesson.id,
        title='Avaliação: Script de Vendas',
        description='Avalie seu conhecimento sobre a estrutura e uso do script oficial',
        passing_score=80,
        max_attempts=3,
        time_limit_minutes=15,
        is_active=True
    )
    db.session.add(quiz)
    db.session.commit()
    
    questions = [
        {
            'question_text': 'Qual é a primeira etapa do script estruturado de vendas?',
            'question_type': 'multiple_choice',
            'options': [
                'Apresentação do produto',
                'Abertura e rapport',
                'Tratamento de objeções',
                'Fechamento da venda'
            ],
            'correct_answer': 'Abertura e rapport',
            'explanation': 'A abertura e criação de rapport é fundamental para estabelecer conexão e confiança com o cliente.',
            'points': 2,
            'order_index': 1
        },
        {
            'question_text': 'O script deve ser seguido rigidamente sem adaptações?',
            'question_type': 'true_false',
            'options': ['Verdadeiro', 'Falso'],
            'correct_answer': 'Falso',
            'explanation': 'O script deve ser adaptado à personalidade do vendedor e ao perfil do cliente, mantendo a estrutura base.',
            'points': 2,
            'order_index': 2
        },
        {
            'question_text': 'Qual é o principal objetivo da etapa de fechamento?',
            'question_type': 'multiple_choice',
            'options': [
                'Resumir todos os benefícios apresentados',
                'Criar urgência e facilitar a decisão de compra',
                'Agendar uma nova reunião',
                'Entregar materiais informativos'
            ],
            'correct_answer': 'Criar urgência e facilitar a decisão de compra',
            'explanation': 'O fechamento deve criar senso de urgência e facilitar a tomada de decisão, removendo obstáculos.',
            'points': 2,
            'order_index': 3
        }
    ]
    
    for q_data in questions:
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data['question_text'],
            question_type=q_data['question_type'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            points=q_data['points'],
            order_index=q_data['order_index']
        )
        question.set_options(q_data['options'])
        db.session.add(question)

def create_legislacao_quiz(module):
    """Cria quiz sobre legislação"""
    
    legislacao_lesson = Lesson.query.filter_by(
        module_id=module.id,
        title='Legislação dos Planos Funerários - Lei 13.261/2016'
    ).first()
    
    if not legislacao_lesson:
        return
    
    quiz = Quiz(
        lesson_id=legislacao_lesson.id,
        title='Avaliação: Legislação dos Planos Funerários',
        description='Teste seus conhecimentos sobre a Lei 13.261/2016 e regulamentações',
        passing_score=85,
        max_attempts=3,
        time_limit_minutes=20,
        is_active=True
    )
    db.session.add(quiz)
    db.session.commit()
    
    questions = [
        {
            'question_text': 'Qual lei regulamenta os planos funerários no Brasil?',
            'question_type': 'multiple_choice',
            'options': [
                'Lei 12.345/2015',
                'Lei 13.261/2016',
                'Lei 14.123/2017',
                'Lei 11.987/2014'
            ],
            'correct_answer': 'Lei 13.261/2016',
            'explanation': 'A Lei nº 13.261, de 22 de março de 2016, é o marco regulatório dos planos funerários no Brasil.',
            'points': 2,
            'order_index': 1
        },
        {
            'question_text': 'Qual é o patrimônio líquido mínimo exigido das empresas administradoras?',
            'question_type': 'multiple_choice',
            'options': [
                '10% da receita líquida anual',
                '12% da receita líquida anual',
                '15% da receita líquida anual',
                '8% da receita líquida anual'
            ],
            'correct_answer': '12% da receita líquida anual',
            'explanation': 'A lei exige patrimônio líquido mínimo de 12% da receita líquida anual dos contratos.',
            'points': 3,
            'order_index': 2
        },
        {
            'question_text': 'Apenas empresas criadas especificamente para administrar planos funerários podem comercializá-los?',
            'question_type': 'true_false',
            'options': ['Verdadeiro', 'Falso'],
            'correct_answer': 'Verdadeiro',
            'explanation': 'Sim, a lei estabelece que apenas empresas criadas especificamente para este fim podem administrar planos funerários.',
            'points': 2,
            'order_index': 3
        },
        {
            'question_text': 'Qual órgão é responsável pela fiscalização dos planos funerários?',
            'question_type': 'multiple_choice',
            'options': [
                'Banco Central',
                'SUSEP',
                'Sistema Nacional de Defesa do Consumidor',
                'Ministério da Fazenda'
            ],
            'correct_answer': 'Sistema Nacional de Defesa do Consumidor',
            'explanation': 'A fiscalização compete aos órgãos do Sistema Nacional de Defesa do Consumidor.',
            'points': 2,
            'order_index': 4
        },
        {
            'question_text': 'A reserva de solvência exigida é de quanto do faturamento?',
            'question_type': 'multiple_choice',
            'options': [
                '8%',
                '10%',
                '12%',
                '15%'
            ],
            'correct_answer': '10%',
            'explanation': 'A lei exige reserva de solvência de 10% do faturamento em bens ativos.',
            'points': 2,
            'order_index': 5
        }
    ]
    
    for q_data in questions:
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data['question_text'],
            question_type=q_data['question_type'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            points=q_data['points'],
            order_index=q_data['order_index']
        )
        question.set_options(q_data['options'])
        db.session.add(question)

if __name__ == '__main__':
    print("Execute este script através da aplicação Flask principal")

