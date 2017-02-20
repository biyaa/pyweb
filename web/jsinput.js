$(function(){
  var search = $('#s');
  var icon   = $('#searchbtn');
  $("#showpic").hide();
  $("#showresult").hide();
  
  // handling the focus event on input2
  $(search).on('focus', function(){
    $(this).animate({
      width: '100%'
    }, 400, function(){
      // callback function
	  //$("#pic").html("<b>Hello world!</b>");
	  $("#showpic").hide();
    });
    $(icon).animate({
      right: '10px'
    }, 400, function(){
      // callback function
    });
  });
  
  // handling the blur event on input2
  $(search).on('blur', function(){
    if(search.val() == '') {
      $(search).animate({
        width: '45%'
      }, 400, function(){ });
      
      $(icon).animate({
        right: '360px'
      }, 400, function(){ });
    }
  });
  
  // handling both form submissions
  $('#searchform').submit(function(e) {
	  //alert ($(search).val());
	  //$.post("http://127.0.0.1/xxx?" + $(search).val(), function(data,status){
	//	 alert("数据：" + data + "\n状态：" + status)
	 // });
	  //$("#showpic").show();
    e.preventDefault();
    

  
    var formData = new FormData($( "#searchform" )[0]);  
    $.ajax({  
      url: '/upload',  
      type: 'POST',  
      data: formData,  
      async: false,  
      cache: false,  
      contentType: false,  
      processData: false,  
      success: function (returndata) {  
            //$("#pic").remove()
            //i = new Image();
            src = 'lastest.jpg' + "?random="+new Date().getTime();
            //i.id = 'pic';
            $("#pic").attr('src',src);

            $.get("/predict",function(data,status){
                $("#ai").text(data.r) 
                $("#showresult").show();
              });
          //alert(returndata.filename);  

      },  
      error: function (returndata) {  
          alert(returndata);  
      }  
    });
    $("#showpic").show();
  });
});
