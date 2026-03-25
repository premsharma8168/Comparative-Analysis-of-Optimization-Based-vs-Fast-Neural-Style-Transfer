document.addEventListener('DOMContentLoaded', () => {
    
    // Fetch available models for Fast NST
    fetch('/api/models')
        .then(res => res.json())
        .then(data => {
            const select = document.getElementById('fast-model-select');
            if (data.models && data.models.length > 0) {
                select.innerHTML = '';
                data.models.forEach(model => {
                    const opt = document.createElement('option');
                    opt.value = model;
                    opt.textContent = model.replace('.t7', '').replace(/fast_neural_style_eccv16_/g, '').replace(/_/g, ' ').toUpperCase();
                    select.appendChild(opt);
                });
            }
        }).catch(err => console.error("Could not fetch models:", err));

    const optForm = document.getElementById('opt-form');
    optForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const contentFile = document.getElementById('opt-content').files[0];
        const styleFile = document.getElementById('opt-style').files[0];
        const steps = document.getElementById('opt-steps').value;

        const formData = new FormData();
        formData.append('content', contentFile);
        formData.append('style', styleFile);
        formData.append('steps', steps);

        const btn = document.getElementById('opt-btn');
        btn.disabled = true;
        btn.textContent = 'Processing...';

        await processImage('/api/optimize', formData, 'opt');

        btn.disabled = false;
        btn.textContent = 'Generate';
    });

    const fastForm = document.getElementById('fast-form');
    fastForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const contentFile = document.getElementById('fast-content').files[0];
        const modelName = document.getElementById('fast-model-select').value;

        const formData = new FormData();
        formData.append('content', contentFile);
        formData.append('model_name', modelName);

        const btn = document.getElementById('fast-btn');
        btn.disabled = true;
        btn.textContent = 'Processing...';

        await processImage('/api/fast', formData, 'fast');

        btn.disabled = false;
        btn.textContent = 'Generate';
    });

    async function processImage(url, formData, prefix) {
        const loader = document.getElementById(`${prefix}-loader`);
        const img = document.getElementById(`${prefix}-result-img`);
        const metrics = document.getElementById(`${prefix}-metrics`);
        const timeSpan = document.getElementById(`${prefix}-time`);

        // Reset UI
        img.classList.add('hidden');
        metrics.classList.add('hidden');
        loader.classList.remove('hidden');

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Server responded with an error');
            }
            
            const data = await response.json();
            
            if (data.status === 'success') {
                img.src = data.result_url + '?t=' + new Date().getTime(); // bypass cache
                timeSpan.textContent = data.time_taken;
                
                img.onload = () => {
                    loader.classList.add('hidden');
                    img.classList.remove('hidden');
                    metrics.classList.remove('hidden');
                };
            } else {
                alert(`Error: ${data.detail || 'Unknown error'}`);
                loader.classList.add('hidden');
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
            loader.classList.add('hidden');
        }
    }
});
