from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.quiz import Quiz, Question, QuizAttempt, QuizAnswer
from src.models.progress import UserActivity
from datetime import datetime
import json

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/lessons/<int:lesson_id>/quiz', methods=['GET'])
def get_lesson_quiz(lesson_id):
    """Retorna o quiz de uma lição específica"""
    try:
        quiz = Quiz.query.filter_by(lesson_id=lesson_id, is_active=True).first()
        
        if not quiz:
            return jsonify({
                'success': False,
                'message': 'Quiz não encontrado para esta lição'
            }), 404
        
        questions = Question.query.filter_by(quiz_id=quiz.id).order_by(Question.order_index).all()
        
        quiz_data = quiz.to_dict()
        quiz_data['questions'] = [question.to_dict() for question in questions]
        
        return jsonify({
            'success': True,
            'quiz': quiz_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar quiz: {str(e)}'
        }), 500

@quiz_bp.route('/quiz/<int:quiz_id>/start', methods=['POST'])
def start_quiz_attempt(quiz_id):
    """Inicia uma nova tentativa de quiz"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'ID do usuário é obrigatório'
            }), 400
        
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Verificar se o usuário já atingiu o limite de tentativas
        attempts_count = QuizAttempt.query.filter_by(
            quiz_id=quiz_id,
            user_id=user_id
        ).count()
        
        if attempts_count >= quiz.max_attempts:
            return jsonify({
                'success': False,
                'message': f'Limite de {quiz.max_attempts} tentativas atingido'
            }), 400
        
        # Criar nova tentativa
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            user_id=user_id,
            started_at=datetime.utcnow()
        )
        
        db.session.add(attempt)
        db.session.commit()
        
        # Registrar atividade
        activity = UserActivity(
            user_id=user_id,
            activity_type='quiz_attempt',
            quiz_id=quiz_id,
            details=json.dumps({'attempt_id': attempt.id, 'action': 'started'})
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'attempt': attempt.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao iniciar quiz: {str(e)}'
        }), 500

@quiz_bp.route('/quiz/attempt/<int:attempt_id>/answer', methods=['POST'])
def submit_quiz_answer(attempt_id):
    """Submete uma resposta para uma questão do quiz"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        user_answer = data.get('answer')
        
        if not question_id or user_answer is None:
            return jsonify({
                'success': False,
                'message': 'ID da questão e resposta são obrigatórios'
            }), 400
        
        attempt = QuizAttempt.query.get_or_404(attempt_id)
        question = Question.query.get_or_404(question_id)
        
        # Verificar se a resposta já foi submetida
        existing_answer = QuizAnswer.query.filter_by(
            attempt_id=attempt_id,
            question_id=question_id
        ).first()
        
        if existing_answer:
            return jsonify({
                'success': False,
                'message': 'Resposta já foi submetida para esta questão'
            }), 400
        
        # Avaliar a resposta
        is_correct = False
        points_earned = 0
        
        if question.question_type == 'multiple_choice':
            is_correct = str(user_answer).strip() == str(question.correct_answer).strip()
        elif question.question_type == 'true_false':
            is_correct = str(user_answer).lower() == str(question.correct_answer).lower()
        elif question.question_type == 'text':
            # Para questões de texto, fazer comparação básica (pode ser melhorada)
            is_correct = str(user_answer).strip().lower() == str(question.correct_answer).strip().lower()
        
        if is_correct:
            points_earned = question.points
        
        # Salvar resposta
        answer = QuizAnswer(
            attempt_id=attempt_id,
            question_id=question_id,
            user_answer=str(user_answer),
            is_correct=is_correct,
            points_earned=points_earned
        )
        
        db.session.add(answer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'answer': answer.to_dict(),
            'is_correct': is_correct,
            'explanation': question.explanation if is_correct else None
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao submeter resposta: {str(e)}'
        }), 500

@quiz_bp.route('/quiz/attempt/<int:attempt_id>/complete', methods=['POST'])
def complete_quiz_attempt(attempt_id):
    """Finaliza uma tentativa de quiz e calcula a pontuação"""
    try:
        attempt = QuizAttempt.query.get_or_404(attempt_id)
        quiz = Quiz.query.get_or_404(attempt.quiz_id)
        
        # Calcular pontuação
        answers = QuizAnswer.query.filter_by(attempt_id=attempt_id).all()
        total_score = sum(answer.points_earned for answer in answers)
        
        # Calcular pontuação máxima possível
        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        max_score = sum(question.points for question in questions)
        
        # Calcular porcentagem
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        passed = percentage >= quiz.passing_score
        
        # Calcular tempo gasto
        time_taken = None
        if attempt.started_at:
            time_taken = int((datetime.utcnow() - attempt.started_at).total_seconds() / 60)
        
        # Atualizar tentativa
        attempt.score = total_score
        attempt.max_score = max_score
        attempt.percentage = percentage
        attempt.passed = passed
        attempt.completed_at = datetime.utcnow()
        attempt.time_taken_minutes = time_taken
        
        db.session.commit()
        
        # Registrar atividade
        activity = UserActivity(
            user_id=attempt.user_id,
            activity_type='quiz_attempt',
            quiz_id=quiz.id,
            details=json.dumps({
                'attempt_id': attempt.id,
                'action': 'completed',
                'score': total_score,
                'percentage': percentage,
                'passed': passed
            })
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'attempt': attempt.to_dict(),
            'feedback': {
                'passed': passed,
                'score': total_score,
                'max_score': max_score,
                'percentage': round(percentage, 2),
                'passing_score': quiz.passing_score,
                'time_taken_minutes': time_taken
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao finalizar quiz: {str(e)}'
        }), 500

@quiz_bp.route('/users/<int:user_id>/quiz-history', methods=['GET'])
def get_user_quiz_history(user_id):
    """Retorna o histórico de quizzes de um usuário"""
    try:
        attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(
            QuizAttempt.started_at.desc()
        ).all()
        
        history = []
        for attempt in attempts:
            attempt_data = attempt.to_dict()
            
            # Adicionar informações do quiz
            quiz = Quiz.query.get(attempt.quiz_id)
            if quiz:
                attempt_data['quiz_title'] = quiz.title
                attempt_data['lesson_id'] = quiz.lesson_id
            
            history.append(attempt_data)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar histórico: {str(e)}'
        }), 500

@quiz_bp.route('/quiz/attempt/<int:attempt_id>/results', methods=['GET'])
def get_quiz_results(attempt_id):
    """Retorna os resultados detalhados de uma tentativa de quiz"""
    try:
        attempt = QuizAttempt.query.get_or_404(attempt_id)
        answers = QuizAnswer.query.filter_by(attempt_id=attempt_id).all()
        
        results = {
            'attempt': attempt.to_dict(),
            'answers': []
        }
        
        for answer in answers:
            question = Question.query.get(answer.question_id)
            answer_data = answer.to_dict()
            answer_data['question'] = question.to_dict(include_correct_answer=True)
            results['answers'].append(answer_data)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar resultados: {str(e)}'
        }), 500

