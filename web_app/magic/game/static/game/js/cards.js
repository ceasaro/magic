$(document).ready(function () {
    console.log('cards loaded');
    $('img.hover-enlarge').mouseenter(
        function () {
            let $img = $(this),
                $img_clone = $img.clone();
            $img_clone.removeAttr('height');
            $img_clone.removeAttr('width');
            $img_clone.addClass('large-hovering-img');
            $img_clone.attr('id', 'L-' + $img.attr('id'));
            $img_clone.insertAfter($img);
            $img_clone.mouseleave(
                function () {
                    $('.large-hovering-img').remove();
                });
        });
});
