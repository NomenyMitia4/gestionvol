let users = []

fetch("http://127.0.0.1:5000/flight/getAll")
.then(response=>{
    if(!response.ok)
    {
        throw new Error("Error");
    }
    return response.json()
.then(data => {
    users = data
    console.log(users); // Now you'll see the actual parsed JSON
    })
})

