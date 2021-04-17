var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        
        console.log('USER:', customer)
        if (customer === 'AnonymousUser') {
            alert('please login')
        } else {
            updateUserOrder(productId, action)

        }
    })
}


function updateUserOrder(productId, action) {
    console.log('logged in')
    alert('item added to cart')
    var url = '/updateItem/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })

        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)
            var cartCount = document.getElementById('lblCartCount');
            var content = cartCount
            content = content.textContent;
            content = isNaN(content) ? 0 : content;
            content++;
            cartCount.innerHTML = content;
        })
}


function increaseValue(id) {
    var value = parseInt(document.getElementById('cart' + id).value, 10);
    var cartCount = document.getElementById('lblCartCount');
    var content = cartCount;
    content = content.textContent;
    content = isNaN(content) ? 0 : content;
    value = isNaN(value) ? 0 : value;
    value++;
    content++;
    document.getElementById('cart'+ id).value = value;
    cartCount.innerHTML = content;
    var qty = document.getElementById('cart' + id).value;
    var price = document.getElementById('totalinput' + id).value;
    var prtotal = parseInt(qty) * parseFloat(price).toFixed(2)
    var prtotal1 = parseFloat(prtotal).toFixed(2) 
    var oldsub = document.getElementById('subtotal').value;
    var gettot = document.getElementById('gettot' + id).value;
    var newsub = parseFloat((oldsub - gettot) + prtotal).toFixed(2);
    var grandTot =parseFloat(newsub) + 50;
    var data = {
        'qty': qty
    }
    $.ajax({
        url: '/change/' + id,
        method: 'GET',
        data: data,
        dataType: 'json',
        success: function (data) {
            if (data == 'true') {
                document.getElementById("total" + id).textContent = prtotal1;
                $('#sub').html("₹"+newsub)
                $('#grand').html("₹"+grandTot)
            } else if (data == 'false') {
                cartClick(id);
            }
        }
    })
    
  }
  
  
  function decreaseValue(id) {
    var value = parseInt(document.getElementById('cart' + id).value, 10);
    var cartCount = document.getElementById('lblCartCount');
    var content = cartCount
    content = content.textContent
    content = isNaN(content) ? 0 : content;
    value = isNaN(value) ? 0 : value;
    value < 1 ? value = 1 : '';
    content < 1 ? content = 1: '';
    content--;
    value--;
    cartCount.innerHTML = content;
    document.getElementById('cart' + id).value = value;
    var qty = document.getElementById('cart' + id).value;
    var price = document.getElementById('totalinput' + id).value;
    var prtotal = parseInt(qty) * parseFloat(price).toFixed(2)
    var prtotal1 = parseFloat(prtotal).toFixed(2) 
    var oldsub = document.getElementById('subtotal').value;
    var gettot = document.getElementById('gettot' + id).value;
    var newsub = parseFloat((oldsub - gettot) + prtotal).toFixed(2);
    var grandTot =parseFloat(newsub) + 50;
    var data = {
        'qty': qty
    }
    $.ajax({
        url: '/change/' + id,
        method: 'GET',
        data: data,
        dataType: 'json',
        success: function (data) {
            if (data == 'true') {
                document.getElementById("total" + id).textContent = prtotal1;
                $('#sub').html("₹"+newsub)
                $('#grand').html("₹"+grandTot)
            } else if (data == 'false') {
                cartClick(id);
            }
        }
    })
    
  }


function change(id) {
    var qty = document.getElementById('cart' + id).value;
    var price = document.getElementById('totalinput' + id).value;
    var prtotal = parseInt(qty) * parseFloat(price).toFixed(2)
    var prtotal1 = parseFloat(prtotal).toFixed(2) 
    var oldsub = document.getElementById('subtotal').value;
    var gettot = document.getElementById('gettot' + id).value;
    var newsub = parseFloat((oldsub - gettot) + prtotal).toFixed(2);
    var grandTot =parseFloat(newsub) + 50;
    var data = {
        'qty': qty
    }
    $.ajax({
        url: '/change/' + id,
        method: 'GET',
        data: data,
        dataType: 'json',
        success: function (data) {
            if (data == 'true') {
                document.getElementById("total" + id).textContent = prtotal1;
                $('#sub').html("₹"+newsub)
                $('#grand').html("₹"+grandTot)
            } else if (data == 'false') {
                cartClick(id);
            }
        }
    })
}

function clicked(id){
    var ok = confirm('Are you sure you want to delete this Address?');
    if (ok == true)
        $.ajax({
            url: '/delete/'+ id,
            method: 'GET',  
            type:JSON,
            success: function(data){
                if(data == 'true'){
                    window.location.reload()
                }
            }
        })
}

function cartClick(id){
    var ok = confirm('Are you sure you want to delete this item from cart?');
    console.log(id)
    if (ok == true)
        $.ajax({
            url: '/delete_cart/'+ id,
            method: 'GET',  
            type:JSON,
            success: function(data){
                if(data == 'true'){
                    window.location.reload()
                }
            }
        })
}

$('#add1').click(function(){
    console.log('get')
    var shipName = $("#shipName").val();
    var address = $("#address1").val();
    var landMark = $("#landMark").val();
    var phone = $("#phone1").val();
    console.log(phone)
    var phoneFormat1 = $("#phone1").val().length === 10;
    var filter = /^[0-9-+]+$/;
    var phoneFormat2 = filter.test(phone);
    var pincode = $("#pincode").val();
    var data = {
        'csrfmiddlewaretoken':'{{csrf_token}}',
        'shipName': shipName,
        'address': address,
        'landMark': landMark,
        'phone': phone,
        'pincode':pincode,
    }
    if (shipName == ''){
        $('#msg').html('shipping name needed')
    }else if(address == ''){
        $('#msg').html('Address needed')
    }else if(landMark == ''){
        $('#msg').html('land mark needed')
    }else if(phone == ''){
        $('#msg').html('Phone number needed')
    }else if(phoneFormat1 == false || phoneFormat2 == false ){
        $('#msg').html("enter valid Phone number")
    }else if(pincode == ''){
        $('#msg').html('Pincode needed')
    }else{
        $.ajax({
            url:'/checkout/',
            method : 'POST',
            data : data,
            type: JSON,

            success:function(data){
                if(data =='true'){
                    window.location.reload()
                }
            }
        })
    }

})



// $(document).ready(function(){
//     $('#upcart').on('change keyup',function(){

//         var productId = this.dataset.product


//         $.ajax({
//             url:'/admin1/addProduct/',
//             method : 'POST',
//             data : formData,
//             cache: false,
//             contentType: false,
//             processData: false,
//             dataType: 'JSON',

//             success: function(data){
//                 if (data == 'true'){
//                   console.log(data)
//                   window.location.replace('/admin1/products/')
//                 }
//                 else if(data == 'false1'){

//                     $("#errormsg").html("category exists")
//                 }

//             }
//         })

//     });
// });
