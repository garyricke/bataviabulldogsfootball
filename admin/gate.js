/* Lightweight client-side admin gate. Note: this is a soft gate for a static
   internal hub, not real security — the page can be viewed by reading source. */
(function () {
  var KEY = 'bhs_admin', PASS = 'love';
  function unlock() {
    try { sessionStorage.setItem(KEY, 'ok'); } catch (e) {}
    document.documentElement.classList.remove('locked');
  }
  if (sessionStorage.getItem(KEY) === 'ok') {
    document.documentElement.classList.remove('locked');
    return;
  }
  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('gateForm');
    if (!form) return;
    var inp = document.getElementById('gatePass'),
        err = document.getElementById('gateErr'),
        card = document.querySelector('.gate__card');
    if (inp) inp.focus();
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if ((inp.value || '').trim().toLowerCase() === PASS) {
        unlock();
      } else {
        err.textContent = 'Incorrect password';
        card.classList.add('gate--shake');
        setTimeout(function () { card.classList.remove('gate--shake'); }, 420);
        inp.value = ''; inp.focus();
      }
    });
  });
})();
