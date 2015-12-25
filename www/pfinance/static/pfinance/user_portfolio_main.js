
$(document).ready(function(){
	//change the color of quote
	num_decorator();
	
	//toggle views of all holdings or just current holdings
	$('#user_stock_view').on('change', function(){
  		var sel = $(this).val();
  		if(sel == "2") {
  			$('#portfolio_table').find(".currentholding").each(function (){
  				var share = $(this).html();
  				if (share == 0) {
  					$(this).closest("tr").hide();
  				}
  			});
  		}
  		else {
  			$('#portfolio_table').find(".currentholding").each(function (){
  				$(this).closest("tr").show();
  			});
  		}
  	});

  $('#user_transaction_view').on('change', function(){
      var sel = $(this).val();
      if (sel.localeCompare('all') == 0) {
          $('#user_transaction_table tbody').find('tr').each(function(){
              $(this).show();
          });
      }
      else {
          $('#user_transaction_table tbody').find('tr').each(function(){
              if($(this).hasClass(sel))
                $(this).show();
              else
                $(this).hide();
          });        
      }

  });

  	//tradedate datepicker obj
  	$( ".date" ).datepicker();

  	//handle add transactions
  	$('#add_tran').on('submit',function(event){
  		event.preventDefault();

  		var ticker = $(this).find('input[name="ticker"]').val();
  	 	
  	 	//check if date is valid
  	 	var trade_date = $(this).find('input[name="trade_date"]').val();
  	 	if(isNaN(Date.parse(trade_date))){
  	 		alert("not a good date");
  	 		return;
  	 	}

  	 	//check if shares is valid
  	 	var shares = $(this).find('input[name="shares"]').val();
  	 	if(isNaN(parseInt(shares,10)) || parseInt(shares,10) <= 0) {
  	 		alert("not a good shares");
  	 		return;
  	 	}

  	 	//check if price is valid
  	 	price = $(this).find('input[name="price"]').val();
  	 	if(isNaN(parseFloat(price)) || parseFloat(price) < 0) {
  	 		alert("not a good price");
  	 		return;
  	 	}

  	 	//check if commission is valid
  	 	commission = $(this).find('input[name="commission"]').val();
  	 	if(isNaN(parseFloat(commission)) || parseFloat(commission) < 0) {
  	 		alert("not a good commission");
  	 		return;
  	 	}

  	 	//submit ajax request
  	 	$.ajax({
        url : $(this).attr('action'), // the endpoint
        type : "POST", // http method

        //date to post
        data: {csrfmiddlewaretoken: $(this).find('input[name="csrfmiddlewaretoken"]').val(),
    						ticker: ticker,
    					trade_date: trade_date,
    						shares: shares,
    						 price: price,
    					commission: commission,
    					 tran_type: $(this).find('select[name="tran_type"]').val(),
    		  },

        // handle a successful response
        success : function(result) {
        	if(result.localeCompare('ticker') == 0){
        		alert("ticker does not exist!")
        	}
        	else if(result.localeCompare('na') == 0) {
        		alert("unknown at the server")
        	}
        	else {
        		location.reload();
        	}
            
        },

        // handle a non-successful response
        error : function() {
            alert("unsuccessful");
        }
    	});

  	 });
});


function num_decorator(){
	//It decorates the quote as follows
	//for positive number, change it to green and put + sign
	//for negative number, change it to red
	//for 0 (<0.01), black
	$('#portfolio_table').find(".colorshow").each(function () {
		var num = parseFloat($(this).html());
		if (Math.abs(num) < 0.01) {
			$(this).html("0.00");
			$(this).css('color', 'black');
		}
		else if (num < 0) {
			$(this).css('color', 'red');
		}
		else {
			$(this).html('+' + $(this).html());
			$(this).css('color', 'green');
		}
	});

}

