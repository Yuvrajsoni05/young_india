const container = document.getElementById('tagContainer');
    const input = document.getElementById('tagInput');
    const hiddenInput = document.getElementById('hiddenInput');

    container.addEventListener('click', () => input.focus());

    input.addEventListener('keydown', function(event) {
      if (event.key === 'Enter' || event.key === ',') {
        event.preventDefault();
        let value = input.value.trim().replace(/,$/, "");
        if (value !== '') {
          if (document.querySelectorAll('.tag').length < 10) {  // Limit to 5 tags
            addTag(value);
            input.value = '';
          } else {
            alert('You can only add up to 10     handler names.');
          }
        }
      }
    });

function addTag(text) {
      const tag = document.createElement('span');
      tag.classList.add('tag');
      tag.innerHTML = `${text} <span class="remove" onclick="removeTag(this)">×</span>`;
      container.insertBefore(tag, input);
      updateHiddenInput();
    }

    function removeTag(element) {
      element.parentElement.remove();
      updateHiddenInput();
    }

    function updateHiddenInput() {
      const tags = document.querySelectorAll('.tag');
      hiddenInput.value = Array.from(tags).map(tag => tag.textContent.replace(' ×', '')).join(',');
    }