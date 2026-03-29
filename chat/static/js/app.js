let currentChat = null

function newChat(){
currentChat = null
document.getElementById("chat-box").innerHTML = ""
}

async function openChat(id){

currentChat = id
let chatBox = document.getElementById("chat-box")
chatBox.innerHTML = "Loading..."

let res = await fetch("/messages/"+id+"/")
let data = await res.json()

chatBox.innerHTML = ""

data.forEach(msg => {

if(msg.role === "user"){
chatBox.innerHTML += `
<div class="message user">
<div class="bubble" ondblclick="editMsg(${msg.id}, this)">
${msg.message}
</div>
</div>`
}else{
chatBox.innerHTML += `
<div class="message bot">
<div class="bubble">
${marked.parse(msg.message)}
<div class="actions">
<button onclick="copyText(this)" class="btn btn-sm btn-outline-light">Copy</button>
<button onclick="regenerate()" class="btn btn-sm btn-outline-warning">Regenerate</button>
</div>
</div>
</div>`
}

})

chatBox.scrollTop = chatBox.scrollHeight
}

async function sendMessage(){

let input = document.getElementById("message")
let message = input.value.trim()
if(!message) return

let chatBox = document.getElementById("chat-box")

chatBox.innerHTML += `<div class="message user"><div class="bubble">${message}</div></div>`

if(!currentChat){
let res = await fetch("/create/")
let data = await res.json()
currentChat = data.id
}

let botDiv = document.createElement("div")
botDiv.className = "message bot"

let bubble = document.createElement("div")
bubble.className = "bubble"

botDiv.appendChild(bubble)
chatBox.appendChild(botDiv)

let res = await fetch("/ask/",{
method:"POST",
headers:{
"Content-Type":"application/json",
"X-CSRFToken": csrfToken
},
body:JSON.stringify({message:message, conversation_id:currentChat})
})

let data = await res.json()

let text = data.reply
let currentText = ""
let i = 0

let interval = setInterval(()=>{
currentText += text.charAt(i)

bubble.innerHTML = marked.parse(currentText) + `
<div class="actions">
<button onclick="copyText(this)" class="btn btn-sm btn-outline-light">Copy</button>
<button onclick="regenerate()" class="btn btn-sm btn-outline-warning">Regenerate</button>
</div>
`

i++
chatBox.scrollTop = chatBox.scrollHeight

if(i >= text.length) clearInterval(interval)

},10)

input.value=""
}

function copyText(btn){
let text = btn.parentElement.parentElement.innerText
navigator.clipboard.writeText(text)
btn.innerText = "Copied!"
setTimeout(()=>btn.innerText="Copy",1000)
}

async function regenerate(){

if(!currentChat) return

let chatBox = document.getElementById("chat-box")

let userMessages = document.querySelectorAll(".message.user .bubble")
if(userMessages.length === 0) return

let lastMessage = userMessages[userMessages.length - 1].innerText

let botMessages = document.querySelectorAll(".message.bot")
if(botMessages.length > 0){
botMessages[botMessages.length - 1].remove()
}

let botDiv = document.createElement("div")
botDiv.className = "message bot"

let bubble = document.createElement("div")
bubble.className = "bubble"

botDiv.appendChild(bubble)
chatBox.appendChild(botDiv)

let res = await fetch("/ask/",{
method:"POST",
headers:{
"Content-Type":"application/json",
"X-CSRFToken": csrfToken
},
body:JSON.stringify({message:lastMessage, conversation_id:currentChat})
})

let data = await res.json()

let text = data.reply
let currentText = ""
let i = 0

let interval = setInterval(()=>{
currentText += text.charAt(i)

bubble.innerHTML = marked.parse(currentText) + `
<div class="actions">
<button onclick="copyText(this)" class="btn btn-sm btn-outline-light">Copy</button>
<button onclick="regenerate()" class="btn btn-sm btn-outline-warning">Regenerate</button>
</div>
`

i++
if(i >= text.length) clearInterval(interval)

},10)
}

function editMsg(id, el){

let newText = prompt("Edit message:", el.innerText)
if(!newText) return

fetch("/edit/"+id+"/",{
method:"POST",
headers:{
"Content-Type":"application/json",
"X-CSRFToken": csrfToken
},
body:JSON.stringify({message:newText})
})
.then(()=>{
el.innerText = newText + " (edited)"
})

}

function deleteChat(id){
fetch("/delete/"+id+"/").then(()=>location.reload())
}

function searchChats(){

let input = document.getElementById("search").value.toLowerCase()
let chats = document.querySelectorAll(".chat-item")

chats.forEach(chat=>{
let title = chat.getAttribute("data-title").toLowerCase()
chat.style.display = title.includes(input) ? "flex" : "none"
})

}