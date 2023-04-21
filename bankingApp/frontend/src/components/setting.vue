<template>
    <div class="Info">
        <h1 class="lead display-5">Setting</h1>
        <p class="lead text-muted"> Change Account Settings </p>
    </div>
    <div class="container">
        <div class="container-2">
            <h1>User Details</h1>
            <h5>Fullname: {{ this.name }}</h5>
            <h5>Username: {{ username }}</h5>
            <h5>Email : {{ email }}</h5>

            <form class="pass" @submit.prevent="changePassword">
                <h2>Change Password</h2>
                <h4>Enter current password:</h4>
                <input type="password" v-model="oPassword">
                <h4>Enter new password:</h4>
                <input type="password" v-model="nPassword">
                <div>
                    <button class="b4 btn btn-info" type="submit">Submit</button>

                </div>
            </form>
            <div class="message">

                {{ message }}
            </div>
            <section v-if="user == true" class="del">
                <form @submit.prevent="deleteUser">
                    <h1>Delete User</h1>
                    
                    <h4>Enter User</h4>
                    <input type="text" v-model="Uname">
                    <button class="b5 btn btn-info" type="submit">Submit</button>
                    <div>{{ this.message2 }}</div>
                </form>
            </section>
        </div>

        <section v-if="user == false">
            <div class="container-3">
                <h1>Contact Support</h1>
                <form @submit.prevent="sendSupport">
                    <h3>Subject</h3>
                    <input class="textfield" type="text" v-model="subject">
                    <h3>Description</h3>
                    <textarea class="textfield" rows="4" v-model="description"></textarea>
                    <div>
                        <button class="b2 btn btn-info" type="submit">Contact Support</button>

                    </div>
                </form>
            </div>
        </section>
        <section v-if="user == true">
            <h1>User Queries</h1>
            <div class="container-3">
                <div v-for="t in tickets" class="container-s">
                    <div>username:{{ t.account.username }} 
                        email:{{ t.account.email }}    
                        <h1>{{ t.subject }}</h1>
                    </div> 
                    <div>{{ t.description }}</div>
                    

                </div>
            </div>

        </section>
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
            x: null,
            username: "",
            Uname: "",
            message: "",
            oPassword: "",
            nPassword: "",
            description: "",
            subject: "",
            user: null,
            tickets: [],
            message2:"",
            email:"",
        }
    },
    methods: {
        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            this.id = data.User.id
            this.name = data.User.fname + " " + data.User.sname
            this.username = data.User.username
            this.email=data.User.email
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },
        async changePassword() {
            const password = JSON.stringify({
                username: this.username, //saving goal
                password: this.oPassword,     //saving per month
                new_password: this.nPassword,  //entered balance
            })
            // let response = await fetch(")
            let response = await fetch("http://127.0.0.1:8000/api/password/", {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                },
                body: password,
            })
            this.message = await response.json()
            this.message = this.message.response
        },
        async sendSupport() {
            const password = JSON.stringify({
                username: this.username, //saving goal
                subject: this.subject,     //saving per month
                description: this.description,  //entered balance
            })
            let response = await fetch("http://127.0.0.1:8000/api/support/", {
                method: 'POST',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                },
                body: password,
            })
            this.message = await response.json()
            this.message = this.message.response
        },

        async getSuperUser() {
            let response = await fetch("http://127.0.0.1:8000/api/superUser/", {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                },
            })
            this.user = await response.json()
            this.user = this.user.check
            console.log(this.user)
        },
        async getTickets() {
            let response = await fetch("http://127.0.0.1:8000/api/support/", {
                method: 'GET',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                },
            })
            this.tickets = await response.json()
            this.tickets = this.tickets.Tickets
            console.log(this.tickets)
        },

        async deleteUser(){
            const item=JSON.stringify({
                username:this.Uname
            })
            let response = await fetch("http://127.0.0.1:8000/api/deleteUser/", {
                method: 'DELETE',
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                },
                body: item,
            })
            this.message2 = await response.json()
            this.message2 = this.message2.response
        }

    },
    mounted() {
        this.getSession();
        this.getSuperUser();
        this.getTickets();
        


    }
}
</script>

<style >
.Info {
    color: white;
    height: 15%;
    /* background-color: #02093B; */
    background-image: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    padding: 2%;

    /* /* font: ; */
}

.container {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    margin-top: 2%;
    margin-bottom: 2%;
}

.container-2 {
    width: 40%;
}

.container-3 {
    border: solid black 2px;
    padding: 3%;
    width: 100%;
}

.message {
    color: red;
}

.b2 {
    margin-top: 2%;
}

.textfield {
    width: 80%;
    font-size: 0.8em;
}

.pass {
    border: solid grey 2px;
    padding: 2%;
    width: 100%;
}

h4 {
    font-size: 1.25em;
}

section{
    margin-top:3%;
    width:50%;
}

.container-s {
    display: flex;
    border: solid black 2px;
    margin-bottom: 5%;
    flex-direction: column;
    padding:2%;
    background-color: rgb(232, 232, 232);
}

.del{
    border:solid black 2px;
    padding:2%;
}
.b5 ,.b4{
    margin-top:5%;
    margin-left:5%;
    margin-bottom:2%;
}

input[type='password']{
    width:80%;
}
</style>