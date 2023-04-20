<template>
    <div>

        <div class="Info">
            <h1 class="lead display-5">Saving Calculator</h1>
            <p class="lead text-muted">Calculate how long it will take to save</p>
        </div>
    </div>

    <div class="padding col border rounded border-secondary p-75 bg-light">
        <form @submit.prevent="SaveCalc">
            <h2>Saving Goal (£):</h2>
            <div class="input-group">
                <input type="Number" step="0.01" v-model="goal" class="form-control border border-dark" required />
            </div>
            <h2>Saving Amount per Month (£):</h2>
            <div class="input-group">
                <input type="Number" step="0.01" v-model="amountM" class="form-control border border-dark" required />
            </div>
            <h2>Use Current Balance?</h2>
            <div class="input-group checkbox">
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" value="yes"
                        v-model="check">
                    <label class="form-check-label" for="flexRadioDefault1">
                        yes
                    </label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" value="no"
                        v-model="check" checked>
                    <label class="form-check-label" for="flexRadioDefault2">
                        no
                    </label>
                </div>
                
                <h2>Enter Balance</h2>
                <div class="form check">
                    <input type="Number" step="0.01" v-model="bal" class="form-control border border-dark" :disabled="check==='yes'" required/>
                </div>


            </div>
            <button class="b btn btn-dark" type="submit">CALCULATE</button>
          <h5>{{ this.result }}</h5>

        </form>
    </div>
</template>

<script>


function getCookie(name) {
    let cookieValue = "";
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
export default {
    data() {
        return {
            goal: null,
            check: "no",
            bal:null,
            amountM:null,
            result:null,

        }
    },
    methods: {

        async SaveCalc(){
            console.log( parseFloat(this.bal).toFixed(2))
            const Calculate = JSON.stringify({
                    goal: parseFloat(this.goal).toFixed(2), //saving goal
                    amount: parseFloat(this.amountM).toFixed(2),     //saving per month
                    balance: parseFloat(this.bal).toFixed(2),  //entered balance
                    check:this.check,    //use current balance or entered amount
                })
            // let response = await fetch(")
            let response = await fetch("http://127.0.0.1:8000/api/Calculator/", {
                    method: 'POST',
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                    },
                    body: Calculate,
                })
            this.result=await response.json()
            this.result=this.result.response
            console.log(this.result)

        },








        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },

    },
    mounted() {
        this.getSession();
    },

}
</script>

<style  scoped>
.Info {
    color: white;
    height: 15%;
    /* background-color: #02093B; */
    background-image: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    padding: 2%;

    /* /* font: ; */
}

.Info p {
    margin-left: 5%;

}

.padding {
    width: 80%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 5%;
    padding:2%;

}

.checkbox {
    display: flex;
    flex-direction: column;


}

.b{
    margin-top:2%;
    width:20%;
    height:60%;
    margin-left:5%;
    margin-bottom:2%;
}
</style>