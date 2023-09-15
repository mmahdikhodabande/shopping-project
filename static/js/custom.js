function showlargeImage(image_src) {
    // console.log(image_src);
    $('#main_image').attr('src', image_src);
}


function add_to_order(product_id) {
    const product_count = $('#product_count').val();
    $.get('/order/add_to_order?product_id=' + product_id + '&count=' + product_count).then(res => {
        if (res.status === 'success') {
            Swal.fire({
                position: 'top-end', icon: 'success', title: res.text, timer: 2000
            })
        }
        if (res.status === 'not_found') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'اوکی',
            })
        }
        if (res.status === 'not_authent') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'اوکی',
                footer: '<a href="/login">ورود به سایت </a>'
            })
        }
    });
}

function success() {
    $.get('').then(res => {
        if (res.status === 'success') {
            Swal.fire({
                position: 'top-end', icon: 'success', title: res.text, timer: 2000
            })
        }
        if (res.status === 'already') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'اوکی',
            })
        }
        if (res.status === 'not_found') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'اوکی',
            })
        }
    });
}


function delete_order_detail(detail_id) {
    $.get('/order/delete_order?detail_id=' + detail_id).then(res => {
        if (res.status === 'success') {
            $('#order_detail_content').html(res.body);
        }
    })
}

function add_and_delete_order(detail_id, num_order) {
    $.get('/order/change_order_detail?detail_id=' + detail_id + '&num_order=' + num_order).then(res => {
        if (res.status === 'success') {
            $('#order_detail_content').html(res.body);
        }
    })
}

function submit_comment_Article(article_id) {
    var comment = $('#comment').val();
    var parentid = $('#id_parent').val();
    console.log(parentid);
    $.get('/articles/submit_comment/', {
        article_comment: comment,
        article_id: article_id,
        parent_Id: parentid
    }).then(res => {
        console.log(res);
        location.reload();
    });
}

function Fill_parent_id(parent_Id) {
    $('#id_parent').val(parent_Id);
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"});
}