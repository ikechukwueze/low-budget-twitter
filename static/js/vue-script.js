console.log('happiness is key')

var get_or_post_tweets_url = document.querySelector('#get-post-tweet').getAttribute('data-get-post-tweet-url')
var like_retweet_url = document.querySelector('#like-retweet').getAttribute('data-like-retweet-url')


const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            all_tweets: [],
            user_details: '',
            form: {tweet: ''},
            counter: 0
        }
    },

    mounted() {
        axios.get(get_or_post_tweets_url)
        .then(response => {
            this.all_tweets = response.data
            console.log(response.data)
        })
        .catch(errors => console.log(errors))

        
    },
  
  
    methods: {
        post_tweet(event) {
            axios({
                method: 'post',
                url: get_or_post_tweets_url,
                data: {tweet: this.form.tweet},
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers: {'X-CSRFToken': 'csrftoken'}
            })
            .then(response => {
                this.form.tweet = ''
                event.target.reset()
                console.log(this.all_tweets)
                //this.all_tweets = response.data
                this.all_tweets = (response.data).concat(this.all_tweets)
                console.log(this.all_tweets)

                //console.log(response.data)
            })
            .catch(errors => console.log(errors))
        },


        like_or_retweet(id, action, event) {
            console.log(event.target)
            //this.counter++
            axios({
                method: 'post',
                url: like_tweet_url,
                data: {
                    tweet_id: parseInt(id),
                    action: action,
                    like_update: 1,
                },
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers: {'X-CSRFToken': 'csrftoken'}
                //headers: {'X-CSRFToken': csrfmiddlewaretoken}
            })
            .then(response => {
                //this.form.tweet = ''
                console.log(this),
                console.log(response.data)
            })
            .catch(errors => console.log(errors))
        },
    }
});



/*
app.component(
    'tweet-input',
    {
        delimiters: ["[[", "]]"],
        props: ['username', 'display_name', 'profile_pic'],
        template: `
        <div class="d-flex p-3 my-2 border rounded-3 mb-3 w-100 bg-light">
            <div class="flex-shrink-0">
            <img class="rounded-circle profile-pic" :src="[[ account.profile_pic_url ]]">
            </div>
            <div class="card ms-1 border-0 w-100 bg-transparent">
                <div class="card-header border-0 bg-transparent">
                    <span class="fw-bold">@{{ account.username }} <i class="bi bi-patch-check-fill" style="font-size:1rem; color: blue;"></i></span>
                    <br>
                    <span>{{ account.display_name }}</span>
                </div>
                <form @submit.prevent="post_tweet" id="post-tweet-form">
                    {% csrf_token %}
                    <div class="card-body py-1 bg-transparent">
                        <textarea class="form-control bg-transparent" minlength="1" maxlength="280s" id="exampleFormControlTextarea1" placeholder="Penny for your thoughts." rows="3" required v-model="form.tweet"></textarea>
                    </div>
                    <div class="card-footer text-muted d-flex justify-content-end border-0 bg-white bg-transparent">
                        <button class="btn btn-sm" type="submit" style="background-color: blue; color: white;">Tweet!</button>
                    </div>
                </form>
            </div>
        </div>
        `

    }
)
*/

app.component(
    'tweet',
    {   
        delimiters: ["[[", "]]"],
        props: [
            'id', 
            'author',
            'date_time',
            'display_name', 
            'likes', 
            'retweets', 
            'tweet', 
            'profile_pic',
            'following',
            'followers'
        ],
        template: `
            <div class="d-flex p-3 my-2 border rounded-3">
                <div class="flex-shrink-0">
                    <img class="rounded-circle profile-pic" :src=[[profile_pic]]>
                </div>
                <div class="card ms-1 w-100 border-0">
                    <div class="card-header border-0 bg-white ">
                        <div class='d-flex justify-content-between'>
                            <div>
                                <span class="fw-bold">[[ display_name ]] <i class="bi bi-patch-check-fill" style="font-size:1rem; color: blue;"></i></span>
                                <span> &#183 </span>
                                <span class="text-muted"> @[[ author ]] </span>
                            </div>
                            <div>
                                <a type='button' class="bi bi-trash" data-bs-toggle="modal" data-bs-target="#staticBackdrop"></a>
                            </div>
                        </div>
                        <div>
                            <span class="text-muted"><small>[[ date_time ]]</small> </span>
                        </div>
                    </div>
                    <div class="card-body py-1">
                        <p class="card-text">[[ tweet ]]</p>
                    </div>
                    <div class="card-footer text-muted d-flex justify-content-around border-0 bg-white">
                        <div><i class="bi bi-chat"></i><span class="badge text-muted">3</span></div>
                        <div><i class="bi bi-arrow-repeat"></i><span class="badge text-muted">[[ retweets ]]</span></div>
                        <div><i class="bi bi-arrow-repeat"></i><span class="badge text-muted">[[ retweets ]]</span></div>
                        <div v-on:click=""><i class="bi bi-heart"></i><span class="badge text-muted">[[ likes ]]</span></div>
                    </div>
                </div>
                <div class="modal" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <h5><strong>Delete tweet?</strong></h5>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-danger">Delete</button>
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }
)




app.mount('#vue-app')

/*
<div class="d-flex p-3 my-2 border rounded-3">
            <div class="flex-shrink-0">
                <img class="rounded-circle" :src='[[profile_pic]]' style="height: 60px; width: 60px;">
            </div>
            <div class="card ms-1 w-100 border-0">
                <div class="card-header border-0 bg-white">
                    <span class="fw-bold">[[ display_name ]] <i class="bi bi-patch-check-fill" style="font-size:1rem; color: blue;"></i></span>
                    <span> &#183 </span>
                    <span class="text-muted"> @[[ author ]] </span>
                    <span> &#183 </span>
                    <span class="text-muted"><small>[[ date_time ]]</small> </span>
                </div>
                <div class="card-body py-1">
                    <p class="card-text" data-id=[[ id ]]>[[ tweet ]]</p>
                </div>
                <div class="card-footer text-muted d-flex justify-content-around border-0 bg-white">
                    <div><i class="bi bi-chat"></i><span class="badge text-muted">3</span></div>
                    <div @click="like_or_retweet(tweet.id, 'retweet', $event)"><i class="bi bi-arrow-repeat"></i><span class="badge text-muted">[[ retweets ]]</span></div>
                    <div @click="like_or_retweet(tweet.id, 'like', $event)"><i class="bi bi-heart"></i><span class="badge text-muted">[[ likes ]]</span></div>
                </div>
            </div>
        </div>
*/