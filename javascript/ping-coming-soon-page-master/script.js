const form = document.getElementById('form');
const email = document.getElementById('email');
const button = document.getElementById('button');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  validate();
});

function validate() {
  const emailValue = email.value.trim();

  if (emailValue === '') {
    setErrorFor(email, 'Email cannot be empty');
  } else if (!isEmail(emailValue)) {
    setErrorFor(email, 'Please provide a valid email address');
  } else {
    setSuccesFor(email);
  }
}

//TODO
function setErrorFor(value, message) {}

//TODO
function setSuccesFor(value) {}

//TODO
function isEmail(email) {}
