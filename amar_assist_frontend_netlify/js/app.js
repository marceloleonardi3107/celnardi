// Sistema de Treinamento Amar Assist - Frontend Netlify
class TrainingSystem {
    constructor() {
        this.currentUser = { id: 2, username: 'vendedor_teste' }; // Usuário de teste
        this.currentModule = null;
        this.currentLesson = null;
        this.currentQuiz = null;
        this.currentAttempt = null;
        this.quizTimer = null;
        this.isOnline = navigator.onLine;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAPIConnection();
        this.loadDashboard();
        this.loadModules();
    }

    setupEventListeners() {
        // Upload de arquivos
        const fileInput = document.getElementById('file-input');
        if (fileInput) {
            fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        }

        // Monitorar conexão
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showConnectionStatus('online');
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showConnectionStatus('offline');
        });
    }

    async checkAPIConnection() {
        try {
            await apiRequest('/health');
            this.showConnectionStatus('connected');
        } catch (error) {
            console.error('API connection failed:', error);
            this.showConnectionStatus('disconnected');
        }
    }

    showConnectionStatus(status) {
        const statusElement = document.getElementById('connection-status');
        if (!statusElement) {
            // Criar elemento de status se não existir
            const statusDiv = document.createElement('div');
            statusDiv.id = 'connection-status';
            statusDiv.className = 'connection-status';
            document.body.appendChild(statusDiv);
        }

        const statusEl = document.getElementById('connection-status');
        statusEl.className = `connection-status ${status}`;
        
        const messages = {
            'online': '🟢 Online',
            'offline': '🔴 Offline',
            'connected': '🟢 API Conectada',
            'disconnected': '🟡 API Desconectada - Modo Offline'
        };
        
        statusEl.textContent = messages[status] || status;
        
        // Auto-hide após 3 segundos se conectado
        if (status === 'connected') {
            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 3000);
        }
    }

    // Navegação entre seções
    showSection(sectionId) {
        // Esconder todas as seções
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });

        // Mostrar seção selecionada
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.style.display = 'block';
        }

        // Atualizar navegação ativa
        document.querySelectorAll('.sidebar .nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.querySelector(`[onclick="showSection('${sectionId}')"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        // Carregar conteúdo específico da seção
        switch(sectionId) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'modules':
                this.loadModules();
                break;
            case 'progress':
                this.loadProgress();
                break;
            case 'upload':
                this.loadUploadSection();
                break;
        }
    }

    // Dashboard
    async loadDashboard() {
        try {
            if (!this.isOnline) {
                this.loadOfflineDashboard();
                return;
            }

            const progress = await this.fetchUserProgress();
            this.updateDashboardStats(progress);
        } catch (error) {
            console.error('Erro ao carregar dashboard:', error);
            this.loadOfflineDashboard();
        }
    }

    loadOfflineDashboard() {
        // Carregar dados do localStorage se disponível
        const cachedProgress = localStorage.getItem('userProgress');
        if (cachedProgress) {
            const progress = JSON.parse(cachedProgress);
            this.updateDashboardStats(progress);
        } else {
            // Dados de exemplo para modo offline
            this.updateDashboardStats({
                completedModules: 0,
                overallProgress: 0,
                averageQuizScore: 0,
                totalStudyTime: 0,
                currentModuleProgress: 0
            });
        }
    }

    updateDashboardStats(progress) {
        // Atualizar cards de estatísticas
        const elements = {
            'completed-modules': progress.completedModules || 0,
            'total-progress': (progress.overallProgress || 0) + '%',
            'quiz-score': (progress.averageQuizScore || 0) + '%',
            'study-time': (progress.totalStudyTime || 0) + 'h'
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
        
        // Atualizar barra de progresso do módulo atual
        const currentModuleProgress = document.getElementById('current-module-progress');
        if (currentModuleProgress) {
            const moduleProgress = progress.currentModuleProgress || 0;
            currentModuleProgress.style.width = moduleProgress + '%';
            currentModuleProgress.textContent = moduleProgress + '%';
        }

        // Salvar no localStorage para modo offline
        localStorage.setItem('userProgress', JSON.stringify(progress));
    }

    // Módulos
    async loadModules() {
        try {
            if (!this.isOnline) {
                this.loadOfflineModules();
                return;
            }

            const data = await apiRequest('/modules');
            
            if (data.success) {
                this.renderModules(data.modules);
                // Cache para modo offline
                localStorage.setItem('modules', JSON.stringify(data.modules));
            } else {
                this.showError('Erro ao carregar módulos: ' + data.message);
            }
        } catch (error) {
            console.error('Erro ao carregar módulos:', error);
            this.loadOfflineModules();
        }
    }

    loadOfflineModules() {
        const cachedModules = localStorage.getItem('modules');
        if (cachedModules) {
            const modules = JSON.parse(cachedModules);
            this.renderModules(modules);
        } else {
            // Módulos de exemplo para modo offline
            const exampleModules = [
                {
                    id: 1,
                    title: 'Fundamentos do Mercado Funerário',
                    description: 'Introdução ao mercado brasileiro de assistência funerária',
                    order_index: 1,
                    lessons_count: 5
                },
                {
                    id: 2,
                    title: 'Legislação e Regulamentação',
                    description: 'Lei 13.261/2016 e suas implicações práticas',
                    order_index: 2,
                    lessons_count: 4
                },
                {
                    id: 3,
                    title: 'Portfólio de Produtos e Serviços',
                    description: 'Planos funerários, jazigos e seguros complementares',
                    order_index: 3,
                    lessons_count: 7
                }
            ];
            this.renderModules(exampleModules);
        }
    }

    renderModules(modules) {
        const container = document.getElementById('modules-container');
        if (!container) return;
        
        container.innerHTML = '';

        modules.forEach(module => {
            const moduleCard = this.createModuleCard(module);
            container.appendChild(moduleCard);
        });
    }

    createModuleCard(module) {
        const card = document.createElement('div');
        card.className = 'col-md-4 mb-4';
        
        // Calcular progresso (placeholder - seria calculado com dados reais)
        const progress = Math.floor(Math.random() * 100);
        const progressColor = progress < 30 ? 'bg-danger' : progress < 70 ? 'bg-warning' : 'bg-success';
        
        card.innerHTML = `
            <div class="card module-card h-100" onclick="trainingSystem.loadModule(${module.id})">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="fas fa-book text-primary"></i>
                        ${module.title}
                    </h5>
                    <p class="card-text">${module.description}</p>
                    <div class="mb-3">
                        <small class="text-muted">Progresso:</small>
                        <div class="progress module-progress">
                            <div class="progress-bar ${progressColor}" style="width: ${progress}%">${progress}%</div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-list"></i> ${module.lessons_count || 0} lições
                        </small>
                        <span class="badge bg-primary">Módulo ${module.order_index}</span>
                    </div>
                </div>
            </div>
        `;
        
        return card;
    }

    async loadModule(moduleId) {
        try {
            if (!this.isOnline) {
                this.showError('Funcionalidade disponível apenas online');
                return;
            }

            const data = await apiRequest(`/modules/${moduleId}`);
            
            if (data.success) {
                this.currentModule = data.module;
                this.renderModuleLessons(data.module);
            } else {
                this.showError('Erro ao carregar módulo: ' + data.message);
            }
        } catch (error) {
            console.error('Erro ao carregar módulo:', error);
            this.showError('Erro de conexão ao carregar módulo');
        }
    }

    renderModuleLessons(module) {
        const container = document.getElementById('modules-container');
        if (!container) return;
        
        container.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h3><i class="fas fa-book text-primary"></i> ${module.title}</h3>
                <button class="btn btn-outline-secondary" onclick="trainingSystem.loadModules()">
                    <i class="fas fa-arrow-left"></i> Voltar aos Módulos
                </button>
            </div>
            <p class="lead">${module.description}</p>
            <div class="row" id="lessons-container"></div>
        `;

        const lessonsContainer = document.getElementById('lessons-container');
        
        if (module.lessons && module.lessons.length > 0) {
            module.lessons.forEach(lesson => {
                const lessonCard = this.createLessonCard(lesson);
                lessonsContainer.appendChild(lessonCard);
            });
        } else {
            lessonsContainer.innerHTML = '<div class="col-12"><div class="alert alert-info">Nenhuma lição disponível neste módulo.</div></div>';
        }
    }

    createLessonCard(lesson) {
        const card = document.createElement('div');
        card.className = 'col-md-6 mb-4';
        
        const typeIcon = this.getLessonTypeIcon(lesson.lesson_type);
        const duration = lesson.duration_minutes ? `${lesson.duration_minutes} min` : 'N/A';
        
        card.innerHTML = `
            <div class="card lesson-card h-100" onclick="trainingSystem.loadLesson(${lesson.module_id}, ${lesson.id})">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="${typeIcon}"></i>
                        ${lesson.title}
                    </h5>
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <small class="text-muted">
                            <i class="fas fa-clock"></i> ${duration}
                        </small>
                        ${lesson.has_quiz ? '<span class="badge bg-success"><i class="fas fa-question-circle"></i> Quiz</span>' : ''}
                    </div>
                    <div class="progress mb-2">
                        <div class="progress-bar bg-info" style="width: 0%">0%</div>
                    </div>
                    <small class="text-muted">Clique para iniciar</small>
                </div>
            </div>
        `;
        
        return card;
    }

    getLessonTypeIcon(type) {
        const icons = {
            'text': 'fas fa-file-text text-primary',
            'video': 'fas fa-play-circle text-danger',
            'audio': 'fas fa-volume-up text-warning',
            'pdf': 'fas fa-file-pdf text-danger'
        };
        return icons[type] || 'fas fa-file text-secondary';
    }

    async fetchUserProgress() {
        try {
            const data = await apiRequest(`/users/${this.currentUser.id}/progress`);
            
            if (data.success) {
                return this.calculateProgressStats(data.progress);
            }
        } catch (error) {
            console.error('Erro ao buscar progresso:', error);
        }
        
        return {
            completedModules: 0,
            overallProgress: 0,
            averageQuizScore: 0,
            totalStudyTime: 0,
            currentModuleProgress: 0
        };
    }

    calculateProgressStats(progressData) {
        // Calcular estatísticas baseadas nos dados de progresso
        let completedModules = 0;
        let totalLessons = 0;
        let completedLessons = 0;
        
        progressData.forEach(moduleProgress => {
            totalLessons += moduleProgress.total_lessons;
            completedLessons += moduleProgress.completed_lessons;
            
            if (moduleProgress.overall_progress >= 100) {
                completedModules++;
            }
        });
        
        const overallProgress = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;
        
        return {
            completedModules,
            overallProgress,
            averageQuizScore: Math.floor(Math.random() * 30) + 70, // Placeholder
            totalStudyTime: Math.floor(Math.random() * 20) + 5, // Placeholder
            currentModuleProgress: progressData.length > 0 ? progressData[0].overall_progress : 0
        };
    }

    async loadProgress() {
        const container = document.getElementById('progress-container');
        if (!container) return;
        
        container.innerHTML = `
            <div class="row">
                <div class="col-12">
                    <div class="alert alert-info">
                        <h4><i class="fas fa-chart-line"></i> Relatório de Progresso</h4>
                        <p>Esta seção mostrará gráficos detalhados do seu progresso no treinamento.</p>
                        ${!this.isOnline ? '<p><em>Funcionalidade completa disponível apenas online.</em></p>' : ''}
                    </div>
                </div>
            </div>
        `;
    }

    async loadUploadSection() {
        if (!this.isOnline) {
            const container = document.getElementById('upload-container');
            if (container) {
                container.innerHTML = `
                    <div class="alert alert-warning">
                        <h4><i class="fas fa-wifi"></i> Conexão Necessária</h4>
                        <p>O upload de arquivos requer conexão com a internet.</p>
                    </div>
                `;
            }
            return;
        }

        // Implementação do upload quando online
        try {
            const data = await apiRequest('/modules');
            
            if (data.success) {
                const select = document.getElementById('lesson-select');
                if (select) {
                    select.innerHTML = '<option value="">Selecione uma lição...</option>';
                    
                    data.modules.forEach(module => {
                        if (module.lessons) {
                            module.lessons.forEach(lesson => {
                                const option = document.createElement('option');
                                option.value = lesson.id;
                                option.textContent = `${module.title} - ${lesson.title}`;
                                select.appendChild(option);
                            });
                        }
                    });
                }
            }
        } catch (error) {
            console.error('Erro ao carregar lições:', error);
        }
    }

    // Utilitários
    showError(message) {
        // Criar toast de erro
        const toast = document.createElement('div');
        toast.className = 'toast-error';
        toast.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-triangle"></i> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove após 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    formatFileSize(bytes) {
        if (!bytes) return 'N/A';
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }
}

// Inicializar sistema quando a página carregar
let trainingSystem;
document.addEventListener('DOMContentLoaded', function() {
    trainingSystem = new TrainingSystem();
    
    // Expor globalmente para uso nos event handlers inline
    window.showSection = (sectionId) => trainingSystem.showSection(sectionId);
    window.trainingSystem = trainingSystem;
});

