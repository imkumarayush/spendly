// main.js — students will add JavaScript here as features are built

(function () {
    var VIDEO_SRC = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    var openBtn = document.getElementById('see-how-it-works');
    var modal = document.getElementById('video-modal');
    var iframe = document.getElementById('modal-video');

    function openModal() {
        iframe.src = VIDEO_SRC;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        iframe.src = '';
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    if (openBtn) {
        openBtn.addEventListener('click', openModal);
    }

    if (modal) {
        Array.prototype.forEach.call(modal.querySelectorAll('[data-modal-close]'), function (el) {
            el.addEventListener('click', closeModal);
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modal.classList.contains('is-open')) {
                closeModal();
            }
        });
    }
})();