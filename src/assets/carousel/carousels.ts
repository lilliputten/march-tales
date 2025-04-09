type CarouselSettings = JQuerySlickOptions; // Record<string, unknown>;

interface ResponsiveItem {
  breakpoint: number;
  settings: CarouselSettings;
}

const defaultCarouselSettings: CarouselSettings = {
  // @see https://kenwheeler.github.io/slick/

  dots: true,
  arrows: false,

  lazyLoad: 'ondemand',

  infinite: true,
  speed: 1000,
  slidesToShow: 4,
  slidesToScroll: 1,

  swipeToSlide: true,

  autoplay: true,
  autoplaySpeed: 2000,
  pauseOnHover: true,

  // focusOnSelect: true,
  // variableWidth: true, // NOTE: It'll break `swipeToSlide` settings and require `no-caption` class to avoid broken cell' widts
  // centerMode: true,
  // centerPadding: '60px',
};

const extraCarouselSettings: Record<string, CarouselSettings> = {
  /* phoneScreenshotsWide: {
   *   slidesToShow: 6,
   *   responsive: [
   *     {
   *       breakpoint: 600,
   *       settings: {
   *         slidesToShow: 3,
   *       },
   *     },
   *   ],
   * },
   */
};

interface ResponsiveSeed {
  width: number;
  count: number;
  step: number;
}

const responsiveSeeds: Record<string, ResponsiveSeed> = {
  phoneScreenshots: { width: 1200, count: 5, step: 200 },
  phoneScreenshotsWide: { width: 1600, count: 8, step: 200 },
  browserScreenshotsWide: { width: 1600, count: 3, step: 400 },
};

function seedResponsive(seed?: ResponsiveSeed) {
  if (!seed) {
    return undefined;
  }
  const { step } = seed;
  let { width, count } = seed;
  const responsives: ResponsiveItem[] = [];
  const result: CarouselSettings = {
    slidesToShow: count,
    responsive: responsives,
  };
  while (count > 0 && width > 0) {
    responsives.push({
      breakpoint: width,
      settings: {
        slidesToShow: count,
      },
    });
    width -= step;
    count--;
  }
  return result;
}

function initCarousel(carousel: HTMLElement) {
  const type = carousel.getAttribute('data-carousel-type');
  const extraSettings = type ? extraCarouselSettings[type] : undefined;
  const seedSettings = type ? seedResponsive(responsiveSeeds[type]) : undefined;
  const settings = {
    ...defaultCarouselSettings,
    ...extraSettings,
    ...seedSettings,
  };
  $(carousel).slick(settings);
}

export function initCarousels() {
  const carousels = $('.slick-carousel');
  if ('IntersectionObserver' in window) {
    // IntersectionObserver Supported
    const onChange = (entries: IntersectionObserverEntry[], observer: IntersectionObserver) => {
      entries.forEach((element) => {
        if (element.isIntersecting) {
          // Stop watching and load the slickSlider
          initCarousel(element.target as HTMLElement);
          observer.unobserve(element.target);
        }
      });
    };
    const observer = new IntersectionObserver(onChange, {
      // @see https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API#creating_an_intersection_observer
      root: null,
      rootMargin: '50%',
      threshold: 0.0,
    });
    carousels.map((_idx: number, carousel: HTMLElement) => {
      observer.observe(carousel);
    });
  } else {
    // IntersectionObserver NOT Supported
    carousels.map((_idx: number, carousel: HTMLElement) => initCarousel(carousel));
  }
}
