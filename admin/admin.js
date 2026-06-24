/* Admin shell: slide-out drawer + logout */
(function () {
  var drawer = document.getElementById('drawer'),
      scrim  = document.getElementById('scrim'),
      menu   = document.getElementById('menuBtn'),
      out    = document.getElementById('logoutBtn');
  function open()  { if (drawer) drawer.classList.add('open'); if (scrim) scrim.classList.add('open'); }
  function close() { if (drawer) drawer.classList.remove('open'); if (scrim) scrim.classList.remove('open'); }
  if (menu)  menu.addEventListener('click', open);
  if (scrim) scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  if (out) out.addEventListener('click', function () {
    try { sessionStorage.removeItem('bhs_admin'); } catch (e) {}
    location.reload();
  });
})();
