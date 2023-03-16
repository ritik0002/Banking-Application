<template>
    <div>
        
        <div class="Info">
        <h1 class="lead display-5">Saving Calculator</h1>
        <p class="lead text-muted">Calculate how much you could save </p>
    </div>
    </div>
    Check
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
        x:null,

        }
    },
    methods: {

        








        async getSession() {
            let response = await fetch("http://127.0.0.1:8000/api/sessionUser/", { credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json();
            if (data.User == "None") {
                window.location.href = "http://127.0.0.1:8000/login/"
            }
        },

    },
    mounted(){
        this.getSession();
    },

}
</script>

<style  scoped>
.Info{
    color:white;
    height:15%;
    /* background-color: #02093B; */
    background-image: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    padding:2%;

    /* /* font: ; */
}
.Info p{
    margin-left:5%;

}
</style>