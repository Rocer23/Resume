document.addEventListener('DOMContentLoaded', function() {
    var commentModal = new bootstrap.Modal(document.getElementById('Modal'));
    var btn = document.getElementById('openModal');
    var closeBtn = document.getElementById('closeModal');

    btn.addEventListener('click', function() {
        commentModal.show();
    })
    closeBtn.addEventListener('click', function() {
        commentModal.hide();
    })
})