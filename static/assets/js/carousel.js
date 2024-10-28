$(document).ready(function () {
    // Initialize the Owl Carousel
    var owl = $(".owl-carousel").owlCarousel({
        merge: true,
        loop: true,
        margin: 10,
        video: true,
        lazyLoad: true,
        responsive: {
            0: { items: 1 }, // 1 item for small screens
            600: { items: 2 }, // 2 items for medium screens
            1000: { items: 2 } // 2 items for larger screens
        }
    });

    // Custom Navigation
    $(".owl-prev").click(function () {
        owl.trigger("prev.owl.carousel");
    });
    $(".owl-next").click(function () {
        owl.trigger("next.owl.carousel");
    });
});
