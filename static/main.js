document.addEventListener('DOMContentLoaded', () => {
    const statusButtons = document.querySelectorAll('.status-btn');

    statusButtons.forEach(button => {
        button.addEventListener('click', () => {
            const movieId = button.dataset.movieId;
            const status = button.dataset.status;

            const formData = new FormData();
            formData.append('status', status);

            fetch(`/movie/${movieId}/status`, {
                method: 'POST',
                body: formData,
                headers: {
                    // Flask's request.form requires a content-type that it can handle,
                    // but fetch with FormData sets the multipart/form-data boundary automatically.
                    // So we don't set Content-Type here.
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCardUI(movieId, status);
                    showToast(`Movie status updated to: ${status.replace('-', ' ')}`, 'success');
                } else {
                    console.error('Failed to update status:', data.error);
                    showToast(`Failed to update status: ${data.error}`, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast(`An error occurred: ${error.message}`, 'danger');
            });
        });
    });

    function updateCardUI(movieId, newStatus) {
        const card = document.querySelector(`.status-btn[data-movie-id="${movieId}"]`).closest('.movie-card');
        const badgeContainer = card.querySelector(`.status-badge[data-movie-id="${movieId}"]`);
        
        // Update badge
        let badgeHtml = '';
        if (newStatus === 'watched') {
            badgeHtml = '<span class="badge bg-success">Watched</span>';
        } else if (newStatus === 'want-to-watch') {
            badgeHtml = '<span class="badge bg-info">Want to Watch</span>';
        }
        badgeContainer.innerHTML = badgeHtml;

        // Update buttons
        const buttons = card.querySelectorAll('.status-btn');
        buttons.forEach(btn => {
            if (btn.dataset.status === newStatus) {
                btn.disabled = true;
            } else {
                btn.disabled = false;
            }
        });
    }

    function showToast(message, type = 'success') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            // Create toast container if it doesn't exist
            const newToastContainer = document.createElement('div');
            newToastContainer.id = 'toast-container';
            newToastContainer.style.position = 'fixed';
            newToastContainer.style.top = '20px';
            newToastContainer.style.right = '20px';
            newToastContainer.style.zIndex = '1050';
            document.body.appendChild(newToastContainer);
        }

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0 fade show`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        document.getElementById('toast-container').appendChild(toast);

        setTimeout(() => {
            bootstrap.Toast.getInstance(toast)?.hide();
            toast.remove();
        }, 3000); // Hide after 3 seconds
    }
});
