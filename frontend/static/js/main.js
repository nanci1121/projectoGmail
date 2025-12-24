document.addEventListener('DOMContentLoaded', () => {
    const labelList = document.getElementById('label-list');
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const selectedLabelText = document.getElementById('selected-label-text');
    const progressContainer = document.getElementById('progress-container');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const percentText = document.getElementById('percent-text');
    const fileList = document.getElementById('file-list');
    const noActivity = document.getElementById('no-activity');

    let selectedLabelId = "0";

    // Cargar etiquetas al inicio
    async function loadLabels() {
        try {
            const response = await fetch('/api/labels');
            const labels = await response.json();

            if (labels.error) throw new Error(labels.error);

            labels.forEach(label => {
                const li = document.createElement('li');
                li.dataset.id = label.id;
                li.innerHTML = `<i class="fas fa-folder"></i> ${label.name}`;
                li.onclick = () => selectLabel(label.id, label.name, li);
                labelList.appendChild(li);
            });
        } catch (error) {
            console.error('Error cargando etiquetas:', error);
        }
    }

    function selectLabel(id, name, element) {
        selectedLabelId = id;
        selectedLabelText.textContent = name;

        // Update active class
        document.querySelectorAll('#label-list li').forEach(li => li.classList.remove('active'));
        element.classList.add('active');
    }

    // Manejar la descarga con SSE
    startBtn.onclick = () => {
        // Reset UI
        fileList.innerHTML = '';
        noActivity.style.display = 'none';
        progressContainer.style.display = 'block';
        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-block';

        const eventSource = new EventSource(`/api/download-progress?label_id=${selectedLabelId}`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.type === 'start') {
                progressText.textContent = `Encontrados ${data.total} correos...`;
                if (data.total === 0) {
                    eventSource.close();
                    finishDownload("No se encontraron adjuntos.");
                }
            } else if (data.type === 'progress') {
                const percent = Math.round((data.current / data.total) * 100);
                progressFill.style.width = `${percent}%`;
                percentText.textContent = `${percent}%`;
                progressText.textContent = `Procesando correo ${data.current} de ${data.total}...`;

                data.files.forEach(filename => {
                    addFileToUI(filename);
                });
            } else if (data.type === 'complete') {
                eventSource.close();
                finishDownload("¡Descarga completada!");
            } else if (data.type === 'stopped') {
                eventSource.close();
                finishDownload("Descarga detenida por el usuario.");
            }
        };

        eventSource.onerror = () => {
            eventSource.close();
            finishDownload("Ocurrió un error inesperado.");
        };
    };

    stopBtn.onclick = async () => {
        stopBtn.disabled = true;
        progressText.textContent = "Deteniendo descarga...";
        await fetch('/api/stop');
    };

    logoutBtn.onclick = async () => {
        if (confirm('¿Quieres cambiar de cuenta? Se cerrará la sesión actual.')) {
            await fetch('/api/logout');
            window.location.reload(); // Esto disparará el flujo de OAuth en el backend
        }
    };

    function addFileToUI(filename) {
        const li = document.createElement('div');
        li.className = 'file-item';
        li.innerHTML = `
            <div class="file-icon"><i class="fas fa-file"></i></div>
            <div class="file-info">
                <div class="file-name">${filename}</div>
                <div class="file-status">Guardado correctamente</div>
            </div>
            <div style="color: #10b981;"><i class="fas fa-check-circle"></i></div>
        `;
        fileList.prepend(li);
        if (noActivity) noActivity.style.display = 'none';
    }

    function finishDownload(msg) {
        progressText.textContent = msg;
        startBtn.style.display = 'inline-block';
        startBtn.disabled = false;
        stopBtn.style.display = 'none';
        stopBtn.disabled = false;
        setTimeout(() => {
            if (msg.includes("completada")) {
                progressFill.style.width = '100%';
            }
        }, 500);
    }

    loadLabels();
});
