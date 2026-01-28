debugger;
document.addEventListener('DOMContentLoaded', function () {
  // Add increment/decrement buttons to series order fields
  const orderInputs = document.querySelectorAll('.series-order-input');

  orderInputs.forEach((input) => {
    // Create container for input and buttons
    const container = document.createElement('div');
    container.className = 'series-order-container d-flex align-items-center gap-1';

    // Create buttons
    const decrementBtn = document.createElement('button');
    decrementBtn.textContent = '-';
    decrementBtn.className = 'btn btn-sm btn-outline-secondary';
    decrementBtn.type = 'button';

    const incrementBtn = document.createElement('button');
    incrementBtn.textContent = '+';
    incrementBtn.className = 'btn btn-sm btn-outline-secondary';
    incrementBtn.type = 'button';

    // Move input to container
    input.parentNode.insertBefore(container, input);
    container.appendChild(decrementBtn);
    container.appendChild(input);
    container.appendChild(incrementBtn);

    // Add click handlers
    decrementBtn.addEventListener('click', function () {
      if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
      }
    });

    incrementBtn.addEventListener('click', function () {
      input.value = parseInt(input.value) + 1;
    });

    // Add some styling to input
    input.style.width = '60px';
    input.style.textAlign = 'center';
  });
});
