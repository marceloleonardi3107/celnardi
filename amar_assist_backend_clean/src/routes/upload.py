from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from src.models.user import db
from src.models.module import MediaFile
import os
import uuid
from datetime import datetime

upload_bp = Blueprint('upload', __name__)

# Extensões permitidas por tipo de arquivo
ALLOWED_EXTENSIONS = {
    'video': {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'},
    'audio': {'mp3', 'wav', 'ogg', 'aac', 'm4a'},
    'image': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'},
    'pdf': {'pdf'},
    'document': {'doc', 'docx', 'txt', 'rtf'}
}

def allowed_file(filename, file_type=None):
    """Verifica se o arquivo tem uma extensão permitida"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if file_type:
        return extension in ALLOWED_EXTENSIONS.get(file_type, set())
    else:
        # Verificar em todos os tipos se não especificado
        all_extensions = set()
        for extensions in ALLOWED_EXTENSIONS.values():
            all_extensions.update(extensions)
        return extension in all_extensions

def get_file_type(filename):
    """Determina o tipo de arquivo baseado na extensão"""
    if '.' not in filename:
        return 'unknown'
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if extension in extensions:
            return file_type
    
    return 'unknown'

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload de arquivo multimídia"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'Nenhum arquivo foi enviado'
            }), 400
        
        file = request.files['file']
        lesson_id = request.form.get('lesson_id')
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'Nenhum arquivo foi selecionado'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': 'Tipo de arquivo não permitido'
            }), 400
        
        # Gerar nome único para o arquivo
        original_filename = file.filename
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Determinar tipo de arquivo
        file_type = get_file_type(original_filename)
        
        # Criar pasta por tipo se não existir
        type_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], file_type)
        os.makedirs(type_folder, exist_ok=True)
        
        # Caminho completo do arquivo
        file_path = os.path.join(type_folder, unique_filename)
        
        # Salvar arquivo
        file.save(file_path)
        
        # Obter informações do arquivo
        file_size = os.path.getsize(file_path)
        
        # Salvar informações no banco de dados
        media_file = MediaFile(
            filename=unique_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            mime_type=file.content_type,
            lesson_id=int(lesson_id) if lesson_id else None
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'file': media_file.to_dict(),
            'url': f'/api/media/{media_file.id}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao fazer upload: {str(e)}'
        }), 500

@upload_bp.route('/media/<int:file_id>', methods=['GET'])
def serve_media_file(file_id):
    """Serve um arquivo de mídia"""
    try:
        media_file = MediaFile.query.get_or_404(file_id)
        
        # Verificar se o arquivo existe
        if not os.path.exists(media_file.file_path):
            return jsonify({
                'success': False,
                'message': 'Arquivo não encontrado no sistema'
            }), 404
        
        directory = os.path.dirname(media_file.file_path)
        filename = os.path.basename(media_file.file_path)
        
        return send_from_directory(directory, filename)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao servir arquivo: {str(e)}'
        }), 500

@upload_bp.route('/media/<int:file_id>/info', methods=['GET'])
def get_media_info(file_id):
    """Retorna informações de um arquivo de mídia"""
    try:
        media_file = MediaFile.query.get_or_404(file_id)
        return jsonify({
            'success': True,
            'file': media_file.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar informações: {str(e)}'
        }), 500

@upload_bp.route('/lessons/<int:lesson_id>/media', methods=['GET'])
def get_lesson_media(lesson_id):
    """Retorna todos os arquivos de mídia de uma lição"""
    try:
        media_files = MediaFile.query.filter_by(lesson_id=lesson_id).all()
        
        files_by_type = {}
        for media_file in media_files:
            file_type = media_file.file_type
            if file_type not in files_by_type:
                files_by_type[file_type] = []
            
            file_data = media_file.to_dict()
            file_data['url'] = f'/api/media/{media_file.id}'
            files_by_type[file_type].append(file_data)
        
        return jsonify({
            'success': True,
            'media_files': files_by_type
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar arquivos: {str(e)}'
        }), 500

@upload_bp.route('/media/<int:file_id>', methods=['DELETE'])
def delete_media_file(file_id):
    """Remove um arquivo de mídia"""
    try:
        media_file = MediaFile.query.get_or_404(file_id)
        
        # Remover arquivo físico se existir
        if os.path.exists(media_file.file_path):
            os.remove(media_file.file_path)
        
        # Remover registro do banco
        db.session.delete(media_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Arquivo removido com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao remover arquivo: {str(e)}'
        }), 500

@upload_bp.route('/upload/batch', methods=['POST'])
def upload_multiple_files():
    """Upload de múltiplos arquivos"""
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'message': 'Nenhum arquivo foi enviado'
            }), 400
        
        files = request.files.getlist('files')
        lesson_id = request.form.get('lesson_id')
        
        uploaded_files = []
        errors = []
        
        for file in files:
            try:
                if file.filename == '':
                    continue
                
                if not allowed_file(file.filename):
                    errors.append(f'Arquivo {file.filename} não permitido')
                    continue
                
                # Processar arquivo (mesmo código do upload individual)
                original_filename = file.filename
                file_extension = original_filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
                
                file_type = get_file_type(original_filename)
                type_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], file_type)
                os.makedirs(type_folder, exist_ok=True)
                
                file_path = os.path.join(type_folder, unique_filename)
                file.save(file_path)
                
                file_size = os.path.getsize(file_path)
                
                media_file = MediaFile(
                    filename=unique_filename,
                    original_filename=original_filename,
                    file_path=file_path,
                    file_type=file_type,
                    file_size=file_size,
                    mime_type=file.content_type,
                    lesson_id=int(lesson_id) if lesson_id else None
                )
                
                db.session.add(media_file)
                db.session.commit()
                
                file_data = media_file.to_dict()
                file_data['url'] = f'/api/media/{media_file.id}'
                uploaded_files.append(file_data)
                
            except Exception as e:
                errors.append(f'Erro ao processar {file.filename}: {str(e)}')
        
        return jsonify({
            'success': True,
            'uploaded_files': uploaded_files,
            'errors': errors,
            'total_uploaded': len(uploaded_files),
            'total_errors': len(errors)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro no upload em lote: {str(e)}'
        }), 500

