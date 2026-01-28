/* eslint-env browser, jquery */
// vim: ts=2:sw=2

(function () {
  function initUnfoldFixes() {
    // Delayed processing of collapsed nodes...
    setTimeout(function () {
      var toOpen = document.querySelectorAll('.collapse.opened-by-default');
      // To open...
      toOpen.forEach(function (node) {
        node.classList.remove('collapsed');
      });
    }, 100);

    // Flatpage fields...
    var labels = document.querySelectorAll('form#flatpage_form label');
    var fields = document.querySelectorAll('form#flatpage_form #id_url');
    // Fields...
    fields.forEach(function (field) {
      var fieldClasses = [
        'border',
        'border-base-200',
        'bg-white',
        'font-medium',
        'min-w-20',
        'placeholder-base-400',
        'rounded',
        'shadow-sm',
        'text-font-default-light',
        'text-sm',
        'focus:ring',
        'focus:ring-primary-300',
        'focus:border-primary-600',
        'focus:outline-none',
        'group-[.errors]:border-red-600',
        'group-[.errors]:focus:ring-red-200',
        'dark:bg-base-900',
        'dark:border-base-700',
        'dark:text-font-default-dark',
        'dark:focus:border-primary-600',
        'dark:focus:ring-primary-700',
        'dark:focus:ring-opacity-50',
        'dark:group-[.errors]:border-red-500',
        'dark:group-[.errors]:focus:ring-red-600/40',
        'px-3',
        'py-2',
        'w-full',
        'max-w-2xl',
      ];
      fieldClasses.forEach(function (className) {
        field.classList.add(className);
      });
    });
    // Labels...
    labels.forEach(function (label) {
      var labelClasses = [
        'block',
        'font-semibold',
        'mb-2',
        'text-font-important-light',
        'text-sm',
        'dark:text-font-important-dark',
      ];
      labelClasses.forEach(function (className) {
        label.classList.add(className);
      });
      var innerText = String(label.innerText);
      if (innerText.endsWith(':')) {
        label.innerText = innerText.substring(0, innerText.length - 1) + ' ';
      }
      if (
        label.classList.contains('required') &&
        !label.getElementsByClassName('text-red-600').length
      ) {
        var star = document.createElement('span');
        star.classList.add('text-red-600');
        star.innerText = '*';
        label.append(star);
      }
    });
  }

  function initSeriesTracks() {
    const tracksTable = document.querySelector('fieldset[aria-labelledby="tracks-heading"]');
    const tracksControls = document.querySelector(
      'fieldset[aria-labelledby="tracks-heading-controls"]',
    );
    const table = tracksTable && tracksTable.querySelector('table.tabular-table');
    const rows = table && table.querySelectorAll('tbody.has_original');
    // TODO: Remove header (thead) and template (tbody.template)
    // TODO: Find and initialize buttons: AddTracks, DeleteSelectedTracks
    // AddTracks
    // DeleteSelectedTracks
    console.log('[initSeriesTracks]', {
      rows,
      table,
      tracksTable,
      tracksControls,
    });
    // debugger;
  }

  function onLoad() {
    initUnfoldFixes();
    initSeriesTracks();
  }

  window.addEventListener('load', onLoad);
})();
