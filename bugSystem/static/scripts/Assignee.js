function getCookie(name) {
    let cookieValue = null;
    // console.log(document.cookie);
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // console.log('inside');
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // console.log(cookieValue);
                break;
            }
        }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');
  
  document.getElementById("predictassigneebutton").addEventListener("click", function() {
      // console.log('predict clicked')
      var summ = document.getElementById("submittedsummary").innerHTML;
      console.log(summ)
  
      fetch('/bugSystem/predict_assignee',{
        method:'POST',
        credentials: 'include',
        headers:{
          
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
          'X-CSRFToken': csrftoken,
        },
          
          
          body : JSON.stringify({ 'summary': summ}),
  
      })
      .then(resp=>resp.text())
      .then(function(resp){
          console.log(typeof(resp))
          const res = JSON.parse(resp)
          console.log(typeof(res))
          document.getElementById("predictedassignee").innerHTML=res.my_data;
          console.log(res.my_data)
      })
      // console.log('predict clicked');
  
    }); 
  
  