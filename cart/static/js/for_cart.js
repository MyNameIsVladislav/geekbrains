
let variable = {

    final_price: $('#final_price').get(0),
    total_qty: $(".basket_qty").get(0),

}

let workItem = {
    target: null,
    qty: null,
    price: null,
}



initScript = {
    variable,
    workItem,

    activeEvent() {
        $('.cart_list').on('click', 'button[data-model-name="qty"]', () => {
            this.workItem = {target: event.target};
            this.changeItem(this.workItem.target.name)

            $.ajax({
                data: {
                  pk: this.workItem.qty.name,
                  qty: this.workItem.qty.value,
                },
                url: url_,
                this: this,

                success: function (response) {
                    this.this.successResponse(response)
                },
                }
            );

        });
    },

    changeItem(id) {
        this.workItem.qty = $('#' + id).get(0)
        this.workItem.price = $('#total_price_' + id).get(0)
        if (this.checkButton()) {
            this.updateValue();
        }
    },

    checkButton () {
        if (this.workItem.target.value === '+' || this.workItem.target.value === '-') {
            return true;
        }
    },

    updateValue() {
        console.log(this.workItem.target.value )
        if (this.workItem.target.value === '+' && this.workItem.qty.value < 10) {
               this.workItem.qty.value = Number(this.workItem.qty.value) + 1;
               console.log(this.workItem.qty.value)
        }
        if (this.workItem.target.value === '-' && this.workItem.qty.value > 1) {
                this.workItem.qty.value = Number(this.workItem.qty.value) - 1;
        }
    },
    successResponse(response) {
        if (response.status) {
            this.workItem.price.innerText = response.price.toFixed(1);
            this.variable.final_price.innerText = response.final_price.toFixed(1) + ' руб.';
            this.variable.total_qty.innerText = response.total_qty
        }
        else {
            console.log("None")
        }
    }
}


$(document).ready(function () {
    initScript.activeEvent()
})
