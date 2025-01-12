/* eslint-disable @typescript-eslint/no-explicit-any */

/* // UNUSED: popperjs
 * import {
 *   applyStyles, // {name: 'applyStyles', enabled: true, phase: 'write', fn: ƒ, effect: ƒ, …}
 *   arrow, // {name: 'arrow', enabled: true, phase: 'main', fn: ƒ, effect: ƒ, …}
 *   computeStyles, // {name: 'computeStyles', enabled: true, phase: 'beforeWrite', data: {…}, fn: ƒ}
 *   createPopper, // ƒ (e,t,r)
 *   createPopperLite, // ƒ (e,t,r)
 *   defaultModifiers, // (9) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
 *   detectOverflow, // ƒ J(e,t)
 *   eventListeners, // {name: 'eventListeners', enabled: true, phase: 'write', fn: ƒ, effect: ƒ, …}
 *   flip, // {name: 'flip', enabled: true, phase: 'main', requiresIfExists: Array(1), fn: ƒ, …}
 *   hide, // {name: 'hide', enabled: true, phase: 'main', requiresIfExists: Array(1), fn: ƒ}
 *   offset, // {name: 'offset', enabled: true, phase: 'main', requires: Array(1), fn: ƒ}
 *   popperGenerator, // ƒ Z(e)
 *   popperOffsets, // {name: 'popperOffsets', enabled: true, phase: 'read', data: {…}, fn: ƒ}
 *   preventOverflow, // {name: 'preventOverflow', enabled: true, phase: 'main', requiresIfExists: Array(1), fn: ƒ}
 * } from '@popperjs/core';
 *
 * interface TPopper {
 *   applyStyles: typeof applyStyles; // {name: 'applyStyles', enabled: true, phase: 'write', fn: ƒ, effect: ƒ, …}
 *   arrow: typeof arrow; // {name: 'arrow', enabled: true, phase: 'main', fn: ƒ, effect: ƒ, …}
 *   computeStyles: typeof computeStyles; // {name: 'computeStyles', enabled: true, phase: 'beforeWrite', data: {…}, fn: ƒ}
 *   createPopper: typeof createPopper; // ƒ (e,t,r)
 *   createPopperLite: typeof createPopperLite; // ƒ (e,t,r)
 *   defaultModifiers: typeof defaultModifiers; // (9) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
 *   detectOverflow: typeof detectOverflow; // ƒ J(e,t)
 *   eventListeners: typeof eventListeners; // {name: 'eventListeners', enabled: true, phase: 'write', fn: ƒ, effect: ƒ, …}
 *   flip: typeof flip; // {name: 'flip', enabled: true, phase: 'main', requiresIfExists: Array(1), fn: ƒ, …}
 *   hide: typeof hide; // {name: 'hide', enabled: true, phase: 'main', requiresIfExists: Array(1), fn: ƒ}
 *   offset: typeof offset; // {name: 'offset', enabled: true, phase: 'main', requires: Array(1), fn: ƒ}
 *   popperGenerator: typeof popperGenerator; // ƒ Z(e)
 *   popperOffsets: typeof popperOffsets; // {name: 'popperOffsets', enabled: true, phase: 'read', data: {…}, fn: ƒ}
 *   preventOverflow: typeof preventOverflow; // {name: 'preventOverflow', enabled: true, phase: 'main', requiresIfExists: Array(1), fn: ƒ}
 * }
 */

/* // UNUSED: Stripe
 * import { StripeConstructor } from '@stripe/stripe-js/dist/stripe-js';
 * // @see node_modules/@stripe/stripe-js/dist/stripe-js/index.d.ts
 */

declare global {
  interface Window {
    test?: unknown; // Just calm linter warning for empty interfaces

    /* // UNUSED: popperjs
     * Popper: TPopper;
     */

    /* // UNUSED: Stripe.js must be loaded directly from https://js.stripe.com/v3, which
     * // places a `Stripe` object on the window
     * Stripe: StripeConstructor;
     */
  }
}
