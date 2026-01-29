/* eslint-env browser, jquery */
/*
 * @changed 2026.01.29, 02:36
 * vim: ts=2:sw=2
 */

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

  /// Series tracks management

  /** Core admin prefix */
  const urlPrefix = '/unfold-admin/tales_django';

  /** @type {HTMLElement} */
  let seriesTracksTable = undefined;

  /** @type {HTMLElement} */
  let seriesTracksControls;

  /** @type {HTMLButtonElement | undefined} */
  let seriesTracksSaveButton;
  /** @type {HTMLButtonElement | undefined} */
  let seriesTracksDeleteButton;
  /** @type {HTMLButtonElement | undefined} */
  let seriesTracksAddButton;

  /** @type {number | undefined} */
  let indicatorTimeout;

  /* // Save data API:
fetch('/unfold-admin/tales_django/series/1/update-tracks/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({
        tracks: [
            {id: 1, series_order: 1, delete: false},
            {id: 2, series_order: 2, delete: false},
            {id: 3, series_order: null, delete: true}
        ]
    })
})
*/

  function getSeriesTracksFormParams() {
    const form = document.getElementById('series_form');
    if (!form) {
      throw new Error('Cannot find series form node');
    }
    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]');
    if (!csrfToken) {
      throw new Error('Cannot find CSRF token');
    }
    const pathname = document.location.pathname;
    const match = pathname.match(/series\/(\d+)\/change\//);
    const seriesId = match && match[1];
    if (!seriesId || isNaN(seriesId)) {
      throw new Error('Cannot fetch series ID from the pathname: ' + pathname);
    }
    return {
      csrfToken,
      seriesId: Number(seriesId),
    };
  }

  function updateSeriesTracksData(data) {
    const { seriesId, csrfToken } = getSeriesTracksFormParams();
    const url = `${urlPrefix}/series/${seriesId}/update-tracks/`;
    const sendData = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(data),
    };
    /** @type {Response | undefined} */
    let response;
    return fetch(url, sendData)
      .then((res) => {
        response = res;
        return res.json();
      })
      .then((resData) => {
        const { ok, status } = response || {};
        if (!ok || status !== 200) {
          const message =
            resData && resData.error ? resData.error : resData || 'Error status: ' + status;
          throw new Error(message);
        }
        seriesTracksSaveButton.classList.toggle('disabled', true);
        seriesTracksDeleteButton.classList.toggle('disabled', true);
        return resData;
      })
      .catch((error) => {
        const message = error && error.message ? error.message : 'Unknown error';
        // eslint-disable-next-line no-console
        console.error('[unfold-fixes:updateSeriesTracksData] error', message, {
          error,
          message,
          response,
          url,
          sendData,
          data,
          seriesId,
          csrfToken,
        });
        debugger; // eslint-disable-line no-debugger
        throw error;
      });
  }

  /** @param {MouseEvent} ev */
  function saveSeriesTracksData(ev) {
    ev.preventDefault();
    // Gather all the orders data
    const table = seriesTracksTable && seriesTracksTable.querySelector('table.tabular-table');
    const rows = table && table.querySelectorAll('tbody.has_original');
    const tracks = /** @type {{ id: number; series_order: number }} */ (
      Array.from(rows)
        .map((row) => {
          const orderInputField = row.querySelector('input[type="number"]');
          if (!orderInputField) {
            throw new Error('Not found order input field');
          }
          const id = Number(row.dataset.id);
          const order = Number(orderInputField.value);
          return { id, series_order: order };
        })
        .filter(Boolean)
    );
    updateSeriesTracksData({ tracks })
      .then((result) => {
        // eslint-disable-next-line no-console
        console.log('[saveSeriesTracksData] done', {
          result,
          tracks,
          rows,
          seriesTracksTable,
          seriesTracksControls,
        });
      })
      .catch((_error) => {
        /// NOOP
      });
  }

  /** @param {MouseEvent} ev */
  function deleteSeriesTracksData(ev) {
    ev.preventDefault();
    // Find rows with delete checboxes
    const rows = seriesTracksTable.querySelectorAll('tbody.has_original');
    const idsToDelete = /** @type {Number[]} */ (
      Array.from(rows)
        .map((row) => {
          const checkbox = /** @type {HTMLInputElement | undefined} */ (
            row.querySelector('input[type="checkbox"]')
          );
          if (checkbox && checkbox.checked) {
            return Number(row.dataset.id);
          }
        })
        .filter(Boolean)
    );
    if (!idsToDelete.length) {
      return;
    }
    const tracks = idsToDelete.map((id) => ({ id, delete: true }));
    updateSeriesTracksData({ tracks })
      .then((result) => {
        // eslint-disable-next-line no-console
        console.log('[deleteSeriesTracksData] done', {
          result,
          tracks,
          idsToDelete,
          rows,
        });
        Array.from(rows).forEach((row) => {
          if (idsToDelete.includes(Number(row.dataset.id))) {
            row.remove();
          }
        });
        requestAnimationFrame(updateSelectOptions);
        // setTimeout(updateSelectOptions, 100);
      })
      .catch((_error) => {
        /// NOOP
      });
  }

  /** @param {MouseEvent} ev */
  function seriesTracksRowMinus(ev) {
    const { currentTarget } = ev;
    const row = currentTarget.closest('tbody.has_original');
    if (!row) {
      throw new Error('Cannot find row for minus button');
    }
    const parent = row.parentNode;
    if (!parent) {
      throw new Error('Cannot find parent node for minus button');
    }
    const orderInputField = row.querySelector('input[type="number"]');
    if (!orderInputField) {
      throw new Error('Not found order input field');
    }
    const origOrder = Number(orderInputField.value);
    let order = origOrder;
    // Decrease the order value
    if (order > 1) {
      order--;
    }
    const prevRow = row.previousElementSibling;
    if (prevRow) {
      const prevOrderInputField = prevRow.querySelector('input[type="number"]');
      if (prevOrderInputField) {
        const prevOrder = Number(prevOrderInputField.value);
        if (prevOrder >= order) {
          prevOrderInputField.value = origOrder;
          parent.insertBefore(row, prevRow);
        }
      }
    }
    orderInputField.value = order;
    if (seriesTracksSaveButton && seriesTracksSaveButton.classList.contains('disabled')) {
      seriesTracksSaveButton.classList.remove('disabled');
    }
    if (indicatorTimeout) {
      clearTimeout(indicatorTimeout);
      const rows = seriesTracksTable.querySelectorAll('tbody.has_original');
      rows.forEach((row) => row.classList.remove('indicate'));
    }
    row.classList.toggle('indicate', true);
    indicatorTimeout = setTimeout(() => {
      row.classList.toggle('indicate', false);
      indicatorTimeout = undefined;
    }, 2000);
  }

  /** @param {MouseEvent} ev */
  function seriesTracksRowPlus(ev) {
    const { currentTarget } = ev;
    const row = currentTarget.closest('tbody.has_original');
    if (!row) {
      throw new Error('Cannot find row for plus button');
    }
    const parent = row.parentNode;
    if (!parent) {
      throw new Error('Cannot find parent node for plus button');
    }
    // Do nothing if the first item
    const orderInputField = row.querySelector('input[type="number"]');
    if (!orderInputField) {
      throw new Error('Not found order input field');
    }
    const origOrder = Number(orderInputField.value);
    let order = origOrder;
    // Increment the order value
    order++;
    const nextRow = row.nextElementSibling;
    if (nextRow) {
      const nextOrderInputField = nextRow.querySelector('input[type="number"]');
      if (nextOrderInputField) {
        const nextOrder = Number(nextOrderInputField.value);
        if (nextOrder <= order) {
          nextOrderInputField.value = origOrder;
          parent.insertBefore(nextRow, row);
        }
      }
    }
    orderInputField.value = order;
    if (seriesTracksSaveButton && seriesTracksSaveButton.classList.contains('disabled')) {
      seriesTracksSaveButton.classList.remove('disabled');
    }
    if (indicatorTimeout) {
      clearTimeout(indicatorTimeout);
      const rows = seriesTracksTable.querySelectorAll('tbody.has_original');
      rows.forEach((row) => row.classList.remove('indicate'));
    }
    row.classList.toggle('indicate', true);
    indicatorTimeout = setTimeout(() => {
      row.classList.toggle('indicate', false);
      indicatorTimeout = undefined;
    }, 2000);
  }

  /** @param {MouseEvent} ev */
  function onSeriesTracksCheckboxChange() {
    // Find rows with delete checboxes
    const rows = seriesTracksTable.querySelectorAll('tbody.has_original');
    const idsToDelete = /** @type {Number[]} */ (
      Array.from(rows)
        .map((row) => {
          const checkbox = /** @type {HTMLInputElement | undefined} */ (
            row.querySelector('input[type="checkbox"]')
          );
          if (checkbox && checkbox.checked) {
            return Number(row.dataset.id);
          }
        })
        .filter(Boolean)
    );
    const hasItemsToDelete = !!(idsToDelete && idsToDelete.length);
    seriesTracksDeleteButton.classList.toggle('disabled', !hasItemsToDelete);
  }

  /** @param {HTMLElement} row */
  function initSeriesTracksRow(row) {
    if (row.classList.contains('inited')) {
      return;
    }
    const idInputField = row.querySelector('input[type="hidden"]');
    if (!idInputField) {
      throw new Error('Not found id input field');
    }
    const id = Number(idInputField.value);
    const orderInputField = row.querySelector('input[type="number"]');
    if (!orderInputField) {
      throw new Error('Not found order input field');
    }
    const titleNode = row.querySelector('td.original p');
    const wrapper = orderInputField.parentNode;
    const checkbox = /** @type {HTMLInputElement | undefined} */ (
      row.querySelector('input[type="checkbox"]')
    );
    row.dataset.id = id;
    if (checkbox) {
      checkbox.addEventListener('change', onSeriesTracksCheckboxChange);
    }
    // Add an edit track button with an icons
    if (titleNode) {
      const icon = document.createElement('span');
      icon.textContent = 'edit_square';
      icon.className = 'edit-icon material-symbols-outlined';
      const link = document.createElement('a');
      link.href = `${urlPrefix}/track/${id}/change/`;
      link.className = 'edit-link';
      link.appendChild(icon);
      titleNode.appendChild(link);
    }
    // Add buttons and No symbol
    if (wrapper) {
      const btnClassName =
        'h-7 w-7 btn btn-sm border border-base-200 rounded transition-all hover:bg-base-50 dark:border-base-700 dark:hover:text-base-200 dark:hover:bg-base-900';
      const minusBtn = document.createElement('button');
      minusBtn.id = 'minusButton';
      minusBtn.textContent = '↑';
      minusBtn.className = btnClassName;
      minusBtn.type = 'button';
      minusBtn.addEventListener('click', seriesTracksRowMinus);
      wrapper.appendChild(minusBtn);
      const plusBtn = document.createElement('button');
      plusBtn.id = 'plusButton';
      plusBtn.textContent = '↓';
      plusBtn.className = btnClassName;
      plusBtn.type = 'button';
      plusBtn.addEventListener('click', seriesTracksRowPlus);
      wrapper.appendChild(plusBtn);
      const noSign = document.createElement('span');
      noSign.id = 'number';
      noSign.textContent = '№';
      noSign.className = 'opacity-50';
      wrapper.prepend(noSign);
    }
    row.classList.add('inited');
  }

  function updateSelectOptions() {
    const select = seriesTracksControls.querySelector('select');
    const options = select.querySelectorAll('option');
    const rows = seriesTracksTable.querySelectorAll('tbody.has_original');
    const ids = /** @type {Number[]} */ (
      Array.from(rows)
        .map((row) => {
          return Number(row.dataset.id);
        })
        .filter(Boolean)
    );
    // const optionIds = Array.from(options).map((opt) => Number(opt.value));
    let enabledCount = 0;
    options.forEach((opt) => {
      const value = Number(opt.value);
      const toHide = ids.includes(value);
      opt.classList.toggle('hidden', toHide);
      if (!toHide) {
        enabledCount++;
      }
    });
    // If only default option or none, then disbale the select
    select.classList.toggle('disabled', enabledCount <= 1);
  }

  /** @param {Event} ev */
  function onSelectChange(ev) {
    const { currentTarget } = ev;
    const value = currentTarget.value;
    seriesTracksAddButton.classList.toggle('disabled', !value);
  }

  function initSeriesTracks() {
    seriesTracksTable = document.querySelector('fieldset[aria-labelledby="tracks-heading"]');
    if (!seriesTracksTable) {
      // eslint-disable-next-line no-console
      console.warn('[unfold-fixes:initSeriesTracks] Cannot find tracks table node, exiting.');
    }
    seriesTracksControls = document.querySelector(
      'fieldset[aria-labelledby="tracks-heading-controls"]',
    );
    if (!seriesTracksControls) {
      // eslint-disable-next-line no-console
      console.warn('[unfold-fixes:initSeriesTracks] Cannot find tracks controls node, exiting.');
    }
    seriesTracksSaveButton = seriesTracksControls.querySelector('#SaveTracks');
    seriesTracksDeleteButton = seriesTracksControls.querySelector('#DeleteSelectedTracks');
    seriesTracksAddButton = seriesTracksControls.querySelector('#AddTrack');
    const table = seriesTracksTable.querySelector('table.tabular-table');
    const rows = seriesTracksTable.querySelectorAll('tbody.has_original');
    // Remove service header and footer (they're not used and bother to detect first and last rows)
    const theadToRemove = table && table.querySelector('thead');
    const tbodyToRemove = table && table.querySelector('tbody.template');
    if (theadToRemove) {
      theadToRemove.remove();
    }
    if (tbodyToRemove) {
      tbodyToRemove.remove();
    }
    if (rows) {
      Array.from(rows).map(initSeriesTracksRow);
    }
    const select = seriesTracksControls.querySelector('select');
    if (select) {
      select.addEventListener('change', onSelectChange);
    }
    if (seriesTracksSaveButton) {
      seriesTracksSaveButton.addEventListener('click', saveSeriesTracksData);
    }
    if (seriesTracksDeleteButton) {
      seriesTracksDeleteButton.addEventListener('click', deleteSeriesTracksData);
    }
    updateSelectOptions();
  }

  function onLoad() {
    initUnfoldFixes();
    initSeriesTracks();
  }

  window.addEventListener('load', onLoad);
})();
