$(document).ready(function () {
    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});
//     // example: https://getbootstrap.com/docs/4.2/components/modal/
//     // show modal
//     // jQuery Selectors: https://www.w3schools.com/jquery/jquery_selectors.asp


//     $('#insertModal').click(function () {
//         const tID = $('#task-form-display').attr('taskID');
//         console.log($('#task-modal').find('.form-control').val());
//         $.ajax({
//             type: 'POST',
//             url: tID ? '/edit/' + tID : '/create',
//             contentType: 'application/json;charset=UTF-8',
//             data: JSON.stringify({
//                 'description': $('#task-modal').find('.form-control').val()
//             }),
//             success: function (res) {
//                 console.log(res.response);
//                 location.reload();
//             },
//             error: function () {
//                 console.log('Error');
//             }
//         });
//     });

//     // Remove from the table
//     $('.remove').click(function () {
//         const remove = $(this)
//         $.ajax({
//             type: 'POST',
//             url: '/delete/' + remove.data('source'),
//             success: function (res) {
//                 console.log(res.response);
//                 location.reload();
//             },
//             error: function () {
//                 console.log('Error');
//             }
//         });
//     });

//     // search
//     // $('#search_start').click(function () {
        
//     //     const input = document.getElementById("searchInput");
//     //     console.log(input);
//     //     console.log(window.location.href);
//     //     $.ajax({
//     //         type: 'POST',
//     //         url: window.location.href +"/"+ input,
//     //         contentType: 'application/json;charset=UTF-8',
//     //         data: JSON.stringify({
//     //             'key': input
//     //         }),
//     //         success: function (res) {
//     //             console.log(res.response)
//     //             location.reload();
//     //         },
//     //         error: function () {
//     //             console.log('Error');
//     //         }
//     //     });
//     // });
    

// });