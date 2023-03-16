<template>
    <div>
        <div>
            <div class="Info">
                <h1 class="lead display-5">Transaction History</h1>
                <p class="lead text-muted">See all your transactions here</p>
            </div>
        </div>
        <div class="container">
            <table class="table">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Date</th>
                        <th scope="col">Type</th>
                        <th scope="col">Name</th>
                        <th scope="col">Amount</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="x in Transactions" :key="x.id">
                        <td>{{x.id}}</td>
                        <td>{{x.date}}</td>
                        <td>{{x.type}}</td>
                        <td>{{x.account.fname }} {{x.account.lname}}</td>
                        <td>{{ x.amount }}</td>
                        <td><button onclick="fetch_current_transaction"> Get Amount</button></td>

                    </tr>
                </tbody>
            </table>
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
            Transactions: null,
        }
    },
    methods: {

        async fetch_Transactions() {
            let response = await fetch("http://127.0.0.1:8000/api/transaction/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            this.Transactions = data.Transaction;
            console.log("yes",this.Transactions);
        },

        async fetch_current_transaction() {

        },




        //if your not authenicated you get sent back to the login screen
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
        this.fetch_Transactions();
    }
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
</style>