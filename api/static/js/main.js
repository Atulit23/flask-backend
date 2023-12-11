async function submitRequest(){
    // alert('Submitted')
    let author = document.getElementById("author").value
    let likefrom = document.getElementById("likefrom").value
    let liketo = document.getElementById("liketo").value
    let replyfrom = document.getElementById("replyfrom").value
    let replyto = document.getElementById("replyto").value
    let startdate = document.getElementById("startdate").value
    let enddate = document.getElementById("enddate").value
    let text = document.getElementById("text").value
    // alert(startdate)
    // alert(author)
    window.location.assign(`http://127.0.0.1:5000?search_author=${author}&like_from=${likefrom}&like_to=${liketo}&reply_from=${replyfrom}&reply_to=${replyto}&search_text=${text}&at_from=${startdate}&at_to=${enddate}`)
}