document.addEventListener('DOMContentLoaded', function() {
    function updateLastSeen() {
        if (document.querySelector('.navbar') && document.querySelector('.navbar').textContent.includes('Выйти')) {
            fetch('/api/update-last-seen/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });
        }
    }

    setInterval(updateLastSeen, 60000);
    updateLastSeen();

    document.querySelectorAll('.like-btn, .dislike-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const action = this.dataset.action;
            const isLike = action === 'like';

            fetch(`/posts/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ is_like: isLike })
            })
            .then(response => {
                if (response.status === 403) {
                    window.location.href = '/login/';
                    return Promise.reject('Not authenticated');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    const postElement = document.getElementById(`post-${postId}`);
                    if (!postElement) return;

                    const likeButtons = postElement.querySelectorAll('.like-btn');
                    const dislikeButtons = postElement.querySelectorAll('.dislike-btn');
                    const likeCounts = postElement.querySelectorAll('.like-count');
                    const dislikeCounts = postElement.querySelectorAll('.dislike-count');

                    likeCounts.forEach(span => {
                        span.textContent = data.likes_count;
                    });

                    dislikeCounts.forEach(span => {
                        span.textContent = data.dislikes_count;
                    });

                    likeButtons.forEach(btn => {
                        btn.classList.remove('active', 'user-liked', 'user-disliked');
                    });

                    dislikeButtons.forEach(btn => {
                        btn.classList.remove('active', 'user-liked', 'user-disliked');
                    });

                    if (isLike) {
                        likeButtons.forEach(btn => {
                            btn.classList.add('active', 'user-liked');
                        });
                        dislikeButtons.forEach(btn => {
                            btn.classList.remove('active', 'user-disliked');
                        });
                    } else {
                        dislikeButtons.forEach(btn => {
                            btn.classList.add('active', 'user-disliked');
                        });
                        likeButtons.forEach(btn => {
                            btn.classList.remove('active', 'user-liked');
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    const imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const oldPreview = document.querySelector('.image-preview');
                    if (oldPreview) {
                        oldPreview.remove();
                    }

                    const previewContainer = document.createElement('div');
                    previewContainer.className = 'image-preview';

                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.alt = 'Предпросмотр изображения';
                    img.style.maxWidth = '100%';
                    img.style.maxHeight = '300px';
                    img.style.marginTop = '10px';
                    img.style.borderRadius = '4px';
                    img.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';

                    const removeBtn = document.createElement('button');
                    removeBtn.type = 'button';
                    removeBtn.textContent = 'Удалить изображение';
                    removeBtn.className = 'btn btn-secondary btn-sm';
                    removeBtn.style.marginTop = '10px';
                    removeBtn.style.marginLeft = '10px';

                    removeBtn.addEventListener('click', function() {
                        previewContainer.remove();
                        imageInput.value = '';
                    });

                    const buttonContainer = document.createElement('div');
                    buttonContainer.appendChild(removeBtn);

                    previewContainer.appendChild(img);
                    previewContainer.appendChild(buttonContainer);

                    imageInput.parentNode.appendChild(previewContainer);
                };
                reader.readAsDataURL(file);
            }
        });
    }

    function formatLastSeen(dateString) {
        const now = new Date();
        const lastSeen = new Date(dateString);
        const diffMs = now - lastSeen;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) {
            return 'только что';
        } else if (diffMins < 60) {
            return `${diffMins} минут назад`;
        } else if (diffHours < 24) {
            return `${diffHours} часов назад`;
        } else {
            return `${diffDays} дней назад`;
        }
    }

    const lastSeenElement = document.querySelector('.last-seen-time');
    if (lastSeenElement) {
        const lastSeenTime = lastSeenElement.getAttribute('data-last-seen');
        if (lastSeenTime) {
            lastSeenElement.textContent = formatLastSeen(lastSeenTime);
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const mobileMenuToggle = document.createElement('button');
    mobileMenuToggle.className = 'mobile-menu-toggle';
    mobileMenuToggle.innerHTML = '☰';

    const navLinks = document.querySelector('.nav-links');
    if (navLinks && window.innerWidth <= 768) {
        navLinks.style.display = 'none';
        document.querySelector('.navbar .container').appendChild(mobileMenuToggle);

        mobileMenuToggle.addEventListener('click', function() {
            if (navLinks.style.display === 'none') {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.right = '0';
                navLinks.style.backgroundColor = '#3498db';
                navLinks.style.padding = '1rem';
                navLinks.style.zIndex = '1000';
            } else {
                navLinks.style.display = 'none';
            }
        });
    }
});
