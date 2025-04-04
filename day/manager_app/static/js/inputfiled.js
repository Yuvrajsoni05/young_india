const container = document.getElementById('tagContainer');
const input = document.getElementById('tagInput');
const hiddenInput = document.getElementById('hiddenInput');

// Focus the input when clicking inside the container
container.addEventListener('click', () => input.focus());

// Keydown event to add tag on "Enter" or ","
input.addEventListener('keydown', function(event) {
  if (event.key === 'Enter' || event.key === '<br>') {
    event.preventDefault();
    addTagFromInput();
  }
});

// Function to add tag from input
function addTagFromInput() {
  let value = input.value.trim().replace(/,$/, "");
  if (value !== '') {
    if (document.querySelectorAll('.tag').length < 22) {  // Limit to 10 tags
      addTag(value);
      input.value = '';  // Reset input field after adding tag
    } else {
      alert('You can only add up to 22 memeber names.');
    }
  }
}

// Function to add a tag to the container
function addTag(text) {
  const tag = document.createElement('span');
  tag.classList.add('tag');
  tag.innerHTML = `${text} <span class="remove" onclick="removeTag(this)">×</span>`;
  container.insertBefore(tag, input);
  updateHiddenInput();
}

// Function to remove a tag
function removeTag(element) {
  element.parentElement.remove();
  updateHiddenInput();
}

// Function to update the hidden input with current tags
function updateHiddenInput() {
  const tags = document.querySelectorAll('.tag');
  hiddenInput.value = Array.from(tags).map(tag => tag.textContent.replace(' ×', '')).join(',');
}

// Add event listener for clicks outside the input or container
document.addEventListener('click', function(event) {
  // If the click is outside the tag container and input field, process the input
  if (!container.contains(event.target) && event.target !== input) {
    if (input.value.trim() !== '') {
      addTagFromInput();  // Add tag when user clicks outside
    }
  }
});

// Prevent input field click from triggering the document click listener
input.addEventListener('click', function(event) {
  event.stopPropagation();
});
