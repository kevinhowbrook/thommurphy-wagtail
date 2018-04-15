

function carousels() {
  $('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    items: 1,
    autoHeight: true,
  //  animateOut: 'fadeOut',
    autoplay: true,
    //autoplayTimeout:1000,
    autoplayHoverPause: true

  })
}
$('.container.main').imagesLoaded( function() {
  // images have loaded
    carousels();
});

function navSwtich() {
  if ($('.nav-wrapper').hasClass('nav-wrapper-on')) {
    $('a.close-nav').show();
  }
  else {
    $('a.close-nav').hide();
  }
}

navSwtich();

function toggleNav() {
  $('a.toggle-nav').click(function () {
    $('.nav-wrapper').toggleClass('nav-wrapper-on');
    $('a.close-nav').css('display', 'block');
    navSwtich();
  });
  $('a.close-nav').click(function () {
    $('.nav-wrapper').toggleClass('nav-wrapper-on');
    navSwtich();
  });

}

toggleNav();

function masonryGrid(wrapper) {
  $(wrapper).imagesLoaded(function () {
    $(wrapper).masonry({
      // options
      itemSelector: '.masonry-grid-item',

    });
  });
}

masonryGrid('.masonry-grid');

Footer();