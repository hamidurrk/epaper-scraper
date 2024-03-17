


        /*----------------Load More Feature content Start----------------*/
        $(document).ready(function() {
            if($(window).width() >= 992){
                $("#all_rows").on("scroll", function (e) {
                    e.preventDefault();

                    if($('.ft-list:last').position().top < $(this).height()){
                        loadmore();
                    }
                });
            }
            if($(window).width() < 992) {

                $('.mob-btn').removeClass('d-none');
                $(".mob-btn").on("click", function (e) {

                    e.preventDefault();

                    loadmore();
                    $('#all_rows').animate({
                        scrollLeft: $('#all_rows')[0].scrollWidth}, "slow");
                });
            }

            function loadmore()
            {
                var val = document.getElementById("row_no").value;

                $.ajax({
                    type: 'GET',
                    url: 'https://epaper.jugantor.com/feature-more',
                    data: {
                        getresult:val
                    },
                    beforeSend:function() {
                        if($(window).width() >= 992){
                            $('.spinner-grow').removeClass('d-none');
                        }
                        if($(window).width() < 992) {
                            $('.mob-btn i').addClass('d-none');
                            $('.spinner-grow-sm').removeClass('d-none');
                        }

                    },
                    success: function (response) {
                        var content = document.getElementById("all_rows");
                        content.innerHTML = content.innerHTML+response;

                        // We increase the value by 10 because we limit the results by 10
                        document.getElementById("row_no").value = Number(val)+3;

                        if(response == ''){

                            if($(window).width() >= 992) {

                                $('.spinner-grow').remove();
                                $('.not-found').removeClass('d-none');
                                $('.not-found').html("<p>খুঁজে পাওয়া যায়নি</p>");
                                let txtHide = setTimeout(txtHidden, 3000);
                                function txtHidden() {
                                    $('.not-found').remove();
                                    clearTimeout(txtHide);
                                }
                            }
                            if($(window).width() < 992) {

                                $('.mob-btn i').removeClass('d-none');
                                var btnHide = setTimeout(btnHidden, 3000);
                                $('.mob-btn').html("<p class='text-white mb-0'>খুঁজে পাওয়া যায়নি</p>");
                                function btnHidden() {
                                    $('.mob-btn').remove();
                                    clearTimeout(btnHide);
                                }
                            }

                        }
                    },
                    complete: function() {

                        if($(window).width() >= 992){
                            $('.spinner-grow').addClass('d-none');
                        }
                        if($(window).width() < 992){
                            $('.spinner-grow-sm').addClass('d-none');
                            $('.mob-btn i').removeClass('d-none');
                        }

                    },
                    error: function(xhr, textStatus, errorThrown) {
                        console.log('Error in Operation');
                    }

                });
            }
        });
        /*----------------Load More Feature content Script Start----------------*/

        //Map Scripts
        $(document).ready(function() {
            $('.map').maphilight();
            fillColor: '008800'
        });
        /*--------------------------*/

        /*----------------Edition Modal Initiator Script Start----------------*/
        $(document).ready(function() {
            $(document).on('click', '.view_modal', function(e) {
                e.preventDefault();

                var edition_id = $('#edition_id').attr("value");
                var ed_map_id = $(this).attr("data-mapid");
                var coords = $(this).attr("coords");
                $.ajax({
                    type: "GET",
                    dataType: "html",
                    url: "https://epaper.jugantor.com/link",
                    data: {
                        coords: coords,
                        edition_id: edition_id,
                        ed_map_id: ed_map_id
                    },
                    success: function(data) {
                        //console.log(data.success);
                        $('#post_modal').modal('show');
                        $('.modal-content').html(data);
                        let load_epaper = document.getElementById("load_epaper");
                        let load_epaper_width = Math.ceil(load_epaper.getBoundingClientRect().width);
                        if (window.innerWidth < 991) {
                            let modal = document.getElementById('post_modal');
                            modal.style.paddingLeft = 0;
                            modal.querySelector('.modal-dialog').style.margin = 0;
                            document.getElementById('link_img').style.width = (load_epaper_width - 16) + 'px';
                        }
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        console.log('Error in Operation');
                    }
                });
            });
        });
        /*------------------------Modal Initiator Script End---------------------*/

        /*----------------Edition Bongabdo Initiator Script Start----------------*/
        $(document).ready(function() {
            var bongabdo = $("[name='arch_date']").val();

            $('#bongabdo').bongabdo({
                date: bongabdo,
                format: "DD MM YY"
            });
        });
        /*----------------Edition Bongabdo Initiator Script End----------------*/

        /*----------------Responsive behaviour script start----------------*/
        $(document).ready(function() {
            var width = $(window).width();
            var outer = document.getElementById("load_epaper");
            var maxWidth = outer.clientWidth;
            var maxHeight = outer.clientHeight;
            window.addEventListener("resize", resize);

            function resize() {
                let scale,
                    width = window.innerWidth,
                    height = window.innerHeight,
                    isMax = (width >= maxWidth && height >= maxHeight);

                scale = width / maxWidth;

                outer.style.transform = width >= 992 ? "" : "scale(" + scale + ")";
                outer.style.transformOrigin = "0 0";

                let load_epaper = document.getElementById("load_epaper");
                let main_paper_div = document.getElementsByClassName('row-div-main')[0];

                let load_epaper_height = Math.ceil(load_epaper.getBoundingClientRect().height);
                let load_epaper_width = Math.ceil(load_epaper.getBoundingClientRect().width);
                if (width >= 992) {
                    load_epaper.parentNode.style.width = 'auto';
                    load_epaper.parentNode.style.height = 'auto';
                    main_paper_div.parentNode.style.width = 'auto';
                    main_paper_div.parentNode.style.height = 'auto';
                    main_paper_div.style.width = 'auto';
                    main_paper_div.style.height = 'auto';
                    document.getElementsByClassName('side-logo')[0].style.display = 'none';
                    document.getElementsByClassName('menu-scrollable')[0].classList.remove('collapse');
                } else {
                    load_epaper.parentNode.style.width = load_epaper_width + 'px';
                    load_epaper.parentNode.style.height = load_epaper_height + 'px';
                    main_paper_div.parentNode.style.width = load_epaper_width + 'px';
                    main_paper_div.parentNode.style.height = 'auto';
                    main_paper_div.parentNode.style.paddingBottom = '260px';
                    main_paper_div.style.width = load_epaper_width + 'px';
                    main_paper_div.style.height = load_epaper_height + 'px';
                    document.getElementsByClassName('menu-scrollable')[0].classList.add('collapse');
                }

            }
            const myInterval = setInterval(() => {
                if (document.readyState === 'ready' || document.readyState === 'complete') {
                    resize();
                    clearInterval(myInterval)

                } else {
                    document.onreadystatechange = function() {
                        if (document.readyState == "complete") {
                            resize();
                            clearInterval(myInterval);
                        }
                    }
                }
            }, 100);
            resize();
        });

        const open = document.getElementById("home-menu-icon-mob");
        const slide = document.getElementById("home-menu-div");
        const close = document.getElementById("close");

        open.onclick = function() {
            slide.classList.toggle("active");
            const backdrop = document.createElement('div');
            backdrop.className = "modal-backdrop fade show";
            backdrop.style.zIndex = 10;
            document.body.appendChild(backdrop);
            document.body.style.overflow = 'hidden';
            document.body.style.position = 'fixed';
        }