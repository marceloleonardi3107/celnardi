from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.module import Module, Lesson, MediaFile
from src.models.progress import UserProgress
from datetime import datetime

modules_bp = Blueprint('modules', __name__)

@modules_bp.route('/modules', methods=['GET'])
def get_modules():
    """Retorna todos os módulos ativos"""
    try:
        modules = Module.query.filter_by(is_active=True).order_by(Module.order_index).all()
        return jsonify({
            'success': True,
            'modules': [module.to_dict() for module in modules]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar módulos: {str(e)}'
        }), 500

@modules_bp.route('/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
    """Retorna um módulo específico com suas lições"""
    try:
        module = Module.query.get_or_404(module_id)
        lessons = Lesson.query.filter_by(
            module_id=module_id, 
            is_active=True
        ).order_by(Lesson.order_index).all()
        
        module_data = module.to_dict()
        module_data['lessons'] = [lesson.to_dict() for lesson in lessons]
        
        return jsonify({
            'success': True,
            'module': module_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar módulo: {str(e)}'
        }), 500

@modules_bp.route('/modules/<int:module_id>/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson(module_id, lesson_id):
    """Retorna uma lição específica"""
    try:
        lesson = Lesson.query.filter_by(
            id=lesson_id, 
            module_id=module_id,
            is_active=True
        ).first_or_404()
        
        # Buscar arquivos de mídia associados
        media_files = MediaFile.query.filter_by(lesson_id=lesson_id).all()
        
        lesson_data = lesson.to_dict()
        lesson_data['media_files'] = [media.to_dict() for media in media_files]
        
        return jsonify({
            'success': True,
            'lesson': lesson_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar lição: {str(e)}'
        }), 500

@modules_bp.route('/modules/<int:module_id>/progress', methods=['POST'])
def update_progress():
    """Atualiza o progresso do usuário em um módulo"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        lesson_id = data.get('lesson_id')
        status = data.get('status', 'in_progress')
        progress_percentage = data.get('progress_percentage', 0)
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'ID do usuário é obrigatório'
            }), 400
        
        # Buscar ou criar registro de progresso
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            module_id=module_id,
            lesson_id=lesson_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                module_id=module_id,
                lesson_id=lesson_id,
                started_at=datetime.utcnow()
            )
            db.session.add(progress)
        
        progress.status = status
        progress.progress_percentage = progress_percentage
        progress.last_accessed_at = datetime.utcnow()
        
        if status == 'completed' and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'progress': progress.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar progresso: {str(e)}'
        }), 500

@modules_bp.route('/users/<int:user_id>/progress', methods=['GET'])
def get_user_progress(user_id):
    """Retorna o progresso de um usuário em todos os módulos"""
    try:
        progress_records = UserProgress.query.filter_by(user_id=user_id).all()
        
        # Organizar progresso por módulo
        progress_by_module = {}
        for progress in progress_records:
            module_id = progress.module_id
            if module_id not in progress_by_module:
                progress_by_module[module_id] = {
                    'module_id': module_id,
                    'lessons': [],
                    'overall_progress': 0,
                    'completed_lessons': 0,
                    'total_lessons': 0
                }
            
            progress_by_module[module_id]['lessons'].append(progress.to_dict())
            if progress.status == 'completed':
                progress_by_module[module_id]['completed_lessons'] += 1
            progress_by_module[module_id]['total_lessons'] += 1
        
        # Calcular progresso geral por módulo
        for module_data in progress_by_module.values():
            if module_data['total_lessons'] > 0:
                module_data['overall_progress'] = (
                    module_data['completed_lessons'] / module_data['total_lessons']
                ) * 100
        
        return jsonify({
            'success': True,
            'progress': list(progress_by_module.values())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar progresso: {str(e)}'
        }), 500

