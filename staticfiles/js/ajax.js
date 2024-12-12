function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function save(e) {
    e.preventDefault();
    const form = e.target;

    fetch(form.action, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(data => {
        try {
            return data.json();
        } catch(Exception) {
            return {
                status: 'success',
                message: 'Failed to fetch information from the server.'
            }
        }
    })
    .then(data => {
        formBody = form.querySelector('.form-body');
        formBody.innerHTML = data.form;

        if(data.status == 'success') alert(
            data.message
        );
    })
    .catch(alert);
}
