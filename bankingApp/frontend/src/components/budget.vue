<template>
    <div>
        <div>
            <div class="Info">
                <h1 class="lead display-5">Budget Calculator</h1>
                <p class="lead text-muted">Work out how much your spending monthly</p>
            </div>
            <div class="big-container">
                <div class="container">
                    <form @submit.prevent="budgetCalc">
        
                        <h2>Topic/Category you spend on:</h2>
                        <div class="input-group">
                            <input type="text" v-model="name" class="form-control border border-dark" required />
                        </div>
                        <h2>Amount earned or amount loss (+/-)</h2>
                        <div class="input-group">
                            <input type="Number" step="0.01" v-model="amount" class="form-control border border-dark"
                                required />
                        </div>
                        <button class="b btn btn-dark" type="submit">Add item</button>
                    </form>
                </div>
                <div class="container-2">
                    <h2 class="title">Items:</h2>
                    <div>
                           <ul> <li v-for="(item, index) in amounts"> {{ index }} &#41; {{ item.name }}: £{{ item.amount }}</li> </ul>
                    </div>
                    <hr>
                    <div class="total">Total Expenses: {{ total }}</div>

                </div>
            </div>
        </div>
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
            amounts: [],
            name:"",
            amount:null,
            salary:null,
            total:0,

        }
    },
    methods: {

        //if your not authenicated you get sent back to the login screen
        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },
        async budgetCalc() {
            this.amounts.push({'name':this.name,'amount':this.amount})
            this.total=0;
            for (let i=0;i<this.amounts.length;i++){
                console.log(this.amounts[i])
                this.total+=Number(this.amounts[i].amount)
            }
        }

    },
    mounted() {
        this.getSession();

    },
}
</script>

<style scoped>
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

.container {
    border: solid black 2px;
    width: 45%;
}

.container-2 {
    border: solid black 2px;
    width: 45%;
}

.big-container {
    display: flex;
    margin: 2%;

}

.b {
    margin-left: 20%;
    width: 30%;
    margin-top: 2%;
    margin-bottom: 2%;
    height: 20%;
    border-radius: 2%;
}

.title{
    text-decoration-line: underline;
    margin-left:2%;
}
ul{
    margin-left:2%;

}
.total{
    margin-left:2%; 
}
</style>