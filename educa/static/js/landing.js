$(document).ready(function(){

    let initalizeSlick = (querySelector,slides) =>{
        $(querySelector).slick({
            slidesToShow: slides,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 2000,
        });
    }

    if($(window).width() <= 430){
        initalizeSlick('.courses-card-items',1);
        $('.slick-arrow').css('display','none');
    }
    else if($(window).width() <= 768){
        initalizeSlick('.courses-card-items',2);
    }else{
        initalizeSlick('.courses-card-items',3);
    }
    
    

    $(window).resize(()=>{
        location.reload()
    });
});