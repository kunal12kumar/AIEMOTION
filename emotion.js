const form = document.querySelector(".inputb");
const submit = document.querySelector(".Submit");
const searchbox = document.querySelector(".searchbox");


form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = searchbox.value;
    console.log(text);
    const data = { key: `${text}` };

    fetch('http://localhost:5000/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch((error) => {
            console.error('Error:', error);
        });



});



