document.addEventListener('DOMContentLoaded', function() {
    const sendBtn = document.getElementById('send-comment');
    sendBtn.addEventListener('click', function(){
        const text = document.getElementById('comment-text').value;
        const newId = document.getElementById('new-id').value;

        fetch("{% url 'add-comment' %}", {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': '{{ csrf_token }}'
            }, 
            body: new URLSearchParams({
                'text': text,
                'news_id': newId
            })
        })
        .then(responce => responce.json())
        .then(data => {
            if (data.status === 'ok') {
                const commentsBlock = document.getElementById('comments');
                const newComment = `
                    <p><strong>${data.username}</strong> (${data.create_at}):</p>
                    <p>${data.text}</p>
                    <hr>`;

                commentsBlock.innerHTML = newComment + commentsBlock.innerHTML;

                // hide modal
                document.getElementById('comment-text').value = '';
                const modal = boostrap.Modal.getInstance(document.getElementById('Modal'));
                modal.hide();
            } else {
                alert(data.massage);
            }
        })
    })
})