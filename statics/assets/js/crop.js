$(".gambar").attr("src", "https://thumbs.dreamstime.com/z/sketch-vegetables-chicken-fish-13103251.jpg");
    var $uploadCrop,
    tempFilename,
    rawImg,
    imageId,
    crop;
    function readFile(input) {
        console.log('his')
            if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                console.log('ds')
                $('.upload-demo').addClass('ready');
                $('#cropImagePop').modal('show');
                rawImg = e.target.result;
                
            }
            reader.readAsDataURL(input.files[0]);
            console.log('dds')
            
        }
        else {
            swal("Sorry - you're browser doesn't support the FileReader API");
        }
    }

    $uploadCrop = $('#upload-demo').croppie({
        viewport: {
            width: 300,
            height: 200,
        },
        
        enableExif: true
    });
    $('#cropImagePop').on('shown.bs.modal', function(){
        // alert('Shown pop');
        $uploadCrop.croppie('bind', {
            url: rawImg
        }).then(function(){
            console.log('jQuery bind complete');
        });
    });

    $('.item-img').on('change', function () { imageId = $(this).data('id'); tempFilename = $(this).val();
    $('#cancelCropBtn').data('id', imageId); readFile(this); });
    $('#cropImageBtn').on('click', function (ev) {
        $uploadCrop.croppie('result', {
            type: 'base64',
            format: 'jpeg',
            size: {width: 300, height: 200}
        }).then(function (resp) {
            $('#itemImgOutput').attr('src', resp);
            crop = resp
            $('#cropImagePop').modal('hide');   
        });
    });



$(".gambar2").attr("src", "https://image.shutterstock.com/image-vector/hand-drawn-grocery-bag-260nw-144937510.jpg");

// product 1st
var $uploadCrop1,
    tempFilename1,
    rawImg1,
    imageId1,
    crop1;
    function readFile1(input) {
        console.log('his')
            if (input.files && input.files[0]) {
            var reader = new FileReader();
            console.log('ddsa')
            reader.onload = function (e) {
                console.log('ds')
                $('.upload-demo1').addClass('ready');
                $('#cropImagePop1').modal('show');
                rawImg1 = e.target.result;
                console.log('rawImg1')
                
            }
            reader.readAsDataURL(input.files[0]);
            console.log('dds')
            
        }
        else {
            swal("Sorry - you're browser doesn't support the FileReader API");
        }
    }

    $uploadCrop1 = $('#upload-demo1').croppie({
        viewport: {
            width: 200,
            height: 200,
        },
        
        enableExif: true
    });
    $('#cropImagePop1').on('shown.bs.modal', function(){
        // alert('Shown pop');
        $uploadCrop1.croppie('bind', {
            url: rawImg1
        }).then(function(){
            console.log('jQuery bind complete1');
        });
    });
    $('.item-img1').on('change', function () { imageId1 = $(this).data('id'); tempFilename1 = $(this).val();
    $('#cancelCropBtn1').data('id', imageId1); readFile1(this); });
    $('#cropImageBtn1').on('click', function (ev) {
        $uploadCrop1.croppie('result', {
            type: 'base64',
            format: 'jpeg',
            size: {width: 200, height: 200}
        }).then(function (resp) {
            $('#itemImgOutput1').attr('src', resp);
            crop1 = resp
            $('#cropImagePop1').modal('hide');   
        });
    });

// imgsecond
var $uploadCrop2,
    tempFilename2,
    rawImg2,
    imageId2,
    crop2;
    function readFile2(input) {
        console.log('his')
            if (input.files && input.files[0]) {
            var reader = new FileReader();
            console.log('ddsa')
            reader.onload = function (e) {
                console.log('ds')
                $('.upload-demo2').addClass('ready');
                $('#cropImagePop2').modal('show');
                rawImg2 = e.target.result;
                console.log('rawImg2')
                
            }
            reader.readAsDataURL(input.files[0]);
            console.log('dds')
            
        }
        else {
            swal("Sorry - you're browser doesn't support the FileReader API");
        }
    }

    $uploadCrop2 = $('#upload-demo2').croppie({
        viewport: {
            width: 200,
            height: 200,
        },
        
        enableExif: true
    });
    $('#cropImagePop2').on('shown.bs.modal', function(){
        // alert('Shown pop');
        $uploadCrop2.croppie('bind', {
            url: rawImg2
        }).then(function(){
            console.log('jQuery bind complete2');
        });
    });
    $('.item-img2').on('change', function () { imageId2 = $(this).data('id'); tempFilename2 = $(this).val();
    $('#cancelCropBtn2').data('id', imageId2); readFile2(this); });
    $('#cropImageBtn2').on('click', function (ev) {
        $uploadCrop2.croppie('result', {
            type: 'base64',
            format: 'jpeg',
            size: {width: 200, height: 200}
        }).then(function (resp) {
            $('#itemImgOutput2').attr('src', resp);
            crop2 = resp
            $('#cropImagePop2').modal('hide');   
        });
    });

// imgthird
    var $uploadCrop3,
    tempFilename3,
    rawImg3,
    imageId3,
    crop3;
    function readFile3(input) {
        console.log('his')
            if (input.files && input.files[0]) {
            var reader = new FileReader();
            console.log('ddsa')
            reader.onload = function (e) {
                console.log('ds')
                $('.upload-demo3').addClass('ready');
                $('#cropImagePop3').modal('show');
                rawImg3 = e.target.result;
                console.log('rawImg3')
                
            }
            reader.readAsDataURL(input.files[0]);
            console.log('dds')
            
        }
        else {
            swal("Sorry - you're browser doesn't support the FileReader API");
        }
    }

    $uploadCrop3 = $('#upload-demo3').croppie({
        viewport: {
            width: 200,
            height: 200,
        },
        
        enableExif: true
    });
    $('#cropImagePop3').on('shown.bs.modal', function(){
        // alert('Shown pop');
        $uploadCrop3.croppie('bind', {
            url: rawImg3
        }).then(function(){
            console.log('jQuery bind complete2');
        });
    });
    $('.item-img3').on('change', function () { imageId3 = $(this).data('id'); tempFilename3 = $(this).val();
    $('#cancelCropBtn3').data('id', imageId3); readFile3(this); });
    $('#cropImageBtn3').on('click', function (ev) {
        $uploadCrop3.croppie('result', {
            type: 'base64',
            format: 'jpeg',
            size: {width: 200, height: 200}
        }).then(function (resp) {
            $('#itemImgOutput3').attr('src', resp);
            crop3 = resp
            $('#cropImagePop3').modal('hide');   
        });
    });

    
// usercrop


// profilePic 

$(".prof").attr("src", "https://www.cometdocs.com/images/default-profile-image.png");
    var $uploadCropPof,
    tempFilenameProf,
    rawImgProf,
    imageIdProf,
    cropProf;
    function readFileProf(input) {
        console.log('his')
            if (input.files && input.files[0]) {
            var reader = new FileReader();
            console.log('ddsa')
            reader.onload = function (e) {
                console.log('ds')
                $('.upload-demoProf').addClass('ready');
                $('#cropImagePopProf').modal('show');
                rawImg3 = e.target.result;
                console.log('rawImgProf')
                
            }
            reader.readAsDataURL(input.files[0]);
            console.log('dds')
            
        }
        else {
            swal("Sorry - you're browser doesn't support the FileReader API");
        }
    }

    $uploadCropProf = $('#upload-demoProf').croppie({
        viewport: {
            width: 150,
            height: 200,
        },
        
        enableExif: true
    });
    $('#cropImagePopProf').on('shown.bs.modal', function(){
        // alert('Shown pop');
        $uploadCropProf.croppie('bind', {
            url: rawImg3
        }).then(function(){
            console.log('jQuery bind completeProf');
        });
    });
    $('.item-imgProf').on('change', function () { imageIdProf = $(this).data('id'); tempFilenameProf = $(this).val();
    $('#cancelCropBtnProf').data('id', imageIdProf); readFileProf(this); });
    $('#cropImageBtnProf').on('click', function (ev) {
        $uploadCropProf.croppie('result', {
            type: 'base64',
            format: 'jpeg',
            size: {width: 150, height: 200}
        }).then(function (resp) {
            $('#itemImgOutputProf').attr('src', resp);
            cropProf = resp
            $('#cropImagePopProf').modal('hide');   
        });
    });