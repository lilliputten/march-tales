export function initAOS() {
  // @see static/libs/aos/
  // @see https://michalsnik.github.io/aos/
  if (window.AOS /* && !window.DEBUG */) {
    window.AOS.init({
      // @see https://github.com/michalsnik/aos?tab=readme-ov-file#1-initialize-aos
      once: true,
    });
  }
}
