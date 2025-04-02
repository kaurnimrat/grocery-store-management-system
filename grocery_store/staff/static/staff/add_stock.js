document.addEventListener("DOMContentLoaded", function() {
    const addStock = document.querySelector("#add_stock")

    addStock.addEventListener("submit", function(event) {
        event.preventDefault()  
        data = {
            item_name: document.querySelector('[name=item_name]').value,
            item_category: document.querySelector('[name=item_category]').value,
            item_price: document.querySelector('[name=item_price]').value,
            item_quantity: document.querySelector('[name=item_quantity]').value,
            
        }

        fetch("http://127.0.0.1:8000/api/addstock", {
            method: 'POST',
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                alert('Item is added to stock')
                window.location.replace('/addstock')
            } else {
                alert(data.message)
            }
        })
        .catch(error => {
            console.log(error)
        })
    })
})