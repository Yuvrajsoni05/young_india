                     {% if messages %}

    {% for message in messages %}
        Swal.fire({
            title: '{% if message.tags == 'success' %}Success! {% else %} Error! {% endif %} ',
            text: "{{ message }}",
            icon: "{% if message.tags == 'success' %}success{% else %}error{% endif %}",
            confirmButtonText: 'OK'
        });
    {% endfor %}

{% endif %}